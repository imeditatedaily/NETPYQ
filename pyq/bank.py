"""Loads the question bank: the built-in samples plus data/questions/*.json.

A question that fails its checks is left out and reported as a Problem,
so one bad entry never takes the app down.
"""

import json
from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Any

from .data.samples import SAMPLE_QUESTIONS
from .model import Question, QuestionError, parse_question
from .syllabus import SUBJECTS

SAMPLES_ORIGIN = "pyq/data/samples.py"


@dataclass(frozen=True, slots=True)
class Problem:
    origin: str
    question_id: str
    errors: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class Bank:
    questions: tuple[Question, ...]
    problems: tuple[Problem, ...] = ()
    by_id: Mapping[str, Question] = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "by_id", {q.id: q for q in self.questions})

    def __getitem__(self, question_id: str) -> Question:
        return self.by_id[question_id]

    def __contains__(self, question_id: object) -> bool:
        return question_id in self.by_id

    def __len__(self) -> int:
        return len(self.questions)


def _sort_key(q: Question) -> tuple:
    # Syllabus order, then newest paper first within a unit (undated last), then id.
    subject_order = list(SUBJECTS).index(q.subject)
    recency = -q.session_order if q.is_dated else 1
    return (subject_order, q.unit_no, recency, q.id)


def build_bank(entries: Iterable[tuple[Any, str]], problems: Iterable[Problem] = (),
               topic_notes: Mapping[str, Mapping[str, str]] | None = None) -> Bank:
    """entries: (raw question dict, where it came from) pairs.

    A question without its own trend_analysis takes the note for its
    micro-topic from topic_notes ({subject: {micro_topic: note}}).
    """
    found = list(problems)
    notes = topic_notes or {}
    questions: dict[str, Question] = {}
    for raw, origin in entries:
        qid = raw.get("id", "(no id)") if isinstance(raw, Mapping) else "(no id)"
        try:
            q = parse_question(raw)
        except QuestionError as e:
            found.append(Problem(origin, str(qid), tuple(e.errors)))
            continue
        if q.id in questions:
            found.append(Problem(origin, q.id, (f'duplicate id "{q.id}"',)))
            continue
        if not q.trend_analysis:
            note = notes.get(q.subject, {}).get(q.micro_topic, "")
            if not note:
                found.append(Problem(origin, q.id, (
                    f'no trend_analysis, and data/topics.json has no note for micro_topic "{q.micro_topic}"',)))
                continue
            q = replace(q, trend_analysis=note)
        questions[q.id] = q
    return Bank(tuple(sorted(questions.values(), key=_sort_key)), tuple(found))


def read_topic_notes(path: Path) -> tuple[dict[str, dict[str, str]], list[Problem]]:
    if not path.is_file():
        return {}, []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return {}, [Problem(path.name, "(whole file)", (f"not valid JSON: line {e.lineno}, column {e.colno}: {e.msg}",))]
    if not isinstance(data, dict) or not all(isinstance(v, dict) for v in data.values()):
        return {}, [Problem(path.name, "(whole file)", ('must look like {"yoga": {"micro-topic": "note", …}, "iks": {…}, "paper1": {…}}',))]
    return {s: {t: n for t, n in topics.items() if isinstance(n, str) and n.strip()} for s, topics in data.items()}, []


def read_question_files(folder: Path) -> tuple[list[tuple[Any, str]], list[Problem]]:
    entries: list[tuple[Any, str]] = []
    problems: list[Problem] = []
    if not folder.is_dir():
        return entries, problems
    for path in sorted(folder.glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            problems.append(Problem(path.name, "(whole file)", (f"not valid JSON: line {e.lineno}, column {e.colno}: {e.msg}",)))
            continue
        if not isinstance(data, list):
            problems.append(Problem(path.name, "(whole file)", ("the file must contain a JSON list [ … ] of questions",)))
            continue
        entries.extend((raw, path.name) for raw in data)
    return entries, problems


def load_bank(folder: Path, include_samples: bool = True, topic_file: Path | None = None) -> Bank:
    entries: list[tuple[Any, str]] = [(q, SAMPLES_ORIGIN) for q in SAMPLE_QUESTIONS] if include_samples else []
    file_entries, problems = read_question_files(folder)
    notes, note_problems = read_topic_notes(topic_file) if topic_file else ({}, [])
    return build_bank(entries + file_entries, problems + note_problems, notes)


def folder_signature(folder: Path, *extra: Path) -> tuple[tuple[str, float], ...]:
    """Changes whenever a question file (or an extra file) is added, removed or edited (used as a cache key)."""
    files = sorted(folder.glob("*.json")) if folder.is_dir() else []
    files += [p for p in extra if p.is_file()]
    return tuple((str(p), p.stat().st_mtime) for p in files)
