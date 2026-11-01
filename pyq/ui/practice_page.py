"""Practice: work through the filtered questions, as many times as you like."""

import streamlit as st

from . import question_view, state, style


def _score_row(run, score) -> None:
    """A compact strip of chips: attempt, score, accuracy, position, wrong and skipped."""
    wrong = score.answered - score.correct
    skipped = max(0, min(run.position, len(run.deck)) - score.answered)
    with st.container(key="practice-strip", horizontal=True, gap="small"):
        st.metric("Attempt", f"#{run.number}")
        st.metric("Score", f"{score.correct} / {score.answered}", help="Correct answers out of those answered in this attempt.")
        st.metric("Accuracy", f"{score.accuracy:.0%}" if score.accuracy is not None else "—")
        st.metric("Question", f"{min(run.position + 1, len(run.deck))} of {len(run.deck)}")
        st.metric("Wrong", str(wrong))
        st.metric("Skipped", str(skipped))


def _finished(run, score, bank) -> None:
    with st.container(border=True):
        st.subheader(f"Attempt #{run.number} complete", anchor=False)
        acc = f"{score.accuracy:.0%}" if score.accuracy is not None else "no answers"
        st.markdown(f"You answered **{score.answered}** of {score.total} questions and got "
                    f"**{score.correct}** right ({acc}).")
        n_mistakes = len(state.mistakes(bank))
        with st.container(horizontal=True):
            st.button("Take this quiz again", type="primary", icon=":material/restart_alt:",
                      on_click=state.restart_same_quiz, args=(bank,))
            st.button(f"Review mistakes ({n_mistakes})", icon=":material/replay:", disabled=not n_mistakes,
                      on_click=state.go, args=("review",))
            st.button("Performance analytics", icon=":material/monitoring:", on_click=state.go, args=("analytics",))


def render() -> None:
    bank, library = state.get_bank(), state.get_library()
    run = state.ensure_run(bank)
    filters = state.current_filters()

    with st.container(horizontal=True, vertical_alignment="center"):
        st.title("Practice", anchor=False)
        st.toggle("Focus mode", key="focus", help="Hides the sidebar and widens the question card. Turn off to change filters.")
    if st.session_state.get("focus"):
        style.focus_mode()
    st.caption(filters.describe())

    if run.filters != filters:
        with st.container(border=True, horizontal=True, vertical_alignment="center"):
            st.markdown(":material/filter_alt: The filters have changed since this attempt started.")
            st.button("Start a new attempt with these filters", on_click=state.start_run, args=(bank,))

    if not run.deck:
        st.warning("No questions match these filters. Widen them in the sidebar.", icon=":material/search_off:")
        return

    score = run.score(bank.by_id)
    _score_row(run, score)
    st.progress(run.position / len(run.deck))

    if run.finished:
        _finished(run, score, bank)
        return

    q = bank[run.current_id]
    chosen = run.answers.get(q.id)
    with st.container(border=True):
        question_view.syllabus_tags(q)
        question_view.question_body(q)
        if chosen is None:
            question_view.answer_form(q, f"p{run.number}-{q.id}", state.submit_practice, bank)
        else:
            note = "" if q.is_correct(chosen) else "Added to Review Mistakes."
            question_view.feedback(q, chosen, bank, library, "practice", note)

    n_mistakes = len(state.mistakes(bank))
    with st.container(horizontal=True, key="practice-nav"):
        if chosen is not None:
            last = run.position == len(run.deck) - 1
            st.button("See my score" if last else "Next question", type="primary",
                      icon=":material/flag:" if last else ":material/arrow_forward:", on_click=state.advance_practice)
        else:
            st.button("Skip", icon=":material/skip_next:", on_click=state.advance_practice,
                      help="Move on without answering. Skipped questions are not scored.")
        st.button(f"Review mistakes ({n_mistakes})", icon=":material/replay:", disabled=not n_mistakes,
                  on_click=state.go, args=("review",))
        st.button("Restart this quiz", icon=":material/restart_alt:", on_click=state.restart_same_quiz, args=(bank,))
