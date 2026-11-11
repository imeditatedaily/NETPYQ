"""Knowledge Base: browse key facts and past questions topic by topic."""

import streamlit as st

from ..knowledge import short_stem, topic_pattern, topics_by_unit
from ..syllabus import SUBJECTS
from . import state
from .question_view import md


def render() -> None:
    if not st.session_state.get("user"):   # never shown to visitors who haven't signed in
        st.info("Sign in to see this page.", icon=":material/lock:")
        st.button("Sign in with Google", icon=":material/login:", on_click=st.login, args=("google",))
        return
    st.title("Knowledge Base")
    st.caption("Key facts for each syllabus topic, how the topic is asked, and every past question on it in your papers.")
    bank, kb, library, texts = state.get_bank(), state.get_knowledge(), state.get_library(), state.get_texts()
    notes = state.get_notes()
    subjects = [s for s in SUBJECTS if any(q.subject == s and q.is_dated for q in bank.questions)]
    if not subjects:
        st.info("Subscribe to a subject to open its knowledge base.", icon=":material/lock:")
        return
    c1, c2 = st.columns([1, 2])
    subject = c1.segmented_control("Subject", subjects, format_func=lambda s: SUBJECTS[s].short, key="kb_subject",
                                   default=subjects[0], required=True)
    units = topics_by_unit([q for q in bank.questions if q.is_dated], subject)
    unit = c2.selectbox("Syllabus unit", list(units), key=f"kb_unit_{subject}")
    topics = units.get(unit, [])
    written = sum(1 for t in topics if kb.note(subject, t))
    st.caption(f"{len(topics)} topics in this unit · key facts written for {written}")

    for topic in topics:
        note = kb.note(subject, topic)
        pattern = topic_pattern(bank.questions, subject, topic)
        label = f"{topic}  ·  {pattern.count} question{'s' if pattern.count != 1 else ''}"
        with st.expander(label, icon=":material/school:" if note else ":material/pending:"):
            if note:
                st.markdown("**Key facts**")
                st.markdown("\n".join(f"- {f}" for f in note.facts))
                if note.traps:
                    st.markdown("**Common traps**")
                    st.markdown("\n".join(f"- :orange[:material/warning:] {t}" for t in note.traps))
                cites = [library.by_id[s].citation for s in note.sources if s in library.by_id]
                if cites:
                    st.caption("From: " + "; ".join(md(c) for c in cites))
            else:
                st.caption("Key facts for this topic are being written.")
            for note in notes.for_topic(subject, topic):
                st.button(f"Read the notes: {note.title}", icon=":material/auto_stories:",
                          key=f"kbn-{subject}-{topic}-{note.id}", on_click=state.open_note, args=(note.id,))
            for text in texts.for_topic(subject, topic):
                st.button(f"Read the {text.title} line by line", icon=":material/menu_book:",
                          key=f"kbt-{subject}-{topic}-{text.id}", on_click=state.open_text, args=(subject, text.id))
            st.markdown(f"**How this topic is asked.** {pattern.sentence()}")
            for x in pattern.questions:
                st.markdown(f"- **{md(x.session_label)}** · {md(short_stem(x, 200))}  \n"
                            f"  :green[Answer: ({x.correct_answer}) {md(x.correct_text)}]")
            if pattern.count:
                st.button(f"Practise these {pattern.count}", icon=":material/target:", key=f"kbp-{subject}-{topic}",
                          on_click=state.practise_topic, args=(subject, unit, topic))
