"""The question card shared by Practice and Review: syllabus tags, the
question in its NTA format, the answer form, and after submission the
verdict, the explanation, the Trend Insight box and where to study it."""

import re
from collections.abc import Callable

import streamlit as st

from ..analytics import topic_frequency
from ..knowledge import short_stem, topic_pattern
from ..bank import Bank
from ..library import Library
from .. import translate
from ..model import ANSWER_SOURCES, QUESTION_TYPES, Question
from . import state

LETTERS = "ABCDEFGHIJ"
ROMAN = ("I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X")
LABELS = {"letters": LETTERS, "roman": ROMAN, "numbers": tuple(str(n) for n in range(1, 11))}
_MD_SPECIAL = re.compile(r"([\\`*_\[\]<>#|$~])")


def md(text: str) -> str:
    """Escapes plain text (options, list items) so Markdown never reinterprets it."""
    return _MD_SPECIAL.sub(r"\\\1", text)


_PROVENANCE = re.compile(r"\s*\((?:no official key|as keyed|provisional|as printed[^)]*)\)", re.I)


_ADMIN_SENTENCE = re.compile(r"source collection|could not be checked|I could not|handout|coaching|transcri|response sheet|"
                             r"printed edition|solved-papers|Madaan", re.I)


def _public(text: str) -> str:
    """Explanations as users see them: notes about keys, books and transcription are for admins."""
    text = _PROVENANCE.sub("", text)
    out = []
    for para in text.split("\n"):
        sentences = re.split(r"(?<=[.!?])\s+", para)
        kept = [x for x in sentences if not _ADMIN_SENTENCE.search(x)]
        out.append(" ".join(kept).replace("()", "").strip() if kept != sentences else para)
    return "\n".join(out)


def _css_key(text: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_-]", "-", text)


def language_toggle(key: str = "lang") -> None:
    """English / हिन्दी: which language questions are shown in."""
    if st.session_state.get(key) not in translate.LANG_NAMES:
        st.session_state[key] = translate.EN
    st.segmented_control("Question language", list(translate.LANG_NAMES), key=key, required=True,
                         format_func=translate.LANG_NAMES.get,
                         help="Questions appear in the language of the paper they come from. Pick a language to "
                              "see every question in it; translated questions are marked.")


def localize(q: Question, note: bool = True) -> Question:
    """q in the chosen language, with a one-line note when it is a translation."""
    lang = st.session_state.get("lang", translate.EN)
    out, status = translate.translated(q, lang, state.get_translations())
    if note and status == "translated":
        src = "Hindi" if lang == translate.EN else "English"
        st.caption(f":material/translate: Translated from the {src} paper"
                   if lang == translate.EN else ":material/translate: अंग्रेज़ी प्रश्नपत्र से अनूदित")
    elif note and status == "missing":
        st.caption(":material/translate: English translation coming soon; shown as printed."
                   if lang == translate.EN else ":material/translate: हिन्दी अनुवाद शीघ्र; मूल रूप में दिखाया गया है।")
    return out


def syllabus_tags(q: Question) -> None:
    """Macro unit and micro-topic above every question."""
    with st.container(horizontal=True, gap="small"):
        st.badge(q.subject_info.display, icon=":material/school:", color="gray")
        st.badge(q.macro_unit, icon=":material/layers:", color="blue")
        st.badge(q.micro_topic, icon=":material/target:", color="orange")
    if state.is_admin():
        st.caption(f"{QUESTION_TYPES[q.question_type]} · {q.source_label} · `{q.id}`", help=q.source_note or None)
    else:   # where a question came from is never shown to users, only its exam session
        st.caption(f"{QUESTION_TYPES[q.question_type]} · {q.session_label}")


def question_body(q: Question) -> None:
    if q.passage:
        with st.expander("Read the passage", icon=":material/article:", expanded=True):
            st.markdown(md(q.passage))
    if q.table_columns:
        with st.container(border=True):
            if q.table_title:
                st.markdown(md(q.table_title))
            table = ["| " + " | ".join(f"**{md(c)}**" if c else " " for c in q.table_columns) + " |",
                     "|" + "---|" * len(q.table_columns)]
            table += ["| " + " | ".join(md(c) if c else " " for c in row) + " |" for row in q.table_rows]
            st.markdown("\n".join(table))
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
        if not state.has_full_access(q.subject):
            st.markdown(":material/lock: **The full trend analysis for this topic is for subscribers.**")
            st.button("See plans", icon=":material/workspace_premium:", key=f"trend-lock-{context}-{q.id}",
                      on_click=state.go, args=("plans",))
            return
        st.markdown(q.trend_analysis)
        others = sum(x.micro_topic == q.micro_topic and x.subject == q.subject for x in bank.questions)
        if others > 1:
            st.button(f"Practise all {others} questions on this micro-topic", icon=":material/target:",
                      key=f"drill-{context}-{q.id}", on_click=state.practise_topic,
                      args=(q.subject, q.macro_unit, q.micro_topic))


def knowledge_box(q: Question, bank: Bank, library: Library, context: str, limit: int = 8) -> None:
    """Shown after every answer, right or wrong: the topic's key facts, how it is asked, and earlier questions on it."""
    kb = state.get_knowledge()
    note = kb.note(q.subject, q.micro_topic)
    pattern = topic_pattern(bank.questions, q.subject, q.micro_topic)
    with st.container(border=True, key=f"kb-{context}-{_css_key(q.id)}"):
        st.markdown(f"#### :material/school: Knowledge Base: {md(q.micro_topic)}")
        if note:
            st.markdown("**Key facts**")
            st.markdown("\n".join(f"- {f}" for f in note.facts))
            cites = [library.by_id[s].citation for s in note.sources if s in library.by_id]
            if cites:
                st.caption("From: " + "; ".join(md(c) for c in cites))
        else:
            st.caption("Key facts for this topic are being written. The explanation above covers this question.")
        st.markdown(f"**How this topic is asked.** {pattern.sentence()}")
        earlier = [x for x in pattern.questions if x.id != q.id]
        if not state.has_full_access(q.subject):
            limit = 2
        if earlier:
            with st.expander(f"Earlier questions on this topic ({len(earlier)})", icon=":material/history:"):
                for x in earlier[:limit]:
                    st.markdown(f"- **{md(x.session_label)}** · {md(short_stem(x))}  \n"
                                f"  :green[Answer: ({x.correct_answer}) {md(x.correct_text)}]")
                if len(earlier) > limit:
                    if state.has_full_access(q.subject):
                        st.caption(f"…and {len(earlier) - limit} more. Use the button in Trend Insight to practise them all.")
                    else:
                        st.caption(f":material/lock: …and {len(earlier) - limit} more for subscribers.")


def study_links(q: Question, library: Library, context: str) -> None:
    sources = [library.by_id[s] for s in q.source_ids if s in library.by_id]
    if not sources:
        return
    st.markdown("##### :material/menu_book: Study this in")
    admin = st.session_state.get("is_admin", False)
    for s in sources:
        status = (":green-badge[in your library]" if s.available else ":gray-badge[not added yet]") if admin else ""
        st.markdown(f"- {md(s.citation)} {status}")
    if not admin:   # the Source Library (with the owner's own files) is for admins only
        return
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
    if q.answer_source and state.is_admin():
        icon = {"official_key": ":material/verified:", "cross_checked": ":material/fact_check:",
                "unverified": ":material/help:"}[q.answer_source]
        st.caption(f"{icon} {ANSWER_SOURCES[q.answer_source]}.")
    _options_review(q, chosen)
    st.markdown("##### Detailed explanation")
    st.markdown(q.detailed_explanation if state.is_admin() else _public(q.detailed_explanation))
    if q.references and state.is_admin():
        st.caption("Sources: " + "; ".join(md(r) for r in q.references))
    knowledge_box(q, bank, library, context)
    trend_insight(q, bank, context)
    study_links(q, library, context)
