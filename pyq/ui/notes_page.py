"""Study Notes: chapter-length notes to read on the site. There is no download: the app's
copy and print protection (protect.py) covers this page like every other."""

import streamlit as st

from ..syllabus import SUBJECTS
from . import state


def render() -> None:
    if not st.session_state.get("user"):   # never shown to visitors who haven't signed in
        st.info("Sign in to see this page.", icon=":material/lock:")
        st.button("Sign in with Google", icon=":material/login:", on_click=st.login, args=("google",))
        return
    st.title("Study Notes")
    st.caption("Chapter notes for the syllabus, written to be read like a book, with the sūtras they rest on.")
    library = state.get_notes()
    subjects = [s for s in SUBJECTS if library.for_subject(s)]
    if not subjects:
        st.info("No notes have been added yet.", icon=":material/menu_book:")
        return
    ss = st.session_state
    if (req := ss.pop("nt_open", None)) and (note := library.by_id(req.get("note") or "")):   # see state.open_note
        ss["nt_subject"] = note.subject
        ss[f"nt_unit_{note.subject}"], ss[f"nt_note_{note.subject}_{note.unit}"] = note.unit, note.id
    subject = subjects[0] if len(subjects) == 1 else st.segmented_control(
        "Subject", subjects, format_func=lambda s: SUBJECTS[s].short, key="nt_subject", default=subjects[0], required=True)
    notes = library.for_subject(subject)
    units = list(dict.fromkeys(n.unit for n in notes))
    c1, c2 = st.columns([1, 1])
    unit = c1.selectbox("Syllabus unit", units, format_func=SUBJECTS[subject].unit_label, key=f"nt_unit_{subject}")
    in_unit = {n.id: n for n in notes if n.unit == unit}
    note = in_unit[c2.selectbox("Chapter", list(in_unit), format_func=lambda i: in_unit[i].label,
                                key=f"nt_note_{subject}_{unit}")]
    full = state.has_full_access(subject)
    if not full:
        with st.container(border=True, horizontal=True, vertical_alignment="center"):
            st.markdown(f":material/lock: You're reading the opening of each chapter. "
                        f"Subscribe to **{SUBJECTS[subject].display}** to read the notes in full.")
            st.button("See plans", icon=":material/workspace_premium:", key="nt_plans", on_click=state.go, args=("plans",))
    sources = state.get_library()
    cites = [sources.by_id[s].citation for s in note.sources if s in sources.by_id]
    with st.container(key="nt-body", border=True):
        st.markdown(note.body if full else note.preview())
        if cites:
            st.caption("Based on: " + "; ".join(cites))
