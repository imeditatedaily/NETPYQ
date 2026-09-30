"""Settings you may want to change."""

from pathlib import Path

# A micro-topic whose accuracy across your attempts is below this goes on
# the "Topics to Revise" list.
REVISION_THRESHOLD = 0.75

# Below this, a topic is shown as weak (red) rather than needs-revision (amber).
WEAK_THRESHOLD = 0.50

# Keep the four built-in PYQ-pattern samples in the bank. Set to False once
# data/questions/ holds enough real papers.
INCLUDE_SAMPLE_QUESTIONS = True

# Every *.json file here is loaded as a list of questions.
QUESTION_DIR = Path(__file__).resolve().parent.parent / "data" / "questions"

# Trend notes per micro-topic, used by questions that leave trend_analysis empty.
TOPIC_FILE = Path(__file__).resolve().parent.parent / "data" / "topics.json"

# The Source Library: PDFs plus sources/catalog.json.
SOURCE_DIR = Path(__file__).resolve().parent.parent / "sources"
