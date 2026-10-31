"""Subscription: one monthly plan per subject, paid on Razorpay's own page."""

import time
from datetime import datetime

import streamlit as st

from ..access import sellable_questions, sellable_subjects
from ..config import SUBJECT_PRICE_INR
from ..syllabus import SUBJECTS
from . import account, state


def _date(ts: int | None) -> str:
    return datetime.fromtimestamp(ts).strftime("%d %b %Y") if ts else "—"


def _papers(questions) -> int:
    return len({q.session_label for q in questions})


def _subject_card(subject: str, full_bank, sellable: list[str]) -> None:
    ss = st.session_state
    info = SUBJECTS[subject]
    questions = sellable_questions(full_bank, subject)
    subs = [s for s in account.subscriptions() if s.subject == subject]
    active = next((s for s in reversed(subs) if s.grants_access(time.time())), None)
    pending = next((s for s in reversed(subs) if s.awaiting_payment and s.short_url), None)

    with st.container(border=True):
        st.subheader(info.display, anchor=False)
        if subject not in sellable:
            st.badge("Coming soon", icon=":material/schedule:", color="gray")
            st.caption("Real papers for this subject are being added. You'll be able to subscribe once they're in.")
            return
        st.markdown(f"**₹{SUBJECT_PRICE_INR} / month** · {len(questions)} questions from {_papers(questions)} "
                    "exam papers, each with a detailed explanation")
        if ss.is_admin:
            st.badge("Full access (admin)", icon=":material/shield_person:", color="blue")
        elif active:
            if active.renews:
                st.success(f"Unlocked. Renews automatically; current period ends {_date(active.current_end)}.",
                           icon=":material/check_circle:")
                with st.popover("Cancel renewal", icon=":material/cancel:"):
                    st.write("Stop future payments? You keep access until the end of the period you paid for.")
                    st.button("Yes, cancel renewal", key=f"cancel-{subject}", type="primary",
                              on_click=account.cancel_subscription, args=(active.razorpay_id,))
            else:
                st.info(f"Unlocked until {_date(active.current_end)}. It won't renew.", icon=":material/event:")
        elif pending:
            st.warning("Payment not completed yet.", icon=":material/hourglass_top:")
            with st.container(horizontal=True):
                st.link_button(f"Pay ₹{SUBJECT_PRICE_INR} on Razorpay", pending.short_url, type="primary",
                               icon=":material/payments:")
                st.button("I've paid: check now", key=f"check-{subject}", icon=":material/sync:",
                          on_click=account.check_payments)
            st.caption("After paying, come back to this tab and press **I've paid: check now**.")
        else:
            st.button(f"Subscribe for ₹{SUBJECT_PRICE_INR}/month", key=f"sub-{subject}", type="primary",
                      icon=":material/lock_open:", on_click=account.start_subscription, args=(subject,))


def render() -> None:
    st.title("Subscription")
    full = state.get_full_bank()
    sellable = sellable_subjects(full)
    if account.razorpay() is None and not st.session_state.is_admin:
        st.info("Payments aren't open yet. Please check back soon.", icon=":material/construction:")
    st.markdown("Each subject is a separate monthly plan. Pay by UPI, card or net banking on Razorpay's secure page; "
                "it renews every month until you cancel. The free sample questions stay available to everyone.")
    for subject in SUBJECTS:
        _subject_card(subject, full, sellable)
    st.button("Refresh payment status", icon=":material/sync:", on_click=account.check_payments, type="tertiary")
