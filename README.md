# UGC NET PYQ Analytical Dashboard: Yoga (100) and Indian Knowledge System (103)

A Streamlit app for UGC NET Paper II practice, built for Python 3.14 and Streamlit Community Cloud.

| Page | What it does |
|---|---|
| **Practice** | Syllabus-mapped questions with the macro unit and micro-topic above each one. On submit: the correct answer, a detailed explanation, a highlighted **Trend Insight** box and links to study sources. Take the same quiz as many times as you like. |
| **Review Mistakes** | Only the questions whose latest answer was wrong. Each round asks them once; anything missed comes back next round, reshuffled, until a round is **100%** correct. |
| **Performance Analytics** | Real-time score and accuracy for the current attempt and the whole session; accuracy by syllabus unit and micro-topic, colour-coded (🟢 ≥75%, 🟠 50–74%, 🔴 <50%); and a **Topics to Revise** list of every micro-topic below 75%, each with a *Practise* button. |
| **Question Bank** | Coverage by unit and exam session, plus the data check. |
| **Source Library** | Study texts mapped to syllabus units: your PDFs (readable in the app) and recommended public-domain translations still to add. |

Every answer, in Practice or Review, is logged in the background (`st.session_state`) with its question, macro unit, micro-topic, chosen option and result. The sidebar filters by subject, exam year or session, syllabus unit, micro-topic and question format.

## About the data

**Real papers.** `data/questions/` holds official papers as they were printed, one JSON file per paper. It currently holds:

| Paper | Questions | Answers |
|---|---|---|
| UGC NET (CBSE) January 2017, Yoga Paper II (booklet JA-100-17, English version) | 50 | Worked out from the primary texts and matched against a published solved-papers key. Q43 and Q44 are marked *unverified*: their answers could not be lined up with that key in the scanned copy. |
| UGC NET June 2019, Yoga Paper 2, **Hindi** | 93 | The original NTA response sheet, question numbers as printed, both passages kept. 64 answers match the published solved-papers key (*cross-checked*); the rest are worked out and *unverified*. Seven items are left out: three are flawed (Q48, Q77, Q95) and four could not be settled (Q49, Q68, Q73, Q89). |
| UGC NET December 2019, Yoga Paper 2, **Hindi** | 97 | The original NTA response sheet (10 Dec 2019), question numbers as printed, both passages kept. 21 answers match the published solved-papers key and are marked *cross-checked*; the rest are worked out and *unverified*. Q17, Q77 and Q79 are left out (answer could not be established). |
| UGC NET June 2021 cycle (merged with December 2020; held Nov 2021 – Jan 2022), Yoga Paper 2, **Hindi** | 72 | Kept in Hindi as printed. Read from a text extraction of the scan, which has no question numbers, so the questions keep their source order. Answers worked out from the texts and marked *unverified*. Three items are left out (a Paper 1 item, an incomplete one, and one whose options are all historically wrong). |
| UGC NET December 2022 cycle (held Feb–Mar 2023), Yoga Paper 2, Q51–66 | 15 | Only these questions were readable in your notes (NTA response-sheet screenshots); Q53 is incomplete there and left out. Answers worked out from the texts and marked *unverified*. |
| UGC NET June 2024, Yoga Paper 2, Q51–150 (booklet series Y, English version) | 100 | Worked out from the primary texts. No official key was published: this is the pen-and-paper exam of 18 June 2024 that NTA cancelled, so every answer is marked *unverified*, and explanations say where an answer is provisional or the item is flawed. The session is inferred from the printed combined booklet. |

Each question keeps the booklet's wording, numbering and labels (List I in Roman numerals where the paper uses them, and shared reading passages). Each is mapped to a syllabus unit and micro-topic, and has its own detailed explanation. The explanations are written for this app; none are copied from a guidebook. The feedback shows how the answer was checked: *official key*, *cross-checked* or *unverified*.

**Samples.** The app also ships **4 sample questions** (2 Yoga, 2 IKS; one each of the Match-the-List, Sequence, Multiple-statement and Assertion–Reason formats) in `pyq/data/samples.py`. They are **PYQ-pattern model questions**, written to NTA's formats and checked against the primary texts. They are **not copied from a specific paper**, carry no exam year, and appear under *Undated / PYQ-pattern* in the session filter.

**Trend analysis.** The Trend Insight box has two parts.

- **The frequency line is counted, not written.** It comes from the dated papers loaded, currently January 2017, June 2019, December 2019, June 2021, December 2022 (partial) and June 2024.
- **The note is written.** It comes from `data/topics.json`: one note per micro-topic on how it is framed, what the examiner targets, the usual traps and a prep move. It makes no claims like "asked 7 times since 2019".

As more papers go in, the following update automatically:

- the "Frequency in loaded papers" line in every Trend Insight box
- the year filter
- the unit × session grid

See [`data/questions/README.md`](data/questions/README.md) for the format.

The syllabus unit titles in `pyq/syllabus.py` follow NTA's published syllabi via exam portals. Check them against the official PDFs at ugcnet.nta.ac.in.

## Deploy on Streamlit Community Cloud (private repository)

1. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with the GitHub account that owns this repository.
2. Select **Create app**, then choose to deploy from an existing GitHub repository. If the repository is not listed, Streamlit asks for permission to read your **private** repositories. Grant it.
3. Fill in the form: repository `imeditatedaily/NETPYQ`, branch `main`, main file path `streamlit_app.py`. Pick an app URL.
4. Open **Advanced settings** and set **Python version** to **3.14**. Community Cloud ignores `.python-version` and `runtime.txt`; only this setting counts.
5. Select **Deploy**. The first build installs `requirements.txt` and takes a few minutes.

An app deployed from a private repository is **private**: only you can open it. To let someone else in, open the app and use **Share → Invite** with their email address. Community Cloud allows **one private app per account**.

Every push to `main` redeploys the app. Adding a question file or a PDF needs no code change.

## Run it on your computer

```bash
python3.14 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
streamlit run streamlit_app.py
pytest                                                  # 33 tests: data, filters, tracking, analytics, full app flows
```

## Your progress

Session state lasts as long as the browser tab. Refreshing or closing the tab starts a new session. Use **Download log (JSON)** in the sidebar to keep your history, and **Load a saved log** to bring it back later or on another device. The CSV download opens in Excel.

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
  data/samples.py         the 4 sample questions
  ui/                     Streamlit pages and widgets (the only package that imports streamlit)
data/questions/           PYQ files, one JSON file per paper
data/topics.json          trend notes per micro-topic, used by questions without their own trend_analysis
sources/                  PDFs + catalog.json for the Source Library
tests/                    pytest suite, including end-to-end runs with Streamlit's AppTest
```

## Source Library

`sources/catalog.json` lists study texts per syllabus unit. It currently holds:

- **4 PDFs in the repository**:
  - the official UGC NET Yoga syllabus (code 100)
  - an open-access (CC BY) paper on yoga trial trends
  - your Ashtakavarga chapter draft
  - a saved ChatGPT conversation, labelled as notes, not a source
- **7 entries for files in your Google Drive "notes ugc" folder** that are too large or not free to publish: Rama Prasad's *Yoga Sutras* with Vyāsa and Vācaspati (1912), the two Hindi *108 Upaniṣad* volumes, and your therapy, Kaivalya Pāda and February 2023 PYQ notes
- **33 recommended texts** still to add. All are public domain, except the Ayush *Common Yoga Protocol* (free from the official site, so link to it rather than redistributing) and Datta & Singh (public domain in India). Examples:
  - Woods's *Yoga-System of Patañjali* (1914, with Vyāsa's commentary)
  - Pancham Sinh's *Haṭha Pradīpikā* (1914)
  - Vasu's *Gheraṇḍa Saṃhitā* (1895)
  - Clark's *Āryabhaṭīya* (1930)
  - Colebrooke's Līlāvatī and Brahmagupta (1817)
  - Ray's *History of Hindu Chemistry*
  - Bhishagratna's *Suśruta Saṃhitā*

To add one, put the PDF in `sources/` and set `file` on its catalog entry. See [`sources/README.md`](sources/README.md). Only add texts you are free to share.
