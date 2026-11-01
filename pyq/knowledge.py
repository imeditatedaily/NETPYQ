"""The knowledge base: key facts per micro-topic, and how each topic is asked.

data/knowledge.json holds written facts:

    {"yoga": {"Bhagavad Gita": {"facts": ["…", "…"], "sources": ["telang-1882-bhagavadgita"]}}, "paper1": {…}}

The question patterns are not written: they are counted from the loaded
papers, so they grow as papers are added. Nothing here imports Streamlit.
"""

import json
from collections import Counter
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from pathlib import Path

from .model import QUESTION_TYPES, Question


@dataclass(frozen=True, slots=True)
class TopicNote:
    facts: tuple[str, ...] = ()
    sources: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class KnowledgeBase:
    notes: dict = field(default_factory=dict)     # {subject: {micro_topic: TopicNote}}
    problems: tuple[str, ...] = ()

    def note(self, subject: str, topic: str) -> TopicNote | None:
        return self.notes.get(subject, {}).get(topic)

    def __len__(self) -> int:
        return sum(len(t) for t in self.notes.values())


def load_knowledge(path: Path) -> KnowledgeBase:
    if not path.is_file():
        return KnowledgeBase()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return KnowledgeBase(problems=(f"{path.name}: not valid JSON (line {e.lineno}): {e.msg}",))
    notes, problems = {}, []
    for subject, topics in (data.items() if isinstance(data, dict) else []):
        for topic, entry in (topics.items() if isinstance(topics, dict) else []):
            facts = entry.get("facts") if isinstance(entry, dict) else None
            if not isinstance(facts, list) or not all(isinstance(f, str) and f.strip() for f in facts):
                problems.append(f'{subject} / {topic}: "facts" must be a list of text')
                continue
            sources = entry.get("sources") or []
            notes.setdefault(subject, {})[topic] = TopicNote(tuple(facts), tuple(s for s in sources if isinstance(s, str)))
    return KnowledgeBase(notes, tuple(problems))


@dataclass(frozen=True, slots=True)
class TopicPattern:
    """How a micro-topic has been asked in the loaded papers."""

    questions: tuple[Question, ...]          # dated questions on the topic, newest first
    formats: tuple[tuple[str, int], ...]     # (format label, count), most common first
    sessions: tuple[str, ...]                # session labels, oldest first

    @property
    def count(self) -> int:
        return len(self.questions)

    def sentence(self) -> str:
        if not self.questions:
            return "Not yet asked in the loaded papers."
        fmt = ", ".join(f"{n} {label.lower()}" for label, n in self.formats)
        papers = len(self.sessions)
        return (f"Asked **{self.count}** time{'s' if self.count != 1 else ''} in **{papers}** paper{'s' if papers != 1 else ''} "
                f"({', '.join(self.sessions)}). Formats: {fmt}.")


def topic_pattern(questions: Iterable[Question], subject: str, topic: str) -> TopicPattern:
    on_topic = [q for q in questions if q.subject == subject and q.micro_topic == topic and q.is_dated]
    on_topic.sort(key=lambda q: (-q.session_order, q.question_no or 0, q.id))
    formats = Counter(QUESTION_TYPES[q.question_type] for q in on_topic).most_common()
    sessions = tuple(dict.fromkeys(q.session_label for q in sorted(on_topic, key=lambda q: q.session_order)))
    return TopicPattern(tuple(on_topic), tuple(formats), sessions)


def short_stem(q: Question, limit: int = 140) -> str:
    text = " ".join(q.question_text.split())
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


def topics_by_unit(questions: Sequence[Question], subject: str) -> dict[str, list[str]]:
    """Micro-topics that have questions, grouped by syllabus unit, in syllabus order."""
    out: dict[str, list[str]] = {}
    for q in sorted((q for q in questions if q.subject == subject), key=lambda q: (q.unit_no, q.micro_topic)):
        topics = out.setdefault(q.macro_unit, [])
        if q.micro_topic not in topics:
            topics.append(q.micro_topic)
    return out
