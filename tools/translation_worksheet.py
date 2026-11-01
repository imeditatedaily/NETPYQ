"""Lists, for one question file, the text a translation file must supply.

    python tools/translation_worksheet.py yoga-2019-june-paper2

Prints each question's id and the strings the rules in pyq/translate.py can't
handle (list entries the rules can handle are shown as null). Passages and
tables shared with an earlier question are shown as @<that id>.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from pyq import translate as tr  # noqa: E402
from pyq.bank import parse_question, read_question_files  # noqa: E402,F401
from pyq.config import QUESTION_DIR  # noqa: E402
from pyq.model import parse_question as parse  # noqa: E402


def main(stem: str) -> None:
    raw = json.loads((QUESTION_DIR / f"{stem}.json").read_text(encoding="utf-8"))
    raw = raw if isinstance(raw, list) else raw["questions"]
    done = tr.load(ROOT / "data" / "translations")
    seen: dict[tuple, str] = {}
    out = {}
    for r in raw:
        q = parse(r)
        if q.id in done:
            continue
        to = tr.EN if tr.language(q) == tr.HI else tr.HI
        need = tr.needed(q)
        row = {}
        for k, v in need.items():
            if k in ("passage", "table_title", "table_columns", "table_rows"):
                key = (k, json.dumps(v, ensure_ascii=False))
                if key in seen:
                    row[k] = "@" + seen[key]
                    continue
                seen[key] = q.id
            if isinstance(v, list) and k != "table_rows":
                row[k] = [x if tr.rule(x, to) is None else None for x in v]
            else:
                row[k] = v
        out[q.id] = {"to": to, **row}
    print(json.dumps(out, ensure_ascii=False, indent=0))


if __name__ == "__main__":
    main(sys.argv[1])
