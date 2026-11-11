"""Everything the app keeps in st.session_state, and the callbacks that change it.

Every answer is also saved to the signed-in user's account (see account.py),
so the log comes back after a refresh or on another device. The current
practice attempt and review loop live only in the browser tab.
"""

from datetime import datetime

import streamlit as st

from ..access import visible_bank
from ..bank import Bank, folder_signature, load_bank
from ..config import (INCLUDE_SAMPLE_QUESTIONS, KNOWLEDGE_FILE, QUESTION_DIR, SOURCE_DIR, TEXT_DIR, TOPIC_FILE,
                      TRANSLATION_DIR)
from ..knowledge import KnowledgeBase, load_knowledge
from ..filters import ALL, Filters, apply
from ..library import Library, load_library
from ..model import Question
from ..texts import TextLibrary, load_texts
from ..tracker import (Answer, PracticeRun, ReviewLoop, make_answer, new_run,
                       outstanding_mistakes, start_review)

FILTER_KEYS = {"subject": "f_subject", "session": "f_session", "unit": "f_unit", "topic": "f_topic", "qtype": "f_qtype"}


# --- data (cached per server process; reloads when files in data/ or sources/ change) ---

@st.cache_resource(show_spinner=False)
def _bank(_signature: tuple) -> Bank:
    return load_bank(QUESTION_DIR, INCLUDE_SAMPLE_QUESTIONS, TOPIC_FILE)


def get_full_bank() -> Bank:
    """Every loaded question, whatever the user has paid for."""
    return _bank(folder_signature(QUESTION_DIR, TOPIC_FILE))


def get_bank() -> Bank:
    """The questions this user may see: free samples plus the subjects they subscribe to."""
    ss = st.session_state
    return visible_bank(get_full_bank(), admin=ss.get("is_admin", False), unlocked=ss.get("unlocked", set()))


@st.cache_resource(show_spinner=False)
def _translations(_signature: tuple) -> dict:
    from ..translate import load
    return load(TRANSLATION_DIR)


def get_translations() -> dict:
    files = sorted(TRANSLATION_DIR.glob("*.json")) if TRANSLATION_DIR.is_dir() else []
    return _translations(tuple((p.name, p.stat().st_mtime) for p in files))


@st.cache_resource(show_spinner=False)
def _knowledge(_mtime: float) -> KnowledgeBase:
    return load_knowledge(KNOWLEDGE_FILE)


def get_knowledge() -> KnowledgeBase:
    return _knowledge(KNOWLEDGE_FILE.stat().st_mtime if KNOWLEDGE_FILE.is_file() else 0.0)


@st.cache_resource(show_spinner=False)
def _texts(_signature: tuple) -> TextLibrary:
    return load_texts(TEXT_DIR)


def get_texts() -> TextLibrary:
    files = sorted(TEXT_DIR.glob("*.json")) if TEXT_DIR.is_dir() else []
    return _texts(tuple((p.name, p.stat().st_mtime) for p in files))


@st.cache_resource(show_spinner=False)
def _library(_signature: tuple) -> Library:
    return load_library(SOURCE_DIR)


def get_library() -> Library:
    files = sorted(SOURCE_DIR.glob("*")) if SOURCE_DIR.is_dir() else []
    return _library(tuple((p.name, p.stat().st_mtime) for p in files))


# --- session state ---------------------------------------------------------------------

def init() -> None:
    ss = st.session_state
    ss.setdefault("log", [])            # list[Answer], every submission
    ss.setdefault("run", None)          # current PracticeRun
    ss.setdefault("review", None)       # current ReviewLoop
    ss.setdefault("runs_started", 0)
    ss.setdefault("loops_started", 0)
    ss.setdefault("shuffle", False)
    ss.setdefault("focus", False)
    ss.setdefault("is_admin", False)
    ss.setdefault("unlocked", set())
    ss.setdefault("subs", [])
    ss.setdefault("lang", "en")         # question language: "en" or "hi"
    for key in FILTER_KEYS.values():
        ss.setdefault(key, ALL)


def log() -> list[Answer]:
    return st.session_state.log


def current_filters() -> Filters:
    ss = st.session_state
    return Filters(**{field: ss[key] for field, key in FILTER_KEYS.items()})


def mistakes(bank: Bank) -> list[str]:
    return [qid for qid in outstanding_mistakes(log()) if qid in bank]


def record(q: Question, chosen: int, mode: str, run_no: int) -> Answer:
    from . import account
    answer = make_answer(q, chosen, mode, run_no, datetime.now())
    st.session_state.log.append(answer)
    account.save_answer(answer)
    return answer


def notice(message: str, icon: str = ":material/info:") -> None:
    """A one-off toast shown on the next run (callbacks cannot draw)."""
    st.session_state["_notice"] = (message, icon)


def show_notice() -> None:
    if pending := st.session_state.pop("_notice", None):
        st.toast(pending[0], icon=pending[1])


# --- navigation: callbacks set a target, streamlit_app.py switches page ------------------

def has_full_access(subject: str) -> bool:
    """Admins, and subscribers to this subject, see everything (full trends, sources stay hidden for all but admins)."""
    ss = st.session_state
    return ss.get("is_admin", False) or subject in ss.get("unlocked", set())


def is_admin() -> bool:
    return st.session_state.get("is_admin", False)


def go(page: str) -> None:
    st.session_state["goto"] = page


# --- practice ----------------------------------------------------------------------------

def open_text(subject: str, text_id: str | None = None, query: str = "") -> None:
    """Opens the Sanskrit Texts page on one text, or on a search (used by the Knowledge Base).
    Widget keys are dropped when the page switches, so the request waits under a plain key
    ("tx_open") that the Texts page applies before it draws its widgets."""
    st.session_state["tx_open"] = {"subject": subject, "text": text_id, "query": query}
    go("texts")


def start_run(bank: Bank, filters: Filters | None = None) -> PracticeRun:
    ss = st.session_state
    filters = filters or current_filters()
    ss.runs_started += 1
    ids = [q.id for q in apply(bank.questions, filters)]
    ss.run = new_run(ss.runs_started, ids, filters, ss.shuffle)
    return ss.run


def ensure_run(bank: Bank) -> PracticeRun:
    """Starts a run if there is none; follows filter changes until the run has answers."""
    run: PracticeRun | None = st.session_state.run
    filters = current_filters()
    if run is None or (run.filters != filters and not run.answers):
        run = start_run(bank, filters)
    return run


def restart_same_quiz(bank: Bank) -> None:
    """Takes the same quiz again: same questions, fresh answers, reshuffled if shuffle is on."""
    run: PracticeRun = st.session_state.run
    start_run(bank, run.filters)
    notice(f"Attempt #{st.session_state.run.number} started on the same questions.", ":material/restart_alt:")


def submit_practice(bank: Bank, question_id: str, choice_key: str) -> None:
    chosen = st.session_state.get(choice_key)
    if chosen is None:
        notice("Choose an option first.", ":material/warning:")
        return
    run: PracticeRun = st.session_state.run
    run.submit(question_id, chosen)
    record(bank[question_id], chosen, "practice", run.number)


def advance_practice() -> None:
    st.session_state.run.advance()


def practise_topic(subject: str, unit: str, topic: str) -> None:
    """Callback: filter to one micro-topic, start a fresh run on it, open Practice."""
    ss = st.session_state
    ss.f_subject, ss.f_session, ss.f_unit, ss.f_topic, ss.f_qtype = subject, ALL, unit, topic, ALL
    ss.run = None
    go("practice")


# --- review ------------------------------------------------------------------------------

def start_loop(bank: Bank) -> None:
    ss = st.session_state
    ss.loops_started += 1
    ss.review = start_review(ss.loops_started, mistakes(bank))


def submit_review(bank: Bank, question_id: str, choice_key: str) -> None:
    chosen = st.session_state.get(choice_key)
    if chosen is None:
        notice("Choose an option first.", ":material/warning:")
        return
    loop: ReviewLoop = st.session_state.review
    q = bank[question_id]
    loop.submit(question_id, chosen, q.is_correct(chosen))
    record(q, chosen, "review", loop.number)


def advance_review() -> None:
    st.session_state.review.advance()


def close_loop() -> None:
    st.session_state.review = None


def reset_session() -> None:
    ss = st.session_state
    from . import account
    ss.log, ss.run, ss.review = [], None, None
    account.save_all_answers([])
    notice("Your progress was cleared.", ":material/delete:")
