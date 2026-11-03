"""Shared helpers for writing practice sets in NTA's formats.

Each question lists the correct option FIRST; build() moves it to a rotating
position (1-4) so answers are spread evenly. Assertion-Reason options keep
NTA's fixed order, so those take the answer number directly.
"""

import json
from pathlib import Path

QUESTION_DIR = Path(__file__).resolve().parent.parent / "data" / "questions"

AR = ["Both (A) and (R) are true and (R) is the correct explanation of (A)",
      "Both (A) and (R) are true but (R) is NOT the correct explanation of (A)",
      "(A) is true but (R) is false",
      "(A) is false but (R) is true"]
PROMPT = "Choose the correct answer from the options given below:"


class PracticeSet:
    def __init__(self, prefix: str, note: str, answer_source: str = "unverified"):
        self.prefix, self.note, self.answer_source = prefix, note, answer_source
        self.q: list[dict] = []

    def mcq(self, unit, topic, text, options, why):
        self.q.append(dict(unit=unit, topic=topic, type="mcq", text=text, options=options, why=why))

    def statements(self, unit, topic, text, items, options, why):
        self.q.append(dict(unit=unit, topic=topic, type="statements", text=text, items=items, options=options, why=why))

    def sequence(self, unit, topic, text, items, options, why):
        self.q.append(dict(unit=unit, topic=topic, type="sequence", text=text, items=items, options=options, why=why))

    def match(self, unit, topic, text, l1, l2, options, why, t1="List I", t2="List II"):
        self.q.append(dict(unit=unit, topic=topic, type="match", text=text, l1=l1, l2=l2, t1=t1, t2=t2,
                           options=options, why=why))

    def ar(self, unit, topic, a, r, answer, why):
        self.q.append(dict(unit=unit, topic=topic, type="assertion_reason", a=a, r=r, answer=answer, why=why))

    def build(self) -> list[dict]:
        out, pos = [], 0
        for n, q in enumerate(self.q, start=1):
            base = {"id": f"{self.prefix}-{n:03d}", "subject": "yoga", "paper": "Paper 2", "question_no": n,
                    "source": {"type": "practice", "note": self.note}, "answer_source": self.answer_source,
                    "macro_unit": q["unit"], "micro_topic": q["topic"], "question_type": q["type"]}
            if q["type"] == "assertion_reason":
                base.update(question_text="Given below are two statements: one is labelled as Assertion (A) and the "
                                          "other is labelled as Reason (R).",
                            assertion=q["a"], reason=q["r"],
                            prompt="In the light of the above statements, choose the correct answer from the options "
                                   "given below:",
                            options=AR, correct_answer=q["answer"])
                label = AR[q["answer"] - 1]
            else:
                opts = list(q["options"])
                assert len(opts) == 4 and len(set(opts)) == 4, (n, opts)
                correct, rest = opts[0], opts[1:]
                target = pos % 4
                pos += 1
                base.update(question_text=q["text"], options=rest[:target] + [correct] + rest[target:],
                            correct_answer=target + 1)
                label = correct
                if q["type"] in ("statements", "sequence"):
                    base.update(items=q["items"], prompt=PROMPT)
                if q["type"] == "match":
                    base.update(lists={"list_i": {"title": q["t1"], "items": q["l1"]},
                                       "list_ii": {"title": q["t2"], "style": "roman", "items": q["l2"]}},
                                prompt=PROMPT)
            base["detailed_explanation"] = f"**Answer: ({base['correct_answer']}) {label}.**\n\n{q['why']}"
            out.append(base)
        return out

    def write(self, filename: str) -> None:
        qs = self.build()
        (QUESTION_DIR / filename).write_text(json.dumps(qs, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"{filename}: {len(qs)} questions")
