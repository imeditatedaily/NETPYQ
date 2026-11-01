"""Question of the day."""

from datetime import date
from urllib.parse import unquote

from pyq import config, daily
from pyq.access import sellable_questions
from pyq.bank import load_bank


def _pool():
    bank = load_bank(config.QUESTION_DIR, True, config.TOPIC_FILE)
    return sellable_questions(bank, "yoga")


def test_same_question_all_day_and_no_repeats_for_weeks():
    pool = _pool()
    d = date(2026, 11, 1)
    assert daily.pick(pool, d) == daily.pick(list(reversed(pool)), d)      # order of loading doesn't matter
    picks = [daily.pick(pool, date.fromordinal(d.toordinal() + i)).id for i in range(60)]
    assert len(set(picks)) == 60


def test_shared_dates_are_checked():
    today = date(2026, 11, 1)
    assert daily.valid_day("2026-10-25", today) == date(2026, 10, 25)
    assert daily.valid_day("2026-11-05", today) == today          # the future
    assert daily.valid_day("2025-01-01", today) == today          # too old
    assert daily.valid_day("nonsense", today) == today
    assert daily.valid_day(None, today) == today


def test_share_links_carry_the_question_and_the_link():
    q = _pool()[0]
    url = "https://netpyq.onrender.com/daily?d=2026-11-01"
    text = daily.share_text(q, "Yoga", url)
    assert url in text and "(1)" in text
    assert unquote(daily.whatsapp_url(text).split("text=")[1]) == text
    assert "t.me/share/url?url=https%3A" in daily.telegram_url(url, "x")
