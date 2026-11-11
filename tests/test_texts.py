"""The Sanskrit texts: every file loads, refs are unique, sources are real, and the search finds quoted lines."""

import json

import pytest

from pyq import config
from pyq.bank import load_bank
from pyq.texts import deva_key, load_texts, roman_key


@pytest.fixture(scope="module")
def library():
    return load_texts(config.TEXT_DIR)


def test_files_load_cleanly(library):
    assert not library.problems, library.problems[:5]
    assert len(library) >= 30 and library.line_count > 5000


@pytest.mark.parametrize("text_id, count", [("isha-upanishad", 18), ("mandukya-upanishad", 12), ("prashna-upanishad", 67),
                                            ("shvetashvatara-upanishad", 113), ("yoga-sutra", 195), ("bhagavad-gita", 701),
                                            ("narada-bhakti-sutra", 84), ("yogatattva-upanishad", 142), ("samkhya-karika", 73)])
def test_well_known_texts_have_their_full_count(library, text_id, count):
    assert len(library.by_id(text_id).lines) == count


@pytest.mark.parametrize("text_id, ref, part", [
    ("yoga-sutra", "1.2", "योगश्चित्तवृत्तिनिरोधः"),
    ("bhagavad-gita", "2.47", "कर्मण्येवाधिकारस्ते"),
    ("katha-upanishad", "1.3.14", "उत्तिष्ठत जाग्रत"),
    ("mundaka-upanishad", "3.1.6", "सत्यमेव जयते"),
    ("narada-bhakti-sutra", "2", "सा त्वस्मिन् परमप्रेमरूपा"),
    ("hatha-pradipika", "2.2", "चले वाते चलं चित्तं"),
])
def test_famous_lines_sit_at_their_usual_reference(library, text_id, ref, part):
    line = next(ln for ln in library.by_id(text_id).lines if ln.ref == ref)
    assert part in line.sa


def test_search_works_in_both_scripts(library):
    assert any(h.text.id == "yoga-sutra" and h.line.ref == "1.2" for h in library.search("योगश्चित्तवृत्तिनिरोधः"))
    assert any(h.text.id == "yoga-sutra" and h.line.ref == "1.2" for h in library.search("yogash chitta vritti nirodhah"))
    assert any(h.text.id == "chandogya-upanishad" for h in library.search("तत्त्वमसि"))
    assert library.search("सत्यमेव जयते", text_id="mundaka-upanishad")[0].line.ref == "3.1.6"
    assert library.search("zz") == [] and library.search("क्ष्म्ल्व्र्यूं") == []


def test_search_keys_ignore_spacing_and_nasal_spelling():
    assert deva_key("यत् किञ्च जगत्यां जगत् ।") == deva_key("यत्किंच जगत्यां जगत्")
    assert roman_key("kurukshetre") == roman_key("कुरुक्षेत्रे") == roman_key("kurukṣetre")


def test_texts_name_real_topics_units_and_sources(library):
    bank = load_bank(config.QUESTION_DIR, True, config.TOPIC_FILE)
    topics = {(q.subject, q.micro_topic) for q in bank.questions}
    ids = {s["id"] for s in json.loads((config.SOURCE_DIR / "catalog.json").read_text())}
    for t in library.texts:
        assert 1 <= t.unit <= 10 and t.sources, t.id
        assert all((t.subject, topic) in topics for topic in t.topics), (t.id, t.topics)
        assert all(s in ids for s in t.sources), (t.id, t.sources)
        assert all(ln.sa == ln.sa.strip() and "  " not in ln.sa for ln in t.lines), t.id


def test_chapters_follow_the_refs(library):
    gita = library.by_id("bhagavad-gita")
    assert gita.chapters == tuple(str(n) for n in range(1, 19)) and len(gita.chapter("2")) == 72
    assert library.by_id("isha-upanishad").chapters == ()


def test_bad_file_is_reported_not_raised(tmp_path):
    (tmp_path / "a.json").write_text("{ nope")
    (tmp_path / "b.json").write_text('{"id": "b", "title": "B", "title_sa": "ब", "subject": "yoga", "unit": 1, '
                                     '"lines": [{"ref": "1", "sa": "अ"}, {"ref": "1", "sa": "आ"}, {"ref": "2"}]}')
    lib = load_texts(tmp_path)
    assert len(lib) == 1 and len(lib.texts[0].lines) == 1 and len(lib.problems) == 3
