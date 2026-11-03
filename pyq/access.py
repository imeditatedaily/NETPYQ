"""Who may see which questions. Nothing here imports Streamlit.

- Everyone who signs in gets the built-in PYQ-pattern samples and the free
  real papers (config.FREE_PAPERS) for free.
- A subject (Paper 1, Yoga, IKS) unlocks with its own monthly subscription.
- Questions transcribed from a published book are not part of any paid plan;
  only the ones in a free paper are shown (to everyone).
- Admins see everything.
"""

from collections.abc import Iterable
from dataclasses import dataclass

from .bank import Bank
from .config import BOOK_SOURCE_MARKERS, FREE_PAPERS
from .model import Question
from .syllabus import SUBJECTS

# A one-time pass is stored like a subscription, under its Razorpay payment-link
# id ("plink_..."), with status "paid" once paid and current_end = the day it ends.
PASS_PREFIX = "plink_"

# Razorpay subscription states that mean "the current period is paid for".
PAID_STATES = frozenset({"active"})
# States that keep access until the end of the period already paid for.
WIND_DOWN_STATES = frozenset({"pending", "halted", "cancelled", "completed"})


@dataclass(frozen=True, slots=True)
class Subscription:
    razorpay_id: str
    email: str
    subject: str                   # a subject id, or several joined by "+" for a combo pass
    status: str                    # Razorpay's status: created, authenticated, active, pending, halted, cancelled, completed, expired
    current_end: int | None = None  # unix time the paid period ends
    short_url: str = ""            # Razorpay's hosted payment page
    created_at: str = ""
    updated_at: str = ""

    @property
    def is_pass(self) -> bool:
        return self.razorpay_id.startswith(PASS_PREFIX)

    @property
    def subjects(self) -> tuple[str, ...]:
        return tuple(self.subject.split("+"))

    def grants_access(self, now: float) -> bool:
        if self.is_pass:
            return self.status == "paid" and self.current_end is not None and now < self.current_end
        if self.status in PAID_STATES:
            return True
        return self.status in WIND_DOWN_STATES and self.current_end is not None and now < self.current_end

    @property
    def awaiting_payment(self) -> bool:
        if self.is_pass:
            return self.status in ("created", "partially_paid")
        return self.status in ("created", "authenticated")

    @property
    def renews(self) -> bool:
        return not self.is_pass and self.status in ("active", "authenticated", "pending")


def is_free(q: Question) -> bool:
    """A free sample, or a question from one of the free real papers."""
    if q.source_type == "model":
        return True
    return (q.subject, q.exam_year, q.exam_cycle) in FREE_PAPERS


def free_paper_label() -> str:
    """For copy: "Yoga, December 2018 and July 2018" (papers of one subject share its name)."""
    by_subject: dict[str, list[str]] = {}
    for s, year, cycle in FREE_PAPERS:
        by_subject.setdefault(s, []).append(f"{cycle} {year}")
    return "; ".join(f"{SUBJECTS[s].short}, {' and '.join(papers)}" for s, papers in by_subject.items())


def free_questions(bank: Bank) -> list[Question]:
    """The real-paper questions everyone gets for free (not the samples)."""
    return [q for q in bank.questions if q.source_type != "model" and is_free(q)]


def is_book_sourced(q: Question) -> bool:
    return any(marker in q.source_note for marker in BOOK_SOURCE_MARKERS)


def sellable_questions(bank: Bank, subject: str) -> list[Question]:
    """The real-paper questions a subscriber to this subject gets."""
    return [q for q in bank.questions if q.subject == subject and q.source_type != "model" and not is_book_sourced(q)]


def sellable_subjects(bank: Bank) -> list[str]:
    """Subjects worth selling: at least one real paper a subscriber may see."""
    return [s for s in SUBJECTS if sellable_questions(bank, s)]


def unlocked_subjects(subs: Iterable[Subscription], now: float) -> set[str]:
    return {subject for s in subs if s.grants_access(now) for subject in s.subjects}


def visible_bank(bank: Bank, *, admin: bool, unlocked: Iterable[str]) -> Bank:
    if admin:
        return bank
    unlocked = set(unlocked)
    kept = tuple(q for q in bank.questions
                 if is_free(q) or (q.subject in unlocked and not is_book_sourced(q)))
    return Bank(kept, bank.problems)
