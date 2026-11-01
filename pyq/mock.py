"""Timed mock tests in the NTA computer-based-test pattern. Nothing here imports Streamlit.

NTA rules this follows: every question carries 2 marks, there is no negative
marking, an answer counts only once it is saved, and a question can be
marked for review (a saved answer that is also marked for review is still
evaluated). Time: 3 hours for 150 questions (Paper 1 + Paper 2), so 72 seconds
a question: 120 minutes for a 100-question Paper 2, 60 for a 50-question Paper 1.
"""

import random
from collections.abc import Sequence
from dataclasses import dataclass, field

from .model import Question

MARKS_PER_QUESTION = 2
SECONDS_PER_QUESTION = 72
MIXED_SIZE = 50

# Palette states, in NTA's words.
NOT_VISITED, NOT_ANSWERED, ANSWERED, MARKED, ANSWERED_MARKED = (
    "not_visited", "not_answered", "answered", "marked", "answered_marked")
STATUS_LABELS = {
    NOT_VISITED: "Not visited",
    NOT_ANSWERED: "Not answered",
    ANSWERED: "Answered",
    MARKED: "Marked for review",
    ANSWERED_MARKED: "Answered & marked for review",
}


@dataclass(frozen=True, slots=True)
class PaperChoice:
    key: str            # "session:June 2024" or "mixed"
    label: str
    question_ids: tuple[str, ...]

    @property
    def minutes(self) -> int:
        return round(len(self.question_ids) * SECONDS_PER_QUESTION / 60)


def paper_choices(questions: Sequence[Question], subject: str, seed: int) -> list[PaperChoice]:
    """Every dated paper of the subject (newest first), then a mixed test from all of them."""
    real = [q for q in questions if q.subject == subject and q.is_dated]
    by_session: dict[str, list[Question]] = {}
    for q in sorted(real, key=lambda q: (q.session_order, q.question_no or 0, q.id)):
        by_session.setdefault(q.session_label, []).append(q)
    out = [PaperChoice(f"session:{s}", f"{s} paper ({len(qs)} questions)", tuple(q.id for q in qs))
           for s, qs in sorted(by_session.items(), key=lambda kv: -kv[1][0].session_order)]
    if len(by_session) > 1:
        ids = [q.id for q in real]
        pick = random.Random(seed).sample(ids, min(MIXED_SIZE, len(ids)))
        out.append(PaperChoice("mixed", f"Mixed test: {len(pick)} questions from every paper", tuple(pick)))
    return out


@dataclass(slots=True)
class MockTest:
    number: int
    title: str
    subject: str
    question_ids: tuple[str, ...]
    started_at: float
    duration_s: int
    answers: dict[str, int] = field(default_factory=dict)
    marked: set[str] = field(default_factory=set)
    visited: set[str] = field(default_factory=set)
    position: int = 0
    submitted_at: float | None = None

    @classmethod
    def start(cls, number: int, choice: PaperChoice, subject: str, now: float) -> "MockTest":
        test = cls(number, choice.label, subject, choice.question_ids, now,
                   len(choice.question_ids) * SECONDS_PER_QUESTION)
        test.visited.add(test.current_id)
        return test

    # --- time ---------------------------------------------------------------------------
    def remaining(self, now: float) -> float:
        end = self.submitted_at if self.submitted_at is not None else now
        return max(0.0, self.started_at + self.duration_s - end)

    def expired(self, now: float) -> bool:
        return self.remaining(now) <= 0

    def time_taken(self, now: float) -> float:
        end = self.submitted_at if self.submitted_at is not None else now
        return min(self.duration_s, end - self.started_at)

    @property
    def submitted(self) -> bool:
        return self.submitted_at is not None

    # --- moving and answering -------------------------------------------------------------
    @property
    def current_id(self) -> str:
        return self.question_ids[self.position]

    def go(self, position: int) -> None:
        self.position = max(0, min(position, len(self.question_ids) - 1))
        self.visited.add(self.current_id)

    def save(self, choice: int | None, mark: bool = False) -> None:
        """Save & Next, or Mark for Review & Next (with or without an answer)."""
        qid = self.current_id
        if choice is not None:
            self.answers[qid] = choice
        if mark:
            self.marked.add(qid)
        else:
            self.marked.discard(qid)
        if self.position < len(self.question_ids) - 1:
            self.go(self.position + 1)

    def clear(self) -> None:
        self.answers.pop(self.current_id, None)

    def submit(self, now: float) -> None:
        if self.submitted_at is None:
            self.submitted_at = min(now, self.started_at + self.duration_s)

    def status(self, qid: str) -> str:
        if qid not in self.visited:
            return NOT_VISITED
        answered, marked = qid in self.answers, qid in self.marked
        if answered and marked:
            return ANSWERED_MARKED
        if marked:
            return MARKED
        return ANSWERED if answered else NOT_ANSWERED

    def counts(self) -> dict[str, int]:
        out = dict.fromkeys(STATUS_LABELS, 0)
        for qid in self.question_ids:
            out[self.status(qid)] += 1
        return out


@dataclass(frozen=True, slots=True)
class MockResult:
    total: int
    correct: int
    wrong: int
    unattempted: int

    @property
    def marks(self) -> int:
        return self.correct * MARKS_PER_QUESTION

    @property
    def max_marks(self) -> int:
        return self.total * MARKS_PER_QUESTION

    @property
    def accuracy(self) -> float | None:
        attempted = self.correct + self.wrong
        return self.correct / attempted if attempted else None


def score(test: MockTest, by_id: dict[str, Question]) -> MockResult:
    correct = sum(by_id[qid].is_correct(c) for qid, c in test.answers.items())
    attempted = len(test.answers)
    return MockResult(len(test.question_ids), correct, attempted - correct, len(test.question_ids) - attempted)
