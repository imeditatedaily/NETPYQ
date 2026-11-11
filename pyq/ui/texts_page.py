"""Sanskrit Texts: the source texts line by line, with a search for the line a question quotes.
Lines that previous-year questions were asked from are highlighted (data/pyq_lines.json)."""

import streamlit as st

from ..bank import Bank
from ..model import Question
from ..syllabus import SUBJECTS
from ..texts import Asked, SanskritText, TextLine
from . import state
from .question_view import md

FREE_LINES = 10      # what a signed-in user without the subject sees of each text


def _paper_tag(q: Question) -> str:
    """'Jun 2023 Q6', 'Nov 2017 P-III Q12': short enough for a badge."""
    bits = [f"{(q.exam_cycle or '')[:3]} {q.exam_year}"]
    if "III" in (q.paper or "") or (q.paper or "").strip().endswith("3"):
        bits.append("P-III")
    if q.question_no is not None:
        bits.append(f"Q{q.question_no}")
    return " ".join(bits)


def _asked_questions(asked: tuple[Asked, ...], bank: Bank) -> tuple[list[Question], list[Question]]:
    """(questions that quote the line, questions answered from it), oldest first; each question once."""
    quoted = [bank[a.question_id] for a in asked if a.how == "quoted" and a.question_id in bank]
    seen = {q.id for q in quoted}
    source = [bank[a.question_id] for a in asked if a.how != "quoted" and a.question_id in bank and a.question_id not in seen]
    order = lambda q: (q.session_order, q.question_no or 0)
    return sorted(quoted, key=order), sorted(source, key=order)


def _badges(asked: tuple[Asked, ...], bank: Bank) -> str:
    quoted, source = _asked_questions(asked, bank)
    out = []
    if quoted:
        out.append(":orange-badge[:material/format_quote: Quoted in " + " · ".join(_paper_tag(q) for q in quoted) + "]")
    if source:
        out.append(":violet-badge[:material/history_edu: Asked in " + " · ".join(_paper_tag(q) for q in source) + "]")
    return " ".join(out)


def _line_md(line: TextLine, show_meaning: bool, prefix: str = "", asked: tuple[Asked, ...] = (), bank: Bank | None = None) -> str:
    badges = _badges(asked, bank) if asked and bank is not None else ""
    rows = [md(x) for x in line.sa.split("\n")]
    if badges:
        rows = [f":orange-background[{r}]" for r in rows]
    out = (f":gray[{md(line.head)}]\n\n" if line.head else "") + f"**{prefix}{line.ref}**" + (f" {badges}" if badges else "")
    out += "  \n" + "  \n".join(rows)
    if show_meaning and line.en:
        out += f"  \n:gray[{md(line.en)}]"
    return out


def _cite(text: SanskritText) -> str:
    return " · ".join(text.divisions) if text.divisions else ""


def _stem(q: Question, limit: int = 220) -> str:
    text = " ".join(q.question_text.split())
    return text if len(text) <= limit else text[: limit - 1].rsplit(" ", 1)[0] + " …"


def render() -> None:
    if not st.session_state.get("user"):   # never shown to visitors who haven't signed in
        st.info("Sign in to see this page.", icon=":material/lock:")
        st.button("Sign in with Google", icon=":material/login:", on_click=st.login, args=("google",))
        return
    st.title("Sanskrit Texts")
    st.caption("The texts themselves, line by line, with chapter and verse numbers. Search for the line a question quotes. "
               "Lines that previous-year papers asked from are highlighted.")
    library, sources = state.get_texts(), state.get_library()
    asked_all, bank = state.get_asked(), state.get_full_bank()
    subjects = [s for s in SUBJECTS if library.for_subject(s)]
    if not subjects:
        st.info("No texts have been added yet.", icon=":material/menu_book:")
        return
    ss = st.session_state
    if (req := ss.pop("tx_open", None)) and req.get("subject") in subjects:   # see state.open_text
        ss["tx_subject"], ss["tx_query"], ss["tx_only"] = req["subject"], req.get("query", ""), bool(req.get("asked"))
        if (text := library.by_id(req.get("text") or "")) and text.subject == req["subject"]:
            ss[f"tx_unit_{text.subject}"], ss[f"tx_text_{text.subject}_{text.unit}"] = text.unit, text.id
    subject = subjects[0] if len(subjects) == 1 else st.segmented_control(
        "Subject", subjects, format_func=lambda s: SUBJECTS[s].short, key="tx_subject", default=subjects[0], required=True)
    texts = library.for_subject(subject)
    full = state.has_full_access(subject)
    n_asked = sum(len(asked_all.get(t.id, {})) for t in texts)
    st.caption(f"{len(texts)} texts · {sum(len(t.lines) for t in texts):,} numbered lines"
               + (f" · {n_asked} lines asked in previous papers" if n_asked else ""))
    if not full:
        with st.container(border=True, horizontal=True, vertical_alignment="center"):
            st.markdown(f":material/lock: You're seeing the first {FREE_LINES} lines of each text. "
                        f"Subscribe to **{SUBJECTS[subject].display}** to read and search them in full.")
            st.button("See plans", icon=":material/workspace_premium:", key="tx_plans", on_click=state.go, args=("plans",))

    query = st.text_input("Find a line", key="tx_query", placeholder="योगश्चित्तवृत्तिनिरोधः   or   yogas citta vritti nirodhah",
                          help="Type any part of a line in Devanagari or in Roman letters. Spaces and punctuation are ignored.")
    if query.strip():
        hits = library.search(query, subject=subject, limit=60 if full else 3)
        if not hits:
            st.info("No line matches. Try a shorter part of the line, or the other script.", icon=":material/search_off:")
        else:
            st.caption(f"{len(hits)} line{'s' if len(hits) != 1 else ''} found" + ("" if full else " (subscribers see every match)"))
            with st.container(key="tx-lines"):
                for h in hits:
                    with st.container(border=True):
                        st.markdown(_line_md(h.line, True, prefix=f"{md(h.text.title)} ",
                                             asked=asked_all.get(h.text.id, {}).get(h.line.ref, ()), bank=bank))
        return

    units = list(dict.fromkeys(t.unit for t in texts))
    c1, c2 = st.columns([1, 1])
    unit = c1.selectbox("Syllabus unit", units, format_func=SUBJECTS[subject].unit_label, key=f"tx_unit_{subject}")
    in_unit = {t.id: t for t in texts if t.unit == unit}

    def text_label(i: str) -> str:
        t, n = in_unit[i], len(asked_all.get(i, {}))
        return f"{t.label}  ({len(t.lines)} lines" + (f" · {n} asked)" if n else ")")

    text = in_unit[c2.selectbox("Text", list(in_unit), key=f"tx_text_{subject}_{unit}", format_func=text_label)]
    if text.about:
        st.markdown(md(text.about))
    cites = [sources.by_id[s].citation for s in text.sources if s in sources.by_id]
    note = " · ".join(x for x in (f"Cited as {_cite(text)}" if _cite(text) else "", "Text from: " + "; ".join(md(c) for c in cites) if cites else "") if x)
    if note:
        st.caption(note)

    asked = asked_all.get(text.id, {})
    only = False
    if asked:
        only = st.toggle(f"Only the {len(asked)} lines asked in previous papers", key="tx_only",
                         help="Orange badge: the question quotes the line. Violet badge: the answer to the question comes from the line.")
    lines = text.lines
    if only:
        lines = tuple(ln for ln in text.lines if ln.ref in asked)
    elif text.chapters and len(text.lines) > 40:
        chapter = st.pills(text.divisions[0].capitalize() if text.divisions else "Chapter", list(text.chapters),
                           key=f"tx_ch_{text.id}", default=text.chapters[0], required=True)
        lines = text.chapter(chapter)
    has_meaning = any(ln.en for ln in lines)
    show_meaning = st.toggle("Show meaning", value=True, key="tx_meaning") if has_meaning else False
    if not full:
        lines = lines[:FREE_LINES]
    with st.container(key="tx-lines"):
        if only:
            for ln in lines:
                with st.container(border=True):
                    st.markdown(_line_md(ln, show_meaning, asked=asked[ln.ref], bank=bank))
                    if full:
                        quoted, source = _asked_questions(asked[ln.ref], bank)
                        for q in quoted + source:
                            st.caption(f"**{_paper_tag(q)}** · {md(_stem(q))}")
        else:
            st.markdown("\n\n".join(_line_md(ln, show_meaning, asked=asked.get(ln.ref, ()), bank=bank) for ln in lines))
    if not full:
        st.caption(f"… {len(text.lines) - len(lines):,} more lines in this text for subscribers.")
