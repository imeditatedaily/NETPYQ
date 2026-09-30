"""The question card shared by Practice and Review: syllabus tags, the
question in its NTA format, the answer form, and after submission the
verdict, the explanation, the Trend Insight box and where to study it."""

import re
from collections.abc import Callable

import streamlit as st

from ..analytics import topic_frequency
from ..bank import Bank
from ..library import Library
from ..model import ANSWER_SOURCES, QUESTION_TYPES, Question
from . import state

LETTERS = "ABCDEFGHIJ"
ROMAN = ("I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X")
LABELS = {"letters": LETTERS, "roman": ROMAN, "numbers": tuple(str(n) for n in range(1, 11))}
_MD_SPECIAL = re.compile(r"([\\`*_\[\]<>#|$~])")


def md(text: str) -> str:
    """Escapes plain text (options, list items) so Markdown never reinterprets it."""
    return _MD_SPECIAL.sub(r"\\\1", text)


def _css_key(text: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_-]", "-", text)


def syllabus_tags(q: Question) -> None:
    """Macro unit and micro-topic above every question."""
    with st.container(horizontal=True, gap="small"):
        st.badge(q.subject_info.display, icon=":material/school:", color="gray")
        st.badge(q.macro_unit, icon=":material/layers:", color="blue")
        st.badge(q.micro_topic, icon=":material/target:", color="orange")
    st.caption(f"{QUESTION_TYPES[q.question_type]} · {q.source_label} · `{q.id}`", help=q.source_note or None)


def question_body(q: Question) -> None:
    if q.passage:
        with st.expander("Read the passage", icon=":material/article:", expanded=True):
            st.markdown(md(q.passage))
    st.markdown(f"#### {md(q.question_text)}")
    if q.list_i:
        rows = max(len(q.list_i), len(q.list_ii))
        table = [f"| {md(q.list_i_title)} | {md(q.list_ii_title)} |", "|---|---|"]
        left_labels, right_labels = (LABELS[s] for s in q.list_styles)
        for i in range(rows):
            left = f"**{left_labels[i]}.** {md(q.list_i[i])}" if i < len(q.list_i) else ""
            right = f"**{right_labels[i]}.** {md(q.list_ii[i])}" if i < len(q.list_ii) else ""
            table.append(f"| {left} | {right} |")
        st.markdown("\n".join(table))
    if q.items:
        labels = LABELS[q.item_style]
        st.markdown("\n\n".join(f"**{labels[i]}.** {md(t)}" for i, t in enumerate(q.items)))
    if q.assertion:
        with st.container(border=True):
            st.markdown(f"**Assertion (A):** {md(q.assertion)}")
        with st.container(border=True):
            st.markdown(f"**Reason (R):** {md(q.reason)}")
    if q.prompt:
        st.markdown(f"*{md(q.prompt)}*")


def answer_form(q: Question, key: str, on_submit: Callable, bank: Bank) -> None:
    choice_key = f"choice-{key}"
    with st.form(f"form-{key}", border=False):
        st.radio(
            "Choose one answer",
            options=list(range(1, len(q.options) + 1)),
            index=None,
            format_func=lambda n: f"({n}) {md(q.options[n - 1])}",
            key=choice_key,
        )
        st.form_submit_button("Submit answer", type="primary", icon=":material/done:",
                              on_click=on_submit, args=(bank, q.id, choice_key))


def _options_review(q: Question, chosen: int) -> None:
    lines = []
    for n, text in enumerate(q.options, start=1):
        if n == q.correct_answer:
            lines.append(f":green[:material/check_circle:] **({n}) {md(text)}**, correct answer")
        elif n == chosen:
            lines.append(f":red[:material/cancel:] ~~({n}) {md(text)}~~, your answer")
        else:
            lines.append(f":gray[:material/radio_button_unchecked: ({n}) {md(text)}]")
    st.markdown("  \n".join(lines))


def trend_insight(q: Question, bank: Bank, context: str) -> None:
    """The highlighted box: the counted frequency, then the written analysis."""
    freq = topic_frequency(bank.questions, q)
    with st.container(key=f"trend-{context}-{_css_key(q.id)}"):
        st.markdown("#### :material/trending_up: Trend Insight")
        st.caption(f"{q.micro_topic} · {q.macro_unit}")
        st.markdown(f"**Frequency in loaded papers.** {freq.sentence(q.subject_info.short)}")
        st.markdown(q.trend_analysis)
        others = sum(x.micro_topic == q.micro_topic and x.subject == q.subject for x in bank.questions)
        if others > 1:
            st.button(f"Practise all {others} questions on this micro-topic", icon=":material/target:",
                      key=f"drill-{context}-{q.id}", on_click=state.practise_topic,
                      args=(q.subject, q.macro_unit, q.micro_topic))


def study_links(q: Question, library: Library, context: str) -> None:
    sources = [library.by_id[s] for s in q.source_ids if s in library.by_id]
    if not sources:
        return
    st.markdown("##### :material/menu_book: Study this in")
    for s in sources:
        status = ":green-badge[in your library]" if s.available else ":gray-badge[not added yet]"
        st.markdown(f"- {md(s.citation)} {status}")
    st.button("Open the Source Library", icon=":material/menu_book:", key=f"lib-{context}-{q.id}",
              on_click=open_library_for, args=(q.macro_unit,))


def open_library_for(unit: str) -> None:
    st.session_state["lib_focus"] = unit
    state.go("library")


def feedback(q: Question, chosen: int, bank: Bank, library: Library, context: str, note: str = "") -> None:
    if q.is_correct(chosen):
        st.success(f"**Correct.** Option ({chosen}) is right.", icon=":material/check_circle:")
    else:
        st.error(f"**Incorrect.** You chose ({chosen}). The correct answer is ({q.correct_answer}): "
                 f"{md(q.correct_text)}", icon=":material/cancel:")
    if note:
        st.caption(note)
    if q.answer_source:
        icon = {"official_key": ":material/verified:", "cross_checked": ":material/fact_check:",
                "unverified": ":material/help:"}[q.answer_source]
        st.caption(f"{icon} {ANSWER_SOURCES[q.answer_source]}.")
    _options_review(q, chosen)
    st.markdown("##### Detailed explanation")
    st.markdown(q.detailed_explanation)
    if q.references:
        st.caption("Sources: " + "; ".join(md(r) for r in q.references))
    trend_insight(q, bank, context)
    study_links(q, library, context)
