"""Sidebar filters: which questions match, and the choices each control offers."""

from collections import Counter
from collections.abc import Iterable, Sequence
from dataclasses import dataclass

from .model import QUESTION_TYPES, UNDATED, Question
from .syllabus import SUBJECTS

ALL = "all"


@dataclass(frozen=True, slots=True)
class Filters:
    subject: str = ALL   # ALL or a subject id
    session: str = ALL   # ALL, "2025", "2025-June" or "undated"
    unit: str = ALL      # ALL or a macro_unit label
    topic: str = ALL     # ALL or a micro_topic
    qtype: str = ALL     # ALL or a question_type

    def matches(self, q: Question) -> bool:
        if self.subject != ALL and q.subject != self.subject:
            return False
        if self.session != ALL:
            if self.session.isdigit():
                if q.exam_year != int(self.session):
                    return False
            elif q.session_key != self.session:
                return False
        if self.unit != ALL and q.macro_unit != self.unit:
            return False
        if self.topic != ALL and q.micro_topic != self.topic:
            return False
        if self.qtype != ALL and q.question_type != self.qtype:
            return False
        return True

    def describe(self) -> str:
        parts = []
        if self.subject != ALL:
            parts.append(SUBJECTS[self.subject].name)
        if self.session != ALL:
            parts.append("Undated" if self.session == UNDATED else self.session.replace("-", " "))
        if self.unit != ALL:
            parts.append(self.unit)
        if self.topic != ALL:
            parts.append(self.topic)
        if self.qtype != ALL:
            parts.append(QUESTION_TYPES[self.qtype])
        return " · ".join(parts) if parts else "All questions"


def apply(questions: Iterable[Question], f: Filters) -> list[Question]:
    return [q for q in questions if f.matches(q)]


def session_choices(questions: Sequence[Question]) -> dict[str, str]:
    """value -> label, newest year first; each year, then its sessions, then undated."""
    dated = [q for q in questions if q.is_dated]
    per_year = Counter(q.exam_year for q in dated)
    per_session = Counter(q.session_key for q in dated)
    order = {q.session_key: q.session_order for q in dated}
    labels = {q.session_key: q.session_label for q in dated}
    choices = {ALL: "All years and sessions"}
    for year in sorted(per_year, reverse=True):
        choices[str(year)] = f"{year}: all sessions ({per_year[year]})"
        for key in sorted((k for k in per_session if k.startswith(f"{year}-")), key=order.get, reverse=True):
            choices[key] = f"   {labels[key]} ({per_session[key]})"
    undated = len(questions) - len(dated)
    if undated:
        choices[UNDATED] = f"Undated / PYQ-pattern ({undated})"
    return choices


def unit_choices(questions: Sequence[Question], subject: str) -> dict[str, str]:
    """Every syllabus unit for the chosen subject(s), with its question count."""
    counts = Counter(q.macro_unit for q in questions)
    choices = {ALL: "All syllabus units"}
    for s in SUBJECTS.values():
        if subject in (ALL, s.id):
            for label in s.unit_labels:
                choices[label] = f"{label} ({counts[label]})"
    return choices


def topic_choices(questions: Sequence[Question], subject: str, unit: str) -> dict[str, str]:
    """Micro-topics within the chosen subject and unit, most frequent first."""
    counts = Counter(
        q.micro_topic for q in questions
        if subject in (ALL, q.subject) and unit in (ALL, q.macro_unit)
    )
    choices = {ALL: f"All micro-topics ({len(counts)})"}
    for topic, n in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])):
        choices[topic] = f"{topic} ({n})"
    return choices


def type_choices() -> dict[str, str]:
    return {ALL: "All formats", **QUESTION_TYPES}
