"""Study notes: every chapter loads, names real topics and catalogued sources, and has sections."""

import json

from pyq import config
from pyq.bank import load_bank
from pyq.notes import load_notes


def test_notes_load_cleanly_and_point_at_real_topics_and_sources():
    lib = load_notes(config.NOTES_DIR)
    assert not lib.problems, lib.problems
    assert len(lib) >= 1
    bank = load_bank(config.QUESTION_DIR, True, config.TOPIC_FILE)
    topics = {(q.subject, q.micro_topic) for q in bank.questions}
    ids = {s["id"] for s in json.loads((config.SOURCE_DIR / "catalog.json").read_text())}
    for n in lib.notes:
        assert n.topics and all((n.subject, t) in topics for t in n.topics), (n.id, n.topics)
        assert n.sources and all(s in ids for s in n.sources), (n.id, n.sources)
        assert len(n.sections) >= 3 and n.words > 300, n.id
        assert n.preview() and len(n.preview()) < len(n.body), n.id


def test_header_problems_are_reported_not_raised(tmp_path):
    (tmp_path / "a.md").write_text("no header")
    (tmp_path / "b.md").write_text("---\ntitle: B\nsubject: yoga\nunit: x\n---\nbody")
    (tmp_path / "c.md").write_text("---\ntitle: C\nsubject: yoga\nunit: 1\ntopics: A | B, C\n---\n# C\n## one\n## two\n")
    lib = load_notes(tmp_path)
    assert len(lib) == 1 and lib.notes[0].topics == ("A", "B, C") and lib.notes[0].sections == ("one", "two")
    assert len(lib.problems) == 2


def test_pyq_markers_become_badges_and_link_questions_to_sections(tmp_path):
    from pyq.notes import expand_markers, load_notes, marked_ids
    (tmp_path / "n.md").write_text(
        "---\ntitle: T\nsubject: yoga\nunit: 6\n---\n# T\n\n## Sleep\n\nFour stages. [[PYQ: A1, B2]]\n\n"
        "## Memory\n\nSeven plus or minus two. [[PYQ:C3]] [[LIKELY]]\n", encoding="utf-8")
    lib = load_notes(tmp_path)
    assert marked_ids(lib.notes[0].body) == ["A1", "B2", "C3"]
    assert [(n.id, h) for n, h in lib.sections_for("B2")] == [("n", "Sleep")]
    assert "Seven plus" in lib.section("n", "Memory")
    out = expand_markers(lib.notes[0].body, {"A1": "Jun 2019 Q4", "C3": "Dec 2023 Q9"}.get)
    assert "PYQ Jun 2019 Q4]" in out and "B2" not in out and "Likely next" in out and "[[" not in out


def test_shipped_note_markers_name_real_questions():
    from pyq.notes import marked_ids
    bank = load_bank(config.QUESTION_DIR, False, config.TOPIC_FILE)
    for n in load_notes(config.NOTES_DIR).notes:
        for qid in marked_ids(n.body):
            assert qid in bank and bank[qid].is_dated, f"{n.id}: {qid} is not a past question"


def test_every_unit6_past_question_is_marked_in_the_notes():
    """The Unit 6 chapters mark every dated Unit 6 question once, so each one links to the part it was asked from."""
    from pyq.notes import marked_ids
    bank = load_bank(config.QUESTION_DIR, False, config.TOPIC_FILE)
    lib = load_notes(config.NOTES_DIR)
    marked = [qid for n in lib.notes if n.unit == 6 for qid in marked_ids(n.body)]
    assert len(marked) == len(set(marked))
    u6 = {q.id for q in bank.questions if q.is_dated and q.macro_unit.startswith("Yoga Unit 6")}
    assert u6 and u6 <= set(marked), sorted(u6 - set(marked))[:10]
