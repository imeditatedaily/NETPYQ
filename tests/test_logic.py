"""Tests for the plain-Python layer: data checks, filters, tracking, analytics, library."""

import json
import random
from datetime import datetime, timedelta

import pytest

from pyq import analytics as an
from pyq.bank import build_bank, load_bank
from pyq.config import QUESTION_DIR, SOURCE_DIR
from pyq.data.samples import SAMPLE_QUESTIONS
from pyq.filters import ALL, Filters, apply, session_choices, topic_choices, unit_choices
from pyq.library import load_library
from pyq.model import QuestionError, parse_question
from pyq.syllabus import IKS, YOGA
from pyq.tracker import (answers_from_dicts, make_answer, new_run, outstanding_mistakes, start_review)

T0 = datetime(2026, 9, 29, 10, 0, 0)


def dated(qid, year, cycle, **overrides):
    raw = {
        "id": qid, "subject": "yoga", "exam_year": year, "exam_cycle": cycle,
        "question_text": "Q?", "options": ["a", "b", "c", "d"], "correct_answer": 1,
        "detailed_explanation": "x", "macro_unit": "Yoga Unit 4: Patanjala Yoga Sutra",
        "micro_topic": "Kleshas and their removal", "trend_analysis": "y",
    }
    raw.update(overrides)
    return raw


def bank_of(*raws):
    return build_bank([(r, "test") for r in raws])


# --- data -------------------------------------------------------------------------------

def test_samples_all_pass_and_cover_four_formats():
    bank = load_bank(QUESTION_DIR, include_samples=True)
    assert bank.problems == ()
    assert len(bank) == 4
    assert {q.question_type for q in bank.questions} == {"match", "sequence", "statements", "assertion_reason"}
    for q in bank.questions:
        assert q.source_type == "model" and not q.is_dated
        assert q.macro_unit and q.micro_topic and q.trend_analysis and q.detailed_explanation


def test_unit_labels_match_the_requested_pattern():
    assert YOGA.unit_label(4) == "Yoga Unit 4: Patanjala Yoga Sutra"
    assert IKS.unit_label(3) == "IKS Unit 3: Astronomy"


@pytest.mark.parametrize(("overrides", "message"), [
    ({"correct_answer": 5}, "correct_answer"),
    ({"correct_answer": True}, "correct_answer"),
    ({"macro_unit": "Yoga Unit 11: Nope"}, "not a syllabus unit"),
    ({"macro_unit": "IKS Unit 3: Astronomy"}, "belongs to Indian Knowledge System"),
    ({"exam_cycle": "Jan"}, "June"),
    ({"source": {"type": "model"}}, "cannot have an exam_year"),
    ({"question_type": "match"}, "list_i"),
    ({"question_type": "assertion_reason"}, "assertion"),
    ({"trend_analysis": " "}, "trend_analysis"),
])
def test_bad_questions_are_rejected_with_a_reason(overrides, message):
    with pytest.raises(QuestionError, match=message):
        parse_question(dated("X", 2025, "June", **overrides))


def test_undated_official_question_is_rejected():
    with pytest.raises(QuestionError, match="needs exam_year"):
        parse_question(dated("X", None, None, source={"type": "official"}))


def test_bank_skips_bad_and_duplicate_questions_but_keeps_the_rest():
    bank = bank_of(dated("A", 2025, "June"), dated("A", 2024, "June"), dated("B", 2025, "June", options=["only"]))
    assert [q.id for q in bank.questions] == ["A"]
    assert {p.question_id for p in bank.problems} == {"A", "B"}


def test_json_files_in_the_question_folder_are_loaded(tmp_path):
    (tmp_path / "yoga-2025.json").write_text(json.dumps([dated("Y25", 2025, "June")]), encoding="utf-8")
    (tmp_path / "broken.json").write_text("[{", encoding="utf-8")
    bank = load_bank(tmp_path, include_samples=False)
    assert [q.id for q in bank.questions] == ["Y25"]
    assert bank.problems[0].origin == "broken.json"


# --- filters ----------------------------------------------------------------------------

def test_filters_and_choices():
    bank = bank_of(
        dated("Y1", 2025, "June"),
        dated("Y2", 2024, "December", macro_unit="Yoga Unit 5: Hatha Yoga Texts", micro_topic="Shatkarma"),
        dated("I1", 2025, "December", subject="iks", macro_unit="IKS Unit 6: Mathematics", micro_topic="Kerala School",
              question_type="statements", items=["p", "q"]),
    )
    ids = lambda **f: [q.id for q in apply(bank.questions, Filters(**f))]
    assert ids(subject="iks") == ["I1"]
    assert sorted(ids(session="2025")) == ["I1", "Y1"]
    assert ids(session="2024-December") == ["Y2"]
    assert ids(unit="Yoga Unit 5: Hatha Yoga Texts") == ["Y2"]
    assert ids(topic="Kleshas and their removal") == ["Y1"]
    assert ids(qtype="statements") == ["I1"]

    sessions = session_choices(bank.questions)
    assert list(sessions)[:4] == [ALL, "2025", "2025-December", "2025-June"]
    assert len(unit_choices(bank.questions, "yoga")) == 11  # "all" + 10 units, empty ones included
    assert list(topic_choices(bank.questions, "yoga", ALL))[1:] == ["Kleshas and their removal", "Shatkarma"]


# --- tracking ---------------------------------------------------------------------------

def test_practice_run_scores_and_restarts_on_the_same_deck():
    bank = load_bank(QUESTION_DIR)
    ids = [q.id for q in bank.questions]
    run = new_run(1, ids, Filters(), shuffle=False)
    run.submit(ids[0], bank[ids[0]].correct_answer)
    run.advance()
    run.submit(ids[1], 99)
    score = run.score(bank.by_id)
    assert (score.correct, score.answered, score.total, score.accuracy) == (1, 2, 4, 0.5)
    again = new_run(2, run.deck, run.filters, shuffle=True, rng=random.Random(1))
    assert sorted(again.deck) == sorted(run.deck) and again.answers == {}


def test_outstanding_mistakes_follow_the_latest_answer():
    bank = load_bank(QUESTION_DIR)
    a, b = bank.questions[0], bank.questions[1]
    log = [
        make_answer(a, 9, "practice", 1, T0),
        make_answer(b, 9, "practice", 1, T0 + timedelta(seconds=1)),
        make_answer(a, a.correct_answer, "review", 1, T0 + timedelta(seconds=2)),
    ]
    assert outstanding_mistakes(log) == [b.id]
    log.append(make_answer(a, 9, "practice", 2, T0 + timedelta(seconds=3)))
    assert outstanding_mistakes(log) == [b.id, a.id]


def test_review_loop_repeats_misses_until_a_round_is_100_percent():
    loop = start_review(1, ["a", "b", "c"], rng=random.Random(0))
    seen_round_1 = []
    while loop.round == 1:
        qid = loop.current_id
        seen_round_1.append(qid)
        loop.submit(qid, 1, correct=(qid != "b"))
        loop.advance(rng=random.Random(0))
    assert sorted(seen_round_1) == ["a", "b", "c"]
    assert loop.results[0].accuracy == pytest.approx(2 / 3)
    assert loop.queue == ["b"] and not loop.done

    loop.submit("b", 1, correct=False)          # missed again: round 3 needed
    loop.advance()
    assert loop.round == 3 and loop.queue == ["b"]
    loop.submit("b", 1, correct=True)
    loop.advance()
    assert loop.done
    assert [(r.round, r.correct, r.total) for r in loop.results] == [(1, 2, 3), (2, 0, 1), (3, 1, 1)]
    assert loop.results[-1].accuracy == 1.0


def test_empty_review_is_done_at_once():
    assert start_review(1, []).done


def test_log_round_trips_through_json():
    bank = load_bank(QUESTION_DIR)
    log = [make_answer(q, 1, "practice", 1, T0) for q in bank.questions]
    restored = answers_from_dicts(json.loads(json.dumps([a.to_dict() for a in log])))
    assert restored == log
    with pytest.raises(ValueError):
        answers_from_dicts([{"question_id": "x"}])
    with pytest.raises(ValueError):
        answers_from_dicts({"not": "a list"})


# --- analytics --------------------------------------------------------------------------

def test_accuracy_bands_and_revision_list():
    bank = load_bank(QUESTION_DIR)
    by_topic = {q.micro_topic: q for q in bank.questions}
    klesha, shat = by_topic["Kleshas and their removal"], by_topic["Shatkarma in Hatha Pradipika and Gheranda Samhita"]
    log = (
        [make_answer(klesha, klesha.correct_answer, "practice", 1, T0)] + [make_answer(klesha, 9, "practice", 1, T0)] * 2
        + [make_answer(shat, shat.correct_answer, "practice", 1, T0)] * 3 + [make_answer(shat, 9, "practice", 1, T0)]
    )
    df = an.log_frame(log)
    topics = an.accuracy_table(df, ["macro_unit", "micro_topic"]).set_index("micro_topic")
    assert topics.loc[klesha.micro_topic, "accuracy"] == pytest.approx(1 / 3)
    assert topics.loc[klesha.micro_topic, "band"] == an.WEAK
    assert topics.loc[shat.micro_topic, "band"] == an.STRONG      # exactly 75% is not flagged
    revise = an.revision_list(df)
    assert revise["micro_topic"].tolist() == [klesha.micro_topic]
    assert an.band(0.6) == an.REVISE


def test_topic_frequency_counts_only_dated_papers():
    bank = bank_of(
        dated("A", 2023, "June"), dated("B", 2025, "June"), dated("C", 2025, "June", micro_topic="Other"),
        dated("D", 2024, "June", macro_unit="Yoga Unit 5: Hatha Yoga Texts", micro_topic="Shatkarma"),
        dated("M", None, None),
    )
    f = an.topic_frequency(bank.questions, bank["A"])
    assert (f.topic_dated, f.unit_dated, f.subject_dated, f.sessions_loaded) == (2, 3, 4, 3)
    assert f.topic_sessions == ("June 2023", "June 2025")
    assert "2 dated question(s)" in f.sentence("Yoga")
    none = an.topic_frequency(load_bank(QUESTION_DIR).questions, load_bank(QUESTION_DIR).questions[0])
    assert "No dated Yoga papers" in none.sentence("Yoga")


# --- library ----------------------------------------------------------------------------

def test_shipped_library_catalog_is_clean_and_links_resolve():
    library = load_library(SOURCE_DIR)
    assert library.problems == ()
    assert sum(s.available for s in library.sources) == 3
    for raw in SAMPLE_QUESTIONS:
        for sid in raw["source_ids"]:
            assert sid in library.by_id, sid


def test_uncatalogued_pdf_still_appears(tmp_path):
    (tmp_path / "catalog.json").write_text("[]", encoding="utf-8")
    (tmp_path / "my-notes.pdf").write_bytes(b"%PDF-1.4")
    library = load_library(tmp_path)
    assert [s.id for s in library.sources] == ["my-notes"]
    assert library.sources[0].available
