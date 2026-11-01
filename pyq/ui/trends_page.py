"""PYQ Trends: how often each unit and micro-topic has been asked, paper by
paper. Built from every real paper (counts only), so free users see it too.
"""

import altair as alt
import pandas as pd
import streamlit as st

from .. import trends
from ..access import sellable_questions, sellable_subjects
from ..filters import ALL
from ..syllabus import SUBJECTS
from . import state

GREEN, AMBER, RUST, GREY = "#2f6b4f", "#eda100", "#c9673a", "#9a9d94"
TREND_COLOURS = {"Rising": GREEN, "Steady": GREY, "Fading": RUST, "—": GREY}
TREND_ICON = {"Rising": "▲ Rising", "Fading": "▼ Fading", "Steady": "● Steady", "—": "—"}


def _short_unit(label: str) -> str:
    # "Yoga Unit 4: Patanjala Yoga Sutra" -> "4 · Patanjala Yoga Sutra"
    head, _, title = label.partition(": ")
    return f"{head.rsplit(' ', 1)[-1]} · {title}"


def _unit_chart(units: pd.DataFrame) -> alt.Chart:
    data = units.assign(label=units["unit"].map(_short_unit), pct=units["share"])
    order = data.sort_values("unit_no")["label"].tolist()
    base = alt.Chart(data).encode(
        y=alt.Y("label:N", sort=order, title=None, axis=alt.Axis(labelLimit=340)),
        x=alt.X("pct:Q", title="Share of all questions", axis=alt.Axis(format="%", tickCount=5)),
        tooltip=[alt.Tooltip("unit:N", title="Unit"), alt.Tooltip("questions:Q", title="Questions"),
                 alt.Tooltip("pct:Q", format=".1%", title="Share"), alt.Tooltip("papers_asked:Q", title="Papers asked in"),
                 alt.Tooltip("trend:N", title="Trend")],
    )
    bars = base.mark_bar(size=18, cornerRadiusEnd=5).encode(
        color=alt.Color("trend:N", title="Trend", legend=alt.Legend(orient="top"),
                        scale=alt.Scale(domain=list(TREND_COLOURS)[:3], range=[GREEN, GREY, RUST])))
    text = base.mark_text(align="left", dx=5, color="#161b15").encode(text=alt.Text("pct:Q", format=".0%"))
    return (bars + text).properties(height=alt.Step(32))


def _heatmap(p: trends.Pattern, subject: str) -> alt.Chart:
    rows = []
    for r in p.units.itertuples():
        for session, n in zip(p.sessions, r.by_session):
            label = session if session in p.full else f"{session} (partial)"
            rows.append({"unit": _short_unit(r.unit), "unit_no": r.unit_no, "paper": label,
                         "questions": n, "share": n / p.sizes[session]})
    df = pd.DataFrame(rows)
    order = df.sort_values("unit_no")["unit"].drop_duplicates().tolist()
    papers = [s if s in p.full else f"{s} (partial)" for s in p.sessions]
    base = alt.Chart(df).encode(
        x=alt.X("paper:N", sort=papers, title=None,
                axis=alt.Axis(labelAngle=-35, labelLimit=160, labelOverlap=False, orient="top")),
        y=alt.Y("unit:N", sort=order, title=None, axis=alt.Axis(labelLimit=340)),
    )
    cells = base.mark_rect(cornerRadius=4).encode(
        color=alt.Color("questions:Q", title="Questions", legend=alt.Legend(orient="bottom"),
                        scale=alt.Scale(range=["#f3eedf", "#cfe3c4", GREEN, "#1d4433"], domainMin=0)),
        tooltip=[alt.Tooltip("unit:N", title="Unit"), alt.Tooltip("paper:N", title="Paper"),
                 alt.Tooltip("questions:Q", title="Questions"), alt.Tooltip("share:Q", format=".0%", title="Share of paper")],
    )
    text = base.mark_text(fontWeight="bold").encode(
        text="questions:Q",
        color=alt.condition(alt.datum.questions > df["questions"].max() * 0.55, alt.value("white"), alt.value("#161b15")))
    return (cells + text).properties(height=alt.Step(32))


def _topic_table(topics: pd.DataFrame, p: trends.Pattern) -> None:
    view = topics.assign(
        unit_label=topics["unit"].map(_short_unit),
        trend_label=topics["trend"].map(TREND_ICON),
        asked_in=topics["papers_asked"].astype(str) + f" of {p.papers}",
    )
    st.dataframe(
        view[["topic", "unit_label", "questions", "asked_share", "asked_in", "by_session", "last_asked", "trend_label"]],
        hide_index=True, width="stretch", height=560,
        column_config={
            "topic": st.column_config.TextColumn("Micro-topic", width="large"),
            "unit_label": st.column_config.TextColumn("Unit", width="small"),
            "questions": st.column_config.NumberColumn("Questions", help="Total questions on this topic"),
            "asked_share": st.column_config.ProgressColumn("Asked in papers", format="percent", min_value=0, max_value=1,
                                                           help="Share of papers that asked at least one question on it"),
            "asked_in": "Papers",
            "by_session": st.column_config.BarChartColumn("Paper by paper", y_min=0,
                                                          help="Questions per paper, oldest to newest: " + ", ".join(p.sessions)),
            "last_asked": "Last asked",
            "trend_label": "Trend",
        })


def _locked(what: str, key: str) -> None:
    """Teaser shown in place of a section a free user cannot see."""
    with st.container(border=True, key=f"locked-{key}"):
        st.markdown(f":material/lock: **{what}** is for subscribers.")
        st.caption("Subscribe to this subject to see the full paper-by-paper pattern, rising and fading topics, "
                   "and every micro-topic counted.")
        st.button("See plans", icon=":material/workspace_premium:", key=f"lock-btn-{key}",
                  on_click=state.go, args=("plans",), type="primary")


def render() -> None:
    full = state.get_full_bank()
    available = sellable_subjects(full)
    st.title("PYQ Trends", anchor=False)
    st.caption("What NTA actually asks: every unit and micro-topic counted across all the real papers loaded. "
               "Use it to decide what to study first.")
    if not available:
        st.info("Real papers are being added. Trends appear here as soon as the first paper is in.",
                icon=":material/schedule:")
        return

    current = st.session_state.get("f_subject", ALL)
    if st.session_state.get("trend_subject") not in available:
        st.session_state.trend_subject = current if current in available else available[0]
    subject = st.segmented_control("Subject", available, key="trend_subject", required=True,
                                   format_func=lambda s: SUBJECTS[s].display)
    p = trends.pattern(sellable_questions(full, subject))
    info = SUBJECTS[subject]
    full_access = state.has_full_access(subject)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Papers analysed", p.papers)
    c2.metric("Questions counted", p.questions)
    c3.metric("Micro-topics asked", len(p.topics))
    c4.metric("Asked in most papers", len(trends.regular_topics(p)),
              help=f"Micro-topics asked in at least {trends.REGULAR_SHARE:.0%} of papers")

    partial = [s for s in p.sessions if s not in p.full]
    if partial:
        st.caption(":material/info: Some papers are still being entered (" +
                   ", ".join(f"{s}: {p.sizes[s]} questions so far" for s in partial) +
                   "). They count towards totals but not towards Rising/Fading.")
    if p.papers < 3:
        st.info(f"Only {p.papers} {info.short} paper is loaded so far, so this shows one paper's spread. "
                "Trends across years appear as more papers are added.", icon=":material/schedule:")

    # --- unit-wise -------------------------------------------------------------------
    st.header("Unit-wise weightage", anchor=False)
    top = p.units.sort_values("share", ascending=False).head(3)
    st.markdown("**The top three units make up " + f"{top['share'].sum():.0%}" + " of all questions:** " +
                ", ".join(f"{_short_unit(u).split(' · ', 1)[1]} ({s:.0%})" for u, s in zip(top["unit"], top["share"])) + ".")
    st.altair_chart(_unit_chart(p.units), width="stretch")
    if not full_access:
        st.header("Topic-wise pattern", anchor=False)
        regular = trends.regular_topics(p)
        if not regular.empty:
            st.subheader("Asked almost every time: a preview", anchor=False)
            cols = st.columns(3)
            for i, r in enumerate(regular.head(3).itertuples()):
                with cols[i].container(border=True):
                    st.markdown(f"**{r.topic}**")
                    st.caption(_short_unit(r.unit))
                    st.progress(float(r.asked_share), text=f"Asked in {r.papers_asked} of {p.papers} papers")
            st.caption(f"{len(p.topics)} micro-topics are counted in all.")
        _locked("The full topic-wise pattern", "topics")
        return
    if p.papers > 1:
        st.subheader("Unit × paper", anchor=False)
        st.caption("Each cell is the number of questions from that unit in that paper. Read across a row to see if a "
                   "unit is gaining or losing weight. Papers marked partial are still being entered.")
        st.altair_chart(_heatmap(p, subject), width="stretch")

    # --- topic-wise ------------------------------------------------------------------
    st.header("Topic-wise pattern", anchor=False)
    regular = trends.regular_topics(p)
    if not regular.empty:
        st.subheader("Asked almost every time", anchor=False)
        st.caption(f"Micro-topics that appeared in at least {trends.REGULAR_SHARE:.0%} of papers. Master these first.")
        cols = st.columns(3)
        for i, r in enumerate(regular.head(9).itertuples()):
            with cols[i % 3].container(border=True):
                st.markdown(f"**{r.topic}**")
                st.caption(_short_unit(r.unit))
                st.progress(float(r.asked_share), text=f"Asked in {r.papers_asked} of {p.papers} papers · {r.questions} questions")
        if len(regular) > 9:
            st.caption(f"…and {len(regular) - 9} more in the table below.")

    if p.full and len(p.full) >= 4:
        rising = p.topics[p.topics["trend"] == "Rising"].head(6)
        fading = p.topics[p.topics["trend"] == "Fading"].head(6)
        left, right = st.columns(2)
        with left.container(border=True):
            st.markdown(f":green[**▲ Rising topics**]  \nA bigger share of recent papers than older ones")
            for r in rising.itertuples():
                st.markdown(f"- {r.topic} · {r.questions} Qs, last asked {r.last_asked}")
            if rising.empty:
                st.caption("None yet.")
        with right.container(border=True):
            st.markdown(f":orange[**▼ Fading topics**]  \nAsked less in recent papers than older ones")
            for r in fading.itertuples():
                st.markdown(f"- {r.topic} · {r.questions} Qs, last asked {r.last_asked}")
            if fading.empty:
                st.caption("None yet.")

    st.subheader("Every micro-topic", anchor=False)
    units = ["All units", *p.units["unit"].tolist()]
    pick = st.selectbox("Unit", units, format_func=lambda u: u if u == "All units" else _short_unit(u))
    shown = p.topics if pick == "All units" else p.topics[p.topics["unit"] == pick]
    _topic_table(shown, p)
    st.caption("Sorted by how many papers asked the topic, then by number of questions. "
               "More papers are being added, and every count here updates as they come in.")
