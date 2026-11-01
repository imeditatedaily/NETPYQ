"""PYQ patterns: how often each syllabus unit and micro-topic has been asked,
paper by paper. Counts only, so they can be shown to every visitor without
giving away the questions. Nothing here imports Streamlit.
"""

from collections.abc import Sequence
from dataclasses import dataclass

import pandas as pd

from .model import Question

# A topic asked in at least this share of the papers loaded is "asked almost every time".
REGULAR_SHARE = 0.6

# Some papers are only partly entered. A paper counts as complete enough to
# judge trends when it has at least this share of the largest paper's questions.
FULL_PAPER_SHARE = 0.5


@dataclass(frozen=True, slots=True)
class Pattern:
    sessions: list[str]          # chronological session labels
    sizes: dict[str, int]        # questions loaded per session
    full: list[str]              # sessions complete enough to judge trends
    per_question: pd.DataFrame   # one row per question: unit, unit_no, topic, session, order
    units: pd.DataFrame          # unit-wise summary
    topics: pd.DataFrame         # topic-wise summary

    @property
    def papers(self) -> int:
        return len(self.sessions)

    @property
    def questions(self) -> int:
        return len(self.per_question)


def _trend(shares: list[float], min_gap: float) -> str:
    """Rising / fading / steady: share of the paper in the newer half of the
    full papers against the older half. Papers vary in length, so shares, not counts."""
    if len(shares) < 4:
        return "—"
    half = len(shares) // 2
    old, new = sum(shares[:half]) / half, sum(shares[-half:]) / half
    if new >= old * 1.5 and new - old >= min_gap:
        return "Rising"
    if new <= old / 1.5 and old - new >= min_gap:
        return "Fading"
    return "Steady"


def pattern(questions: Sequence[Question]) -> Pattern:
    """Patterns over the dated questions given (normally one subject's real papers)."""
    dated = [q for q in questions if q.is_dated]
    rows = pd.DataFrame(
        [{"unit": q.macro_unit, "unit_no": q.unit_no, "topic": q.micro_topic,
          "session": q.session_label, "order": q.session_order} for q in dated],
        columns=["unit", "unit_no", "topic", "session", "order"],
    )
    sessions = rows.sort_values("order")["session"].drop_duplicates().tolist()
    sizes = rows["session"].value_counts().to_dict()
    biggest = max(sizes.values(), default=0)
    full = [s for s in sessions if sizes[s] >= FULL_PAPER_SHARE * biggest]
    if rows.empty:
        empty = pd.DataFrame()
        return Pattern(sessions, sizes, full, rows, empty, empty)

    def summarise(by: list[str], min_gap: float) -> pd.DataFrame:
        grid = rows.pivot_table(index=by, columns="session", values="order", aggfunc="size", fill_value=0)
        grid = grid.reindex(columns=sessions, fill_value=0)
        out = pd.DataFrame(index=grid.index)
        out["questions"] = grid.sum(axis=1)
        out["papers_asked"] = (grid > 0).sum(axis=1)
        out["asked_share"] = out["papers_asked"] / len(sessions)
        out["per_paper"] = out["questions"] / len(sessions)
        out["share"] = out["questions"] / len(rows)
        out["last_asked"] = grid.apply(lambda r: next((s for s in reversed(sessions) if r[s] > 0), "—"), axis=1)
        out["trend"] = grid.apply(lambda r: _trend([r[s] / sizes[s] for s in full], min_gap), axis=1)
        out["by_session"] = grid.values.tolist()
        return out.reset_index()

    units = summarise(["unit", "unit_no"], min_gap=0.02).sort_values("unit_no").reset_index(drop=True)
    topics = summarise(["unit", "unit_no", "topic"], min_gap=0.01).sort_values(
        ["papers_asked", "questions"], ascending=False).reset_index(drop=True)
    return Pattern(sessions, sizes, full, rows, units, topics)


def regular_topics(p: Pattern, share: float = REGULAR_SHARE) -> pd.DataFrame:
    """Topics asked in most papers: the safest ones to master. Needs a few papers to mean anything."""
    if p.topics.empty or p.papers < 3:
        return p.topics
    return p.topics[p.topics["asked_share"] >= share]
