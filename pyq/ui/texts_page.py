"""Sanskrit Texts: the source texts line by line, with a search for the line a question quotes."""

import streamlit as st

from ..syllabus import SUBJECTS
from ..texts import SanskritText, TextLine
from . import state
from .question_view import md

FREE_LINES = 10      # what a signed-in user without the subject sees of each text


def _line_md(line: TextLine, show_meaning: bool, prefix: str = "") -> str:
    body = "  \n".join(md(x) for x in line.sa.split("\n"))
    out = (f":gray[{md(line.head)}]\n\n" if line.head else "") + f"**{prefix}{line.ref}**  \n{body}"
    if show_meaning and line.en:
        out += f"  \n:gray[{md(line.en)}]"
    return out


def _cite(text: SanskritText) -> str:
    return " · ".join(text.divisions) if text.divisions else ""


def render() -> None:
    if not st.session_state.get("user"):   # never shown to visitors who haven't signed in
        st.info("Sign in to see this page.", icon=":material/lock:")
        st.button("Sign in with Google", icon=":material/login:", on_click=st.login, args=("google",))
        return
    st.title("Sanskrit Texts")
    st.caption("The texts themselves, line by line, with chapter and verse numbers. Search for the line a question quotes.")
    library, sources = state.get_texts(), state.get_library()
    subjects = [s for s in SUBJECTS if library.for_subject(s)]
    if not subjects:
        st.info("No texts have been added yet.", icon=":material/menu_book:")
        return
    ss = st.session_state
    if (req := ss.pop("tx_open", None)) and req.get("subject") in subjects:   # see state.open_text
        ss["tx_subject"], ss["tx_query"] = req["subject"], req.get("query", "")
        if (text := library.by_id(req.get("text") or "")) and text.subject == req["subject"]:
            ss[f"tx_unit_{text.subject}"], ss[f"tx_text_{text.subject}_{text.unit}"] = text.unit, text.id
    subject = subjects[0] if len(subjects) == 1 else st.segmented_control(
        "Subject", subjects, format_func=lambda s: SUBJECTS[s].short, key="tx_subject", default=subjects[0], required=True)
    texts = library.for_subject(subject)
    full = state.has_full_access(subject)
    st.caption(f"{len(texts)} texts · {sum(len(t.lines) for t in texts):,} numbered lines")
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
                        st.markdown(_line_md(h.line, True, prefix=f"{md(h.text.title)} "))
        return

    units = list(dict.fromkeys(t.unit for t in texts))
    c1, c2 = st.columns([1, 1])
    unit = c1.selectbox("Syllabus unit", units, format_func=SUBJECTS[subject].unit_label, key=f"tx_unit_{subject}")
    in_unit = {t.id: t for t in texts if t.unit == unit}
    text = in_unit[c2.selectbox("Text", list(in_unit), key=f"tx_text_{subject}_{unit}",
                                format_func=lambda i: f"{in_unit[i].label}  ({len(in_unit[i].lines)})")]
    if text.about:
        st.markdown(md(text.about))
    cites = [sources.by_id[s].citation for s in text.sources if s in sources.by_id]
    note = " · ".join(x for x in (f"Cited as {_cite(text)}" if _cite(text) else "", "Text from: " + "; ".join(md(c) for c in cites) if cites else "") if x)
    if note:
        st.caption(note)

    lines = text.lines
    if text.chapters and len(text.lines) > 40:
        chapter = st.pills(text.divisions[0].capitalize() if text.divisions else "Chapter", list(text.chapters),
                           key=f"tx_ch_{text.id}", default=text.chapters[0], required=True)
        lines = text.chapter(chapter)
    has_meaning = any(ln.en for ln in lines)
    show_meaning = st.toggle("Show meaning", value=True, key="tx_meaning") if has_meaning else False
    if not full:
        lines = lines[:FREE_LINES]
    with st.container(key="tx-lines"):
        st.markdown("\n\n".join(_line_md(ln, show_meaning) for ln in lines))
    if not full:
        st.caption(f"… {len(text.lines) - len(lines):,} more lines in this text for subscribers.")
