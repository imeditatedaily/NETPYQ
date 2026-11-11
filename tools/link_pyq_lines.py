"""Finds the Sanskrit lines that previous-year questions were asked from, and writes
data/pyq_lines.json for the Sanskrit Texts page:

    {"hatha-pradipika": {"1.17": [["YOGA-2019JUN-P2-Q12", "quoted"], ...], ...}, ...}

"quoted"  the question itself (stem, options, lists, statements) quotes the line;
"source"  the explanation gives the line as the answer's source, by verse number
          ("YS 2.46", "Haṭha Pradīpikā 1.17") or by quoting it in italics.

Only dated papers count (practice sets and model questions do not). Run it again after
adding a paper:

    python tools/link_pyq_lines.py            # writes the file and prints a summary
    python tools/link_pyq_lines.py --review   # also lists every link with the words that matched
"""

import bisect
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from pyq.config import QUESTION_DIR, TEXT_DIR  # noqa: E402
from pyq.texts import deva_key, load_texts, roman_key  # noqa: E402

OUT = ROOT / "data" / "pyq_lines.json"

MIN_DEVA, MIN_ROMAN = 12, 14       # shortest quote that counts (characters of the search key)
SINGLE_WORD = 18                   # a single word must be at least this long (a long compound)
MAX_PLACES = 4                     # a phrase found in more lines than this is a stock phrase, not a quote
MAX_RANGE = 6                      # "HP 1.13–45" names a passage, not the lines a question asks
WHOLE_LINE = 0.75                  # a run of technical terms counts only when it is (nearly) the whole line
NEIGHBOURS = 3                     # editions number some verses differently: look this far either side of a cited verse …
RENUMBERED = {"hatha-pradipika", "gheranda-samhita", "shiva-samhita", "goraksha-shataka", "nadabindu-upanishad",
              "dhyanabindu-upanishad", "yogachudamani-upanishad", "yogakundali-upanishad", "yogatattva-upanishad",
              "yogashikha-upanishad", "trishikhibrahmana-upanishad", "darshana-upanishad", "tejobindu-upanishad"}
                                   # … but only in these texts, whose editions differ (the Yoga Sūtra, Gītā and the
                                   # principal Upaniṣads are numbered alike everywhere), and only for a single verse

DEVA_WORD = re.compile(r"[ऀ-ॣ०-ॿ]+")
ROMAN_WORD = re.compile(r"[A-Za-zÀ-ɏḀ-ỿ]+")

# How explanations cite texts. Each pattern must be followed by a verse number.
CITE = {
    "yoga-sutra": r"YS|Yoga[ -]?S[uū]tras?",
    "hatha-pradipika": r"HP|HYP|Ha[tṭ]ha[ -]?(?:Yoga[ -]?)?Prad[iī]pik[aā]",
    "gheranda-samhita": r"GS|Ghera[nṇ][dḍ]a(?:[ -]Sa[mṃ]hit[aā])?",
    "bhagavad-gita": r"BG|Bhagavad[ -]?G[iī]t[aā]|G[iī]t[aā]",
    "shiva-samhita": r"[SŚ]iva[ -]Sa[mṃ]hit[aā]",
    "samkhya-karika": r"SK|S[aā][mṃ]khya[ -]?K[aā]rik[aā]",
    "narada-bhakti-sutra": r"NBS|N[aā]rada[ -]Bhakti[ -]?S[uū]tras?",
    "goraksha-shataka": r"Gorak[sṣ]a[ -]?[SŚ]ataka",
    "yajnavalkya-smriti": r"Y[aā]j[nñ]avalkya[ -]Sm[rṛ]ti",
    "katha-upanishad": r"Ka[tṭ]ha(?:[ -]Upani[sṣ]ad)?",
    "chandogya-upanishad": r"Ch[aā]ndogya(?:[ -]Upani[sṣ]ad)?",
    "shvetashvatara-upanishad": r"[SŚ]vet[aā][sś]vatara(?:[ -]Upani[sṣ]ad)?",
    "taittiriya-upanishad": r"Taittir[iī]ya(?:[ -]Upani[sṣ]ad)?",
    "mundaka-upanishad": r"Mu[nṇ][dḍ]aka(?:[ -]Upani[sṣ]ad)?",
    "prashna-upanishad": r"Pra[sś]na(?:[ -]Upani[sṣ]ad)?",
    "aitareya-upanishad": r"Aitareya(?:[ -]Upani[sṣ]ad)?",
    "kena-upanishad": r"Kena(?:[ -]Upani[sṣ]ad)?",
    "brihadaranyaka-upanishad": r"B[rṛ]had[aā]ra[nṇ]yaka(?:[ -]Upani[sṣ]ad)?|BU|B[AĀ]U",
    "isha-upanishad": r"[IĪ][sś][aā](?:v[aā]sya)?(?:[ -]Upani[sṣ]ad)",
    "mandukya-upanishad": r"M[aā][nṇ][dḍ][uū]kya(?:[ -]Upani[sṣ]ad)?",
    "yogakundali-upanishad": r"Yogaku[nṇ][dḍ]al[iī](?:[ -]Upani[sṣ]ad)?",
    "yogashikha-upanishad": r"Yoga[sś]ikh[aā](?:[ -]Upani[sṣ]ad)?",
    "yogatattva-upanishad": r"Yogatattva(?:[ -]Upani[sṣ]ad)?",
    "yogachudamani-upanishad": r"Yogac[uū][dḍ][aā]ma[nṇ]i(?:[ -]Upani[sṣ]ad)?",
    "dhyanabindu-upanishad": r"Dhy[aā]nabindu(?:[ -]Upani[sṣ]ad)?",
    "nadabindu-upanishad": r"N[aā]dabindu(?:[ -]Upani[sṣ]ad)?",
    "amritabindu-upanishad": r"Am[rṛ]tabindu(?:[ -]Upani[sṣ]ad)?",
    "amritanada-upanishad": r"Am[rṛ]tan[aā]da(?:[ -]Upani[sṣ]ad)?",
    "tejobindu-upanishad": r"Tejobindu(?:[ -]Upani[sṣ]ad)?",
    "kshurika-upanishad": r"K[sṣ]urik[aā](?:[ -]Upani[sṣ]ad)?",
    "hamsa-upanishad": r"Ha[mṃ]sa[ -]Upani[sṣ]ad",
    "darshana-upanishad": r"Dar[sś]ana[ -]Upani[sṣ]ad",
    "trishikhibrahmana-upanishad": r"Tri[sś]ikhi(?:br[aā]hma[nṇ]a)?(?:[ -]Upani[sṣ]ad)?",
    "yogaraja-upanishad": r"Yogar[aā]ja(?:[ -]Upani[sṣ]ad)?",
    "advayataraka-upanishad": r"Advayat[aā]raka(?:[ -]Upani[sṣ]ad)?",
    "mandalabrahmana-upanishad": r"Ma[nṇ][dḍ]alabr[aā]hma[nṇ]a(?:[ -]Upani[sṣ]ad)?",
    "brahmavidya-upanishad": r"Brahmavidy[aā](?:[ -]Upani[sṣ]ad)?",
    "laghu-yoga-vasishtha": r"Laghu[ -]Yoga[ -]?V[aā]s[iī][sṣ][tṭ]ha",
}
NUM = r"\d+(?:\.\d+)*"
CITE_RE = re.compile(
    r"(?<![\w-])(?P<name>" + "|".join(f"(?P<t{i}>{p})" for i, p in enumerate(CITE.values())) + r")\.?,?\s+"
    r"(?:(?:verse|v\.|sūtra|sutra|śloka|mantra)\s+)?"
    r"(?P<refs>" + NUM + r"(?:\s*[–-]\s*" + NUM + r")?(?:\s*(?:,|and|&)\s*" + NUM + r"(?:\s*[–-]\s*" + NUM + r")?)*)")
CITE_IDS = list(CITE)

# Names of practices and other technical terms. Options such as "Śāmbhavī mudrā" or "Ujjāyī, Śītalī" are terms the
# question asks about, not quotations: a run made only of these words is not counted as quoting the line it is in.
TERMS = {roman_key(w) for w in """
    mudra mudrā bandha bandh chakra cakra kumbhaka kumbhak asana āsana pranayama prāṇāyāma pratyahara pratyāhāra
    dharana dhāraṇā dhyana dhyāna samadhi samādhi yama niyama yoga ishvara īśvara pranidhana praṇidhāna abhyasa abhyāsa
    vairagya vairāgya karma nivritti nivṛtti pravritti pravṛtti indriya nigraha pratyaksha pratyakṣa rupa rūpa vidya vidyā
    adhyatma adhyātma shvasa śvāsa prashvasa praśvāsa shambhavi śāmbhavī viparitakarani viparītakaraṇī svadhishthana
    swadhishthana svādhiṣṭhāna muladhara mūlādhāra manipura maṇipūra anahata anāhata vishuddha viśuddha ajna ājñā
    ujjayi ujjāyī shitali śītalī sitkari sītkārī bhastrika bhastrikā bhramari bhrāmarī murccha mūrcchā plavini plāvinī
    suryabhedana sūryabhedana mahamudra mahāmudrā mahabandha mahābandha mahavedha mahāvedha jalandhara jālandhara
    moola mūla uddiyana uḍḍīyāna khechari khecarī vajroli vajrolī asteya brahmacharya brahmacarya satya ahimsa ahiṃsā
    aparigraha shaucha śauca santosha santoṣa tapas svadhyaya svādhyāya ida iḍā pingala piṅgalā sushumna suṣumṇā
    gandhari gāndhārī hastijihva hastijihvā nadi nāḍī prana prāṇa apana apāna
""".split()}
NOT_THE_SOURCE = re.compile(r"(?:compare|cf\.|unlike|contrast|not in|like)\W*$", re.I)


def question_fields(q: dict) -> list[str]:
    """The question's own words, one string per field (a quote never runs across two options)."""
    out = [q.get("question_text") or "", q.get("assertion") or "", q.get("reason") or ""]
    out += list(q.get("options") or []) + list(q.get("items") or [])
    for side in ("list_i", "list_ii"):
        out += list(((q.get("lists") or {}).get(side) or {}).get("items") or [])
    return [s for s in out if s]


class Corpus:
    """Every line's search key joined into one string, so a phrase is found with str.find."""

    def __init__(self, texts, keyf):
        self.keys, self.where, starts, parts, pos = [], [], [], [], 0
        for t in texts:
            for ln in t.lines:
                k = keyf(ln.sa)
                self.keys.append(k)
                self.where.append((t.id, ln.ref))
                starts.append(pos)
                parts.append(k)
                pos += len(k) + 1
        self.starts, self.blob = starts, "|".join(parts)
        self.grams = {self.blob[i:i + 6] for i in range(len(self.blob) - 5)}

    def has(self, key: str) -> bool:
        return key[:6] in self.grams and key[-6:] in self.grams and self.blob.find(key) >= 0

    def key_of(self, place: tuple[str, str]) -> str:
        return self.keys[self.where.index(place)]

    def places(self, key: str) -> list[tuple[str, str]]:
        out, i = [], self.blob.find(key)
        while i >= 0:
            out.append(self.where[bisect.bisect_right(self.starts, i) - 1])
            i = self.blob.find(key, i + 1)
        return list(dict.fromkeys(out))


def quotes(text: str, corpus: Corpus, word_re, keyf, min_len: int) -> list[tuple[str, str]]:
    """The longest runs of words in `text` found inside a single line: [(the words, their key)]."""
    words = word_re.findall(text)
    found, i = [], 0
    while i < len(words):
        best = None
        for j in range(i + 1, min(len(words), i + 60) + 1):
            key = keyf("".join(words[i:j]))
            if len(key) < 6:
                continue
            if not corpus.has(key):
                break
            best = (j, key)
        if best and len(best[1]) >= min_len and (best[0] - i > 1 or len(best[1]) >= SINGLE_WORD):
            found.append((" ".join(words[i:best[0]]), best[1]))
            i = best[0]
        else:
            i += 1
    return found


def expand(text, refs: str) -> list[str]:
    """'2.49–2.53, 3.1' → the refs of those lines in `text` (a bare '2.1' of a three-level text means all of 2.1.x)."""
    have = [ln.ref for ln in text.lines]
    out = []
    for part in re.split(r"\s*(?:,|and|&)\s*", refs):
        a, _, b = (x.strip() for x in re.split(r"\s*([–-])\s*", part, maxsplit=1)) if re.search("[–-]", part) else (part, "", "")
        if not b:
            if a in have:
                out.append(a)
            else:
                under = [r for r in have if r.startswith(a + ".")]
                if 0 < len(under) <= MAX_RANGE:
                    out += under
            continue
        pa, pb = a.split("."), b.split(".")
        pb = pa[: len(pa) - len(pb)] + pb               # "2.52–53" → 2.53
        if pa[:-1] != pb[:-1] or not (pa[-1].isdigit() and pb[-1].isdigit()):
            continue
        lo, hi = int(pa[-1]), int(pb[-1])
        if 0 <= hi - lo < MAX_RANGE:
            out += [r for r in (".".join(pa[:-1] + [str(n)]) for n in range(lo, hi + 1)) if r in have]
    return out


def sanskrit_words(english: set[str], *parts: str) -> set[str]:
    """Devanagari words, and Roman words that are not English, as search keys."""
    out = set()
    for s in parts:
        out |= {deva_key(w) for w in DEVA_WORD.findall(s) if len(deva_key(w)) >= 4}
        out |= {roman_key(w) for w in ROMAN_WORD.findall(s) if len(roman_key(w)) >= 5 and w.lower() not in english}
    return out


def english_words() -> set[str]:
    """Words of the General Paper (Paper 1), which has no Sanskrit: a ready-made English vocabulary."""
    out = set()
    for f in QUESTION_DIR.glob("paper1-*.json"):
        for q in json.loads(f.read_text(encoding="utf-8")):
            text = " ".join([q.get("question_text") or "", q.get("detailed_explanation") or ""] + list(q.get("options") or []))
            out |= {w.lower() for w in re.findall(r"[A-Za-z]+", text)}
    return out


def best_line(text, ref: str, words: set[str], may_move: bool) -> tuple[str | None, list[str]]:
    """The cited line, or a line up to NEIGHBOURS away when the cited number belongs to another edition:
    whichever shares the most Sanskrit words with the question and its explanation."""
    refs = [ln.ref for ln in text.lines]
    i = refs.index(ref)
    chapter = ref.rsplit(".", 1)[0] if "." in ref else None

    def shared(r):
        ln = text.lines[refs.index(r)]
        rk, dk = roman_key(ln.sa), deva_key(ln.sa)
        return sorted(w for w in words if w in rk or w in dk)

    def enough(found):        # two shared words, or one long one: a lone "āsana" or "tamas" proves nothing
        return len(found) >= 2 or any(len(w) >= 7 for w in found)

    exact = shared(ref) if enough(shared(ref)) else []
    near = [r for r in refs[max(0, i - NEIGHBOURS): i + NEIGHBOURS + 1]
            if r != ref and (r.rsplit(".", 1)[0] if "." in r else None) == chapter]
    best = max(near, key=lambda r: len(shared(r)), default=None)
    if exact:
        return ref, exact
    if may_move and best and len(shared(best)) >= 2:
        return best, shared(best)
    return None, []


def main(review: bool = False) -> None:
    lib = load_texts(TEXT_DIR)
    texts = [t for t in lib.texts]
    by_id = {t.id: t for t in texts}
    deva, roman = Corpus(texts, deva_key), Corpus(texts, roman_key)
    names = {deva_key(t.title_sa) for t in texts} | {roman_key(t.title) for t in texts}
    names |= {deva_key(x) for x in ("हठप्रदीपिका", "हठयोगप्रदीपिका", "घेरण्डसंहिता", "शिवसंहिता", "योगसूत्र",
                                     "भगवद्गीता", "श्रीमद्भगवद्गीता", "पातञ्जलयोगसूत्र", "पतंजलियोगसूत्र")}
    names |= {roman_key(x) for x in ("Hatha Pradipika", "Hathayoga Pradipika", "Gheranda Samhita", "Shiva Samhita",
                                     "Yoga Sutra", "Patanjala Yoga Sutra", "Bhagavad Gita", "Srimad Bhagavad Gita")}
    names = {n for n in names if len(n) >= 6}
    english = english_words()

    def is_name(key: str) -> bool:
        return any(key in n or (n in key and len(key) - len(n) < 8) for n in names)

    questions = []
    for f in sorted(QUESTION_DIR.glob("*.json")):
        for q in json.loads(f.read_text(encoding="utf-8")):
            if q.get("exam_year") and q.get("subject") != "paper1":
                questions.append(q)

    links = defaultdict(lambda: defaultdict(dict))      # text → ref → question id → how
    log = []
    for q in questions:
        own = question_fields(q)
        blob_r = roman_key(" ".join(own))
        named = {t.id for t in texts if roman_key(t.title.split(" ")[0]) in blob_r and len(roman_key(t.title.split(" ")[0])) >= 4}
        for field in own:
            for word_re, keyf, corpus, min_len in ((DEVA_WORD, deva_key, deva, MIN_DEVA),
                                                   (ROMAN_WORD, roman_key, roman, MIN_ROMAN)):
                for words, key in quotes(field, corpus, word_re, keyf, min_len):
                    if is_name(key):
                        continue
                    places = corpus.places(key)
                    if all(roman_key(w) in TERMS for w in words.split()):
                        places = [p for p in places if len(key) >= WHOLE_LINE * len(corpus.key_of(p))]
                        if not places:
                            log.append(f"term only {q['id']}: {words}")
                            continue
                    if " " not in words and len(places) > 2:
                        log.append(f"stock word skipped ({len(places)} lines) {q['id']}: {words}")
                        continue
                    if named and any(t in named for t, _ in places):
                        places = [p for p in places if p[0] in named]
                    if len(places) > MAX_PLACES:
                        log.append(f"stock phrase skipped ({len(places)} lines) {q['id']}: {words}")
                        continue
                    for t, ref in places:
                        links[t][ref][q["id"]] = "quoted"
                        log.append(f"quoted  {q['id']} → {t} {ref}: {words}")

        expl = q.get("detailed_explanation") or ""
        cited_from = expl + "\n" + "\n".join(q.get("references") or [])
        words = sanskrit_words(english, *own, expl)
        for m in CITE_RE.finditer(cited_from):
            if NOT_THE_SOURCE.search(cited_from[max(0, m.start() - 30):m.start()]):
                continue
            t = by_id[CITE_IDS[next(i for i in range(len(CITE_IDS)) if m.group(f"t{i}"))]]
            cited_refs = expand(t, m.group("refs"))
            for cited in cited_refs:
                ref, shared = best_line(t, cited, words, t.id in RENUMBERED and len(cited_refs) == 1)
                if not ref:
                    log.append(f"CHECK   {q['id']} cites {t.id} {cited} but no line near it shares a word")
                    continue
                links[t.id][ref].setdefault(q["id"], "source")
                moved = f" (cited as {cited})" if ref != cited else ""
                log.append(f"source  {q['id']} → {t.id} {ref}{moved} ({', '.join(shared[:4])})")
        for italic in re.findall(r"\*([^*]+)\*", expl):
            for words_, key in quotes(italic, roman, ROMAN_WORD, roman_key, 18):
                if is_name(key):
                    continue
                places = roman.places(key)
                if 0 < len(places) <= 2:
                    for t, ref in places:
                        links[t][ref].setdefault(q["id"], "source")
                        log.append(f"source  {q['id']} → {t} {ref} (italic: {words_})")

    data = {t: {ref: sorted([qid, how] for qid, how in qs.items())
                for ref, qs in sorted(refs.items(), key=lambda kv: [int(x) if x.isdigit() else x for x in kv[0].split(".")])}
            for t, refs in sorted(links.items())}
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    n_lines = sum(len(r) for r in data.values())
    n_q = len({qid for r in data.values() for qs in r.values() for qid, _ in qs})
    print(f"{n_lines} lines in {len(data)} texts, asked by {n_q} of {len(questions)} dated questions → {OUT.relative_to(ROOT)}")
    for t, refs in data.items():
        quoted = sum(any(h == "quoted" for _, h in qs) for qs in refs.values())
        print(f"  {t:30} {len(refs):4} lines ({quoted} quoted)")
    if review:
        print("\n".join(log))


if __name__ == "__main__":
    main(review="--review" in sys.argv)
