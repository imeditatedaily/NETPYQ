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
| UGC NET (CBSE) January 2017, Yoga **Paper III** (booklet JA-100-17, English version) | 75 | From the **official question booklet** on ugcnetonline.in. No official key was available, so answers are worked out from the primary texts and marked *unverified*; less certain ones say *provisional*. All 75 questions are in; explanations say where an answer rests on judgement. |
| UGC NET (CBSE) November 2017, Yoga Paper II, **Hindi** | 50 | From a published solved-papers collection (admins only), with six items from the **official booklet** (ugcnetonline.in). Every answer follows the **official CBSE answer key** (uploaded to the Drive notes folder); question numbers follow the booklet. Q13 is in; the key gives marks for every option, and the app scores it that way. |
| UGC NET (CBSE) November 2017, Yoga **Paper III** (booklet N-10017, English version) | 75 | From the **official question booklet** on ugcnetonline.in, with the reading passage. Answers worked out from the primary texts and marked *unverified*. All 75 questions are in. |
| UGC NET (CBSE) July 2018, Yoga Paper II, **Hindi** | 100 | From the same collection (admins only), checked against the **official booklet** (ugcnetonline.in): it fixed the numbering of six items and supplied eight missing ones with its printed Hindi (*unverified*). All 100 questions are in; Q21, Q22, Q50 and Q65 note where the answer depends on the source. |
| UGC NET (NTA) December 2018, Yoga Paper 2, **Hindi** | 100 | Numbered as in **NTA's master question paper** (22 Dec 2018, first shift; prepp.in copy). 80 questions come from the same collection (admins only), with both reading passages; the other 18 are transcribed from the master paper. Every answer follows **NTA's final answer key**, matched by question ID. Q12 and Q26 are in, with both options NTA's key accepts. |
| UGC NET June 2019 (26 June, first shift), Yoga Paper 2, **Hindi** | 100 | The original NTA response sheet, question numbers as printed, both passages kept. Every answer follows **NTA's answer key**, matched to each question by its NTA question ID. Q37, Q48 and Q95 were cancelled by NTA; they are kept, and every option scores, as in the exam. |
| UGC NET (NTA) December 2019, Yoga Paper 2 (6 Dec, first shift), **Hindi** | 100 | A candidate's NTA response sheet, renumbered to **NTA's master question paper** for the shift (prepp.in copy), Q51–150, with NTA question IDs kept; both passages kept. (It was listed as 10 Dec 2019 before; the master paper shows it is the 6 Dec first-shift paper, its questions shuffled on the sheet.) 21 answers match the published solved-papers key and are marked *cross-checked*; the rest are worked out and *unverified*. All 100 questions are in; Q94 and Q119 say how sure the answer is. |
| UGC NET (NTA) June 2020 cycle, Yoga Paper 2 (held 5 Nov 2020, second shift) | 100 | From **NTA's master question paper** (NDLI copy), Q51–150, English version. No answer key was available: answers worked out and marked *unverified*. All 100 questions are in. Where the paper itself is flawed (no option exactly right) or the source behind an answer could not be verified, the explanation says so plainly. Q132 (nut-fat order) and Q146 (asks for two practices, allows one) are flawed in the paper. |
| UGC NET December 2020 & June 2021 cycle (22 Nov 2021, first shift), Yoga Paper 2, **Hindi** | 100 | Numbered as in the **official NTA paper** (NDLI copy in the Drive notes folder), which also supplied 16 questions, with NTA question IDs kept. No key was available, so answers are worked out from the texts and marked *unverified*. All 100 questions are in; Q28 and Q41 are flawed in the paper and their explanations say why. |
| UGC NET (NTA) December 2021 & June 2022 cycle, Yoga Paper 2 (held 9 July 2022, slot 2) | 100 | From **NTA's question paper** (NDLI copy), Q51–150, English version. No answer key was available: answers worked out and marked *unverified*. All 100 questions are in. Where the paper itself is flawed (no option exactly right) or the source behind an answer could not be verified, the explanation says so plainly. |
| UGC NET December 2022 cycle (21 Feb 2023, second shift), Yoga Paper 2 | 100 | A printed NTA response sheet ("2023 old paper yoga.pdf"), Sl. No. 1–100, English version. No key was available, so answers are worked out from the texts and marked *unverified*. |
| UGC NET June 2023 (21 June 2023), Yoga Paper 2 | 100 | A printout of the NTA response sheet, Part B 1–100, English version. Answers worked out from the texts and marked *unverified*. |
| UGC NET (NTA) December 2023, Yoga Paper 2 (8 Dec, second shift) | 100 | From **NTA's master question paper** (NDLI copy), Q51–150, English version; replaces the 15-question coaching handout, whose Hindi is kept as the Hindi translation of those 15. No answer key was available: answers worked out and marked *unverified*. In Q111 and Q115 the English version prints two identical options, so the Hindi version's codes are used. |
| UGC NET June 2024, Yoga Paper 2, Q51–150 (booklet series Y, English version) | 100 | Worked out from the primary texts. No official key was published: this is the pen-and-paper exam of 18 June 2024 that NTA cancelled, so every answer is marked *unverified*, and explanations say where an answer is provisional or the item is flawed. The session is inferred from the printed combined booklet. |
| UGC NET June 2024 re-exam (4 Sep 2024, second shift), Yoga Paper 2, Q51–150, **Hindi** | 100 | The NTA response sheet, question numbers as printed, both passages kept, NTA question IDs kept for matching against the key later. No key was available, so answers are worked out from the texts and marked *unverified*. All 100 questions are in. Where the paper itself is flawed (no option exactly right) or the source behind an answer could not be verified, the explanation says so plainly. Q131 (no option gives Gītā 16.21) is flawed in the paper. |
| UGC NET (NTA) December 2024 cycle, Yoga Paper 2 (held 7 Jan 2025, second shift) | 100 | From **NTA's master question paper** (NDLI copy), Q51–150, English version. No answer key was available: answers worked out and marked *unverified*. All 100 questions are in. Where the paper itself is flawed (no option exactly right) or the source behind an answer could not be verified, the explanation says so plainly. Q131 (Vasiṣṭha Saṃhitā match) is flawed in the paper. |
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
| UGC NET (NTA) December 2018, Paper 1, 22 Dec first shift | 48 | From **NTA's master question paper** (prepp.in copy), English; every answer from NTA's final key, matched by question ID. Q34 (no correct option; marks to all) and Q43 (two answers accepted) are left out. Not from a book, so Paper 1 subscribers see it. |
| UGC NET (NTA) December 2020 & June 2021 cycle, Paper 1 (22 Nov 2021, first shift) | 48 | From the **official NTA paper** (NDLI copy in the Drive notes folder, the same file as the Yoga paper), English, NTA question IDs kept. Answers worked out and marked *unverified*. Left out: Q15 (answer could not be settled) and Q40 (the English version misprints Q35 in its place). |
| UGC NET (NTA) December 2021 & June 2022 cycle, Paper 1 (held 9 July 2022, slot 2) | 48 | From **NTA's question paper** (NDLI copy), English. Answers worked out and marked *unverified*; Q36 and Q42 left out. |
| UGC NET December 2022 cycle, Paper 1 (21 Feb 2023, second shift) | 50 | From the same NTA response sheet as the Yoga paper (Sl. No. 101–150, numbered 1–50 here). Answers worked out and marked *unverified*. |
| UGC NET June 2023, Paper 1 (21 June 2023) | 50 | From the same NTA response sheet as the Yoga paper, Part A 1–50. Answers worked out and marked *unverified*. |
| UGC NET (NTA) December 2023, Paper 1 (8 Dec, second shift) | 50 | From **NTA's master question paper** (NDLI copy), English. No answer key was available: answers worked out and marked *unverified*. |
| UGC NET (NTA) December 2024 cycle, Paper 1 (held 7 Jan 2025, second shift) | 50 | From **NTA's master question paper** (NDLI copy), English. Answers worked out and marked *unverified*. |
| UGC NET (NTA) June 2019, Paper 1 (26 June, first shift) | 50 | From **NTA's master question paper** (NDLI copy in the Drive notes folder), English version, with answers from **NTA's answer key** matched by question ID. |
| UGC NET (NTA) December 2019, Paper 1 (6 Dec, first shift) | 49 | From **NTA's master question paper** (prepp.in copy), English, the same session as the Yoga paper. Answers worked out and marked *unverified*; Q13 left out. |
| UGC NET (NTA) June 2020 cycle, Paper 1 (held 5 Nov 2020, second shift) | 48 | From **NTA's master question paper** (NDLI copy), English. Answers worked out and marked *unverified*; Q17 and Q28 left out. |
| UGC NET (NTA) June 2025, Paper 1 (27 June, second shift) | 49 | From the **official NTA response sheet**, with answers from **NTA's final answer key**; Q8 was dropped by NTA. Unlike the book papers above, subscribers see these. |

Paper 1 data-interpretation tables are stored as real tables (the `table` field) and shown above their questions. The June 2024 Paper 1 is not on the site yet.

Each question keeps the booklet's wording, numbering and labels (List I in Roman numerals where the paper uses them, and shared reading passages). Each is mapped to a syllabus unit and micro-topic, and has its own detailed explanation. The explanations are written for this app; none are copied from a guidebook. The feedback shows how the answer was checked: *official key*, *cross-checked* or *unverified*.

**Samples.** The app also ships **4 sample questions** (2 Yoga, 2 IKS; one each of the Match-the-List, Sequence, Multiple-statement and Assertion–Reason formats) in `pyq/data/samples.py`. They are **PYQ-pattern model questions**, written to NTA's formats and checked against the primary texts. They are **not copied from a specific paper**, carry no exam year, and appear under *Undated / PYQ-pattern* in the session filter.

**Trend analysis.** The Trend Insight box has two parts.

- **The frequency line is counted, not written.** It comes from the dated papers loaded, counted per subject. For Yoga these are currently January 2017 (Papers II and III), November 2017 (Papers II and III), July 2018, December 2018, June 2019, December 2019, June 2020 (held Nov 2020), June 2021 (held Nov 2021), June 2022 (held July 2022), December 2022, June 2023, December 2023, June 2024 (the cancelled paper and the September re-exam), December 2024 (held Jan 2025) and June 2025; for Paper 1, July 2016 to December 2018 (three December 2018 sets), June 2019, December 2019, June 2020, June 2021 (held Nov 2021), June 2022, December 2022, June 2023, December 2023, December 2024 and June 2025.
- **The note is written.** It comes from `data/topics.json`: one note per micro-topic on how it is framed, what the examiner targets, the usual traps and a prep move. It makes no claims like "asked 7 times since 2019".

As more papers go in, the following update automatically:

- the "Frequency in loaded papers" line in every Trend Insight box
- the year filter
- the unit × session grid

See [`data/questions/README.md`](data/questions/README.md) for the format.

The syllabus unit titles in `pyq/syllabus.py` follow NTA's published syllabi via exam portals. Check them against the official PDFs at ugcnet.nta.ac.in.

## Knowledge Base

`data/knowledge.json` holds key facts for every micro-topic in the loaded papers (154 topics), each with the Source Library texts it comes from. After every answer, right or wrong, the question view shows a **Knowledge Base** box: the topic's key facts, how the topic has been asked (how often, in which sessions, in which formats) and the earlier questions on it with their answers. The **Knowledge Base** page lists the same by syllabus unit, with a button to practise each topic. `tests/test_knowledge.py` fails if a topic in the bank has no facts, or if a fact cites a source that isn't in `sources/catalog.json`.

## Sanskrit Texts

Exam questions quote the texts themselves: a mantra, a sūtra, half a verse. The **Sanskrit Texts** page holds the source texts line by line in Devanagari, each line with the chapter-and-verse number it is cited by, and a search box that finds a quoted line typed in Devanagari or in Roman letters (spaces, punctuation and anusvāra spelling are ignored). There are 42 texts and about 21,100 numbered lines so far: for Unit 1 the Nārada Bhakti Sūtra, Gorakṣa Śataka, Sāṃkhya Kārikā, Yājñavalkya Smṛti (all three adhyāyas), the Mokṣadharma of the Śānti Parva and the Araṇya Kāṇḍa of the Vālmīki Rāmāyaṇa; for Unit 2 the ten principal Upaniṣads, the Bhagavad Gītā and the Laghu Yoga Vāsiṣṭha; for Unit 3 the Śvetāśvatara and twenty Yoga Upaniṣads, including the Yogarāja and Darśana; for Unit 4 the Yoga Sūtra; for Unit 5 the Haṭha Pradīpikā, Gheraṇḍa Saṃhitā and Śiva Saṃhitā. Each Knowledge Base topic that has a text links to it.

Each text is one file, `data/texts/<id>.json`: its title, syllabus unit, the micro-topics it belongs to, its sources (ids from `sources/catalog.json`) and its `lines`, each `{"ref": "1.2", "sa": "योगश्चित्तवृत्तिनिरोधः ॥"}` with an optional `"en"` meaning and `"head"` rubric. The texts come from proofread public e-texts (GRETIL, the Advaita Śāradā project, the sanskrit/raw_etexts collection), not from scanned books, so the spelling can be trusted more than OCR; verse numbers follow those editions and can differ by one or two from a printed book. Signed-in users without the subject see the first ten lines of each text. `tests/test_texts.py` checks that every file loads, refs are unique, well-known verses sit at their usual numbers and the search works in both scripts.

**Lines asked in previous papers are highlighted.** `tools/link_pyq_lines.py` reads every dated paper and writes `data/pyq_lines.json`, which the page uses to mark each line a question was asked from: an orange badge ("Quoted in Jun 2023 Q15") when the question itself quotes the line, a violet one ("Asked in Dec 2018 Q86") when the question's explanation gives the line as the source of the answer, by verse number or by quoting it. A switch shows only those lines, each with the questions asked from it, and each Knowledge Base topic has a button for its text's asked lines. Bare technical terms ("Śāmbhavī mudrā", "Ujjāyī, Śītalī") are not counted as quotes, and where an explanation's verse number belongs to another edition of the Haṭha Pradīpikā, Gheraṇḍa Saṃhitā or a minor Upaniṣad, the matching verse a few numbers away is used. Run `python tools/link_pyq_lines.py` again after adding a paper (`--review` lists every link and why it was made).

## Study Notes

Chapter-length notes in Hindi, to be read like a book: so far the darśanas (Vaiśeṣika, Nyāya, Sāṃkhya), written in our own words from the chapter PDFs in the owner's Drive and checked line by line against the sūtras and kārikās. Each note is one Markdown file, `data/notes/<id>.md`, with a short header (title, subject, unit, order, topics, sources) between `---` lines. The notes are read on the site only, with no download, and the app's copy protection covers the page; signed-in users without the subject see the opening section. Knowledge Base topics link to their notes. `tests/test_notes.py` checks the headers, topics and sources.

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
  texts.py                the Sanskrit texts line by line, the search over them, and the lines asked in papers
  notes.py                the Study Notes: chapter notes in Markdown
  data/samples.py         the 4 sample questions
  access.py               who sees what: free samples, paid subjects, book-sourced questions
  store.py                the database: answers and subscriptions per user (SQLAlchemy)
  payments.py             Razorpay Subscriptions over its REST API
  ui/                     Streamlit pages and widgets (the only package that imports streamlit)
    account.py            Google sign-in gate, per-user session, subscription actions
    plans_page.py         Subscription page;  admin_page.py: subscribers and usage
data/questions/           PYQ files, one JSON file per paper
data/knowledge.json       key facts per micro-topic, with their sources
data/texts/               Sanskrit source texts, one JSON file per text, a numbered line per verse
data/pyq_lines.json       which lines previous-year questions were asked from (tools/link_pyq_lines.py)
data/notes/               Study Notes, one Markdown file per chapter
tools/                    scripts that build practice sets and link papers to texts
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
