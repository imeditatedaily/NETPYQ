"""The database: each user's answers and subscriptions. Nothing here imports Streamlit.

Works with SQLite (local development, tests) and PostgreSQL (production,
for example Supabase). Tables are created on first use.
"""

from collections.abc import Iterable
from datetime import datetime, timezone

from sqlalchemy import (Boolean, Column, Engine, Integer, MetaData, String, Table, Text, create_engine, delete,
                        insert, select, update)

from .access import Subscription
from .tracker import Answer

metadata = MetaData()

answers = Table(
    "answers", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("email", String(320), nullable=False, index=True),
    Column("at", String(32), nullable=False),
    Column("mode", String(16), nullable=False),
    Column("run", Integer, nullable=False),
    Column("question_id", String(80), nullable=False),
    Column("subject", String(16), nullable=False),
    Column("macro_unit", Text, nullable=False),
    Column("micro_topic", Text, nullable=False),
    Column("question_type", String(32), nullable=False),
    Column("exam_session", Text, nullable=False),
    Column("chosen", Integer, nullable=False),
    Column("correct_answer", Integer, nullable=False),
    Column("is_correct", Boolean, nullable=False),
)

subscriptions = Table(
    "subscriptions", metadata,
    Column("razorpay_id", String(64), primary_key=True),
    Column("email", String(320), nullable=False, index=True),
    Column("subject", String(16), nullable=False),
    Column("status", String(24), nullable=False),
    Column("current_end", Integer, nullable=True),
    Column("short_url", Text, nullable=False, default=""),
    Column("created_at", String(32), nullable=False),
    Column("updated_at", String(32), nullable=False),
)

ANSWER_FIELDS = tuple(Answer.__dataclass_fields__)


def normalise_url(url: str) -> str:
    """Accepts the postgres:// or postgresql:// strings Supabase and others hand out."""
    for prefix in ("postgres://", "postgresql://"):
        if url.startswith(prefix):
            return "postgresql+psycopg://" + url[len(prefix):]
    return url


def make_engine(url: str) -> Engine:
    engine = create_engine(normalise_url(url), pool_pre_ping=True)
    metadata.create_all(engine)
    return engine


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


# --- answers ---------------------------------------------------------------------------

def load_answers(engine: Engine, email: str) -> list[Answer]:
    with engine.connect() as conn:
        rows = conn.execute(select(answers).where(answers.c.email == email).order_by(answers.c.id)).mappings()
        return [Answer(**{k: row[k] for k in ANSWER_FIELDS}) for row in rows]


def add_answer(engine: Engine, email: str, answer: Answer) -> None:
    with engine.begin() as conn:
        conn.execute(insert(answers).values(email=email, **answer.to_dict()))


def replace_answers(engine: Engine, email: str, log: Iterable[Answer]) -> None:
    rows = [{"email": email, **a.to_dict()} for a in log]
    with engine.begin() as conn:
        conn.execute(delete(answers).where(answers.c.email == email))
        if rows:
            conn.execute(insert(answers), rows)


def answer_counts(engine: Engine) -> dict[str, int]:
    """Answers logged per user (for the admin page)."""
    from sqlalchemy import func
    with engine.connect() as conn:
        rows = conn.execute(select(answers.c.email, func.count()).group_by(answers.c.email))
        return {email: n for email, n in rows}


# --- subscriptions ---------------------------------------------------------------------

def _to_sub(row) -> Subscription:
    return Subscription(**{k: row[k] for k in Subscription.__dataclass_fields__})


def list_subscriptions(engine: Engine, email: str | None = None) -> list[Subscription]:
    query = select(subscriptions).order_by(subscriptions.c.created_at)
    if email is not None:
        query = query.where(subscriptions.c.email == email)
    with engine.connect() as conn:
        return [_to_sub(row) for row in conn.execute(query).mappings()]


def save_subscription(engine: Engine, sub: Subscription) -> Subscription:
    """Inserts or updates by Razorpay id; returns the saved record."""
    now = _now()
    values = {"email": sub.email, "subject": sub.subject, "status": sub.status,
              "current_end": sub.current_end, "short_url": sub.short_url, "updated_at": now}
    with engine.begin() as conn:
        changed = conn.execute(update(subscriptions).where(subscriptions.c.razorpay_id == sub.razorpay_id)
                               .values(**values)).rowcount
        if not changed:
            conn.execute(insert(subscriptions).values(razorpay_id=sub.razorpay_id,
                                                      created_at=sub.created_at or now, **values))
        row = conn.execute(select(subscriptions).where(subscriptions.c.razorpay_id == sub.razorpay_id)).mappings().one()
    return _to_sub(row)
