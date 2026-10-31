"""Who may see which questions. Nothing here imports Streamlit.

- Everyone who signs in gets the built-in PYQ-pattern samples for free.
- A subject (Paper 1, Yoga, IKS) unlocks with its own monthly subscription.
- Questions transcribed from a published book are never shown to subscribers.
- Admins see everything.
"""

from collections.abc import Iterable
from dataclasses import dataclass

from .bank import Bank
from .config import BOOK_SOURCE_MARKERS
from .model import Question
from .syllabus import SUBJECTS

# Razorpay subscription states that mean "the current period is paid for".
PAID_STATES = frozenset({"active"})
# States that keep access until the end of the period already paid for.
WIND_DOWN_STATES = frozenset({"pending", "halted", "cancelled", "completed"})


@dataclass(frozen=True, slots=True)
class Subscription:
    razorpay_id: str
    email: str
    subject: str
    status: str                    # Razorpay's status: created, authenticated, active, pending, halted, cancelled, completed, expired
    current_end: int | None = None  # unix time the paid period ends
    short_url: str = ""            # Razorpay's hosted payment page
    created_at: str = ""
    updated_at: str = ""

    def grants_access(self, now: float) -> bool:
        if self.status in PAID_STATES:
            return True
        return self.status in WIND_DOWN_STATES and self.current_end is not None and now < self.current_end

    @property
    def awaiting_payment(self) -> bool:
        return self.status in ("created", "authenticated")

    @property
    def renews(self) -> bool:
        return self.status in ("active", "authenticated", "pending")


def is_book_sourced(q: Question) -> bool:
    return any(marker in q.source_note for marker in BOOK_SOURCE_MARKERS)


def sellable_questions(bank: Bank, subject: str) -> list[Question]:
    """The real-paper questions a subscriber to this subject gets."""
    return [q for q in bank.questions if q.subject == subject and q.source_type != "model" and not is_book_sourced(q)]


def sellable_subjects(bank: Bank) -> list[str]:
    """Subjects worth selling: at least one real paper a subscriber may see."""
    return [s for s in SUBJECTS if sellable_questions(bank, s)]


def unlocked_subjects(subs: Iterable[Subscription], now: float) -> set[str]:
    return {s.subject for s in subs if s.grants_access(now)}


def visible_bank(bank: Bank, *, admin: bool, unlocked: Iterable[str]) -> Bank:
    if admin:
        return bank
    unlocked = set(unlocked)
    kept = tuple(q for q in bank.questions
                 if q.source_type == "model" or (q.subject in unlocked and not is_book_sourced(q)))
    return Bank(kept, bank.problems)
