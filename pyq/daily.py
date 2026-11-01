"""Question of the day: one real question per day, the same for everyone, so a
shared link shows what the sender saw. Nothing here imports Streamlit."""

import random
from collections.abc import Sequence
from datetime import date
from urllib.parse import quote

from .model import Question

SHUFFLE_SEED = 2026
OLDEST_DAYS = 60    # a shared link keeps working for this many days


def pick(pool: Sequence[Question], day: date) -> Question:
    """Walks a fixed shuffle of the pool one question a day, so nothing repeats until the pool runs out."""
    ordered = sorted(pool, key=lambda q: q.id)
    random.Random(SHUFFLE_SEED).shuffle(ordered)
    return ordered[day.toordinal() % len(ordered)]


def valid_day(raw: str | None, today: date) -> date:
    """The ?d= date from a shared link, if it is a real, recent day; otherwise today."""
    try:
        d = date.fromisoformat(raw or "")
    except ValueError:
        return today
    return d if 0 <= (today - d).days <= OLDEST_DAYS else today


def share_text(q: Question, subject_name: str, url: str) -> str:
    opts = "\n".join(f"({i}) {o}" for i, o in enumerate(q.options, start=1))
    stem = q.question_text if len(q.question_text) < 220 else q.question_text[:217] + "…"
    return (f"UGC NET {subject_name}: question of the day ({q.session_label})\n\n{stem}\n{opts}\n\n"
            f"Answer + explanation: {url}")


def whatsapp_url(text: str) -> str:
    return "https://wa.me/?text=" + quote(text)


def telegram_url(url: str, text: str) -> str:
    return f"https://t.me/share/url?url={quote(url)}&text={quote(text)}"
