"""Admin: the visit-to-payment funnel, who has paid, and how much each user has practised."""

import time
from datetime import datetime, timedelta, timezone

import altair as alt
import pandas as pd
import streamlit as st

from .. import store
from ..config import PASSES, SUBJECT_PRICE_INR
from ..syllabus import SUBJECTS
from . import account

PERIODS = {"Last 7 days": 7, "Last 30 days": 30, "Last 90 days": 90, "All time": None}


def _names(sub) -> str:
    return " + ".join(SUBJECTS[s].short if s in SUBJECTS else s for s in sub.subjects)


def _funnel(eng, subs) -> None:
    st.subheader("Funnel: where people drop off", anchor=False)
    period = st.segmented_control("Period", list(PERIODS), default="Last 30 days", key="admin_period")
    days = PERIODS.get(period or "Last 30 days")
    since = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat(timespec="seconds") if days else ""
    rows = store.list_events(eng, since)
    steps = store.funnel(rows, subs, since)
    df = pd.DataFrame(steps, columns=["event", "Step", "People"])
    first = df["People"].iloc[0] or 1
    df["Of visitors"] = df["People"] / first
    df["From previous step"] = (df["People"] / df["People"].shift(1).replace(0, pd.NA)).astype("Float64")
    chart = alt.Chart(df).mark_bar(cornerRadiusEnd=5, color="#2f6b4f").encode(
        y=alt.Y("Step:N", sort=None, title=None, axis=alt.Axis(labelLimit=260)),
        x=alt.X("People:Q", title="People"),
        tooltip=["Step", "People", alt.Tooltip("Of visitors:Q", format=".1%")],
    ).properties(height=alt.Step(36))
    st.altair_chart(chart, width="stretch")
    st.dataframe(df.drop(columns="event"), hide_index=True, column_config={
        "Of visitors": st.column_config.NumberColumn(format="percent"),
        "From previous step": st.column_config.NumberColumn(format="percent")})
    worst = df.iloc[1:].dropna(subset=["From previous step"])
    if not worst.empty and df["People"].iloc[0]:
        w = worst.loc[worst["From previous step"].idxmin()]
        st.info(f"The biggest drop is at **{w['Step']}**: only {w['From previous step']:.0%} of the people at the "
                "step before get there.", icon=":material/insights:")
    st.caption("Visits count browser sessions on the landing page; later steps count distinct signed-in emails. "
               "Paid counts people whose payment went through, from Razorpay.")
    if rows:
        daily = pd.DataFrame(rows)
        daily["day"] = daily["at"].str[:10]
        daily = daily[daily["event"].isin(["visit", "signin", "daily"])].groupby(["day", "event"]).size().reset_index(name="n")
        if not daily.empty:
            st.altair_chart(alt.Chart(daily).mark_line(point=True).encode(
                x=alt.X("day:T", title=None), y=alt.Y("n:Q", title="Per day"),
                color=alt.Color("event:N", title=None, scale=alt.Scale(
                    domain=["visit", "signin", "daily"], range=["#2f6b4f", "#eda100", "#6b4fa0"])),
            ).properties(height=220), width="stretch")
            st.caption("visit = landing page, signin = signed in, daily = question-of-the-day views (shares).")


def render() -> None:
    st.title("Admin")
    if not st.session_state.get("is_admin"):
        st.error("Admins only.")
        return
    eng = account.engine()
    subs = store.list_subscriptions(eng)
    counts = store.answer_counts(eng)
    now = time.time()
    paying = [s for s in subs if s.grants_access(now)]
    monthly = [s for s in paying if not s.is_pass]
    pass_prices = {"+".join(v[2]): v[1] for v in PASSES.values()}
    pass_revenue = sum(pass_prices.get(s.subject, 0) for s in subs if s.is_pass and s.status == "paid")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Users with saved progress", len(counts))
    c2.metric("Paying now", len({s.email for s in paying}))
    c3.metric("Monthly plans (₹/month)", f"₹{len(monthly) * SUBJECT_PRICE_INR:,}")
    c4.metric("Exam passes sold (₹)", f"₹{pass_revenue:,}")

    _funnel(eng, subs)

    st.subheader("Subscriptions and passes", anchor=False)
    if subs:
        st.dataframe(pd.DataFrame([{
            "Email": s.email, "Plan": "Exam pass" if s.is_pass else "Monthly", "Subjects": _names(s),
            "Status": s.status, "Has access": s.grants_access(now),
            "Paid until": datetime.fromtimestamp(s.current_end).strftime("%d %b %Y") if s.current_end else "",
            "Razorpay id": s.razorpay_id, "Started": s.created_at[:10],
        } for s in reversed(subs)]), hide_index=True, width="stretch")
    else:
        st.caption("No subscriptions yet.")

    st.subheader("Practice by user", anchor=False)
    if counts:
        st.dataframe(pd.DataFrame(sorted(counts.items(), key=lambda kv: -kv[1]), columns=["Email", "Answers logged"]),
                     hide_index=True, width="stretch")
    else:
        st.caption("No answers saved yet.")
    st.caption("Statuses come from Razorpay and refresh when each user opens the app. "
               "Refunds and full payment history are in the Razorpay dashboard.")
