"""Timed mock tests: palette states, timer, NTA scoring."""

import pytest

from pyq import config, mock
from pyq.access import visible_bank
from pyq.bank import load_bank


@pytest.fixture(scope="module")
def free_bank():
    return visible_bank(load_bank(config.QUESTION_DIR, True, config.TOPIC_FILE), admin=False, unlocked=set())


def test_free_user_can_sit_the_free_paper(free_bank):
    choices = mock.paper_choices(free_bank.questions, "yoga", seed=1)
    assert [c.key for c in choices] == ["session:June 2024"]     # one paper, so no mixed test
    assert len(choices[0].question_ids) == 100 and choices[0].minutes == 120


def test_palette_and_scoring(free_bank):
    choice = mock.paper_choices(free_bank.questions, "yoga", seed=1)[0]
    t = mock.MockTest.start(1, choice, "yoga", now=1000.0)
    ids = choice.question_ids
    assert t.status(ids[0]) == mock.NOT_ANSWERED and t.status(ids[1]) == mock.NOT_VISITED

    right = free_bank[ids[0]].correct_answer
    t.save(right)                                   # Q1 correct, moves to Q2
    assert t.status(ids[0]) == mock.ANSWERED and t.position == 1
    t.save(None, mark=True)                         # Q2 marked, no answer
    assert t.status(ids[1]) == mock.MARKED
    wrong = right % 4 + 1 if free_bank[ids[2]].correct_answer != right % 4 + 1 else (right + 1) % 4 + 1
    t.save(wrong if wrong != free_bank[ids[2]].correct_answer else (wrong % 4) + 1, mark=True)
    assert t.status(ids[2]) == mock.ANSWERED_MARKED
    t.go(2); t.clear()
    assert t.status(ids[2]) == mock.MARKED

    r = mock.score(t, free_bank.by_id)
    assert (r.correct, r.wrong, r.unattempted, r.marks, r.max_marks) == (1, 0, 99, 2, 200)


def test_timer_and_submit(free_bank):
    choice = mock.paper_choices(free_bank.questions, "yoga", seed=1)[0]
    t = mock.MockTest.start(1, choice, "yoga", now=0.0)
    assert t.remaining(60) == 7200 - 60 and not t.expired(60)
    assert t.expired(7200)
    t.submit(9999)                                   # late submit is capped at the time limit
    assert t.time_taken(99999) == 7200 and t.remaining(99999) == 0
