# Adding real PYQs

Every `*.json` file in this folder is loaded as a list of questions, next to the
four built-in samples in `pyq/data/samples.py`. One file per paper keeps things
tidy, for example `yoga-2025-june.json` or `iks-2024-december.json`.

A file holds a JSON list:

```json
[
  {
    "id": "YOGA-2025J-042",
    "subject": "yoga",
    "exam_year": 2025,
    "exam_cycle": "June",
    "source": { "type": "official", "note": "paper date, shift and question number" },
    "question_type": "mcq",
    "question_text": "According to Yoga Sūtra 2.4, which of the following is NOT a state of the kleśas?",
    "options": ["Prasupta", "Tanu", "Kṣipta", "Udāra"],
    "correct_answer": 3,
    "detailed_explanation": "**Answer: (3) Kṣipta.**\n\nYS 2.4 names four states: prasupta, tanu, vicchinna and udāra. Kṣipta is one of the five citta-bhūmis.",
    "macro_unit": "Yoga Unit 4: Patanjala Yoga Sutra",
    "micro_topic": "Kleshas and their removal",
    "trend_analysis": "**Pattern.** …\n\n**What the examiner targets.**\n\n- …",
    "references": ["Yoga Sūtra 2.4 with Vyāsa's bhāṣya"],
    "source_ids": ["woods-1914-yoga-system"]
  }
]
```

The id, session and note above only show the format.

## Fields

| Field | Required | Notes |
|---|---|---|
| `id` | yes | Unique and permanent: saved logs refer to it. |
| `subject` | yes | `yoga` or `iks` |
| `exam_year`, `exam_cycle` | for real PYQs | e.g. `2025` and `"June"` or `"December"`. `null` for both on a model question. |
| `source.type` | recommended | `official`, `memory_based` or `model`. Defaults to `official` when a year is given. |
| `question_type` | recommended | `mcq`, `match`, `assertion_reason`, `statements`, `sequence` (default `mcq`) |
| `question_text` | yes | The stem |
| `lists` | `match` | `{"list_i": {"title": "List I", "items": [...]}, "list_ii": {"title": "List II", "items": [...]}}`, labelled A–D and I–IV automatically |
| `items` | `statements`, `sequence` | Labelled A, B, C… automatically |
| `assertion`, `reason` | `assertion_reason` | |
| `prompt` | no | e.g. "Choose the correct answer from the options given below:" |
| `options` | yes | In the paper's order; shown as (1)–(4) |
| `correct_answer` | yes | The option **number**, 1–4, as in NTA answer keys |
| `detailed_explanation` | yes | Markdown |
| `macro_unit` | yes | Exactly one of the labels in `pyq/syllabus.py`, e.g. `Yoga Unit 4: Patanjala Yoga Sutra`, `IKS Unit 3: Astronomy` |
| `micro_topic` | yes | Spell it identically every time; frequencies group by this text |
| `trend_analysis` | yes | Markdown, shown in the Trend Insight box |
| `references` | no | Shown under the explanation |
| `source_ids` | no | Ids from `sources/catalog.json`, shown as "Study this in" |

A question with a problem is skipped and listed, with the reason, under
**Question Bank → Data check**. The rest of the app keeps working.

Once a real paper is in, the year filter, the unit × session grid and the
"Frequency in loaded papers" line of every Trend Insight box count it
automatically. Set `INCLUDE_SAMPLE_QUESTIONS = False` in `pyq/config.py` if you
no longer want the samples.
