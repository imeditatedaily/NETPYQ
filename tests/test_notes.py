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
