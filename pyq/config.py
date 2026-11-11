"""Settings you may want to change."""

import os
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

# The other language of each question (see pyq/translate.py).
TRANSLATION_DIR = Path(__file__).resolve().parent.parent / "data" / "translations"

# Knowledge base: key facts per micro-topic, shown after every answer.
KNOWLEDGE_FILE = Path(__file__).resolve().parent.parent / "data" / "knowledge.json"

# Sanskrit source texts, line by line (see pyq/texts.py).
TEXT_DIR = Path(__file__).resolve().parent.parent / "data" / "texts"

# The Source Library: PDFs plus sources/catalog.json.
SOURCE_DIR = Path(__file__).resolve().parent.parent / "sources"

# --- accounts and subscriptions ------------------------------------------------------

# Real papers anyone who signs in may practise for free: (subject, exam_year, exam_cycle).
FREE_PAPERS = (("yoga", 2018, "December"), ("yoga", 2018, "July"))

# Monthly price of one subject (Paper 1, Yoga or IKS), in rupees. The amount
# actually charged is set on the Razorpay plan; keep the two the same.
SUBJECT_PRICE_INR = 500

# One-time exam passes, paid once on a Razorpay payment link. Each gives these
# subjects for PASS_DAYS from the day of payment, and never renews.
#   key: (name, price in rupees, subjects)
PASSES = {
    "yoga": ("Yoga exam pass", 999, ("yoga",)),
    "paper1": ("Paper 1 exam pass", 999, ("paper1",)),
    "iks": ("IKS exam pass", 999, ("iks",)),
    "combo": ("Paper 1 + Yoga exam pass", 1499, ("paper1", "yoga")),
}
PASS_DAYS = 182          # about six months: one NET cycle

# Questions whose source note mentions any of these are transcribed from a
# published book. They are not part of any paid plan and do not count towards
# making a subject available for sale; only those in a FREE_PAPERS paper are shown.
BOOK_SOURCE_MARKERS = ("Madaan", "solved-papers collection")

# Where progress is kept when no [database] url is set (local development only).
LOCAL_DB_FILE = Path(__file__).resolve().parent.parent / ".data" / "netpyq.db"


# The page "/" opens on: the Home dashboard. Tests set NETPYQ_START_PAGE=practice so they open on Practice.
START_PAGE = os.environ.get("NETPYQ_START_PAGE", "home")
