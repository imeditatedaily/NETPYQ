"""Everything the app keeps in st.session_state, and the callbacks that change it.

Session state lasts as long as the browser tab. Refreshing or closing the
tab starts a new session, which is why the sidebar offers a download of
the attempt log and a way to load it back.
"""

import json
from datetime import datetime

import streamlit as st

from ..bank import Bank, folder_signature, load_bank
from ..config import INCLUDE_SAMPLE_QUESTIONS, QUESTION_DIR, SOURCE_DIR
from ..filters import ALL, Filters, apply
from ..library import Library, load_library
from ..model import Question
from ..tracker import (Answer, PracticeRun, ReviewLoop, answers_from_dicts, make_answer, new_run,
                       outstanding_mistakes, start_review)

FILTER_KEYS = {"subject": "f_subject", "session": "f_session", "unit": "f_unit", "topic": "f_topic", "qtype": "f_qtype"}


# --- data (cached per server process; reloads when files in data/ or sources/ change) ---

@st.cache_resource(show_spinner=False)
def _bank(_signature: tuple) -> Bank:
    return load_bank(QUESTION_DIR, INCLUDE_SAMPLE_QUESTIONS)


def get_bank() -> Bank:
    return _bank(folder_signature(QUESTION_DIR))


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
    ss.setdefault("upload_nonce", 0)
    ss.setdefault("shuffle", False)
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
    answer = make_answer(q, chosen, mode, run_no, datetime.now())
    st.session_state.log.append(answer)
    return answer


def notice(message: str, icon: str = ":material/info:") -> None:
    """A one-off toast shown on the next run (callbacks cannot draw)."""
    st.session_state["_notice"] = (message, icon)


def show_notice() -> None:
    if pending := st.session_state.pop("_notice", None):
        st.toast(pending[0], icon=pending[1])


# --- navigation: callbacks set a target, streamlit_app.py switches page ------------------

def go(page: str) -> None:
    st.session_state["goto"] = page


# --- practice ----------------------------------------------------------------------------

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


# --- saving and restoring the log --------------------------------------------------------

def log_json() -> str:
    return json.dumps([a.to_dict() for a in log()], ensure_ascii=False, indent=1)


def load_log_file(uploader_key: str) -> None:
    ss = st.session_state
    upload = ss.get(uploader_key)
    if upload is None:
        return
    try:
        restored = answers_from_dicts(json.loads(upload.getvalue().decode("utf-8")))
    except (ValueError, UnicodeDecodeError) as e:
        notice(f"Could not load that file: {e}", ":material/error:")
    else:
        ss.log = restored
        ss.review = None
        notice(f"Restored {len(restored)} logged answers.", ":material/upload:")
    ss.upload_nonce += 1  # a fresh uploader widget, so the same file can be loaded again


def reset_session() -> None:
    ss = st.session_state
    ss.log, ss.run, ss.review = [], None, None
    notice("Session cleared.", ":material/delete:")
