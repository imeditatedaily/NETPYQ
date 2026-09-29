"""Aggregations behind Performance Analytics and the Question Bank view.

Performance figures come from your attempt log. Exam-frequency figures come
only from dated papers in the bank, so they are exact for whatever papers
are loaded and never count the PYQ-pattern samples.
"""

from collections.abc import Sequence
from dataclasses import dataclass

import pandas as pd

from .config import REVISION_THRESHOLD, WEAK_THRESHOLD
from .model import Question
from .syllabus import SUBJECTS
from .tracker import Answer

LOG_COLUMNS = list(Answer.__dataclass_fields__)

STRONG, REVISE, WEAK = "Strong", "Needs revision", "Weak"
BAND_ICON = {STRONG: "🟢", REVISE: "🟠", WEAK: "🔴"}


def band(accuracy: float) -> str:
    if accuracy >= REVISION_THRESHOLD:
        return STRONG
    return REVISE if accuracy >= WEAK_THRESHOLD else WEAK


def log_frame(log: Sequence[Answer]) -> pd.DataFrame:
    return pd.DataFrame([a.to_dict() for a in log], columns=LOG_COLUMNS)


def accuracy_table(df: pd.DataFrame, by: list[str]) -> pd.DataFrame:
    """Attempts, correct answers and accuracy grouped by `by`, weakest first."""
    if df.empty:
        return pd.DataFrame(columns=[*by, "attempts", "correct", "questions", "accuracy", "band", "status"])
    out = (
        df.groupby(by, as_index=False)
        .agg(attempts=("is_correct", "size"), correct=("is_correct", "sum"),
             questions=("question_id", "nunique"))
    )
    out["accuracy"] = out["correct"] / out["attempts"]
    out["band"] = out["accuracy"].map(band)
    out["status"] = out["band"].map(lambda b: f"{BAND_ICON[b]} {b}")
    return out.sort_values(["accuracy", "attempts"], ascending=[True, False], ignore_index=True)


def revision_list(df: pd.DataFrame, threshold: float = REVISION_THRESHOLD) -> pd.DataFrame:
    """Micro-topics whose accuracy across all your attempts is below the threshold."""
    table = accuracy_table(df, ["subject", "macro_unit", "micro_topic"])
    return table[table["accuracy"] < threshold].reset_index(drop=True)


def strengths(df: pd.DataFrame, threshold: float = REVISION_THRESHOLD) -> pd.DataFrame:
    table = accuracy_table(df, ["subject", "macro_unit", "micro_topic"])
    return table[table["accuracy"] >= threshold].sort_values("accuracy", ascending=False, ignore_index=True)


def run_history(df: pd.DataFrame) -> pd.DataFrame:
    """Score per practice attempt, to show progress across repeated quizzes."""
    practice = df[df["mode"] == "practice"]
    if practice.empty:
        return pd.DataFrame(columns=["run", "answered", "correct", "accuracy"])
    out = practice.groupby("run", as_index=False).agg(answered=("is_correct", "size"), correct=("is_correct", "sum"))
    out["accuracy"] = out["correct"] / out["answered"]
    return out


def coverage(questions: Sequence[Question]) -> pd.DataFrame:
    """One row per question: subject, unit, session. Feeds the unit × session grid."""
    return pd.DataFrame(
        [{
            "subject": SUBJECTS[q.subject].name,
            "unit": q.macro_unit,
            "unit_no": q.unit_no,
            "session": q.session_label,
            "session_order": q.session_order,
            "dated": q.is_dated,
        } for q in questions],
        columns=["subject", "unit", "unit_no", "session", "session_order", "dated"],
    )


@dataclass(frozen=True, slots=True)
class TopicFrequency:
    sessions_loaded: int      # dated sessions of this subject in the bank
    subject_dated: int        # dated questions of this subject
    unit_dated: int           # … of them in this question's unit
    topic_dated: int          # … of them on this micro-topic
    topic_sessions: tuple[str, ...]

    def sentence(self, subject_short: str) -> str:
        if self.topic_dated:
            share = round(100 * self.unit_dated / self.subject_dated)
            return (
                f"This micro-topic appears in **{self.topic_dated} dated question(s)** across "
                f"{len(self.topic_sessions)} session(s): {', '.join(self.topic_sessions)}. Its unit accounts for "
                f"{self.unit_dated} of the {self.subject_dated} dated {subject_short} questions loaded ({share}%)."
            )
        if self.sessions_loaded:
            share = round(100 * self.unit_dated / self.subject_dated)
            return (
                f"No question on this micro-topic in the {self.sessions_loaded} dated {subject_short} session(s) loaded. "
                f"Its unit accounts for {self.unit_dated} of {self.subject_dated} dated questions ({share}%)."
            )
        return (
            f"No dated {subject_short} papers are loaded yet, so there is nothing to count. Add official papers "
            "to `data/questions/` and this line counts appearances session by session."
        )


def topic_frequency(questions: Sequence[Question], q: Question) -> TopicFrequency:
    dated = [x for x in questions if x.subject == q.subject and x.is_dated]
    on_topic = sorted((x for x in dated if x.micro_topic == q.micro_topic), key=lambda x: x.session_order)
    sessions = tuple(dict.fromkeys(x.session_label for x in on_topic))
    return TopicFrequency(
        sessions_loaded=len({x.session_key for x in dated}),
        subject_dated=len(dated),
        unit_dated=sum(x.macro_unit == q.macro_unit for x in dated),
        topic_dated=len(on_topic),
        topic_sessions=sessions,
    )
