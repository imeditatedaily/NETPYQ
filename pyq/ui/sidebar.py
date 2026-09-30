"""Sidebar: filters that scope every page, and the session's attempt log."""

import streamlit as st

from ..analytics import log_frame
from ..bank import Bank
from ..filters import ALL, apply, session_choices, topic_choices, type_choices, unit_choices
from ..syllabus import SUBJECTS
from . import state


def _select(label: str, choices: dict[str, str], key: str, **kwargs) -> str:
    # A dependent filter can lose its current value (say, a unit of the other
    # subject); fall back to "all" before the widget is drawn.
    if st.session_state.get(key) not in choices:
        st.session_state[key] = ALL
    return st.selectbox(label, list(choices), format_func=choices.__getitem__, key=key, **kwargs)


def render(bank: Bank) -> None:
    ss = st.session_state
    questions = bank.questions
    with st.sidebar:
        st.header("Filters", anchor=False)
        subject = st.segmented_control(
            "Subject", [ALL, *SUBJECTS], key="f_subject", required=True,
            format_func=lambda s: "All" if s == ALL else SUBJECTS[s].short,
        )
        in_subject = [q for q in questions if subject in (ALL, q.subject)]
        _select("Exam year / session", session_choices(in_subject), "f_session",
                help="Only dated papers appear by year. The built-in samples are undated.")
        unit = _select("Syllabus unit", unit_choices(in_subject, subject), "f_unit")
        _select("Micro-topic", topic_choices(questions, subject, unit), "f_topic")
        _select("Question format", type_choices(), "f_qtype")
        st.toggle("Shuffle questions", key="shuffle", help="Applies when a new attempt starts.")
        matched = len(apply(questions, state.current_filters()))
        st.caption(f"**{matched}** of {len(questions)} questions match")

        st.divider()
        st.header("This session", anchor=False)
        log = state.log()
        correct = sum(a.is_correct for a in log)
        c1, c2 = st.columns(2)
        c1.metric("Answers logged", len(log))
        c2.metric("Accuracy", f"{correct / len(log):.0%}" if log else "—")
        st.caption(f"{len(state.mistakes(bank))} question(s) waiting in Review Mistakes.")

        st.download_button("Download log (JSON)", state.log_json(), file_name="ugc-net-attempt-log.json",
                           mime="application/json", icon=":material/download:", on_click="ignore",
                           disabled=not log, width="stretch",
                           help="Keeps your history: load it back after a refresh or on another device.")
        st.download_button("Download log (CSV)", log_frame(log).to_csv(index=False), file_name="ugc-net-attempt-log.csv",
                           mime="text/csv", icon=":material/table:", on_click="ignore", disabled=not log, width="stretch")
        uploader_key = f"log_upload_{ss.upload_nonce}"
        st.file_uploader("Load a saved log (JSON)", type=["json"], key=uploader_key,
                         on_change=state.load_log_file, args=(uploader_key,))
        with st.popover("Clear session", icon=":material/delete:", width="stretch"):
            st.write("Delete every logged answer and the current attempt? Download the log first if you want to keep it.")
            st.button("Yes, clear everything", type="primary", on_click=state.reset_session)
        st.caption("Answers are kept for this browser tab only. Refreshing starts a new session, so download the log to keep it.")
