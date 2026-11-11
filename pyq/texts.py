"""Sanskrit source texts, line by line.

Exam questions quote the texts themselves (a mantra, a sūtra, half a verse), so
each text is kept as numbered lines in data/texts/<id>.json:

    {"id": "yoga-sutra", "title": "Pātañjala Yoga Sūtra", "title_sa": "पातञ्जलयोगसूत्रम्", "subject": "yoga", "unit": 4,
     "about": "…", "divisions": ["pāda", "sūtra"], "topics": ["…"], "sources": ["gretil-etexts"],
     "lines": [{"ref": "1.2", "sa": "योगश्चित्तवृत्तिनिरोधः ॥", "en": "optional meaning", "head": "optional rubric"}]}

"ref" is the chapter-and-verse number as it is cited ("2.47", "1.3.14"); a line
break inside "sa" is a line break in the verse. Nothing here imports Streamlit.
"""

import json
import re
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True, slots=True)
class TextLine:
    ref: str
    sa: str
    en: str = ""
    head: str = ""      # the editor's rubric above this line, where the edition has one


@dataclass(frozen=True, slots=True)
class SanskritText:
    id: str
    title: str
    title_sa: str
    subject: str
    unit: int
    about: str = ""
    divisions: tuple[str, ...] = ()       # what each part of a ref counts, e.g. ("adhyāya", "śloka")
    topics: tuple[str, ...] = ()          # micro-topics in the bank this text belongs to
    sources: tuple[str, ...] = ()
    lines: tuple[TextLine, ...] = ()

    @property
    def chapters(self) -> tuple[str, ...]:
        """The first part of each ref, in order, for texts cited as chapter.verse; empty for a single run of lines."""
        if not self.lines or all("." not in ln.ref for ln in self.lines):
            return ()
        return tuple(dict.fromkeys(ln.ref.split(".")[0] for ln in self.lines))

    def chapter(self, chapter: str) -> tuple[TextLine, ...]:
        return tuple(ln for ln in self.lines if ln.ref.split(".")[0] == chapter)

    @property
    def label(self) -> str:
        return f"{self.title} · {self.title_sa}"


@dataclass(frozen=True, slots=True)
class Asked:
    """A previous-year question asked from a line: "quoted" when the question quotes it,
    "source" when the line is where the answer comes from."""
    question_id: str
    how: str


@dataclass(frozen=True, slots=True)
class Hit:
    text: SanskritText
    line: TextLine


@dataclass(frozen=True, slots=True)
class TextLibrary:
    texts: tuple[SanskritText, ...] = ()
    problems: tuple[str, ...] = ()
    _keys: dict = field(default_factory=dict, compare=False, repr=False)   # {(text id, ref): (devanagari key, roman key)}

    def __len__(self) -> int:
        return len(self.texts)

    def by_id(self, text_id: str) -> SanskritText | None:
        return next((t for t in self.texts if t.id == text_id), None)

    def for_subject(self, subject: str) -> tuple[SanskritText, ...]:
        return tuple(t for t in self.texts if t.subject == subject)

    def for_topic(self, subject: str, topic: str) -> tuple[SanskritText, ...]:
        return tuple(t for t in self.texts if t.subject == subject and topic in t.topics)

    @property
    def line_count(self) -> int:
        return sum(len(t.lines) for t in self.texts)

    def search(self, query: str, subject: str | None = None, text_id: str | None = None, limit: int = 60) -> list[Hit]:
        """Lines that contain the query. Devanagari and Roman spellings both work; spaces,
        punctuation and the anusvāra/class-nasal difference are ignored."""
        deva = bool(re.search(r"[ऀ-ॿ]", query))
        key = deva_key(query) if deva else roman_key(query)
        if len(key) < 3:
            return []
        hits = []
        for t in self.texts:
            if (subject and t.subject != subject) or (text_id and t.id != text_id):
                continue
            for ln in t.lines:
                if key in self._keys[(t.id, ln.ref)][0 if deva else 1]:
                    hits.append(Hit(t, ln))
                    if len(hits) >= limit:
                        return hits
        return hits


# --- search keys -------------------------------------------------------------------

_NASAL_VIRAMA = re.compile("[ङञणनम]्(?=[क-ह])")
_DROP_DEVA = re.compile(r"[^ऄ-हा-्ॠ-ॣंः]")


def deva_key(s: str) -> str:
    """Devanagari with spaces, dandas, digits and avagrahas removed, and class nasals written as anusvāra."""
    s = unicodedata.normalize("NFC", s).replace("ँ", "ं").replace("ꣳ", "ं")
    s = _DROP_DEVA.sub("", s)
    return _NASAL_VIRAMA.sub("ं", s)


_CONS = {"क": "k", "ख": "kh", "ग": "g", "घ": "gh", "ङ": "n", "च": "c", "छ": "ch", "ज": "j", "झ": "jh", "ञ": "n",
         "ट": "t", "ठ": "th", "ड": "d", "ढ": "dh", "ण": "n", "त": "t", "थ": "th", "द": "d", "ध": "dh", "न": "n",
         "प": "p", "फ": "ph", "ब": "b", "भ": "bh", "म": "m", "य": "y", "र": "r", "ल": "l", "ळ": "l", "व": "v",
         "श": "s", "ष": "s", "स": "s", "ह": "h"}
_VOWELS = {"अ": "a", "आ": "a", "इ": "i", "ई": "i", "उ": "u", "ऊ": "u", "ऋ": "r", "ॠ": "r", "ऌ": "l", "ए": "e", "ऐ": "ai",
           "ओ": "o", "औ": "au"}
_SIGNS = {"ा": "a", "ि": "i", "ी": "i", "ु": "u", "ू": "u", "ृ": "r", "ॄ": "r", "ॢ": "l", "े": "e", "ै": "ai", "ो": "o",
          "ौ": "au"}


def _romanise(s: str) -> str:
    out = []
    chars = unicodedata.normalize("NFC", s)
    for i, ch in enumerate(chars):
        if ch in _CONS:
            out.append(_CONS[ch])
            nxt = chars[i + 1] if i + 1 < len(chars) else ""
            if nxt not in _SIGNS and nxt != "्":
                out.append("a")
        elif ch in _VOWELS:
            out.append(_VOWELS[ch])
        elif ch in _SIGNS:
            out.append(_SIGNS[ch])
        elif ch in "ंँ":
            out.append("m")
        elif ch == "ः":
            out.append("h")
        elif ch == "ॐ":
            out.append("om")
    return "".join(out)


def _loosen(s: str) -> str:
    """Folds the spellings people type for the same sound: sh/s, ch/c, aa/a, ee/i, oo/u, w/v, ri/r, n/m before a consonant."""
    s = "".join(c for c in unicodedata.normalize("NFD", s.lower()) if c.isascii() and c.isalpha())
    s = s.replace("w", "v").replace("ee", "i").replace("oo", "u").replace("ri", "r").replace("ru", "r")
    s = re.sub(r"(?<=[kgcjtdpbs])h", "", s)                 # aspirates and sh/ch are typed inconsistently
    s = re.sub(r"[nm](?=[kgcjtdpbsyrlvh])", "m", s)         # anusvāra or class nasal
    return re.sub(r"(.)\1+", r"\1", s)


def roman_key(s: str) -> str:
    return _loosen(_romanise(s) if re.search(r"[ऀ-ॿ]", s) else s)


# --- loading -----------------------------------------------------------------------

def _load_one(path: Path) -> tuple[SanskritText | None, list[str]]:
    try:
        d = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return None, [f"{path.name}: not valid JSON (line {e.lineno}): {e.msg}"]
    problems = []
    for key in ("id", "title", "title_sa", "subject", "unit", "lines"):
        if key not in d:
            return None, [f'{path.name}: "{key}" is missing']
    if d["id"] != path.stem:
        problems.append(f'{path.name}: "id" should be "{path.stem}"')
    lines, seen = [], set()
    for i, ln in enumerate(d["lines"] if isinstance(d["lines"], list) else []):
        ref, sa = (ln.get("ref"), ln.get("sa")) if isinstance(ln, dict) else (None, None)
        if not (isinstance(ref, str) and ref.strip() and isinstance(sa, str) and sa.strip()):
            problems.append(f'{path.name}: line {i + 1} needs "ref" and "sa"')
            continue
        if ref in seen:
            problems.append(f'{path.name}: ref "{ref}" is used twice')
            continue
        seen.add(ref)
        lines.append(TextLine(ref, sa, str(ln.get("en") or ""), str(ln.get("head") or "")))
    if not lines:
        return None, problems + [f"{path.name}: no lines"]
    return SanskritText(d["id"], d["title"], d["title_sa"], d["subject"], int(d["unit"]), str(d.get("about") or ""),
                        tuple(d.get("divisions") or ()), tuple(d.get("topics") or ()), tuple(d.get("sources") or ()),
                        tuple(lines)), problems


def load_asked(path: Path) -> dict[str, dict[str, tuple[Asked, ...]]]:
    """data/pyq_lines.json, written by tools/link_pyq_lines.py: text id → ref → the questions asked from that line."""
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return {t: {ref: tuple(Asked(str(q), str(how)) for q, how in qs) for ref, qs in refs.items()}
            for t, refs in raw.items() if isinstance(refs, dict)}


def load_texts(folder: Path) -> TextLibrary:
    texts, problems, keys = [], [], {}
    for path in sorted(folder.glob("*.json")) if folder.is_dir() else []:
        text, found = _load_one(path)
        problems += found
        if text:
            texts.append(text)
            for ln in text.lines:
                keys[(text.id, ln.ref)] = (deva_key(ln.sa), roman_key(ln.sa))
    texts.sort(key=lambda t: (t.subject, t.unit, t.title))
    return TextLibrary(tuple(texts), tuple(problems), keys)
