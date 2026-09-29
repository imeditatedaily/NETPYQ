"""The Question record and the checks every question must pass."""

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any, Literal

from .syllabus import SUBJECTS, UNIT_INDEX, Subject

type QuestionType = Literal["mcq", "match", "assertion_reason", "statements", "sequence"]
type SourceType = Literal["official", "memory_based", "model"]

QUESTION_TYPES: dict[str, str] = {
    "mcq": "Single correct answer",
    "match": "Match List I with List II",
    "assertion_reason": "Assertion–Reason",
    "statements": "Multiple statements",
    "sequence": "Sequence / chronology",
}

SOURCE_TYPES: dict[str, str] = {
    "official": "Official NTA paper",
    "memory_based": "Memory-based PYQ",
    "model": "PYQ-pattern model",
}

CYCLES = ("June", "December")
UNDATED = "undated"


class QuestionError(ValueError):
    """Raised with every problem found in one question, not just the first."""

    def __init__(self, errors: list[str]):
        super().__init__("; ".join(errors))
        self.errors = errors


@dataclass(frozen=True, slots=True, kw_only=True)
class Question:
    id: str
    subject: str
    question_text: str
    options: tuple[str, ...]
    correct_answer: int  # option number, 1-based, as in NTA answer keys
    detailed_explanation: str
    macro_unit: str
    micro_topic: str
    trend_analysis: str
    question_type: QuestionType = "mcq"
    exam_year: int | None = None
    exam_cycle: str | None = None
    source_type: SourceType = "model"
    source_note: str = ""
    items: tuple[str, ...] = ()          # statements / sequence items, labelled A, B, C…
    list_i_title: str = "List I"
    list_i: tuple[str, ...] = ()         # match: labelled A, B, C…
    list_ii_title: str = "List II"
    list_ii: tuple[str, ...] = ()        # match: labelled I, II, III…
    assertion: str = ""
    reason: str = ""
    prompt: str = ""
    references: tuple[str, ...] = ()
    source_ids: tuple[str, ...] = ()     # Source Library entries to study this from

    @property
    def subject_info(self) -> Subject:
        return SUBJECTS[self.subject]

    @property
    def unit_no(self) -> int:
        return UNIT_INDEX[self.macro_unit][1]

    @property
    def is_dated(self) -> bool:
        return self.exam_year is not None

    @property
    def session_key(self) -> str:
        return f"{self.exam_year}-{self.exam_cycle}" if self.is_dated else UNDATED

    @property
    def session_label(self) -> str:
        return f"{self.exam_cycle} {self.exam_year}" if self.is_dated else "Undated"

    @property
    def session_order(self) -> int:
        """Chronological sort key; undated questions sort last."""
        if not self.is_dated:
            return 1_000_000
        return self.exam_year * 2 + CYCLES.index(self.exam_cycle)

    @property
    def source_label(self) -> str:
        if self.source_type == "model":
            return "PYQ-pattern model, undated"
        return f"{self.session_label} · {SOURCE_TYPES[self.source_type]}"

    @property
    def correct_text(self) -> str:
        return self.options[self.correct_answer - 1]

    def is_correct(self, chosen: int) -> bool:
        return chosen == self.correct_answer


def _text(raw: Mapping[str, Any], key: str) -> str:
    value = raw.get(key)
    return value.strip() if isinstance(value, str) else ""


def _texts(value: Any) -> tuple[str, ...] | None:
    if isinstance(value, (list, tuple)) and all(isinstance(v, str) and v.strip() for v in value):
        return tuple(v.strip() for v in value)
    return None


def _list_block(lists: Any, key: str, default_title: str) -> tuple[str, tuple[str, ...] | None]:
    """Reads lists.list_i / lists.list_ii: {"title": ..., "items": [...]}."""
    block = lists.get(key) if isinstance(lists, Mapping) else None
    if not isinstance(block, Mapping):
        return default_title, None
    title = block.get("title")
    return (title.strip() if isinstance(title, str) and title.strip() else default_title), _texts(block.get("items"))


def parse_question(raw: Mapping[str, Any]) -> Question:
    """Builds a Question from a dict (Python data or parsed JSON).

    Raises QuestionError listing everything that is wrong, so a whole file
    can be fixed in one pass.
    """
    if not isinstance(raw, Mapping):
        raise QuestionError(["not a dictionary / JSON object"])
    errors: list[str] = []

    for key in ("id", "subject", "question_text", "detailed_explanation",
                "macro_unit", "micro_topic", "trend_analysis"):
        if not _text(raw, key):
            errors.append(f'"{key}" is missing or empty')

    subject = _text(raw, "subject")
    if subject and subject not in SUBJECTS:
        errors.append(f'subject "{subject}" is not one of: {", ".join(SUBJECTS)}')

    macro_unit = _text(raw, "macro_unit")
    if macro_unit:
        if macro_unit not in UNIT_INDEX:
            errors.append(f'macro_unit "{macro_unit}" is not a syllabus unit label (see pyq/syllabus.py)')
        elif UNIT_INDEX[macro_unit][0].id != subject:
            errors.append(f'macro_unit "{macro_unit}" belongs to {UNIT_INDEX[macro_unit][0].name}, not "{subject}"')

    options = _texts(raw.get("options"))
    correct = raw.get("correct_answer")
    if options is None or len(options) < 2:
        errors.append('"options" must be a list of at least two answer texts')
    elif not isinstance(correct, int) or isinstance(correct, bool) or not 1 <= correct <= len(options):
        errors.append(f'"correct_answer" must be an option number from 1 to {len(options)}')

    qtype = raw.get("question_type", "mcq")
    if qtype not in QUESTION_TYPES:
        errors.append(f'question_type "{qtype}" is not one of: {", ".join(QUESTION_TYPES)}')

    list_i_title, list_i = _list_block(raw.get("lists"), "list_i", "List I")
    list_ii_title, list_ii = _list_block(raw.get("lists"), "list_ii", "List II")
    if qtype == "match" and not (list_i and list_ii):
        errors.append("a match question needs lists.list_i.items and lists.list_ii.items")

    items = _texts(raw.get("items")) if raw.get("items") is not None else ()
    if items is None:
        errors.append('"items" must be a list of texts')
    elif qtype in ("statements", "sequence") and len(items) < 2:
        errors.append(f'a {qtype} question needs an "items" list')

    if qtype == "assertion_reason" and not (_text(raw, "assertion") and _text(raw, "reason")):
        errors.append('an assertion_reason question needs "assertion" and "reason"')

    year, cycle = raw.get("exam_year"), raw.get("exam_cycle")
    dated = year is not None or cycle is not None
    if dated:
        if not isinstance(year, int) or isinstance(year, bool) or not 2000 <= year <= 2100:
            errors.append('"exam_year" must be a year such as 2025')
        if cycle not in CYCLES:
            errors.append('"exam_cycle" must be "June" or "December"')

    source = raw.get("source") or {}
    source_type = source.get("type") if isinstance(source, Mapping) else None
    source_type = source_type or ("official" if dated else "model")
    if source_type not in SOURCE_TYPES:
        errors.append(f'source.type "{source_type}" is not one of: {", ".join(SOURCE_TYPES)}')
    elif source_type == "model" and dated:
        errors.append("a model question cannot have an exam_year or exam_cycle")
    elif source_type != "model" and not dated:
        errors.append(f"a {source_type} question needs exam_year and exam_cycle")

    references = _texts(raw.get("references") or [])
    if references is None:
        errors.append('"references" must be a list of texts')
    source_ids = _texts(raw.get("source_ids") or [])
    if source_ids is None:
        errors.append('"source_ids" must be a list of Source Library ids')

    if errors:
        raise QuestionError(errors)

    return Question(
        id=_text(raw, "id"),
        subject=subject,
        question_text=_text(raw, "question_text"),
        options=options,
        correct_answer=correct,
        detailed_explanation=_text(raw, "detailed_explanation"),
        macro_unit=macro_unit,
        micro_topic=_text(raw, "micro_topic"),
        trend_analysis=_text(raw, "trend_analysis"),
        question_type=qtype,
        exam_year=year,
        exam_cycle=cycle,
        source_type=source_type,
        source_note=source.get("note", "") if isinstance(source, Mapping) else "",
        items=items or (),
        list_i_title=list_i_title,
        list_i=list_i or (),
        list_ii_title=list_ii_title,
        list_ii=list_ii or (),
        assertion=_text(raw, "assertion"),
        reason=_text(raw, "reason"),
        prompt=_text(raw, "prompt"),
        references=references,
        source_ids=source_ids,
    )
