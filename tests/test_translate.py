"""The Hindi/English switch: rules for formulaic text, and translation files."""

import json

import pytest

from pyq import config, translate as tr
from pyq.access import sellable_questions, sellable_subjects
from pyq.bank import load_bank
from pyq.model import parse_question


@pytest.mark.parametrize("text, to, expected", [
    ("केवल A, B, E", "en", "A, B, E only"),
    ("A, B and C only", "hi", "केवल A, B और C"),
    ("A-II, B-IV, C-III, D-I", "hi", "A-II, B-IV, C-III, D-I"),
    ("(a) और (b)", "en", "(a) and (b)"),
    ("(A) सही है, लेकिन (R) गलत है।", "en", "(A) is true but (R) is false"),
    ("Both A and R are true but R is NOT the correct explanation of A", "hi",
     "(A) और (R) दोनों सही हैं, परन्तु (R), (A) की सही व्याख्या नहीं है"),
    ("नीचे दिये गये विकल्पों में से सही उत्तर चुनिए :", "en", "Choose the correct answer from the options given below :"),
    ("सूची - II", "en", "List II"),
    ("Six", "hi", "छः"),
    ("समाधि", "en", None),
])
def test_rules(text, to, expected):
    assert tr.rule(text, to) == expected


def _q(**kw):
    raw = {"id": "T-1", "subject": "yoga", "question_text": "योग क्या है?", "options": ["एक", "दो", "केवल A, B", "चार"],
           "correct_answer": 1, "detailed_explanation": "x", "macro_unit": "Yoga Unit 1: Fundamentals of Yoga",
           "micro_topic": "t", "source": {"type": "official"}, "exam_year": 2024, "exam_cycle": "June"} | kw
    return parse_question(raw)


def test_a_translation_file_with_nulls_and_rules():
    q = _q()
    assert tr.language(q) == tr.HI
    table = {"T-1": {"question_text": "What is yoga?", "options": [None, None, None, None]}}
    out, status = tr.translated(q, tr.EN, table)
    assert status == "translated"
    assert out.question_text == "What is yoga?" and out.options == ("One", "Two", "A, B only", "Four")
    assert out.correct_answer == q.correct_answer and out.id == q.id
    assert tr.translated(q, tr.HI, table) == (q, "original")
    assert tr.translated(q, tr.EN, {})[1] == "missing"


def test_shared_passage_reference():
    a, b = _q(id="T-1", passage="एक गद्यांश"), _q(id="T-2", passage="एक गद्यांश")
    table = {"T-1": {"question_text": "Q1", "passage": "A passage", "options": [None] * 4},
             "T-2": {"question_text": "Q2", "passage": "@T-1", "options": [None] * 4}}
    assert tr.translated(b, tr.EN, table)[0].passage == "A passage"


def test_translation_files_are_well_formed():
    bank = load_bank(config.QUESTION_DIR, True, config.TOPIC_FILE)
    by_id = {q.id: q for q in bank.questions}
    table = tr.load(config.TRANSLATION_DIR)
    for qid, fields in table.items():
        assert qid in by_id, f"{qid} is not a question"
        q = by_id[qid]
        to = tr.EN if tr.language(q) == tr.HI else tr.HI
        out, status = tr.translated(q, to, table)
        assert status == "translated", f"{qid}: incomplete translation ({sorted(tr.needed(q))})"
        assert len(out.options) == len(q.options) and len(out.items) == len(q.items)
        assert len(out.list_i) == len(q.list_i) and len(out.list_ii) == len(q.list_ii)
