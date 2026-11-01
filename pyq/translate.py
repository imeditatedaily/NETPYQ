"""The Hindi/English switch. Each question is stored in the language its paper
was transcribed in; data/translations/ holds the other language, field by
field, keyed by question id. Formulaic text (NTA's instructions, "A, B, E
only" options, match codes) is translated by rule here, so the files only
need the real sentences. Nothing here imports Streamlit.

A translation file is a JSON object: {question_id: {field: text or [texts]}}.
In a list, null means "translate this entry by rule". "@<question id>" as a
field's value reuses that question's translation (shared passages and tables);
"=" keeps the field as it is (a passage already in the target language).
Fields: question_text, options, items, list_i_title, list_i, list_ii_title,
list_ii, assertion, reason, prompt, passage, table_title, table_columns,
table_rows.
"""

import json
import re
from collections.abc import Mapping
from dataclasses import replace
from pathlib import Path

from .model import Question

EN, HI = "en", "hi"
LANG_NAMES = {EN: "English", HI: "हिन्दी"}
_DEVANAGARI = re.compile(r"[ऀ-ॿ]")

TEXT_FIELDS = ("question_text", "assertion", "reason", "prompt", "passage", "table_title",
               "list_i_title", "list_ii_title")
LIST_FIELDS = ("options", "items", "list_i", "list_ii", "table_columns")


def language(q: Question) -> str:
    """The language a question was transcribed in: whichever script most of its letters use."""
    sample = " ".join([q.question_text, *q.options, *q.items, *q.list_i, *q.list_ii, q.assertion])
    deva = len(_DEVANAGARI.findall(sample))
    latin = len(re.findall(r"[a-z]", sample))      # lowercase only: answer codes (A-IV, B-II) are capitals
    return HI if deva > latin else EN


# --- rule-based pieces --------------------------------------------------------------------

# NTA's standing instructions, in the spellings that occur in the papers.
_PROMPTS_HI_EN = {
    "नीचे दिए गए विकल्पों में से सही उत्तर का चयन कीजिए": "Choose the correct answer from the options given below",
    "नीचे दिए गए विकल्पों में से सही उत्तर चुनें": "Choose the correct answer from the options given below",
    "नीचे दिए गए विकल्पों में से सही उत्तर चुनिए": "Choose the correct answer from the options given below",
    "नीचे दिए गए विकल्पों में से सबसे उपयुक्त उत्तर का चयन कीजिए": "Choose the most appropriate answer from the options given below",
    "नीचे दिए गए विकल्पों में से सबसे उपयुक्त उत्तर चुनें": "Choose the most appropriate answer from the options given below",
    "दिए गए विकल्प में से सही उत्तर चयन कीजिए": "Choose the correct answer from the options given",
    "दिए गए विकल्पों में से सही उत्तर का चयन कीजिए": "Choose the correct answer from the options given",
    "सही विकल्प चुनिए": "Choose the correct option",
    "सही विकल्प चुनें": "Choose the correct option",
    "सही उत्तर चुनिए": "Choose the correct answer",
    "सही उत्तर चुनें": "Choose the correct answer",
    "कूट": "Codes",
    "उपर्युक्त कथनों के आलोक में, नीचे दिए गए विकल्पों में से सही उत्तर का चयन कीजिए":
        "In the light of the above statements, choose the correct answer from the options given below",
    "उपर्युक्त कथनों के आलोक में, नीचे दिए गए विकल्पों में से सबसे उपयुक्त उत्तर का चयन कीजिए":
        "In the light of the above statements, choose the most appropriate answer from the options given below",
    "उपरोक्त कथनों के आलोक में, नीचे दिए गए विकल्पों में से सही उत्तर का चयन कीजिए":
        "In the light of the above statements, choose the correct answer from the options given below",
}
_PROMPTS_EN_HI = {
    "Choose the correct answer from the options given below": "नीचे दिए गए विकल्पों में से सही उत्तर का चयन कीजिए",
    "Choose the most appropriate answer from the options given below": "नीचे दिए गए विकल्पों में से सबसे उपयुक्त उत्तर का चयन कीजिए",
    "Choose the correct answer from the options given": "दिए गए विकल्पों में से सही उत्तर का चयन कीजिए",
    "Choose the correct option": "सही विकल्प चुनिए",
    "Choose the correct answer": "सही उत्तर चुनिए",
    "Codes": "कूट",
    "Code": "कूट",
    "In the light of the above statements, choose the correct answer from the options given below":
        "उपर्युक्त कथनों के आलोक में, नीचे दिए गए विकल्पों में से सही उत्तर का चयन कीजिए",
    "In the light of the above statements, choose the most appropriate answer from the options given below":
        "उपर्युक्त कथनों के आलोक में, नीचे दिए गए विकल्पों में से सबसे उपयुक्त उत्तर का चयन कीजिए",
    "In light of the above statements, choose the correct answer from the options given below":
        "उपर्युक्त कथनों के आलोक में, नीचे दिए गए विकल्पों में से सही उत्तर का चयन कीजिए",
    "In the light of the above statements, choose the most appropriate answer from the options given":
        "उपर्युक्त कथनों के आलोक में, दिए गए विकल्पों में से सबसे उपयुक्त उत्तर का चयन कीजिए",
}
_PROMPTS_HI_EN |= {
    "उपर्युक्त दोनों कथनों के संदर्भ में निम्नलिखित में से सही विकल्प चुनिए": "In the context of the above two statements, choose the correct option from the following",
    "उपरोक्त दो कथनों के संदर्भ में निम्नलिखित में से सही विकल्प चुनिए": "In the context of the above two statements, choose the correct option from the following",
    "नीचे दिए गए विकल्पों में से सही विकल्प चुनें": "Choose the correct option from the options given below",
    "निम्नलिखित में से सही विकल्प चुनें": "Choose the correct option from the following",
    "दिए गए विकल्पों में से सही विकल्प चुनें": "Choose the correct option from the options given",
    "सही विकल्प का चयन करें": "Choose the correct option",
    "उपरोक्त कथनों के आलोक में, नीचे दिए गए विकल्पों में से सबसे उपयुक्त उत्तर का चयन कीजिए":
        "In the light of the above statements, choose the most appropriate answer from the options given below",
}
_PROMPTS_EN_HI |= {
    "Use the codes given below for correct answer": "सही उत्तर के लिए नीचे दिए गए कूटों का प्रयोग कीजिए",
    "Use the codes given below for the correct answer": "सही उत्तर के लिए नीचे दिए गए कूटों का प्रयोग कीजिए",
    "Use the codes for the correct answer": "सही उत्तर के लिए कूटों का प्रयोग कीजिए",
    "In the context of above two statements, which one of the following is correct ?": "उपर्युक्त दोनों कथनों के संदर्भ में, निम्नलिखित में से कौन-सा सही है?",
    "In the context of above two statements, which one of the following is correct": "उपर्युक्त दोनों कथनों के संदर्भ में, निम्नलिखित में से कौन-सा सही है",
    "Find the correct combination according to the codes": "कूटों के अनुसार सही संयोजन ज्ञात कीजिए",
    "Find the correct combination according to the code": "कूट के अनुसार सही संयोजन ज्ञात कीजिए",
    "Find the correct combination according to the codes given below": "नीचे दिए गए कूटों के अनुसार सही संयोजन ज्ञात कीजिए",
    "Find the correct answer according to the codes given below": "नीचे दिए गए कूटों के अनुसार सही उत्तर ज्ञात कीजिए",
}
_HI_SPELLINGS = (("दिये गये", "दिए गए"), ("चुनिये", "चुनिए"), ("कीजिये", "कीजिए"))

# Number words that turn up as whole options.
_NUMBERS = {"One": "एक", "Two": "दो", "Three": "तीन", "Four": "चार", "Five": "पाँच", "Six": "छः", "Seven": "सात",
            "Eight": "आठ", "Nine": "नौ", "Ten": "दस", "Eleven": "ग्यारह", "Twelve": "बारह", "Sixteen": "सोलह",
            "First": "प्रथम", "Second": "द्वितीय", "Third": "तृतीय", "Fourth": "चतुर्थ", "Fifth": "पंचम"}
_NUMBERS_HI = {v: k for k, v in _NUMBERS.items()} | {"छह": "Six", "पांच": "Five", "छ:": "Six"}

# List titles: "List I", "सूची - II" and so on.
_TITLE = re.compile(r"^(List|सूची)\s*[-–]?\s*(I{1,2})$")

# Option codes: (a), A, IV, (iii), 2 … joined by commas, dashes, "and"/"और"/"तथा".
_TOK = r"\(?(?:[A-H]|[a-h]|[IVX]{1,4}|[ivx]{1,4}|\d{1,3})\)?"
_JOIN = r"(?:\s*[-–,]\s*|\s+(?:and|और|तथा|&)\s+|\s+)"
_CODES = rf"{_TOK}(?:{_JOIN}{_TOK})*"
_PURE_CODE = re.compile(rf"^{_CODES}$")


def _codes(s: str, to: str) -> str:
    s = s.strip()
    return re.sub(r"\s+(?:और|तथा)\s+", " and ", s) if to == EN else re.sub(r"\s+and\s+", " और ", s)


# Assertion–Reason options, recognised by meaning.
_AR = {
    EN: ("Both (A) and (R) are true and (R) is the correct explanation of (A)",
         "Both (A) and (R) are true but (R) is NOT the correct explanation of (A)",
         "(A) is true but (R) is false", "(A) is false but (R) is true"),
    HI: ("(A) और (R) दोनों सही हैं और (R), (A) की सही व्याख्या है",
         "(A) और (R) दोनों सही हैं, परन्तु (R), (A) की सही व्याख्या नहीं है",
         "(A) सही है, परन्तु (R) गलत है", "(A) गलत है, परन्तु (R) सही है"),
}


def _assertion_reason(t: str) -> int | None:
    x = t.lower().replace("(", "").replace(")", "")
    if "both a and r" in x or "a और r दोनों" in x:
        if "not the correct explanation" in x or "व्याख्या नहीं" in x or "संबंधित नहीं" in x:
            return 1
        if "correct explanation" in x or "व्याख्या है" in x or "संबंधित हैं" in x:
            return 0
        return None
    if re.match(r"^a is (true|correct),? but r is (false|not correct)", x) or \
            re.match(r"^a सही है,? (परन्तु|लेकिन|किन्तु) r (गलत|सही नहीं)", x):
        return 2
    if re.match(r"^a is (false|not correct),? but r is (true|correct)", x) or \
            re.match(r"^a (गलत|सही नहीं) है,? (परन्तु|लेकिन|किन्तु) r सही", x):
        return 3
    return None


# "Statement I and II" options, recognised by meaning.
_STATEMENTS = {
    EN: ("Both Statement I and Statement II are true", "Both Statement I and Statement II are false",
         "Statement I is true but Statement II is false", "Statement I is false but Statement II is true"),
    HI: ("कथन I और II दोनों सही हैं", "कथन I और II दोनों गलत हैं",
         "कथन I सही है, लेकिन कथन II गलत है", "कथन I गलत है, लेकिन कथन II सही है"),
}
_T, _F = r"(?:true|correct|सही|सत्य)", r"(?:false|incorrect|not correct|गलत|असत्य|सही नहीं)"


def _statements(t: str) -> int | None:
    x = re.sub(r"[.।]\s*$", "", t.strip()).lower().replace("statement ", "s").replace("कथन ", "s")
    if re.fullmatch(rf"(?:both )?si (?:and|और|एवं|तथा) s?ii (?:are )?(?:both |दोनों )?{_F}(?: हैं)?", x):
        return 1
    if re.fullmatch(rf"(?:both )?si (?:and|और|एवं|तथा) s?ii (?:are )?(?:both |दोनों )?{_T}(?: हैं)?", x):
        return 0
    if re.fullmatch(rf"si (?:is )?{_T}(?: है)?,? (?:but|and|लेकिन|परन्तु|परंतु|किन्तु|और) sii (?:is )?{_F}(?: है)?", x):
        return 2
    if re.fullmatch(rf"si (?:is )?{_F}(?: है)?,? (?:but|and|लेकिन|परन्तु|परंतु|किन्तु|और) sii (?:is )?{_T}(?: है)?", x):
        return 3
    return None


def _split_tail(text: str) -> tuple[str, str]:
    m = re.match(r"^(.*?)(\s*[:।.?]\s*)$", text)
    return (m.group(1), m.group(2)) if m else (text, "")


def rule(text: str, to: str) -> str | None:
    """A translation of formulaic text, or None if it needs a human (or a file)."""
    t = text.strip()
    if not t:
        return text
    if re.fullmatch(r"[\d.,\s%₹/:+×()-]+", t):
        return text
    if (ar := _assertion_reason(t)) is not None:
        return _AR[to][ar]
    if (st := _statements(t)) is not None:
        return _STATEMENTS[to][st]
    if m := _TITLE.match(t):
        return ("List " if to == EN else "सूची ") + m.group(2)
    for a, b in _HI_SPELLINGS:
        t = t.replace(a, b)
    body, tail = _split_tail(t)
    only = re.fullmatch(rf"(?:केवल|[Oo]nly)\s*({_CODES})|({_CODES})\s*(?:केवल|[Oo]nly)", t.rstrip("।. "))
    if only:
        codes = _codes(only.group(1) or only.group(2), to)
        return f"{codes} only" if to == EN else f"केवल {codes}"
    both = re.fullmatch(rf"(?:[Bb]oth\s+)?({_TOK})\s+(?:and|और|तथा)\s+({_TOK})(?:\s+दोनों|\s+both)?", t)
    if both and ("दोनों" in t or "oth" in t):
        a, b = both.groups()
        return f"Both {a} and {b}" if to == EN else f"{a} और {b} दोनों"
    correct = re.fullmatch(rf"({_CODES})\s+(are|is)\s+(correct|true)\.?|({_CODES})\s+सही\s+(हैं|है)\s*[।.]?", t)
    if correct:
        codes = correct.group(1) or correct.group(4)
        many = bool(re.search(r",|\band\b|&|और|तथा", codes))
        if to == EN:
            return f"{_codes(codes, EN).replace('&', 'and')} {'are' if many else 'is'} correct."
        return f"{_codes(codes.replace('&', 'and'), HI)} सही {'हैं' if many else 'है'}।"
    if _PURE_CODE.match(t):
        return _codes(t, to)
    if to == EN:
        if body in _PROMPTS_HI_EN:
            return _PROMPTS_HI_EN[body] + tail.replace("।", ".")
        if t in _NUMBERS_HI:
            return _NUMBERS_HI[t]
    else:
        if body in _PROMPTS_EN_HI:
            return _PROMPTS_EN_HI[body] + (tail.replace(".", "।"))
        if t in _NUMBERS:
            return _NUMBERS[t]
    return None


# --- loading and applying -----------------------------------------------------------------

def load(folder: Path) -> dict[str, dict]:
    out: dict[str, dict] = {}
    if folder.is_dir():
        for path in sorted(folder.glob("*.json")):
            out.update(json.loads(path.read_text(encoding="utf-8")))
    return out


def _fields(q: Question) -> dict:
    out = {f: getattr(q, f) for f in TEXT_FIELDS}
    out |= {f: list(getattr(q, f)) for f in LIST_FIELDS}
    out["table_rows"] = [list(r) for r in q.table_rows]
    return out


def needed(q: Question) -> dict:
    """The strings of q that rules can't translate: what a translation file must supply."""
    to = EN if language(q) == HI else HI
    need: dict = {}
    for name, value in _fields(q).items():
        if name == "table_rows":
            rows = [[c for c in row if rule(c, to) is None] for row in value]
            if any(rows):
                need[name] = value
        elif isinstance(value, list):
            if any(rule(v, to) is None for v in value):
                need[name] = value
        elif value and rule(value, to) is None:
            need[name] = value
    return need


def translated(q: Question, to: str, table: Mapping[str, dict]) -> tuple[Question, str]:
    """q in language `to`, and its status: "original", "translated" or "missing"."""
    if language(q) == to:
        return q, "original"
    given = table.get(q.id, {})
    changes: dict = {}
    for name, value in _fields(q).items():
        v = given.get(name)
        if v == "=":                                        # already in the target language: keep it
            changes[name] = value if not isinstance(value, list) else tuple(value)
            continue
        if isinstance(v, str) and v.startswith("@"):        # shared passage/table: "@<question id>"
            v = table.get(v[1:], {}).get(name)
        if v is not None:
            if name == "table_rows":
                changes[name] = tuple(tuple(r) for r in v)
            elif isinstance(v, list):                       # null entries fall back to the rules
                out = [x if x is not None else rule(orig, to) for x, orig in zip(v, value)]
                if any(o is None for o in out) or len(v) != len(value):
                    return q, "missing"
                changes[name] = tuple(out)
            else:
                changes[name] = v
            continue
        if name == "table_rows":
            rows = [[rule(c, to) for c in row] for row in value]
            if any(c is None for row in rows for c in row):
                return q, "missing"
            changes[name] = tuple(tuple(r) for r in rows)
        elif isinstance(value, list):
            out = [rule(v, to) for v in value]
            if any(o is None for o in out):
                return q, "missing"
            changes[name] = tuple(out)
        elif value:
            out = rule(value, to)
            if out is None:
                return q, "missing"
            changes[name] = out
    return replace(q, **changes), "translated"
