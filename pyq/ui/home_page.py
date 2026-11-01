"""Home: the dashboard a signed-in student lands on — continue, today's question,
weak topics, subject tiles and the practice sets."""

from collections import defaultdict

import streamlit as st

from ..filters import ALL
from ..model import PRACTICE
from ..syllabus import SUBJECTS
from . import state


def _open_subject(subject: str, session: str = ALL) -> None:
    ss = st.session_state
    ss.f_subject, ss.f_session, ss.f_unit, ss.f_topic, ss.f_qtype = subject, session, ALL, ALL, ALL
    ss.run = None
    state.go("practice")


def _weak_topics(log, limit: int = 3) -> list[tuple[str, str, str, int, int]]:
    """(subject, unit, topic, correct, attempts) for the weakest topics with at least two answers."""
    tally = defaultdict(lambda: [0, 0])
    for a in log:
        t = tally[(a.subject, a.macro_unit, a.micro_topic)]
        t[0] += a.is_correct
        t[1] += 1
    rows = [(s, u, m, c, n) for (s, u, m), (c, n) in tally.items() if n >= 2 and c / n < 0.7]
    return sorted(rows, key=lambda r: (r[3] / r[4], -r[4]))[:limit]


def _greeting() -> str:
    name = (st.session_state.get("user") or "").split("@")[0].split(".")[0]
    return f"Welcome back{', ' + name.title() if name and name.lower() != 'dev' else ''}"


def _continue_card(bank) -> None:
    run = st.session_state.run
    with st.container(key="home-card-continue"):
        if run and run.deck and not run.finished and (run.answers or run.position):
            score = run.score(bank.by_id)
            st.markdown("#### :material/play_circle: Continue where you left off")
            st.markdown(f"Attempt #{run.number} · question **{run.position + 1} of {len(run.deck)}** · "
                        f"{score.correct} / {score.answered} correct  \n{run.filters.describe()}")
            st.button("Continue practising", icon=":material/arrow_forward:", key="home-continue",
                      on_click=state.go, args=("practice",))
        else:
            st.markdown("#### :material/rocket_launch: Start practising")
            st.markdown("Pick a subject below, or jump straight into every question you can open.")
            st.button("Start now", icon=":material/arrow_forward:", key="home-start", on_click=_open_subject, args=(ALL,))


def _side_cards(bank) -> None:
    n_mistakes = len(state.mistakes(bank))
    with st.container(key="home-card-daily"):
        st.markdown("#### :material/today: Question of the day")
        st.caption("One real PYQ every day, with a share button for your study group.")
        st.button("Open today's question", icon=":material/today:", key="home-daily", on_click=state.go, args=("daily",))
    with st.container(key="home-card-review"):
        st.markdown("#### :material/replay: Review mistakes")
        st.caption(f"{n_mistakes} question(s) you got wrong are waiting." if n_mistakes else
                   "Nothing to review yet — wrong answers collect here.")
        st.button("Review now", icon=":material/replay:", key="home-review", disabled=not n_mistakes,
                  on_click=state.go, args=("review",))


def _subject_tiles(bank) -> None:
    ss = st.session_state
    full = state.get_full_bank()
    st.subheader("Your subjects", anchor=False)
    cols = st.columns(len(SUBJECTS))
    for col, (sid, info) in zip(cols, SUBJECTS.items()):
        total = sum(q.subject == sid for q in full.questions)
        visible = sum(q.subject == sid for q in bank.questions)
        is_open = ss.get("is_admin") or sid in ss.get("unlocked", set())
        with col, st.container(key=f"home-subject-{sid}-{'open' if is_open else 'locked'}"):
            st.markdown(f"#### {info.short}")
            st.caption(info.display)
            if is_open:
                st.markdown(f":green-badge[:material/lock_open: unlocked] **{visible}** questions")
            else:
                st.markdown(f":gray-badge[:material/lock: locked] **{visible}** free of {total}")
            st.button("Practise", icon=":material/quiz:", key=f"home-go-{sid}", disabled=not visible,
                      on_click=_open_subject, args=(sid,), width="stretch")
            if not is_open and total > visible:
                st.button("Unlock", icon=":material/workspace_premium:", key=f"home-unlock-{sid}", type="tertiary",
                          on_click=state.go, args=("plans",))


def _practice_sets(bank) -> None:
    by_subject = defaultdict(int)
    for q in bank.questions:
        if q.session_key == PRACTICE:
            by_subject[q.subject] += 1
    with st.container(key="home-card-sets"):
        st.markdown("#### :material/library_books: Practice sets")
        if not by_subject:
            st.caption("Practice sets in NTA's pattern come with each subject's subscription.")
            st.button("See plans", icon=":material/workspace_premium:", key="home-sets-plans", on_click=state.go, args=("plans",))
            return
        st.caption("Fresh questions written in NTA's exact pattern, by topic.")
        with st.container(horizontal=True):
            for sid, n in by_subject.items():
                st.button(f"{SUBJECTS[sid].short}: {n} questions", icon=":material/quiz:", key=f"home-sets-{sid}",
                          on_click=_open_subject, args=(sid, PRACTICE))


def _weak_card() -> None:
    weak = _weak_topics(state.log())
    with st.container(key="home-card-weak"):
        st.markdown("#### :material/target: Topics to work on")
        if not weak:
            st.caption("Answer a few questions and your weakest topics will show up here.")
            return
        for sid, unit, topic, c, n in weak:
            with st.container(horizontal=True, vertical_alignment="center"):
                st.markdown(f"**{topic}**  \n:gray[{SUBJECTS[sid].short} · {c}/{n} correct]")
                st.button("Drill", icon=":material/target:", key=f"home-weak-{sid}-{topic}",
                          on_click=state.practise_topic, args=(sid, unit, topic))


def render() -> None:
    bank = state.get_bank()
    st.title(_greeting(), anchor=False)
    log = state.log()
    correct = sum(a.is_correct for a in log)
    st.caption(f"{len(log)} answers so far · accuracy {correct / len(log):.0%}" if log else
               "Your progress is saved to your account as you practise.")
    left, right = st.columns([3, 2])
    with left:
        _continue_card(bank)
        _weak_card()
    with right:
        _side_cards(bank)
    _subject_tiles(bank)
    _practice_sets(bank)
