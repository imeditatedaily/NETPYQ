"""Mock Test: sit a full paper against the clock in NTA's computer-based-test
layout (question palette, Save & Next, Mark for Review), then see the score."""

import time
from datetime import datetime

import pandas as pd
import streamlit as st

from .. import mock
from ..access import free_paper_label
from ..mock import MockTest, paper_choices
from ..syllabus import SUBJECTS
from ..tracker import make_answer
from . import question_view, state

PALETTE_CSS = """
<style>
[class*="st-key-pal-"], [class*="st-key-pal-"] .stButton { width: 100%; }
[class*="st-key-pal-"] button { width: 100%; min-width: 0; min-height: 2.4rem; padding: 0; font-weight: 700; border-radius: .55rem; }
[class*="st-key-pal-not_visited-"] button { background: #fff; color: #161b15; border: 1px solid #cfc6b0; }
[class*="st-key-pal-not_answered-"] button { background: #c9673a; color: #fff; border: 0; border-radius: .55rem .55rem 1.1rem 1.1rem; }
[class*="st-key-pal-answered-"] button { background: #2f6b4f; color: #fff; border: 0; border-radius: 1.1rem 1.1rem .55rem .55rem; }
[class*="st-key-pal-marked-"] button { background: #6b4fa0; color: #fff; border: 0; border-radius: 50%; }
[class*="st-key-pal-answered_marked-"] button { background: #6b4fa0; color: #fff; border: 0; border-radius: 50%;
  box-shadow: inset 0 0 0 3px #d8f45a; }
[class*="st-key-pal-"][class*="-current"] button { outline: 3px solid #161b15; outline-offset: 2px; }
.mock-timer { background: #1d4433; color: #fff; border-radius: .8rem; padding: .6rem 1rem; font-weight: 700;
  font-size: 1.05rem; text-align: center; font-variant-numeric: tabular-nums; }
.mock-timer.low { background: #a4532c; }
</style>
"""

SWATCH = {mock.NOT_VISITED: "⬜", mock.NOT_ANSWERED: "🟧", mock.ANSWERED: "🟩", mock.MARKED: "🟪",
          mock.ANSWERED_MARKED: "🟪✓"}


def _test() -> MockTest | None:
    return st.session_state.get("mock")


def _choice_key(test: MockTest, qid: str) -> str:
    return f"mock-{test.number}-{qid}"


# --- callbacks ---------------------------------------------------------------------------

def _start(subject: str, choices: dict) -> None:
    ss = st.session_state
    choice = choices[ss.mock_paper]
    done = [a.run for a in state.log() if a.mode == "mock"]
    ss.mocks_started = max([ss.get("mocks_started", 0), *done]) + 1
    ss.mock = MockTest.start(ss.mocks_started, choice, subject, time.time())


def _save(mark: bool) -> None:
    test = _test()
    test.save(st.session_state.get(_choice_key(test, test.current_id)), mark)


def _clear() -> None:
    test = _test()
    test.clear()
    st.session_state[_choice_key(test, test.current_id)] = None


def _go(position: int) -> None:
    _test().go(position)


def _submit() -> None:
    test = _test()
    if test.submitted:
        return
    test.submit(time.time())
    bank = state.get_bank()
    from . import account
    when = datetime.now()
    for qid, chosen in test.answers.items():
        answer = make_answer(bank[qid], chosen, "mock", test.number, when)
        st.session_state.log.append(answer)
        account.save_answer(answer)


def _close() -> None:
    st.session_state.mock = None


# --- screens -----------------------------------------------------------------------------

def _setup() -> None:
    bank = state.get_bank()
    st.title("Mock Test", anchor=False)
    st.caption("Sit a real paper against the clock, exactly as in the NTA computer-based test.")
    subjects = [s for s in SUBJECTS if any(q.subject == s and q.is_dated for q in bank.questions)]
    if not subjects:
        st.info("Mock tests use real papers. Subscribe to a subject to unlock its papers.", icon=":material/lock:")
        return
    left, right = st.columns([3, 2], gap="large")
    with left:
        ss = st.session_state
        if ss.get("mock_subject") not in subjects:
            ss.mock_subject = subjects[0]
        subject = st.segmented_control("Subject", subjects, key="mock_subject", required=True,
                                       format_func=lambda s: SUBJECTS[s].display)
        choices = {c.key: c for c in paper_choices(bank.questions, subject, seed=ss.get("mocks_started", 0))}
        if ss.get("mock_paper") not in choices:
            ss.mock_paper = next(iter(choices))
        st.radio("Paper", list(choices), key="mock_paper", format_func=lambda k: choices[k].label)
        picked = choices[ss.mock_paper]
        st.markdown(f"**{len(picked.question_ids)} questions · {picked.minutes} minutes · "
                    f"{len(picked.question_ids) * mock.MARKS_PER_QUESTION} marks**")
        st.button("Start the test", type="primary", icon=":material/timer:", on_click=_start, args=(subject, choices))
    with right.container(border=True):
        st.markdown("**Instructions (NTA pattern)**")
        st.markdown(
            f"- Each question carries **{mock.MARKS_PER_QUESTION} marks**. There is **no negative marking**.\n"
            f"- Time: {mock.SECONDS_PER_QUESTION} seconds a question, as in the real exam (3 hours for 150 questions). "
            "The test submits itself when the timer reaches zero.\n"
            "- An answer counts only after **Save & Next**. **Mark for Review & Next** keeps a question to revisit; "
            "a saved answer that is marked for review is still evaluated.\n"
            "- Jump to any question from the palette. Your score, every explanation and a unit-wise breakdown appear "
            "when you submit, and wrong answers join **Review Mistakes**.")
        st.markdown("  \n".join(f"{SWATCH[s]} {label}" for s, label in mock.STATUS_LABELS.items()))
    if not st.session_state.get("unlocked") and not st.session_state.get("is_admin"):
        st.caption(f"On the free plan you can sit the free papers ({free_paper_label()}). Subscribe to sit every paper.")
    _history()


@st.fragment(run_every=1)
def _timer() -> None:
    test = _test()
    if test is None or test.submitted:
        return
    left = test.remaining(time.time())
    if left <= 0:
        _submit()
        st.rerun(scope="app")
    h, rem = divmod(int(left), 3600)
    m, s = divmod(rem, 60)
    low = " low" if left < 300 else ""
    st.html(f'<div class="mock-timer{low}">⏱ Time left {h}:{m:02d}:{s:02d}</div>')


def _palette(test: MockTest) -> None:
    counts = test.counts()
    st.markdown("**Question palette**")
    per_row = 5
    for start in range(0, len(test.question_ids), per_row):
        cols = st.columns(per_row, gap="small")
        for col, i in zip(cols, range(start, min(start + per_row, len(test.question_ids)))):
            qid = test.question_ids[i]
            current = "-current" if i == test.position else ""
            col.button(str(i + 1), key=f"pal-{test.status(qid)}-{i}{current}", on_click=_go, args=(i,))
    st.caption("  \n".join(f"{SWATCH[s]} {label}: **{counts[s]}**" for s, label in mock.STATUS_LABELS.items()))


def _in_progress(test: MockTest) -> None:
    bank = state.get_bank()
    head, timer = st.columns([3, 1], vertical_alignment="center")
    head.subheader(f"{SUBJECTS[test.subject].display} · {test.title}", anchor=False)
    with timer:
        _timer()

    main, side = st.columns([3, 1.25], gap="large")
    with main:
        q = bank[test.current_id]
        with st.container(border=True):
            st.caption(f"Question {test.position + 1} of {len(test.question_ids)} · "
                       f"{mock.MARKS_PER_QUESTION} marks · no negative marking")
            q = question_view.localize(q)
            question_view.question_body(q)
            key = _choice_key(test, q.id)
            if key not in st.session_state:
                st.session_state[key] = test.answers.get(q.id)
            st.radio("Choose one answer", options=list(range(1, len(q.options) + 1)), key=key,
                     format_func=lambda n: f"({n}) {question_view.md(q.options[n - 1])}")
        with st.container(horizontal=True):
            st.button("Save & Next", type="primary", icon=":material/save:", on_click=_save, args=(False,))
            st.button("Mark for Review & Next", icon=":material/bookmark:", on_click=_save, args=(True,))
            st.button("Clear Response", icon=":material/backspace:", on_click=_clear)
            st.button("Previous", icon=":material/arrow_back:", on_click=_go, args=(test.position - 1,),
                      disabled=test.position == 0)
    with side:
        _palette(test)
        with st.popover("Submit test", icon=":material/assignment_turned_in:", type="primary", width="stretch"):
            c = test.counts()
            st.markdown(f"Answered: **{c[mock.ANSWERED] + c[mock.ANSWERED_MARKED]}** · "
                        f"Not answered: **{len(test.question_ids) - len(test.answers)}** · "
                        f"Marked for review: **{c[mock.MARKED] + c[mock.ANSWERED_MARKED]}**")
            st.write("Submit now? You can't change answers afterwards.")
            st.button("Yes, submit", type="primary", on_click=_submit)


def _result(test: MockTest) -> None:
    bank, library = state.get_bank(), state.get_library()
    r = mock.score(test, bank.by_id)
    st.title("Mock test result", anchor=False)
    st.caption(f"{SUBJECTS[test.subject].display} · {test.title}")
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Score", f"{r.marks} / {r.max_marks}")
    c2.metric("Correct", r.correct)
    c3.metric("Wrong", r.wrong)
    c4.metric("Not attempted", r.unattempted)
    mins, secs = divmod(int(test.time_taken(time.time())), 60)
    c5.metric("Time taken", f"{mins}m {secs:02d}s")
    if r.accuracy is not None:
        st.progress(r.marks / r.max_marks, text=f"{r.marks / r.max_marks:.0%} of the marks · "
                                                f"{r.accuracy:.0%} accuracy on the questions you attempted")
    with st.container(horizontal=True):
        st.button("Take another test", type="primary", icon=":material/timer:", on_click=_close)
        st.button("Review mistakes", icon=":material/replay:", on_click=state.go, args=("review",))
        st.button("Performance analytics", icon=":material/monitoring:", on_click=state.go, args=("analytics",))

    rows = []
    for qid in test.question_ids:
        q, chosen = bank[qid], test.answers.get(qid)
        rows.append({"Unit": q.macro_unit, "no": q.unit_no, "correct": chosen is not None and q.is_correct(chosen),
                     "wrong": chosen is not None and not q.is_correct(chosen), "skipped": chosen is None})
    df = pd.DataFrame(rows).sort_values("no").groupby("Unit", sort=False).agg(
        Questions=("correct", "size"), Correct=("correct", "sum"), Wrong=("wrong", "sum"), Skipped=("skipped", "sum"))
    df["Marks"] = df["Correct"] * mock.MARKS_PER_QUESTION
    df["Score"] = df["Correct"] / df["Questions"]
    st.subheader("Unit-wise", anchor=False)
    st.dataframe(df.reset_index(), hide_index=True, column_config={
        "Score": st.column_config.ProgressColumn("Score", format="percent", min_value=0, max_value=1)})

    st.subheader("Question by question", anchor=False)
    show = st.segmented_control("Show", ["Wrong", "Not attempted", "Correct", "All"], default="Wrong", key="mock_show")
    for i, qid in enumerate(test.question_ids, start=1):
        q, chosen = bank[qid], test.answers.get(qid)
        verdict = "Not attempted" if chosen is None else ("Correct" if q.is_correct(chosen) else "Wrong")
        if show not in ("All", verdict):
            continue
        icon = {"Correct": ":material/check_circle:", "Wrong": ":material/cancel:", "Not attempted": ":material/remove:"}[verdict]
        with st.expander(f"Q{i} · {verdict} · {q.micro_topic}", icon=icon):
            q = question_view.localize(q, note=False)
            question_view.question_body(q)
            if chosen is None:
                st.markdown(f":green[**Answer: ({q.correct_answer}) {question_view.md(q.correct_text)}**]")
            else:
                question_view._options_review(q, chosen)
            st.markdown(q.detailed_explanation)


def _history() -> None:
    log = [a for a in state.log() if a.mode == "mock"]
    if not log:
        return
    df = pd.DataFrame([a.to_dict() for a in log])
    hist = df.groupby("run").agg(Date=("at", "first"), Subject=("subject", "first"), Attempted=("is_correct", "size"),
                                 Correct=("is_correct", "sum")).reset_index()
    hist["Marks"] = hist["Correct"] * mock.MARKS_PER_QUESTION
    hist["Date"] = hist["Date"].str[:16].str.replace("T", " ")
    hist["Subject"] = hist["Subject"].map(lambda s: SUBJECTS[s].short if s in SUBJECTS else s)
    st.subheader("Your past mock tests", anchor=False)
    st.dataframe(hist.rename(columns={"run": "Test"}).sort_values("Test", ascending=False), hide_index=True)


def render() -> None:
    st.html(PALETTE_CSS)
    test = _test()
    if test is None:
        _setup()
    elif test.submitted:
        _result(test)
    else:
        if test.expired(time.time()):
            _submit()
            st.rerun()
        _in_progress(test)
