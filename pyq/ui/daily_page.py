"""Question of the day: public, no sign-in, with WhatsApp and Telegram share buttons."""

from datetime import datetime, timedelta, timezone

import streamlit as st

from .. import daily
from ..access import free_paper_label, sellable_questions, sellable_subjects
from ..syllabus import SUBJECTS
from . import question_view, state

IST = timezone(timedelta(hours=5, minutes=30))
DEFAULT_APP_URL = "https://netpyq.onrender.com"

CSS = """
<style>
.st-key-daily-share a { border-radius: 999px !important; font-weight: 600; }
.st-key-daily-wa a { background: #25d366 !important; color: #fff !important; border: 0 !important; }
.st-key-daily-tg a { background: #229ed9 !important; color: #fff !important; border: 0 !important; }
.st-key-daily-cta { background: #1d4433; border-radius: 1rem; padding: 1.2rem 1.4rem; }
.st-key-daily-cta p, .st-key-daily-cta h3 { color: #fff !important; }
.st-key-daily-cta button { background: #d8f45a !important; color: #161b15 !important; border: 0 !important;
  border-radius: 999px !important; font-weight: 600; }
.st-key-daily-cta button p, .st-key-daily-cta button span { color: #161b15 !important; }
</style>
"""


def _app_url() -> str:
    try:
        url = st.secrets.get("app_url", "") or DEFAULT_APP_URL
    except Exception:
        url = DEFAULT_APP_URL
    # app_url may point at the Subscription page (the payment return address); share the site root.
    return url.split("/plans")[0].rstrip("/")


def _pool() -> list:
    full = state.get_full_bank()
    return [q for s in sellable_subjects(full) for q in sellable_questions(full, s)]


def render() -> None:
    from . import account
    account.track("daily", once=True)
    st.html(CSS)
    today = datetime.now(IST).date()
    day = daily.valid_day(st.query_params.get("d"), today)
    pool = _pool()
    st.title("Question of the day", anchor=False)
    if not pool:
        st.info("Real papers are being added. The question of the day starts as soon as the first one is in.")
        return
    q = daily.pick(pool, day)
    subject = SUBJECTS[q.subject]
    st.caption(f"{day:%A, %d %B %Y} · UGC NET {subject.display} · from the {q.session_label} paper. "
               "A new real question every day.")

    if not st.session_state.get("user"):     # signed in, the toggle is in the sidebar
        question_view.language_toggle()
    with st.container(border=True):
        q = question_view.localize(q)
        question_view.question_body(q)
        key = f"daily-{day.isoformat()}"
        checked = st.session_state.get(f"{key}-checked")
        st.radio("Your answer", list(range(1, len(q.options) + 1)), index=None, key=key, disabled=bool(checked),
                 format_func=lambda n: f"({n}) {question_view.md(q.options[n - 1])}")
        if not checked:
            if st.button("Check my answer", type="primary", icon=":material/done:"):
                if st.session_state.get(key) is None:
                    st.warning("Pick an option first.")
                else:
                    st.session_state[f"{key}-checked"] = True
                    st.rerun()
        else:
            chosen = st.session_state.get(key)
            if q.is_correct(chosen):
                st.success(f"**Correct!** ({q.correct_answer}) {question_view.md(q.correct_text)}",
                           icon=":material/check_circle:")
            else:
                st.error(f"**Not quite.** The answer is ({q.correct_answer}) {question_view.md(q.correct_text)}",
                         icon=":material/cancel:")
            st.markdown("##### Explanation")
            st.markdown(question_view.public_explanation(q))

    url = f"{_app_url()}/daily?d={day.isoformat()}"
    text = daily.share_text(q, subject.short, url)
    st.markdown("**Challenge your friends.** Send today's question to your NET group:")
    with st.container(horizontal=True, key="daily-share"):
        with st.container(key="daily-wa", width="content"):
            st.link_button("Share on WhatsApp", daily.whatsapp_url(text), icon=":material/chat:")
        with st.container(key="daily-tg", width="content"):
            st.link_button("Share on Telegram", daily.telegram_url(url, text.rsplit("\n\n", 1)[0]),
                           icon=":material/send:")
    st.code(url, language=None)

    with st.container(key="daily-cta"):
        if st.session_state.get("user"):
            st.markdown("### Keep going\nPractise more questions on this topic, or sit a timed mock test.")
            st.button("Practise this topic", icon=":material/target:", on_click=state.practise_topic,
                      args=(q.subject, q.macro_unit, q.micro_topic))
        else:
            st.markdown(f"### Want the full paper?\nSign in free and sit two complete real papers ({free_paper_label()}) "
                        "with every explanation, a timed mock test and PYQ trends.")
            st.button("Start free with Google", icon=":material/login:", on_click=st.login, args=("google",))
    yesterday = day - timedelta(days=1)
    if (today - yesterday).days <= daily.OLDEST_DAYS:
        st.markdown(f"[← Yesterday's question](daily?d={yesterday.isoformat()})")
