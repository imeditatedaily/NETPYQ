"""Study notes: chapter-length notes in Markdown, read on the site (never offered as downloads).

Each note is one file, data/notes/<id>.md, with a small header:

    ---
    title: न्याय दर्शन
    title_en: Nyāya Darśana
    subject: yoga
    unit: 1
    order: 2
    topics: Shad-darshanas: Samkhya, Yoga and Vedanta
    sources: dasgupta-1922-history-indian-philosophy | notes-bharatiya-darshan-drive
    ---
    # न्याय दर्शन
    …

"topics" and "sources" are separated by " | " (topic names contain commas). The body is
Markdown; "## " headings divide it into sections. Nothing here imports Streamlit.

Two markers tie the notes to the papers:

    [[PYQ: YOGA-2019DEC-P2-Q081, YOGA-2023JUN-P2-Q12]]   the past questions asked from this point
    [[LIKELY]]                                            a point not yet asked that the pattern suggests

They are shown as badges ("PYQ Dec 2019 Q81 · Jun 2023 Q12", "Likely next"), and a question links back to
the section that marks it (NoteLibrary.sections_for).
"""

import re
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path

_FIELDS = ("title", "title_en", "subject", "unit", "order", "topics", "sources")
_PYQ = re.compile(r"\[\[PYQ:\s*([^\]]+)\]\]")
_LIKELY = re.compile(r"\[\[LIKELY\]\]")


def marked_ids(text: str) -> list[str]:
    """The question ids in the [[PYQ: …]] markers of a piece of notes, in order."""
    return [i.strip() for m in _PYQ.finditer(text) for i in m.group(1).split(",") if i.strip()]


def expand_markers(text: str, label: Callable[[str], str | None]) -> str:
    """Markdown with the markers turned into badges; `label` names a question id ("Jun 2023 Q6") or None to drop it."""
    def pyq(m: re.Match) -> str:
        names = list(dict.fromkeys(n for n in (label(i.strip()) for i in m.group(1).split(",")) if n))
        return f":orange-badge[:material/history_edu: PYQ {' · '.join(names)}]" if names else ""
    return _LIKELY.sub(":blue-badge[:material/trending_up: Likely next]", _PYQ.sub(pyq, text))


@dataclass(frozen=True, slots=True)
class Note:
    id: str
    title: str
    title_en: str
    subject: str
    unit: int
    order: int
    topics: tuple[str, ...]
    sources: tuple[str, ...]
    body: str

    @property
    def label(self) -> str:
        return f"{self.title} · {self.title_en}" if self.title_en else self.title

    @property
    def sections(self) -> tuple[str, ...]:
        return tuple(m.group(1).strip() for m in re.finditer(r"^## (.+)$", self.body, flags=re.M))

    def section_texts(self) -> tuple[tuple[str, str], ...]:
        """(heading, text) for each "## " section; the text before the first heading is left out."""
        parts = re.split(r"^## (.+)$", self.body, flags=re.M)
        return tuple((parts[i].strip(), parts[i + 1]) for i in range(1, len(parts) - 1, 2))

    def preview(self) -> str:
        """The note up to its second section: what someone without the subject may read."""
        starts = [m.start() for m in re.finditer(r"^## ", self.body, flags=re.M)]
        return self.body[: starts[1]] if len(starts) > 1 else self.body

    @property
    def words(self) -> int:
        return len(self.body.split())


@dataclass(frozen=True, slots=True)
class NoteLibrary:
    notes: tuple[Note, ...] = ()
    problems: tuple[str, ...] = ()
    _by_question: dict = field(default_factory=dict, compare=False, repr=False)   # question id → [(note id, heading)]

    def __post_init__(self) -> None:
        for n in self.notes:
            for heading, text in n.section_texts():
                for qid in marked_ids(text):
                    places = self._by_question.setdefault(qid, [])
                    if (n.id, heading) not in places:
                        places.append((n.id, heading))

    def sections_for(self, question_id: str) -> list[tuple[Note, str]]:
        """The notes sections a past question was asked from: [(note, section heading)]."""
        return [(self.by_id(nid), h) for nid, h in self._by_question.get(question_id, [])]

    def section(self, note_id: str, heading: str) -> str:
        note = self.by_id(note_id)
        return next((t for h, t in note.section_texts() if h == heading), "") if note else ""

    def __len__(self) -> int:
        return len(self.notes)

    def by_id(self, note_id: str) -> Note | None:
        return next((n for n in self.notes if n.id == note_id), None)

    def for_subject(self, subject: str) -> tuple[Note, ...]:
        return tuple(n for n in self.notes if n.subject == subject)

    def for_topic(self, subject: str, topic: str) -> tuple[Note, ...]:
        return tuple(n for n in self.notes if n.subject == subject and topic in n.topics)


def _parse(path: Path) -> tuple[Note | None, list[str]]:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, flags=re.S)
    if not m:
        return None, [f"{path.name}: the header between --- lines is missing"]
    head, body = {}, m.group(2).strip() + "\n"
    for line in m.group(1).splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            head[key.strip()] = value.strip()
    missing = [k for k in ("title", "subject", "unit") if not head.get(k)]
    if missing:
        return None, [f'{path.name}: header needs {", ".join(missing)}']
    unknown = sorted(set(head) - set(_FIELDS))
    problems = [f'{path.name}: unknown header field "{u}"' for u in unknown]
    try:
        unit, order = int(head["unit"]), int(head.get("order") or 0)
    except ValueError:
        return None, problems + [f'{path.name}: "unit" and "order" must be numbers']
    split = lambda v: tuple(x.strip() for x in (v or "").split(" | ") if x.strip())
    return Note(path.stem, head["title"], head.get("title_en", ""), head["subject"], unit, order,
                split(head.get("topics")), split(head.get("sources")), body), problems


def load_notes(folder: Path) -> NoteLibrary:
    notes, problems = [], []
    for path in sorted(folder.glob("*.md")) if folder.is_dir() else []:
        note, found = _parse(path)
        problems += found
        if note:
            notes.append(note)
    notes.sort(key=lambda n: (n.subject, n.unit, n.order, n.title))
    return NoteLibrary(tuple(notes), tuple(problems))
