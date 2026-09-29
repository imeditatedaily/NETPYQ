"""The Source Library: study texts mapped to syllabus units.

sources/catalog.json describes each text. An entry with a "file" points at
a PDF in sources/; an entry without one is a recommended text you have not
added yet. A PDF dropped into sources/ without a catalog entry still shows
up, as "uncatalogued", so adding a file is never wasted.
"""

import json
from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path

from .syllabus import UNIT_INDEX

KINDS: dict[str, str] = {
    "primary": "Primary text (translation)",
    "study": "Study / history",
    "paper": "Research paper",
    "notes": "Your notes (not a source)",
}


@dataclass(frozen=True, slots=True)
class Source:
    id: str
    title: str
    author: str = ""
    year: str = ""
    kind: str = "study"
    units: tuple[str, ...] = ()
    file: str | None = None
    licence: str = ""
    where: str = ""
    note: str = ""
    path: Path | None = None   # set when the file exists

    @property
    def available(self) -> bool:
        return self.path is not None

    @property
    def citation(self) -> str:
        bits = [b for b in (self.author, self.year) if b]
        return f"{self.title}" + (f" ({', '.join(bits)})" if bits else "")


@dataclass(frozen=True, slots=True)
class Library:
    sources: tuple[Source, ...]
    problems: tuple[str, ...] = ()
    by_id: Mapping[str, Source] = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "by_id", {s.id: s for s in self.sources})

    def for_unit(self, unit: str) -> list[Source]:
        return [s for s in self.sources if unit in s.units]


def load_library(folder: Path) -> Library:
    problems: list[str] = []
    raw: list = []
    catalog = folder / "catalog.json"
    if catalog.is_file():
        try:
            raw = json.loads(catalog.read_text(encoding="utf-8"))
            if not isinstance(raw, list):
                problems.append("catalog.json must contain a JSON list [ … ]")
                raw = []
        except json.JSONDecodeError as e:
            problems.append(f"catalog.json is not valid JSON: line {e.lineno}, column {e.colno}: {e.msg}")

    sources: list[Source] = []
    seen: set[str] = set()
    catalogued_files: set[str] = set()
    for i, entry in enumerate(raw, start=1):
        if not isinstance(entry, Mapping) or not entry.get("id") or not entry.get("title"):
            problems.append(f"catalog entry {i} needs at least an id and a title")
            continue
        sid = str(entry["id"])
        if sid in seen:
            problems.append(f'catalog entry {i}: duplicate id "{sid}"')
            continue
        seen.add(sid)
        units = tuple(u for u in entry.get("units", []) if isinstance(u, str))
        for u in units:
            if u not in UNIT_INDEX:
                problems.append(f'{sid}: "{u}" is not a syllabus unit label')
        kind = entry.get("kind", "study")
        if kind not in KINDS:
            problems.append(f'{sid}: kind "{kind}" is not one of {", ".join(KINDS)}')
            kind = "study"
        file = entry.get("file") or None
        path = None
        if file:
            catalogued_files.add(file)
            candidate = folder / file
            if candidate.is_file():
                path = candidate
            else:
                problems.append(f'{sid}: file "{file}" is not in sources/')
        sources.append(Source(
            id=sid, title=str(entry["title"]), author=str(entry.get("author", "")),
            year=str(entry.get("year", "")), kind=kind,
            units=tuple(u for u in units if u in UNIT_INDEX),
            file=file, licence=str(entry.get("licence", "")), where=str(entry.get("where", "")),
            note=str(entry.get("note", "")), path=path,
        ))

    if folder.is_dir():
        for pdf in sorted(folder.glob("*.pdf")):
            if pdf.name not in catalogued_files:
                sources.append(Source(
                    id=pdf.stem, title=pdf.stem.replace("-", " ").replace("_", " ").strip().capitalize(),
                    kind="study", file=pdf.name, path=pdf,
                    note="Uncatalogued: add an entry to sources/catalog.json to map it to syllabus units.",
                ))

    return Library(tuple(sources), tuple(problems))
