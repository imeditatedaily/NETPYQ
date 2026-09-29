"""Performance Analytics: the live score, strengths vs weaknesses, and the revision plan."""

import altair as alt
import pandas as pd
import streamlit as st

from .. import analytics as an
from ..config import REVISION_THRESHOLD, WEAK_THRESHOLD
from . import state

# Status colours (reserved for good / needs work / weak) with an icon and a label beside them.
BAND_COLOURS = {an.STRONG: "#0ca30c", an.REVISE: "#ec835a", an.WEAK: "#d03b3b"}
BADGE = {an.STRONG: "green", an.REVISE: "orange", an.WEAK: "red"}


def _legend() -> str:
    lo, hi = round(WEAK_THRESHOLD * 100), round(REVISION_THRESHOLD * 100)
    return (f"🟢 **{an.STRONG}**: {hi}% or more · 🟠 **{an.REVISE}**: {lo}–{hi - 1}% · "
            f"🔴 **{an.WEAK}**: below {lo}%")


def _real_time_score(bank) -> None:
    st.subheader("Real-time score", anchor=False)
    run = st.session_state.run
    log = state.log()
    with st.container(border=True):
        st.markdown("**Current attempt**" + (f" (#{run.number}): {run.filters.describe()}" if run else ""))
        c1, c2, c3 = st.columns(3)
        if run:
            s = run.score(bank.by_id)
            c1.metric("Score", f"{s.correct} / {s.answered}")
            c2.metric("Accuracy", f"{s.accuracy:.0%}" if s.accuracy is not None else "—")
            c3.metric("Answered", f"{s.answered} of {s.total}")
        else:
            c1.metric("Score", "—")
    with st.container(border=True):
        st.markdown("**All attempts this session** (Practice and Review)")
        correct = sum(a.is_correct for a in log)
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Answers logged", len(log))
        c2.metric("Correct", correct)
        c3.metric("Accuracy", f"{correct / len(log):.0%}" if log else "—")
        c4.metric("Waiting in Review", len(state.mistakes(bank)))


def _unit_chart(units: pd.DataFrame) -> alt.Chart:
    # No numbers drawn on the bars: text colour cannot follow the light/dark theme
    # reliably, and every value is in the table below and in the tooltip.
    base = alt.Chart(units).encode(
        y=alt.Y("macro_unit:N", sort=alt.EncodingSortField("accuracy", order="ascending"), title=None,
                axis=alt.Axis(labelLimit=320)),
        x=alt.X("accuracy:Q", scale=alt.Scale(domain=[0, 1]), axis=alt.Axis(format="%", title="Accuracy", tickCount=5)),
        tooltip=[alt.Tooltip("macro_unit:N", title="Unit"), alt.Tooltip("accuracy:Q", format=".0%", title="Accuracy"),
                 alt.Tooltip("correct:Q", title="Correct"), alt.Tooltip("attempts:Q", title="Attempts"),
                 alt.Tooltip("band:N", title="Status")],
    )
    bars = base.mark_bar(size=16, cornerRadiusEnd=4).encode(
        color=alt.Color("band:N", title=None, legend=alt.Legend(orient="top"),
                        scale=alt.Scale(domain=list(BAND_COLOURS), range=list(BAND_COLOURS.values()))),
    )
    threshold = alt.Chart(pd.DataFrame({"x": [REVISION_THRESHOLD]})).mark_rule(strokeWidth=1, color="#898781").encode(x="x:Q")
    return (bars + threshold).properties(height=alt.Step(34))


def _strengths_weaknesses(df: pd.DataFrame) -> None:
    st.subheader("Strengths and weaknesses", anchor=False)
    st.caption(_legend() + ". The grey line marks the revision threshold.")
    by_unit, by_topic = st.tabs(["By syllabus unit", "By micro-topic"])
    progress = st.column_config.ProgressColumn("Accuracy", format="percent", min_value=0, max_value=1)
    with by_unit:
        units = an.accuracy_table(df, ["macro_unit"])
        st.altair_chart(_unit_chart(units), width="stretch")
        st.dataframe(units[["status", "macro_unit", "accuracy", "correct", "attempts", "questions"]], hide_index=True,
                     column_config={"status": "Status", "macro_unit": "Syllabus unit", "accuracy": progress,
                                    "correct": "Correct", "attempts": "Attempts", "questions": "Questions"})
    with by_topic:
        topics = an.accuracy_table(df, ["macro_unit", "micro_topic"])
        st.dataframe(topics[["status", "micro_topic", "macro_unit", "accuracy", "correct", "attempts"]], hide_index=True,
                     column_config={"status": "Status", "micro_topic": "Micro-topic", "macro_unit": "Syllabus unit",
                                    "accuracy": progress, "correct": "Correct", "attempts": "Attempts"})


def _revision_plan(df: pd.DataFrame) -> None:
    st.header("Topics to Revise", anchor=False)
    revise = an.revision_list(df)
    if revise.empty:
        st.success(f"No micro-topic is below {REVISION_THRESHOLD:.0%} across your attempts.", icon=":material/task_alt:")
    else:
        st.caption(f"Every micro-topic where your accuracy across all attempts is below {REVISION_THRESHOLD:.0%}, weakest first.")
        for i, row in revise.iterrows():
            with st.container(border=True):
                left, right = st.columns([3, 1], vertical_alignment="center")
                with left:
                    st.badge(f"{an.BAND_ICON[row.band]} {row.band}", color=BADGE[row.band])
                    st.markdown(f"**{row.micro_topic}**  \n{row.macro_unit}")
                    st.progress(float(row.accuracy), text=f"{row.accuracy:.0%}: {row.correct} of {row.attempts} correct")
                right.button("Practise", key=f"revise-{i}", icon=":material/target:", type="primary", width="stretch",
                             on_click=state.practise_topic, args=(row.subject, row.macro_unit, row.micro_topic))
    strong = an.strengths(df)
    if not strong.empty:
        with st.expander(f"Strengths ({len(strong)} micro-topics at {REVISION_THRESHOLD:.0%} or more)"):
            for row in strong.itertuples():
                st.markdown(f"🟢 **{row.micro_topic}** ({row.macro_unit}): {row.accuracy:.0%}, {row.correct}/{row.attempts}")


def _history(df: pd.DataFrame) -> None:
    runs = an.run_history(df)
    if len(runs) < 2:
        return
    st.subheader("Accuracy across attempts", anchor=False)
    st.caption("One bar per Practice attempt, to show whether repeating a quiz is paying off.")
    chart = alt.Chart(runs).mark_bar(size=24, cornerRadiusEnd=4, color="#2a78d6").encode(
        x=alt.X("run:O", title="Attempt"),
        y=alt.Y("accuracy:Q", scale=alt.Scale(domain=[0, 1]), axis=alt.Axis(format="%", title="Accuracy")),
        tooltip=[alt.Tooltip("run:O", title="Attempt"), alt.Tooltip("accuracy:Q", format=".0%", title="Accuracy"),
                 alt.Tooltip("correct:Q", title="Correct"), alt.Tooltip("answered:Q", title="Answered")],
    )
    st.altair_chart(chart, width="stretch")


def render() -> None:
    bank = state.get_bank()
    st.title("Performance Analytics", anchor=False)
    _real_time_score(bank)

    df = an.log_frame(state.log())
    if df.empty:
        st.info("Answer a few questions in Practice and your strengths, weaknesses and revision list appear here.",
                icon=":material/insights:")
        return

    _strengths_weaknesses(df)
    _revision_plan(df)
    _history(df)
    with st.expander(f"Attempt log ({len(df)} answers)"):
        st.dataframe(df, hide_index=True)
