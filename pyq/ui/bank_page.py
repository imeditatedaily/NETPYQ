"""Question Bank: what is loaded, how it spreads over units and sessions, and the data check."""

import altair as alt
import pandas as pd
import streamlit as st

from .. import analytics as an
from ..filters import ALL
from ..syllabus import SUBJECTS, SYLLABUS_NOTE
from . import state


def _heatmap(cov: pd.DataFrame) -> alt.Chart:
    counts = cov.groupby(["unit", "unit_no", "subject", "session", "session_order"], as_index=False).size()
    subject_rank = {s.name: i for i, s in enumerate(SUBJECTS.values())}
    unit_order = (counts.assign(rank=counts["subject"].map(subject_rank))
                  .sort_values(["rank", "unit_no"])["unit"].drop_duplicates().tolist())
    session_order = counts.sort_values("session_order")["session"].drop_duplicates().tolist()
    base = alt.Chart(counts).encode(
        x=alt.X("session:N", sort=session_order, title=None, axis=alt.Axis(labelAngle=0),
                scale=alt.Scale(paddingInner=0.08)),
        y=alt.Y("unit:N", sort=unit_order, title=None, axis=alt.Axis(labelLimit=360),
                scale=alt.Scale(paddingInner=0.12)),
    )
    cells = base.mark_rect(cornerRadius=3).encode(
        color=alt.Color("size:Q", title="Questions", scale=alt.Scale(scheme="blues", domainMin=0)),
        tooltip=[alt.Tooltip("unit:N", title="Unit"), alt.Tooltip("session:N", title="Session"),
                 alt.Tooltip("size:Q", title="Questions")],
    )
    text = base.mark_text(fontWeight="bold").encode(
        text="size:Q",
        color=alt.condition(alt.datum.size > counts["size"].max() / 2, alt.value("white"), alt.value("#0b0b0b")),
    )
    return (cells + text).properties(height=alt.Step(30))


def render() -> None:
    bank, library = state.get_bank(), state.get_library()
    subject = st.session_state.f_subject
    questions = [q for q in bank.questions if subject in (ALL, q.subject)]
    dated = [q for q in questions if q.is_dated]

    st.title("Question Bank", anchor=False)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Questions", len(questions))
    c2.metric("From dated papers", len(dated))
    c3.metric("Exam sessions", len({q.session_key for q in dated}))
    c4.metric("Micro-topics", len({(q.subject, q.micro_topic) for q in questions}))

    if not dated:
        st.info(
            "**No dated papers are loaded yet.** The questions here are PYQ-pattern samples, so the grid has a single "
            "*Undated* column and every frequency figure reads zero. Add official papers as JSON files in "
            "`data/questions/` (see the README there) and this page, the year filter and every Trend Insight box "
            "fill in with exact counts.", icon=":material/info:")

    st.subheader("Unit × exam session", anchor=False)
    st.caption("Each cell counts questions from one unit in one session. Read across a row to see whether a unit is rising or fading.")
    cov = an.coverage(questions)
    if cov.empty:
        st.write("No questions for this subject.")
    else:
        st.altair_chart(_heatmap(cov), width="stretch")

    st.subheader("Syllabus coverage", anchor=False)
    rows = []
    for s in SUBJECTS.values():
        if subject not in (ALL, s.id):
            continue
        for label in s.unit_labels:
            in_unit = [q for q in questions if q.macro_unit == label]
            rows.append({"Syllabus unit": label, "Questions": len(in_unit),
                         "From dated papers": sum(q.is_dated for q in in_unit),
                         "Micro-topics": len({q.micro_topic for q in in_unit}),
                         "Study sources": len(library.for_unit(label))})
    st.dataframe(pd.DataFrame(rows), hide_index=True)
    st.caption(SYLLABUS_NOTE)

    st.subheader("Data check", anchor=False)
    unknown = sorted({sid for q in bank.questions for sid in q.source_ids if sid not in library.by_id})
    if not bank.problems and not unknown:
        st.success(f"All {len(bank)} questions passed the checks.", icon=":material/verified:")
    for p in bank.problems:
        st.error(f"**{p.question_id}** in `{p.origin}`: " + "; ".join(p.errors), icon=":material/error:")
    if unknown:
        st.warning("These source_ids are not in sources/catalog.json: " + ", ".join(f"`{u}`" for u in unknown),
                   icon=":material/link_off:")
