"""Tests for the plain-Python layer: data checks, filters, tracking, analytics, library."""

import json
import random
from datetime import datetime, timedelta

import pytest

from pyq import analytics as an
from pyq.bank import build_bank, load_bank, read_topic_notes
from pyq.config import QUESTION_DIR, SOURCE_DIR, TOPIC_FILE
from pyq.data.samples import SAMPLE_QUESTIONS
from pyq.filters import ALL, Filters, apply, session_choices, topic_choices, unit_choices
from pyq.library import load_library
from pyq.model import QuestionError, parse_question
from pyq.syllabus import IKS, PAPER1, SUBJECTS, UNIT_INDEX, YOGA
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


def bank_of(*raws, notes=None):
    return build_bank([(r, "test") for r in raws], topic_notes=notes)


def samples_bank():
    """The four built-in samples alone, whatever papers are in data/questions."""
    return build_bank([(q, "samples") for q in SAMPLE_QUESTIONS])


def shipped_bank():
    return load_bank(QUESTION_DIR, include_samples=True, topic_file=TOPIC_FILE)


# --- data -------------------------------------------------------------------------------

def test_samples_all_pass_and_cover_four_formats():
    bank = samples_bank()
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
    ({"answer_source": "my_guess"}, "answer_source"),
    ({"question_no": 0}, "question_no"),
    ({"paper": 2}, "paper"),
    ({"question_type": "statements", "items": ["p", "q"], "item_style": "greek"}, "item_style"),
    ({"question_type": "match", "lists": {"list_i": {"items": ["a"], "style": "x"}, "list_ii": {"items": ["b"]}}},
     "style"),
])
def test_bad_questions_are_rejected_with_a_reason(overrides, message):
    with pytest.raises(QuestionError, match=message):
        parse_question(dated("X", 2025, "June", **overrides))


def test_shipped_papers_load_cleanly_with_answers_notes_and_sources():
    bank = shipped_bank()
    assert bank.problems == ()
    papers = [q for q in bank.questions if q.is_dated]
    jan17 = sorted((q for q in papers if q.session_key == "2017-January" and q.subject == "yoga"),
                   key=lambda q: q.question_no)
    assert [q.question_no for q in jan17] == list(range(1, 51))
    assert {q.paper for q in jan17} == {"Paper II"}
    library = load_library(SOURCE_DIR)
    notes, problems = read_topic_notes(TOPIC_FILE)
    assert problems == []
    for q in papers:
        assert q.source_type == "official" and q.answer_source in ("official_key", "cross_checked", "unverified")
        assert q.trend_analysis == notes[q.subject][q.micro_topic]   # filled from data/topics.json
        assert q.detailed_explanation.startswith(f"**Answer: ({q.correct_answer})")
        assert all(sid in library.by_id for sid in q.source_ids), q.id
    assert jan17[0].source_label == "January 2017 · Paper II · Q1 · Official paper"
    jun24 = [q for q in papers if q.session_key == "2024-June"]
    assert sorted(q.question_no for q in jun24) == list(range(51, 151))   # Paper 2 of a combined booklet
    assert {q.answer_source for q in jun24} == {"unverified"}              # no key was published for this paper


def test_shipped_paper_1_sessions_keep_their_numbering():
    by_paper = {}
    for q in shipped_bank().questions:
        if q.subject == "paper1":
            by_paper.setdefault((q.session_key, q.paper), []).append(q.question_no)
    assert {k: sorted(v) for k, v in by_paper.items()} == {
        ("2016-July", "Paper I"): list(range(1, 61)),
        ("2017-January", "Paper I"): list(range(1, 61)),
        ("2017-November", "Paper I"): [n for n in range(1, 51) if n != 35],       # cancelled in the official key
        ("2018-July", "Paper I"): list(range(1, 51)),
        ("2018-December", "Paper 1 (set A)"): list(range(1, 51)),
        ("2018-December", "Paper 1 (set B)"): [n for n in range(1, 51) if n != 45],  # flawed item left out
    }


def test_questions_without_trend_analysis_take_the_topic_note():
    note = {"yoga": {"Kleshas and their removal": "Note from topics.json"}}
    bank = bank_of(dated("A", 2025, "June", trend_analysis=""), dated("B", 2025, "June", trend_analysis="Own note"),
                   dated("C", 2025, "June", trend_analysis="", micro_topic="Unknown topic"), notes=note)
    assert [q.trend_analysis for q in bank.questions] == ["Note from topics.json", "Own note"]
    assert bank.problems[0].question_id == "C" and "topics.json" in bank.problems[0].errors[0]


def test_topic_file_problems_are_reported(tmp_path):
    bad = tmp_path / "topics.json"
    bad.write_text('["not", "a", "mapping"]', encoding="utf-8")
    notes, problems = read_topic_notes(bad)
    assert notes == {} and "must look like" in problems[0].errors[0]
    bad.write_text("{", encoding="utf-8")
    assert "not valid JSON" in read_topic_notes(bad)[1][0].errors[0]
    assert read_topic_notes(tmp_path / "missing.json") == ({}, [])


def test_sessions_are_months_in_calendar_order():
    bank = bank_of(dated("J", 2017, "January"), dated("N", 2017, "November"), dated("Y", 2018, "July"),
                   dated("D", 2019, "December", paper="Paper 2", question_no=7, answer_source="official_key",
                         passage="Read me", question_type="statements", items=["p", "q"], item_style="roman"))
    order = sorted(bank.questions, key=lambda q: q.session_order)
    assert [q.id for q in order] == ["J", "N", "Y", "D"]
    assert list(session_choices(bank.questions))[-3:] == ["2017", "2017-November", "2017-January"]
    d = bank["D"]
    assert (d.paper, d.question_no, d.answer_source, d.passage, d.item_style) == (
        "Paper 2", 7, "official_key", "Read me", "roman")
    assert d.source_label == "December 2019 · Paper 2 · Q7 · Official paper"
    assert bank["J"].list_styles == ("letters", "roman")


def test_data_table_is_read_and_checked():
    table = {"title": "Sales (in lakh)", "columns": ["Year", "A", "B"], "rows": [["2012", "40", ""], ["2013", "35", "50"]]}
    q = parse_question(dated("T", 2016, "July", table=table))
    assert (q.table_title, q.table_columns) == ("Sales (in lakh)", ("Year", "A", "B"))
    assert q.table_rows == (("2012", "40", ""), ("2013", "35", "50"))
    with pytest.raises(QuestionError, match="one per column"):
        parse_question(dated("T", 2016, "July", table={"columns": ["Year", "A"], "rows": [["2012"]]}))
    with pytest.raises(QuestionError, match='needs "columns"'):
        parse_question(dated("T", 2016, "July", table={"rows": [["2012"]]}))


def test_paper_1_is_a_third_subject_with_its_ten_units():
    assert list(SUBJECTS) == ["yoga", "iks", "paper1"]
    assert PAPER1.unit_label(7) == "Paper 1 Unit 7: Data Interpretation"
    assert UNIT_INDEX["Paper 1 Unit 10: Higher Education System"] == (PAPER1, 10)
    q = parse_question(dated("P", 2018, "July", subject="paper1", macro_unit=PAPER1.unit_label(1),
                             micro_topic="Teaching methods"))
    assert q.subject_info.display == "General Paper on Teaching and Research Aptitude (Paper 1)"
    with pytest.raises(QuestionError, match="belongs to"):
        parse_question(dated("P", 2018, "July", subject="yoga", macro_unit=PAPER1.unit_label(1)))


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
    bank = samples_bank()
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
    bank = shipped_bank()
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
    bank = shipped_bank()
    log = [make_answer(q, 1, "practice", 1, T0) for q in bank.questions]
    restored = answers_from_dicts(json.loads(json.dumps([a.to_dict() for a in log])))
    assert restored == log
    with pytest.raises(ValueError):
        answers_from_dicts([{"question_id": "x"}])
    with pytest.raises(ValueError):
        answers_from_dicts({"not": "a list"})


# --- analytics --------------------------------------------------------------------------

def test_accuracy_bands_and_revision_list():
    bank = samples_bank()
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
    samples = samples_bank().questions
    assert "No dated Yoga papers" in an.topic_frequency(samples, samples[0]).sentence("Yoga")


# --- library ----------------------------------------------------------------------------

def test_shipped_library_catalog_is_clean_and_links_resolve():
    library = load_library(SOURCE_DIR)
    assert library.problems == ()
    assert sum(s.available for s in library.sources) == 5   # incl. the Yoga and Paper 1 syllabi
    for raw in SAMPLE_QUESTIONS:
        for sid in raw["source_ids"]:
            assert sid in library.by_id, sid


def test_uncatalogued_pdf_still_appears(tmp_path):
    (tmp_path / "catalog.json").write_text("[]", encoding="utf-8")
    (tmp_path / "my-notes.pdf").write_bytes(b"%PDF-1.4")
    library = load_library(tmp_path)
    assert [s.id for s in library.sources] == ["my-notes"]
    assert library.sources[0].available
