"""Review Mistakes: loop over the questions you got wrong until one round is 100%."""

from collections import Counter

import pandas as pd
import streamlit as st

from . import question_view, state


def _home(bank) -> None:
    ids = state.mistakes(bank)
    if not ids:
        st.success("No outstanding mistakes. Every question you have answered wrong this session has since been "
                   "answered correctly.", icon=":material/task_alt:")
        st.button("Go to Practice", icon=":material/quiz:", on_click=state.go, args=("practice",))
        return

    st.markdown(
        f"**{len(ids)} question(s)** have a wrong most-recent answer. The loop asks each of them once; "
        "every question you miss comes back in the next round, reshuffled, until a round is answered **100%** correctly."
    )
    misses = Counter(a.question_id for a in state.log() if not a.is_correct)
    table = pd.DataFrame([{
        "Micro-topic": bank[qid].micro_topic,
        "Syllabus unit": bank[qid].macro_unit,
        "Times missed": misses[qid],
        "Question": bank[qid].id,
    } for qid in ids])
    st.dataframe(table, hide_index=True)
    st.button(f"Start the review loop ({len(ids)})", type="primary", icon=":material/replay:",
              on_click=state.start_loop, args=(bank,))


def _done(loop) -> None:
    st.success(f"**100%.** Round {loop.round} was answered completely correctly, so this loop is finished.",
               icon=":material/celebration:")
    rounds = pd.DataFrame([{"Round": r.round, "Correct": r.correct, "Asked": r.total, "Accuracy": r.accuracy}
                           for r in loop.results])
    st.dataframe(rounds, hide_index=True, column_config={
        "Accuracy": st.column_config.ProgressColumn("Accuracy", format="percent", min_value=0, max_value=1),
    })
    with st.container(horizontal=True):
        st.button("Close the loop", type="primary", icon=":material/done_all:", on_click=state.close_loop)
        st.button("Performance analytics", icon=":material/monitoring:", on_click=state.go, args=("analytics",))


def render() -> None:
    bank, library = state.get_bank(), state.get_library()
    loop = st.session_state.review
    st.title("Review Mistakes", anchor=False)

    if loop is None:
        _home(bank)
        return
    if loop.done:
        _done(loop)
        return

    answered = len(loop.answers)
    c1, c2, c3 = st.columns(3)
    c1.metric("Round", loop.round, help="Each round asks only what you missed in the round before.")
    c2.metric("This round", f"{loop.round_correct} / {answered} correct" if answered else "—")
    c3.metric("Left in this round", len(loop.queue) - (1 if loop.current_id in loop.answers else 0))
    st.progress(answered / loop.round_size if loop.round_size else 0.0)
    if loop.results:
        st.caption("Earlier rounds: " + ", ".join(f"round {r.round} {r.accuracy:.0%}" for r in loop.results))

    q = bank[loop.current_id]
    chosen = loop.answers.get(q.id)
    with st.container(border=True):
        question_view.syllabus_tags(q)
        question_view.question_body(q)
        if chosen is None:
            question_view.answer_form(q, f"r{loop.number}-{loop.round}-{q.id}", state.submit_review, bank)
        else:
            note = ("Cleared for this loop." if q.is_correct(chosen)
                    else "It comes back in the next round.")
            question_view.feedback(q, chosen, bank, library, "review", note)

    with st.container(horizontal=True):
        if chosen is not None:
            label = "Next" if len(loop.queue) > 1 else f"Finish round {loop.round}"
            st.button(label, type="primary", icon=":material/arrow_forward:", on_click=state.advance_review)
        st.button("End the loop", icon=":material/close:", on_click=state.close_loop,
                  help="Stop here. Your mistakes stay listed until you answer them correctly.")
