"""Admin: who has subscribed, and how much each user has practised."""

import time
from datetime import datetime

import pandas as pd
import streamlit as st

from .. import store
from ..config import SUBJECT_PRICE_INR
from ..syllabus import SUBJECTS
from . import account


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

    c1, c2, c3 = st.columns(3)
    c1.metric("Users with saved progress", len(counts))
    c2.metric("Paid subject plans now", len(paying))
    c3.metric("Monthly revenue (approx.)", f"₹{len(paying) * SUBJECT_PRICE_INR:,}")

    st.subheader("Subscriptions", anchor=False)
    if subs:
        st.dataframe(pd.DataFrame([{
            "Email": s.email, "Subject": SUBJECTS[s.subject].short if s.subject in SUBJECTS else s.subject,
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
