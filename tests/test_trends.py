"""PYQ Trends: unit-wise and topic-wise counts over the real papers."""

import pytest

from pyq import trends
from pyq.access import sellable_questions
from pyq.bank import load_bank
from pyq.config import INCLUDE_SAMPLE_QUESTIONS, QUESTION_DIR, TOPIC_FILE


@pytest.fixture(scope="module")
def yoga():
    bank = load_bank(QUESTION_DIR, INCLUDE_SAMPLE_QUESTIONS, TOPIC_FILE)
    return trends.pattern(sellable_questions(bank, "yoga"))


def test_counts_add_up(yoga):
    assert yoga.units["questions"].sum() == yoga.questions == yoga.topics["questions"].sum()
    assert yoga.units["share"].sum() == pytest.approx(1)
    assert sum(yoga.sizes.values()) == yoga.questions


def test_sessions_are_chronological_and_partial_papers_flagged(yoga):
    order = {s: i for i, s in enumerate(yoga.sessions)}
    assert all(order[a] < order[b] for a, b in zip(yoga.full, yoga.full[1:]))
    biggest = max(yoga.sizes.values())
    assert all(yoga.sizes[s] >= trends.FULL_PAPER_SHARE * biggest for s in yoga.full)


def test_topic_rows_are_consistent(yoga):
    for r in yoga.topics.itertuples():
        assert len(r.by_session) == yoga.papers
        assert sum(r.by_session) == r.questions
        assert r.papers_asked == sum(n > 0 for n in r.by_session)
        assert r.trend in ("Rising", "Steady", "Fading", "—")


def test_regular_topics_meet_the_bar(yoga):
    regular = trends.regular_topics(yoga)
    assert not regular.empty
    assert (regular["asked_share"] >= trends.REGULAR_SHARE).all()


def test_trend_uses_shares_not_counts():
    # Same share of each paper, papers of different length: steady, not fading.
    assert trends._trend([0.1, 0.1, 0.1, 0.1], 0.01) == "Steady"
    assert trends._trend([0.02, 0.02, 0.10, 0.10], 0.01) == "Rising"
    assert trends._trend([0.10, 0.10, 0.02, 0.02], 0.01) == "Fading"
    assert trends._trend([0.1, 0.2], 0.01) == "—"


def test_empty_bank():
    p = trends.pattern([])
    assert p.papers == 0 and p.units.empty and trends.regular_topics(p).empty
