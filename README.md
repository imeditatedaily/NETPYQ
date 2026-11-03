# UGC NET PYQ Analytical Dashboard: Paper 1, Yoga (100) and Indian Knowledge System (103)

A Streamlit app for UGC NET practice (the General Paper, Paper 1, and Paper 2 for Yoga and IKS), built for Python 3.14 and Streamlit Community Cloud.

| Page | What it does |
|---|---|
| **Practice** | Syllabus-mapped questions with the macro unit and micro-topic above each one. On submit: the correct answer, a detailed explanation, a highlighted **Trend Insight** box and links to study sources. Take the same quiz as many times as you like. |
| **Review Mistakes** | Only the questions whose latest answer was wrong. Each round asks them once; anything missed comes back next round, reshuffled, until a round is **100%** correct. |
| **Performance Analytics** | Real-time score and accuracy for the current attempt and the whole session; accuracy by syllabus unit and micro-topic, colour-coded (🟢 ≥75%, 🟠 50–74%, 🔴 <50%); and a **Topics to Revise** list of every micro-topic below 75%, each with a *Practise* button. |
| **Question Bank** | Coverage by unit and exam session, plus the data check. |
| **Source Library** | Study texts mapped to syllabus units: your PDFs (readable in the app) and recommended public-domain translations still to add. |

Every answer, in Practice or Review, is logged with its question, macro unit, micro-topic, chosen option and result, and saved to the user's account. The sidebar filters by subject, exam year or session, syllabus unit, micro-topic and question format.

## About the data

**Real papers.** `data/questions/` holds official papers as they were printed, one JSON file per paper. It currently holds:

| Paper | Questions | Answers |
|---|---|---|
| UGC NET (CBSE) January 2017, Yoga Paper II (booklet JA-100-17, English version) | 50 | Worked out from the primary texts and matched against a published solved-papers key. All 50 now match it (Q43 and Q44 were confirmed against the collection's Hindi edition). |
| UGC NET (CBSE) January 2017, Yoga **Paper III** (booklet JA-100-17, English version) | 72 | From the **official question booklet** on ugcnetonline.in. No official key was available, so answers are worked out from the primary texts and marked *unverified*; less certain ones say *provisional*. Q27, Q52 and Q65 are left out (reasons in the source note). |
| UGC NET (CBSE) November 2017, Yoga Paper II, **Hindi** | 48 | From a published solved-papers collection (admins only). Answers worked out from the texts and checked against its key. Q11, Q13, Q30 and Q43 were filled from the **official booklet** (ugcnetonline.in) with its printed Hindi and are *unverified*; Q6 and Q27 are left out. |
| UGC NET (CBSE) November 2017, Yoga **Paper III** (booklet N-10017, English version) | 72 | From the **official question booklet** on ugcnetonline.in, with the reading passage. Answers worked out from the primary texts and marked *unverified*. Q23, Q30 and Q52 are left out (reasons in the source note). |
| UGC NET (CBSE) July 2018, Yoga Paper II, **Hindi** | 95 | From the same collection (admins only), checked against the **official booklet** (ugcnetonline.in): it fixed the numbering of six items and supplied eight missing ones with its printed Hindi (*unverified*). Five disputed or flawed items are left out (Q21, Q22, Q33, Q50, Q65). |
| UGC NET (NTA) December 2018, Yoga Paper 2, **Hindi** | 80 | From the same collection (admins only), with both reading passages. Q12 and Q26 were cancelled by NTA; eighteen garbled or unsettled items left out. |
| UGC NET June 2019, Yoga Paper 2, **Hindi** | 93 | The original NTA response sheet, question numbers as printed, both passages kept. 64 answers match the published solved-papers key (*cross-checked*); the rest are worked out and *unverified*. Seven items are left out: three are flawed (Q48, Q77, Q95) and four could not be settled (Q49, Q68, Q73, Q89). |
| UGC NET December 2019, Yoga Paper 2, **Hindi** | 97 | The original NTA response sheet (10 Dec 2019), question numbers as printed, both passages kept. 21 answers match the published solved-papers key and are marked *cross-checked*; the rest are worked out and *unverified*. Q17, Q77 and Q79 are left out (answer could not be established). |
| UGC NET June 2021 cycle (merged with December 2020; held Nov 2021 – Jan 2022), Yoga Paper 2, **Hindi** | 72 | Kept in Hindi as printed. Read from a text extraction of the scan, which has no question numbers, so the questions keep their source order. Answers worked out from the texts and marked *unverified*. Three items are left out (a Paper 1 item, an incomplete one, and one whose options are all historically wrong). |
| UGC NET December 2022 cycle (21 Feb 2023, second shift), Yoga Paper 2 | 100 | A printed NTA response sheet ("2023 old paper yoga.pdf"), Sl. No. 1–100, English version. No key was available, so answers are worked out from the texts and marked *unverified*. |
| UGC NET June 2023 (21 June 2023), Yoga Paper 2 | 100 | A printout of the NTA response sheet, Part B 1–100, English version. Answers worked out from the texts and marked *unverified*. |
| UGC NET December 2023, Yoga Paper 2, Yoga Sūtra questions only | 15 | From a coaching handout that reproduces them with their NTA question IDs; answers checked against the sūtras (*cross-checked*). |
| UGC NET June 2024, Yoga Paper 2, Q51–150 (booklet series Y, English version) | 100 | Worked out from the primary texts. No official key was published: this is the pen-and-paper exam of 18 June 2024 that NTA cancelled, so every answer is marked *unverified*, and explanations say where an answer is provisional or the item is flawed. The session is inferred from the printed combined booklet. |
| UGC NET June 2024 re-exam (4 Sep 2024, second shift), Yoga Paper 2, Q51–150, **Hindi** | 89 | The NTA response sheet, question numbers as printed, both passages kept, NTA question IDs kept for matching against the key later. No key was available, so answers are worked out from the texts and marked *unverified*; less certain ones say *provisional*. Eleven items are left out because the item is flawed or its answer could not be settled (Q54, 56, 75, 95, 103, 120, 124, 131, 136, 137, 148); the reasons are in the paper's source note. |
| UGC NET June 2025 (27 June, second shift), Yoga Paper 2, Q51–150 | 100 | The official NTA response sheet, question numbers as printed, Hindi or English as on the sheet. Every answer follows **NTA's final answer key** (matched by question ID); where the key accepts two options the explanation says so. |

**Paper 1** (General Paper on Teaching and Research Aptitude), from the solved papers in K. V. S. Madaan's *NTA UGC NET/SET/JRF Paper 1* (Pearson, 3rd ed., 2019) in your shared Drive folder "My book's". Question numbers follow the book. Every answer was worked out independently and checked against the book's key; they are marked *cross-checked* except where noted.

| Paper | Questions | Notes |
|---|---|---|
| UGC NET (CBSE) July 2016, Paper I | 60 | All 60 match the key. |
| UGC NET (CBSE) January 2017, Paper I | 60 | All 60 match the key. A few typesetting slips in the book (a series term, garbled option or item wording) are corrected and flagged in the explanations. |
| UGC NET (CBSE) November 2017, Paper I | 49 | Q35 left out: the official key cancelled it (no option was correct). |
| UGC NET (CBSE) July 2018, Paper I | 50 | All 50 match the key. |
| UGC NET (NTA) December 2018, Paper 1, set A | 50 | Q41 (a current-affairs item) is *unverified*. |
| UGC NET (NTA) December 2018, Paper 1, set B | 49 | A second December 2018 shift. Q45 left out as flawed; in Q29 the book's key accepts an invalid conclusion, so the valid option is used and marked *unverified*. |
| UGC NET December 2022 cycle, Paper 1 (21 Feb 2023, second shift) | 50 | From the same NTA response sheet as the Yoga paper (Sl. No. 101–150, numbered 1–50 here). Answers worked out and marked *unverified*. |
| UGC NET June 2023, Paper 1 (21 June 2023) | 50 | From the same NTA response sheet as the Yoga paper, Part A 1–50. Answers worked out and marked *unverified*. |
| UGC NET (NTA) June 2025, Paper 1 (27 June, second shift) | 49 | From the **official NTA response sheet**, with answers from **NTA's final answer key**; Q8 was dropped by NTA. Unlike the book papers above, subscribers see these. |

Paper 1 data-interpretation tables are stored as real tables (the `table` field) and shown above their questions. Paper 1s from 2019 to 2021 and 2024 are not in your Drive yet. Add the PDFs there, or allow this project's network access to ugcnet.nta.ac.in, and they can go in the same way.

Each question keeps the booklet's wording, numbering and labels (List I in Roman numerals where the paper uses them, and shared reading passages). Each is mapped to a syllabus unit and micro-topic, and has its own detailed explanation. The explanations are written for this app; none are copied from a guidebook. The feedback shows how the answer was checked: *official key*, *cross-checked* or *unverified*.

**Samples.** The app also ships **4 sample questions** (2 Yoga, 2 IKS; one each of the Match-the-List, Sequence, Multiple-statement and Assertion–Reason formats) in `pyq/data/samples.py`. They are **PYQ-pattern model questions**, written to NTA's formats and checked against the primary texts. They are **not copied from a specific paper**, carry no exam year, and appear under *Undated / PYQ-pattern* in the session filter.

**Trend analysis.** The Trend Insight box has two parts.

- **The frequency line is counted, not written.** It comes from the dated papers loaded, counted per subject. For Yoga these are currently January 2017 (Papers II and III), November 2017 (Papers II and III), July 2018, December 2018, June 2019, December 2019, June 2021, December 2022, June 2023, December 2023 (partial), June 2024 (the cancelled paper and the September re-exam) and June 2025; for Paper 1, July 2016 to December 2018, December 2022, June 2023 and June 2025.
- **The note is written.** It comes from `data/topics.json`: one note per micro-topic on how it is framed, what the examiner targets, the usual traps and a prep move. It makes no claims like "asked 7 times since 2019".

As more papers go in, the following update automatically:

- the "Frequency in loaded papers" line in every Trend Insight box
- the year filter
- the unit × session grid

See [`data/questions/README.md`](data/questions/README.md) for the format.

The syllabus unit titles in `pyq/syllabus.py` follow NTA's published syllabi via exam portals. Check them against the official PDFs at ugcnet.nta.ac.in.

## Knowledge Base

`data/knowledge.json` holds key facts for every micro-topic in the loaded papers (154 topics), each with the Source Library texts it comes from. After every answer, right or wrong, the question view shows a **Knowledge Base** box: the topic's key facts, how the topic has been asked (how often, in which sessions, in which formats) and the earlier questions on it with their answers. The **Knowledge Base** page lists the same by syllabus unit, with a button to practise each topic. `tests/test_knowledge.py` fails if a topic in the bank has no facts, or if a fact cites a source that isn't in `sources/catalog.json`.

## Accounts, saved progress and subscriptions

Users sign in with Google. Every answer is saved to their account (PostgreSQL, for example Supabase), so progress follows them across refreshes and devices. Each subject unlocks with its own **₹500/month** Razorpay subscription; signed-in users get the 4 sample questions free. Questions transcribed from a published book (the six Paper 1 papers, and the Yoga November 2017, July 2018 and December 2018 papers from a solved-papers collection) are shown only to admins, as is the Source Library. The **Subscription** page handles payments; the **Admin** page lists subscribers.

**To go live, follow [`SETUP.md`](SETUP.md)** (Supabase, Render, Google sign-in, Razorpay). Streamlit Community Cloud's terms don't allow commercial apps, so the paid app runs on Render (`render.yaml`).

## Run it on your computer

```bash
python3.14 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
NETPYQ_DEV_MODE=1 streamlit run streamlit_app.py        # no sign-in, full access, local SQLite file
pytest                                                  # 68 tests: data, filters, tracking, analytics, accounts, payments, app flows
```

## Project layout

```
streamlit_app.py          entry point: page setup, navigation, sidebar
pyq/
  config.py               revision threshold (75%), weak threshold (50%), folders, samples on/off
  syllabus.py             the 10 units of each subject and their labels
  model.py                the Question record and its checks
  bank.py                 loads samples + data/questions/*.json + topic notes; skips and reports bad entries
  filters.py              sidebar filter logic
  tracker.py              attempt log, practice runs, the review loop
  analytics.py            accuracy tables, revision list, frequency counts (pandas)
  library.py              the Source Library catalog
  knowledge.py            the knowledge base: key facts per topic, and how each topic is asked
  data/samples.py         the 4 sample questions
  access.py               who sees what: free samples, paid subjects, book-sourced questions
  store.py                the database: answers and subscriptions per user (SQLAlchemy)
  payments.py             Razorpay Subscriptions over its REST API
  ui/                     Streamlit pages and widgets (the only package that imports streamlit)
    account.py            Google sign-in gate, per-user session, subscription actions
    plans_page.py         Subscription page;  admin_page.py: subscribers and usage
data/questions/           PYQ files, one JSON file per paper
data/knowledge.json       key facts per micro-topic, with their sources
data/topics.json          trend notes per micro-topic, used by questions without their own trend_analysis
sources/                  PDFs + catalog.json for the Source Library
tests/                    pytest suite, including end-to-end runs with Streamlit's AppTest
SETUP.md                  step-by-step: accounts and secrets needed to go live
render.yaml               Render hosting blueprint
```

## Source Library

`sources/catalog.json` lists study texts per syllabus unit. It currently holds:

- **5 PDFs in the repository**:
  - the official UGC NET Yoga syllabus (code 100)
  - the official UGC NET General Paper (Paper 1) syllabus
  - an open-access (CC BY) paper on yoga trial trends
  - your Ashtakavarga chapter draft
  - a saved ChatGPT conversation, labelled as notes, not a source
- **8 entries for files in your Google Drive "notes UGC" folder** that are too large or not free to publish: Rama Prasad's *Yoga Sutras* with Vyāsa and Vācaspati (1912), the two Hindi *108 Upaniṣad* volumes, the *Mālinīvijayottara Tantra*, and your therapy, Kaivalya Pāda and February 2023 PYQ notes
- **2 Paper 1 books** in the shared folder "My book's": Madaan's *NTA UGC NET/SET/JRF Paper 1* (Pearson, 2019), which supplied the Paper 1 papers, and a Hindi Paper 1 reference book
- **37 entries for the shared Google Drive folder "My book's"**, catalogued unit by unit with their exact file names. Examples:
  - Unit 1: Nārada Bhakti Sūtra, Sāṃkhya Kārikā with Gauḍapāda, Yājñavalkya Smṛti
  - Units 2–3: Gita Press *ईशादि नौ उपनिषद्* and Gītā, the five-Upaniṣad Hindi compilation, verse notes
  - Unit 4: the UPRTOU and UOU Yoga Sūtra course books
  - Unit 5: Kaivalyadhama's *Vasiṣṭha Saṃhitā* and *Haṭha Pradīpikā*, Mallik's *Siddha-Siddhānta-Paddhati*, *Haṭharatnāvalī*
  - Units 6–8: psychology, anatomy and disease-wise therapy notes
  - Unit 9: Gharote and Ganguly's *Teaching Methods for Yogic Practices*
  - Unit 10: five of the six "contemporary practices" the syllabus names (Sūkṣma Vyāyāma, Cyclic Meditation, MSRT, Yoga Nidra, Savitā dhyāna; not Transcendental Meditation)
- **33 recommended texts** still to add. All are public domain, except the Ayush *Common Yoga Protocol* (free from the official site, so link to it rather than redistributing) and Datta & Singh (public domain in India). Examples:
  - Woods's *Yoga-System of Patañjali* (1914, with Vyāsa's commentary)
  - Pancham Sinh's *Haṭha Pradīpikā* (1914)
  - Vasu's *Gheraṇḍa Saṃhitā* (1895)
  - Clark's *Āryabhaṭīya* (1930)
  - Colebrooke's Līlāvatī and Brahmagupta (1817)
  - Ray's *History of Hindu Chemistry*
  - Bhishagratna's *Suśruta Saṃhitā*

To add one, put the PDF in `sources/` and set `file` on its catalog entry. See [`sources/README.md`](sources/README.md). Only add texts you are free to share.
