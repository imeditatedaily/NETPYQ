"""The knowledge base file: every topic in the bank has key facts, with real sources."""

import json

import pytest

from pyq import config
from pyq.bank import load_bank
from pyq.knowledge import load_knowledge, topic_pattern, topics_by_unit


@pytest.fixture(scope="module")
def bank():
    return load_bank(config.QUESTION_DIR, True, config.TOPIC_FILE)


@pytest.fixture(scope="module")
def kb():
    return load_knowledge(config.KNOWLEDGE_FILE)


def test_file_loads_cleanly(kb):
    assert not kb.problems and len(kb) > 100


def test_every_real_topic_has_facts(bank, kb):
    missing = {(q.subject, q.micro_topic) for q in bank.questions
               if q.source_type != "model" and not kb.note(q.subject, q.micro_topic)}
    assert not missing, sorted(missing)


def test_every_note_names_a_topic_in_the_bank(bank, kb):
    topics = {(q.subject, q.micro_topic) for q in bank.questions}
    stray = [(s, t) for s, d in kb.notes.items() for t in d if (s, t) not in topics]
    assert not stray, stray


def test_sources_are_in_the_catalogue(kb):
    ids = {s["id"] for s in json.loads((config.SOURCE_DIR / "catalog.json").read_text())}
    bad = [(s, t, x) for s, d in kb.notes.items() for t, n in d.items() for x in n.sources if x not in ids]
    assert not bad, bad


def test_pattern_and_units(bank):
    pat = topic_pattern(bank.questions, "yoga", "Bhagavad Gita")
    assert pat.count >= 5 and "asked" in pat.sentence().lower()
    units = topics_by_unit(bank.questions, "yoga")
    assert any("Bhagavad Gita" in ts for ts in units.values())


def test_bad_file_is_reported_not_raised(tmp_path):
    f = tmp_path / "k.json"
    f.write_text("{ nope")
    assert load_knowledge(f).problems


def test_traps_are_loaded_and_checked(tmp_path):
    f = tmp_path / "k.json"
    f.write_text('{"yoga": {"A": {"facts": ["x"], "traps": ["y"]}, "B": {"facts": ["x"], "traps": "nope"}}}')
    kb = load_knowledge(f)
    assert kb.note("yoga", "A").traps == ("y",)
    assert kb.note("yoga", "B").traps == () and kb.problems
