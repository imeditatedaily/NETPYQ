"""Accounts: who sees what, saved progress, and Razorpay subscriptions."""

from datetime import datetime
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from pyq import config, store
from pyq.access import Subscription, is_book_sourced, sellable_subjects, unlocked_subjects, visible_bank
from pyq.bank import load_bank
from pyq.payments import PaymentError, Razorpay, needs_refresh
from pyq.tracker import make_answer

APP = str(Path(__file__).resolve().parent.parent / "streamlit_app.py")
NOW = 1_800_000_000

OFFICIAL_DEC_2018 = "Paper 1 (22 Dec, shift 1)"   # from NTA's master question paper, not from a book


@pytest.fixture(scope="module")
def bank():
    return load_bank(config.QUESTION_DIR, True, config.TOPIC_FILE)


# --- access ----------------------------------------------------------------------------

def test_free_user_sees_the_samples_and_the_free_paper(bank):
    free = visible_bank(bank, admin=False, unlocked=set())
    real = [q for q in free.questions if q.source_type != "model"]
    assert sum(q.source_type == "model" for q in free.questions) == 4
    assert len(real) == 100 + 100                     # Yoga December 2018 and July 2018
    assert all((q.subject, q.exam_year, q.exam_cycle) in config.FREE_PAPERS for q in real)
    assert not any(q.exam_year == 2024 for q in real)  # June 2024 is paid now


def test_yoga_subscriber_gets_every_yoga_paper_but_no_book_questions(bank):
    yoga = visible_bank(bank, admin=False, unlocked={"yoga"})
    real = [q for q in yoga.questions if q.source_type != "model"]
    assert real and all(q.subject == "yoga" for q in real)
    p1 = visible_bank(bank, admin=False, unlocked={"paper1"})
    assert not any(q.subject == "paper1" and q.is_dated and q.exam_year < 2019 and q.paper != OFFICIAL_DEC_2018
                   for q in p1.questions)                                                         # the book papers stay hidden
    assert any(q.paper == OFFICIAL_DEC_2018 for q in p1.questions)   # NTA's own December 2018 paper is sold
    assert any(q.subject == "paper1" and q.exam_year == 2025 for q in p1.questions)


def test_admin_sees_everything(bank):
    assert len(visible_bank(bank, admin=True, unlocked=set())) == len(bank)


def test_book_sourced_questions_are_detected(bank):
    assert all(is_book_sourced(q) for q in bank.questions
               if q.subject == "paper1" and q.is_dated and q.exam_year < 2019 and q.paper != OFFICIAL_DEC_2018)
    assert not any(is_book_sourced(q) for q in bank.questions if q.paper == OFFICIAL_DEC_2018)
    from_book = {q.session_label for q in bank.questions if q.subject == "yoga" and is_book_sourced(q)}
    assert from_book == {"November 2017", "July 2018", "December 2018"}    # transcribed from a solved-papers collection
    assert any(not is_book_sourced(q) for q in bank.questions if q.subject == "yoga")
    assert sellable_subjects(bank) == ["yoga", "paper1"]   # Paper 1 from the official June 2025 response sheet


@pytest.mark.parametrize("status,end,expected", [
    ("active", None, True),
    ("created", None, False),
    ("authenticated", None, False),
    ("cancelled", NOW + 60, True),      # cancelled, but the paid month hasn't ended
    ("cancelled", NOW - 60, False),
    ("halted", NOW - 60, False),
    ("pending", NOW + 60, True),        # renewal retrying, still inside the paid month
    ("expired", None, False),
])
def test_which_razorpay_states_grant_access(status, end, expected):
    sub = Subscription("sub_1", "a@b.c", "yoga", status, end)
    assert sub.grants_access(NOW) is expected
    assert unlocked_subjects([sub], NOW) == ({"yoga"} if expected else set())


def test_when_to_ask_razorpay_again():
    assert needs_refresh(Subscription("s", "e", "yoga", "created"), NOW)
    assert not needs_refresh(Subscription("s", "e", "yoga", "active", NOW + 60), NOW)
    assert needs_refresh(Subscription("s", "e", "yoga", "active", NOW - 60), NOW)     # renewal due
    assert not needs_refresh(Subscription("s", "e", "yoga", "cancelled", NOW + 60), NOW)


# --- storage ---------------------------------------------------------------------------

def test_answers_and_subscriptions_round_trip(tmp_path, bank):
    eng = store.make_engine(f"sqlite:///{tmp_path / 'db.sqlite'}")
    q = bank.questions[0]
    a1 = make_answer(q, 1, "practice", 1, datetime(2026, 1, 1))
    a2 = make_answer(q, q.correct_answer, "review", 1, datetime(2026, 1, 2))
    store.add_answer(eng, "x@gmail.com", a1)
    store.add_answer(eng, "x@gmail.com", a2)
    store.add_answer(eng, "y@gmail.com", a1)
    assert store.load_answers(eng, "x@gmail.com") == [a1, a2]
    store.replace_answers(eng, "x@gmail.com", [a2])
    assert store.load_answers(eng, "x@gmail.com") == [a2]
    assert store.answer_counts(eng) == {"x@gmail.com": 1, "y@gmail.com": 1}

    sub = store.save_subscription(eng, Subscription("sub_9", "x@gmail.com", "yoga", "created", short_url="https://rzp.io/x"))
    assert sub.created_at
    store.save_subscription(eng, Subscription("sub_9", "x@gmail.com", "yoga", "active", NOW))
    [saved] = store.list_subscriptions(eng, "x@gmail.com")
    assert (saved.status, saved.current_end, saved.created_at) == ("active", NOW, sub.created_at)
    assert store.list_subscriptions(eng, "y@gmail.com") == []


def test_supabase_style_urls_use_psycopg():
    assert store.normalise_url("postgresql://u:p@h:5432/db") == "postgresql+psycopg://u:p@h:5432/db"
    assert store.normalise_url("postgres://u:p@h/db") == "postgresql+psycopg://u:p@h/db"
    assert store.normalise_url("sqlite:///x.db") == "sqlite:///x.db"


# --- Razorpay (no network: requests is replaced) ----------------------------------------

class FakeResponse:
    def __init__(self, status, data):
        self.status_code, self._data, self.text = status, data, str(data)

    @property
    def ok(self):
        return self.status_code < 400

    def json(self):
        return self._data


def test_razorpay_create_refresh_and_errors(monkeypatch):
    calls = []

    def fake_request(method, url, json=None, auth=None, timeout=None):
        calls.append((method, url, json, auth))
        if method == "POST" and url.endswith("/subscriptions"):
            return FakeResponse(200, {"id": "sub_A", "status": "created", "short_url": "https://rzp.io/i/abc"})
        if url.endswith("/subscriptions/sub_A"):
            return FakeResponse(200, {"id": "sub_A", "status": "active", "current_end": NOW})
        return FakeResponse(400, {"error": {"description": "The id provided does not exist"}})

    monkeypatch.setattr("pyq.payments.requests.request", fake_request)
    rzp = Razorpay("rzp_test_key", "secret")
    sub = rzp.create_subscription("plan_Y", "x@gmail.com", "yoga")
    assert (sub.razorpay_id, sub.status, sub.short_url) == ("sub_A", "created", "https://rzp.io/i/abc")
    assert calls[0][2]["plan_id"] == "plan_Y" and calls[0][2]["notes"] == {"email": "x@gmail.com", "subject": "yoga"}
    assert calls[0][3] == ("rzp_test_key", "secret")
    fresh = rzp.refresh(sub)
    assert fresh.status == "active" and fresh.current_end == NOW and fresh.grants_access(NOW - 1)
    with pytest.raises(PaymentError, match="does not exist"):
        rzp.refresh(Subscription("sub_missing", "x", "yoga", "created"))


# --- the app as a signed-in, non-admin user ------------------------------------------------

def as_user(unlocked=()) -> AppTest:
    """The dev user, but treated as a regular (non-admin) student."""
    at = AppTest.from_file(APP, default_timeout=60)
    at.session_state["user"] = "dev@localhost"   # already signed in, so the dev-mode admin setup is skipped
    at.session_state["is_admin"] = False
    at.session_state["unlocked"] = set(unlocked)
    at.session_state["log"] = []
    at.run()
    assert not at.exception, [e.message for e in at.exception]
    return at


def test_free_user_practises_samples_and_is_offered_plans():
    at = as_user()
    assert at.metric[3].value == "1 of 204"                # 4 samples + December 2018 (100) + July 2018 (100)
    assert any("free plan" in m.value for m in at.markdown)
    assert "Source Library" not in str(at.get("navigation"))


def test_locked_subject_shows_the_paywall():
    at = as_user()
    at.segmented_control(key="f_subject").set_value("yoga").run()
    assert any("is locked" in m.value for m in at.markdown)


def test_subscriber_sees_the_whole_subject():
    at = as_user(unlocked={"yoga"})
    at.segmented_control(key="f_subject").set_value("yoga").run()
    assert not any("is locked" in m.value for m in at.markdown)
    assert int(at.metric[3].value.split(" of ")[1]) > 400


def test_subscription_page_lists_plans():
    at = as_user()
    at.session_state["goto"] = "plans"
    at.run()
    assert not at.exception, [e.message for e in at.exception]
    assert at.title[0].value == "Subscription"
    md = "\n".join(m.value for m in at.markdown)
    assert "₹500 / month" in md
    assert any(b.label.startswith("Subscribe for ₹500") for b in at.button)


def test_answers_are_saved_and_come_back_in_a_new_session():
    at = AppTest.from_file(APP, default_timeout=60).run()          # dev mode: signs in as the dev user
    at.selectbox(key="f_session").set_value("undated").run()
    at.radio[0].set_value(1)
    next(b for b in at.button if b.label.startswith("Submit answer")).click().run()
    assert at.metric[1].value == "0 / 1"

    again = AppTest.from_file(APP, default_timeout=60).run()       # a new browser session
    assert len(again.session_state["log"]) == 1
    assert again.session_state["log"][0].chosen == 1


@pytest.mark.parametrize("path", ["pricing", "privacy", "terms", "refund", "shipping", "contact"])
def test_policy_pages_render(path):
    at = as_user()
    at.session_state["goto"] = path
    at.run()
    assert not at.exception, [e.message for e in at.exception]
    assert at.title and "NTA" in "\n".join(c.value for c in at.caption)


def _trends(unlocked=()):
    at = as_user(unlocked)
    at.session_state["goto"] = "trends"
    at = at.run()
    assert not at.exception, [e.message for e in at.exception]
    return " ".join(m.value for m in at.markdown)


def test_free_user_sees_only_a_preview_of_the_trends():
    text = _trends()
    assert "is for subscribers" in text and "Every micro-topic" not in text


def test_subscriber_sees_the_full_trends():
    at = as_user({"yoga", "paper1"})
    at.session_state["goto"] = "trends"
    at = at.run()
    assert not [m for m in at.markdown if "is for subscribers" in m.value]
    assert any(s.value == "Every micro-topic" for s in at.subheader)


def test_users_are_not_told_where_a_question_came_from():
    at = as_user({"yoga"})
    at.segmented_control(key="f_subject").set_value("yoga").run()
    captions = " ".join(c.value for c in at.caption)
    assert "Official paper" not in captions and "YOGA-" not in captions


def test_practice_sets_come_with_the_subscription_and_stay_out_of_the_trends(bank):
    practice = [q for q in bank.questions if q.source_type == "practice"]
    assert practice and not any(q.is_dated for q in practice)
    assert {q.session_key for q in practice} == {"practice"}
    free = visible_bank(bank, admin=False, unlocked=set())
    assert not any(q.source_type == "practice" for q in free.questions)
    yoga = visible_bank(bank, admin=False, unlocked={"yoga"})
    assert any(q.source_type == "practice" and q.subject == "yoga" for q in yoga.questions)


def test_signed_out_visitors_never_see_trends_or_the_knowledge_base():
    from pyq.ui import landing
    html = landing.LOCKED_TEASER + landing.PREVIEW
    assert "Sign in" in html and "%" not in landing.LOCKED_TEASER   # no real trend numbers before sign-in
    assert "lp-bars" not in landing.PREVIEW and "Trend insight" not in landing.PREVIEW
