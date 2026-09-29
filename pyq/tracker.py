"""Session tracking: the attempt log, practice runs and the mistake-review loop.

Nothing here imports Streamlit. The app keeps these objects in
st.session_state; the tests drive them directly.
"""

import random
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Literal

from .filters import Filters
from .model import Question

type Mode = Literal["practice", "review"]


@dataclass(frozen=True, slots=True)
class Answer:
    """One logged answer. Every submission, in either mode, adds one."""

    at: str                 # ISO timestamp
    mode: Mode
    run: int                # practice attempt number, or review loop number
    question_id: str
    subject: str
    macro_unit: str
    micro_topic: str
    question_type: str
    exam_session: str
    chosen: int
    correct_answer: int
    is_correct: bool

    def to_dict(self) -> dict:
        return asdict(self)


def make_answer(q: Question, chosen: int, mode: Mode, run: int, now: datetime | None = None) -> Answer:
    return Answer(
        at=(now or datetime.now()).isoformat(timespec="seconds"),
        mode=mode,
        run=run,
        question_id=q.id,
        subject=q.subject,
        macro_unit=q.macro_unit,
        micro_topic=q.micro_topic,
        question_type=q.question_type,
        exam_session=q.session_label,
        chosen=chosen,
        correct_answer=q.correct_answer,
        is_correct=q.is_correct(chosen),
    )


def answers_from_dicts(rows: Iterable[dict]) -> list[Answer]:
    """Rebuilds a log from an exported file. Raises ValueError on a bad row."""
    if not isinstance(rows, list):
        raise ValueError("the file must contain a list of answers")
    names = set(Answer.__dataclass_fields__)
    log = []
    for i, row in enumerate(rows, start=1):
        if not isinstance(row, dict) or not names <= row.keys():
            raise ValueError(f"row {i} is not an answer from this app")
        values = {k: row[k] for k in names}
        if not isinstance(values["is_correct"], bool) or values["mode"] not in ("practice", "review"):
            raise ValueError(f"row {i} has an invalid value")
        log.append(Answer(**values))
    return log


@dataclass(frozen=True, slots=True)
class Score:
    correct: int
    answered: int
    total: int

    @property
    def accuracy(self) -> float | None:
        return self.correct / self.answered if self.answered else None


@dataclass(slots=True)
class PracticeRun:
    """One pass through a deck of questions. Restarting creates a new run
    over the same deck, so the same quiz can be taken again and again."""

    number: int
    deck: list[str]
    filters: Filters
    shuffled: bool = False
    position: int = 0
    answers: dict[str, int] = field(default_factory=dict)  # question id -> chosen option

    @property
    def current_id(self) -> str | None:
        return self.deck[self.position] if self.position < len(self.deck) else None

    @property
    def finished(self) -> bool:
        return self.position >= len(self.deck)

    def submit(self, question_id: str, chosen: int) -> None:
        self.answers[question_id] = chosen

    def advance(self) -> None:
        self.position = min(self.position + 1, len(self.deck))

    def score(self, questions: Mapping[str, Question]) -> Score:
        correct = sum(questions[qid].is_correct(c) for qid, c in self.answers.items())
        return Score(correct, len(self.answers), len(self.deck))


def new_run(number: int, question_ids: Sequence[str], filters: Filters, shuffle: bool,
            rng: random.Random | None = None) -> PracticeRun:
    deck = list(question_ids)
    if shuffle:
        (rng or random).shuffle(deck)
    return PracticeRun(number=number, deck=deck, filters=filters, shuffled=shuffle)


def outstanding_mistakes(log: Sequence[Answer]) -> list[str]:
    """Questions whose most recent answer was wrong, oldest miss first.

    A question drops off as soon as you answer it correctly, in Practice or
    in Review, and comes back if you miss it again.
    """
    latest: dict[str, Answer] = {}
    for a in log:
        latest[a.question_id] = a
    wrong = [a for a in latest.values() if not a.is_correct]
    return [a.question_id for a in sorted(wrong, key=lambda a: a.at)]


@dataclass(frozen=True, slots=True)
class RoundResult:
    round: int
    correct: int
    total: int

    @property
    def accuracy(self) -> float:
        return self.correct / self.total if self.total else 0.0


@dataclass(slots=True)
class ReviewLoop:
    """Loops over your mistakes until one round is answered 100% correctly.

    Round 1 asks every mistake once. Each later round asks only the
    questions missed in the round before, reshuffled, so a missed question
    always comes back after the others have had a turn.
    """

    number: int
    queue: list[str]                       # still to answer in this round, head first
    round: int = 1
    round_size: int = 0
    missed: list[str] = field(default_factory=list)
    answers: dict[str, int] = field(default_factory=dict)  # this round: id -> chosen
    results: list[RoundResult] = field(default_factory=list)
    done: bool = False

    @property
    def current_id(self) -> str | None:
        return self.queue[0] if self.queue else None

    @property
    def round_correct(self) -> int:
        return len(self.answers) - len(self.missed)

    def submit(self, question_id: str, chosen: int, correct: bool) -> None:
        self.answers[question_id] = chosen
        if not correct:
            self.missed.append(question_id)

    def advance(self, rng: random.Random | None = None) -> None:
        """Moves past the current question; closes the round when it is empty."""
        if self.queue:
            self.queue.pop(0)
        if self.queue:
            return
        self.results.append(RoundResult(self.round, self.round_size - len(self.missed), self.round_size))
        if not self.missed:
            self.done = True
            return
        nxt = self.missed[:]
        (rng or random).shuffle(nxt)
        self.round += 1
        self.round_size = len(nxt)
        self.queue, self.missed, self.answers = nxt, [], {}


def start_review(number: int, mistake_ids: Sequence[str], rng: random.Random | None = None) -> ReviewLoop:
    queue = list(mistake_ids)
    (rng or random).shuffle(queue)
    return ReviewLoop(number=number, queue=queue, round_size=len(queue), done=not queue)
