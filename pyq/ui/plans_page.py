"""Subscription: one-time exam passes (pay once, six months) and monthly plans,
both paid on Razorpay's own pages."""

import time
from datetime import datetime

import streamlit as st

from ..access import free_paper_label, sellable_questions, sellable_subjects
from ..config import PASS_DAYS, PASSES, SUBJECT_PRICE_INR
from ..syllabus import SUBJECTS
from . import account, state


def _date(ts: int | None) -> str:
    return datetime.fromtimestamp(ts).strftime("%d %b %Y") if ts else "—"


def _papers(questions) -> int:
    return len({q.session_label for q in questions})


def _pending(subs, match) -> None:
    """A started-but-unpaid payment: the link to pay and a button to check."""
    pending = next((s for s in reversed(subs) if match(s) and s.awaiting_payment and s.short_url), None)
    if not pending:
        return False
    st.warning("Payment not completed yet.", icon=":material/hourglass_top:")
    with st.container(horizontal=True):
        st.link_button("Pay on Razorpay", pending.short_url, type="primary", icon=":material/payments:")
        st.button("I've paid: check now", key=f"check-{pending.razorpay_id}", icon=":material/sync:",
                  on_click=account.check_payments)
    st.caption("After paying, come back to this tab and press **I've paid: check now**.")
    return True


def _active_passes(subs, now) -> None:
    passes = [s for s in subs if s.is_pass and s.grants_access(now)]
    for p in passes:
        names = " + ".join(SUBJECTS[x].short for x in p.subjects if x in SUBJECTS)
        st.success(f"**Exam pass active: {names}.** Full access until {_date(p.current_end)}. It doesn't renew.",
                   icon=":material/verified:")


def _pass_card(key: str, sellable: list[str], subs, now, highlight: bool) -> None:
    name, price, subjects = PASSES[key]
    if not all(s in sellable for s in subjects):
        return
    months = PASS_DAYS // 30
    with st.container(border=True, key=f"pass-card-{key}{'-hot' if highlight else ''}"):
        if highlight:
            st.badge("Best value", icon=":material/star:", color="green")
        st.subheader(name, anchor=False)
        st.markdown(f"### ₹{price:,}  \n:gray[one payment · {months} months of full access]")
        monthly = SUBJECT_PRICE_INR * len(subjects) * months
        st.caption(f"Monthly plans for the same {months} months would cost ₹{monthly:,}. Doesn't renew.")
        owned = any(s.is_pass and s.subject == "+".join(subjects) and s.grants_access(now) for s in subs)
        if st.session_state.is_admin:
            st.badge("Full access (admin)", icon=":material/shield_person:", color="blue")
        elif owned:
            st.badge("You have this pass", icon=":material/check_circle:", color="green")
        elif not _pending(subs, lambda s: s.is_pass and s.subject == "+".join(subjects)):
            st.button(f"Pay ₹{price:,} once", key=f"pass-{key}", type="primary", icon=":material/bolt:",
                      on_click=account.start_pass, args=(key,), width="stretch")


def _subject_card(subject: str, full_bank, sellable: list[str], subs, now) -> None:
    info = SUBJECTS[subject]
    questions = sellable_questions(full_bank, subject)
    mine = [s for s in subs if s.subject == subject and not s.is_pass]
    active = next((s for s in reversed(mine) if s.grants_access(now)), None)

    with st.container(border=True):
        st.subheader(info.display, anchor=False)
        if subject not in sellable:
            st.badge("Coming soon", icon=":material/schedule:", color="gray")
            st.caption("Real papers for this subject are being added. You'll be able to subscribe once they're in.")
            return
        n = _papers(questions)
        st.markdown(f"**₹{SUBJECT_PRICE_INR} / month** · {len(questions)} questions from {n} "
                    f"exam paper{'s' if n != 1 else ''}, each with a detailed explanation. More papers being added.")
        if st.session_state.is_admin:
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
        elif subject in st.session_state.unlocked:
            st.caption("Already unlocked by your exam pass.")
        elif not _pending(subs, lambda s: not s.is_pass and s.subject == subject):
            st.button(f"Subscribe for ₹{SUBJECT_PRICE_INR}/month", key=f"sub-{subject}",
                      icon=":material/autorenew:", on_click=account.start_subscription, args=(subject,))


def render() -> None:
    account.track("plans", once=True)
    st.title("Subscription")
    full = state.get_full_bank()
    sellable = sellable_subjects(full)
    subs, now = account.subscriptions(), time.time()
    if account.razorpay() is None and not st.session_state.is_admin:
        st.info("Payments aren't open yet. Please check back soon.", icon=":material/construction:")
    st.markdown("Pay by UPI, card or net banking on Razorpay's secure page. "
                f"The free real papers ({free_paper_label()}) stay available to everyone.")
    st.warning("**No refunds.** Payments are final once made, including partly used months. Cancelling a monthly "
               "plan stops the next payment only. Please try the free paper before you pay.", icon=":material/info:")
    _active_passes(subs, now)

    st.header("Exam pass: pay once", anchor=False)
    st.caption(f"Full access for {PASS_DAYS // 30} months from the day you pay, about one NET cycle. No renewals, "
               "nothing to cancel.")
    keys = [k for k in PASSES if all(s in sellable for s in PASSES[k][2])]
    keys.sort(key=lambda k: -len(PASSES[k][2]))        # the combo first
    cols = st.columns(max(1, len(keys)))
    for col, key in zip(cols, keys):
        with col:
            _pass_card(key, sellable, subs, now, highlight=len(PASSES[key][2]) > 1)

    st.header("Or pay monthly", anchor=False)
    for subject in SUBJECTS:
        _subject_card(subject, full, sellable, subs, now)
    st.button("Refresh payment status", icon=":material/sync:", on_click=account.check_payments, type="tertiary")
