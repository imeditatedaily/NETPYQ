"""End-to-end tests: drive the real app with Streamlit's AppTest (no browser needed)."""

from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

APP = str(Path(__file__).resolve().parent.parent / "streamlit_app.py")


def click(at: AppTest, label: str, page: str | None = None) -> AppTest:
    """Clicks a button. AppTest forgets in-app page switches between runs for
    function-based pages, so pass `page` to stay on the page being tested."""
    for button in at.button:
        if button.label.startswith(label):
            if page:
                at.session_state["goto"] = page
            return button.click().run()
    raise AssertionError(f"no button starting {label!r}; have {[b.label for b in at.button]}")


def answer(at: AppTest, option: int, page: str | None = None) -> AppTest:
    at.radio[0].set_value(option)
    return click(at, "Submit answer", page)


def texts(at: AppTest) -> str:
    return "\n".join(m.value for m in at.markdown)


def captions(at: AppTest) -> str:
    return "\n".join(c.value for c in at.caption)


@pytest.fixture
def app() -> AppTest:
    """The app as it opens: every loaded question, real papers first."""
    app = AppTest.from_file(APP, default_timeout=60).run()
    assert not app.exception, [e.message for e in app.exception]
    return app


@pytest.fixture
def at(app) -> AppTest:
    """Scoped to the four built-in samples, so these flows do not depend on which papers are loaded."""
    app.selectbox(key="f_session").set_value("undated").run()
    assert not app.exception, [e.message for e in app.exception]
    return app


def test_real_paper_question_shows_its_source_answer_check_and_topic_note(app):
    app.selectbox(key="f_session").set_value("2017-January").run()
    md = texts(app)
    assert "Yoga Unit 1: Fundamentals of Yoga" in md and "Etymology and definitions of Yoga" in md
    assert "January 2017 · Paper II · Q1 · Official paper" in captions(app)
    app = answer(app, 3)
    assert app.success[0].value.startswith("**Correct.**")
    assert "published solved-papers key" in captions(app)
    md = texts(app)
    assert "dated question(s)" in md and "Pattern." in md   # counted frequency, then the note from topics.json


def test_passage_and_roman_labels_render_as_in_the_booklet(app):
    app.selectbox(key="f_session").set_value("2017-January").run()
    app.selectbox(key="f_topic").set_value("Shatkarma: practice and benefits").run()
    md = texts(app)
    passage, stem = md.find('"Shatkarmas" include six groups'), md.find("Shatkarma procedure for cleansing")
    assert 0 <= passage < stem   # the shared passage is shown above the question
    app.selectbox(key="f_topic").set_value("Siddha Siddhanta Paddhati").run()
    app.selectbox(key="f_qtype").set_value("statements").run()      # Q10, whose statements are numbered I–IV
    assert "**I.** Surya Chakra" in texts(app) and "**II.** Tālu Chakra" in texts(app)


def test_paper_1_data_table_renders_above_its_question(app):
    app.segmented_control(key="f_subject").set_value("paper1").run()
    app.selectbox(key="f_session").set_value("2016-July").run()
    app.selectbox(key="f_topic").set_value("Data interpretation: tables").run()
    assert not app.exception, [e.message for e in app.exception]
    md = texts(app)
    table, stem = md.find("| **Year** | **Percentage profit (%): A**"), md.find("In which year, the percentage profit")
    assert 0 <= table < stem
    assert "July 2016 · Paper I · Q1 · Official paper" in captions(app)


def test_first_question_shows_syllabus_tags(at):
    assert at.title[0].value == "Practice"
    md = texts(at)
    assert "Yoga Unit 4: Patanjala Yoga Sutra" in md
    assert "Kleshas and their removal" in md
    assert at.radio[0].options[2].startswith("(3)")


def test_submit_reveals_answer_explanation_and_trend_insight(at):
    at = answer(at, 1)  # wrong
    assert "Incorrect" in at.error[0].value and "(3)" in at.error[0].value
    md = texts(at)
    assert "Detailed explanation" in md and "Trend Insight" in md and "Frequency in loaded papers" in md
    assert at.metric[1].value == "0 / 1"  # score for this attempt


def test_full_loop_practice_review_to_100_percent_and_revision_plan(at):
    at = answer(at, 1)                      # Q1 wrong (kleśa)
    at = click(at, "Next question")
    at = answer(at, 2)                      # Q2 right (ṣaṭkarma)
    assert at.success[0].value.startswith("**Correct.**")

    at = click(at, "Review mistakes (1)")
    assert at.title[0].value == "Review Mistakes"
    at = click(at, "Start the review loop (1)", "review")
    at = answer(at, 1, "review")            # still wrong
    at = click(at, "Finish round 1", "review")
    assert at.metric[0].value == "2"        # round 2 holds the missed question
    at = answer(at, 3, "review")            # right this time
    at = click(at, "Finish round 2", "review")
    assert "100%" in at.success[0].value

    at = click(at, "Performance analytics")
    assert at.title[0].value == "Performance Analytics"
    assert any(h.value == "Topics to Revise" for h in at.header)
    md = texts(at)
    assert "Kleshas and their removal" in md          # 1 of 3 correct = 33%, flagged
    assert "1 of 3 correct" in "\n".join(str(p.proto.text) for p in at.get("progress"))


def test_same_quiz_can_be_retaken(at):
    first = int(at.metric[0].value.lstrip("#"))
    at = answer(at, 3)
    at = click(at, "Restart this quiz")
    assert at.metric[0].value == f"#{first + 1}"
    assert at.metric[1].value == "0 / 0"
    assert at.radio[0].value is None


def test_filters_scope_practice(at):
    at.segmented_control(key="f_subject").set_value("iks").run()
    assert "IKS Unit" in texts(at)
    at.selectbox(key="f_unit").set_value("IKS Unit 3: Astronomy").run()
    assert "Aryabhata and the Earth's rotation" in texts(at)
    assert at.metric[3].value == "1 of 1"


@pytest.mark.parametrize("page", ["analytics", "bank", "library", "review"])
def test_every_page_renders_without_errors(at, page):
    at.session_state["goto"] = page
    at = at.run()
    assert not at.exception, [e.message for e in at.exception]
    assert at.title
