"""The public landing page shown before sign-in: what a student gets, a
question they can try, pricing and FAQs. Every number on it is counted from
the question bank, so it stays true as papers are added.
"""

from dataclasses import dataclass
from html import escape

import streamlit as st

from ..access import sellable_questions, sellable_subjects
from ..config import SUBJECT_PRICE_INR
from ..syllabus import SUBJECTS
from . import state


@dataclass(frozen=True)
class SubjectStats:
    questions: int
    papers: int
    topics: int
    first_year: int | None
    last_year: int | None


def _stats(bank, subject: str) -> SubjectStats:
    qs = sellable_questions(bank, subject)
    years = [q.exam_year for q in qs if q.exam_year]
    return SubjectStats(len(qs), len({q.session_label for q in qs}), len({q.micro_topic for q in qs}),
                        min(years, default=None), max(years, default=None))


# --- icons: stroke icons painted as CSS backgrounds (st.html strips inline <svg>) -----------

_ICON_PATHS = {
    "paper": '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5"/><path d="M9 13h6M9 17h4"/>',
    "bulb": '<path d="M9 18h6M10 21h4"/><path d="M12 3a6 6 0 0 0-4 10.5c.8.8 1 1.5 1 2.5h6c0-1 .2-1.7 1-2.5A6 6 0 0 0 12 3z"/>',
    "trend": '<path d="M3 17l6-6 4 4 8-8"/><path d="M15 7h6v6"/>',
    "loop": '<path d="M21 12a9 9 0 1 1-3-6.7L21 8"/><path d="M21 3v5h-5"/>',
    "chart": '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
    "grid": '<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/>'
            '<rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>',
}


def _icon_css() -> str:
    from urllib.parse import quote
    rules = []
    for name, paths in _ICON_PATHS.items():
        svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#1d4433" '
               f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{paths}</svg>')
        rules.append(f'.lp-ico.{name} {{ background-image: url("data:image/svg+xml,{quote(svg)}"); }}')
    return "<style>" + "\n".join(rules) + "</style>"


# --- styles ----------------------------------------------------------------------------

CSS = """
<style>
:root {
  --lp-green: #1d4433; --lp-green-2: #2f6b4f; --lp-ink: #161b15; --lp-muted: #5c6258;
  --lp-cream: #f5f0e4; --lp-card: #fbf8f0; --lp-line: #ddd4bf; --lp-lime: #d8f45a; --lp-amber: #eda100;
  --lp-serif: "Fraunces", Georgia, "Times New Roman", serif;
}
/* Wider, calmer canvas for the landing page. */
.block-container { max-width: 1180px; padding-top: 3.2rem; }

.lp-eyebrow { font-size: .78rem; letter-spacing: .22em; text-transform: uppercase; color: var(--lp-green-2);
  font-weight: 600; margin: 0 0 1rem; }
.lp-h1 { font-family: var(--lp-serif); font-weight: 800; font-size: clamp(2.3rem, 5.2vw, 4.1rem);
  line-height: 1.04; letter-spacing: -.02em; color: var(--lp-ink); margin: 0 0 1.2rem; }
.lp-h1 em { display: block; color: var(--lp-green); font-style: italic; }
.lp-lead { font-size: 1.13rem; line-height: 1.65; color: var(--lp-muted); max-width: 36rem; margin: 0 0 .4rem; }
.lp-lead b { color: var(--lp-ink); font-weight: 600; }
.lp-fine { font-size: .86rem; color: var(--lp-muted); margin-top: .2rem; }
.lp-fine { display: flex; flex-wrap: wrap; gap: .3rem 1.1rem; }
.lp-fine span { white-space: nowrap; }
.lp-fine span::before { content: "✓ "; color: var(--lp-green-2); font-weight: 700; }

.lp-maker { display: inline-block; background: var(--lp-lime); color: var(--lp-ink); font-size: .82rem; font-weight: 600;
  border-radius: 999px; padding: .3rem .85rem; margin: -.3rem 0 1.1rem; }

/* Sign-in buttons */
[class*="st-key-lp-signin"] button { border-radius: 999px; padding: .85rem 1.7rem; font-weight: 600;
  font-size: 1rem; border: 0; box-shadow: 0 6px 18px rgba(29, 68, 51, .18); transition: transform .15s ease; }
[class*="st-key-lp-signin"] button:hover { transform: translateY(-1px); }
.st-key-lp-signin-hero button, .st-key-lp-signin-price button { background: var(--lp-green); color: #fff; }
.st-key-lp-signin-hero button:hover, .st-key-lp-signin-price button:hover { background: #163628; color: #fff; }
.st-key-lp-signin-final button { background: var(--lp-lime); color: var(--lp-ink); }
.st-key-lp-signin-final button:hover { background: #cbe84a; color: var(--lp-ink); }

/* Product preview card in the hero */
.lp-preview { background: var(--lp-card); border: 1px solid var(--lp-line); border-radius: 1.25rem;
  padding: 1.35rem 1.4rem; box-shadow: 0 24px 50px -24px rgba(29, 68, 51, .35); transform: rotate(.6deg); }
.lp-preview-top { display: flex; justify-content: space-between; align-items: center; font-size: .78rem;
  color: var(--lp-muted); margin-bottom: .8rem; }
.lp-chip { display: inline-block; background: #e5eedc; color: var(--lp-green); border-radius: 999px;
  padding: .18rem .65rem; font-size: .74rem; font-weight: 600; }
.lp-chip.lime { background: var(--lp-lime); color: var(--lp-ink); }
.lp-q { font-weight: 600; color: var(--lp-ink); line-height: 1.45; margin: 0 0 .8rem; font-size: .98rem; }
.lp-opt { border: 1px solid var(--lp-line); border-radius: .7rem; padding: .5rem .8rem; margin: .4rem 0;
  font-size: .9rem; color: var(--lp-ink); background: #fff; }
.lp-opt.right { border-color: var(--lp-green-2); background: #e9f3e6; font-weight: 600; }
.lp-opt.right::after { content: "  ✓ correct"; color: var(--lp-green-2); font-size: .78rem; }
.lp-insight { margin-top: .9rem; border: 2px solid var(--lp-amber); background: rgba(237, 161, 0, .09);
  border-radius: .8rem; padding: .7rem .9rem; font-size: .84rem; line-height: 1.5; color: var(--lp-ink); }
.lp-insight b { display: block; font-size: .72rem; letter-spacing: .14em; text-transform: uppercase;
  color: #9a6a00; margin-bottom: .2rem; }
.lp-bars { margin-top: .9rem; display: grid; gap: .45rem; font-size: .78rem; color: var(--lp-muted); }
.lp-bar { display: grid; grid-template-columns: 9.5rem 1fr 2.4rem; gap: .6rem; align-items: center; }
.lp-bar i { display: block; height: .5rem; border-radius: 999px; background: #e7e0cf; position: relative; overflow: hidden; }
.lp-bar i::after { content: ""; position: absolute; inset: 0; width: var(--w); background: var(--c); border-radius: 999px; }

/* Stats strip */
.lp-stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 1px;
  background: var(--lp-line); border: 1px solid var(--lp-line); border-radius: 1.1rem; overflow: hidden; margin: 2.6rem 0 1rem; }
.lp-stat { background: var(--lp-card); padding: 1.25rem 1.3rem; }
.lp-stat strong { display: block; font-family: var(--lp-serif); font-size: 2.2rem; font-weight: 700;
  color: var(--lp-green); line-height: 1.1; }
.lp-stat span { font-size: .88rem; color: var(--lp-muted); }

/* Sections */
.lp-section { margin: 4.2rem 0 1.2rem; }
.lp-h2 { font-family: var(--lp-serif); font-weight: 700; font-size: clamp(1.8rem, 3.4vw, 2.6rem);
  line-height: 1.12; letter-spacing: -.015em; color: var(--lp-ink); margin: 0 0 .7rem; }
.lp-h2 em { color: var(--lp-green); }
.lp-sub { color: var(--lp-muted); font-size: 1.05rem; line-height: 1.6; max-width: 44rem; margin: 0 0 1.8rem; }

.lp-vs { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1rem; }
.lp-vs > div { border-radius: 1.1rem; padding: 1.4rem 1.5rem; }
.lp-vs .old { background: #ece5d4; color: var(--lp-muted); }
.lp-vs .new { background: var(--lp-green); color: #eef3e8; }
.lp-vs h4 { font-family: var(--lp-serif); font-size: 1.25rem; margin: 0 0 .8rem; color: inherit; }
.lp-vs .new h4 { color: var(--lp-lime); }
.lp-vs ul { margin: 0; padding-left: 1.1rem; line-height: 1.85; }
.lp-vs .old li { text-decoration: line-through; text-decoration-color: rgba(92, 98, 88, .45); }

.lp-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1rem; }
.lp-card { background: var(--lp-card); border: 1px solid var(--lp-line); border-radius: 1.1rem; padding: 1.4rem 1.4rem 1.3rem;
  transition: transform .2s ease, box-shadow .2s ease; }
.lp-card:hover { transform: translateY(-3px); box-shadow: 0 16px 30px -18px rgba(29, 68, 51, .4); }
.lp-ico { width: 2.6rem; height: 2.6rem; border-radius: .8rem; background: var(--lp-lime); color: var(--lp-green);
  background-repeat: no-repeat; background-position: center; background-size: 1.35rem; margin-bottom: .9rem; }
.lp-card h3 { font-family: var(--lp-serif); font-size: 1.22rem; font-weight: 700; margin: 0 0 .4rem; color: var(--lp-ink); padding: 0; }
.lp-card p { margin: 0; color: var(--lp-muted); line-height: 1.6; font-size: .96rem; }

/* Try-a-question: a pure-CSS quiz (radio buttons + :checked), no script needed */
.lp-try { background: var(--lp-card); border: 1px solid var(--lp-line); border-radius: 1.3rem; padding: 1.6rem 1.7rem; }
.lp-try table { width: 100%; border-collapse: collapse; margin: .4rem 0 1rem; font-size: .93rem; }
.lp-try th { text-align: left; font-size: .75rem; letter-spacing: .1em; text-transform: uppercase; color: var(--lp-green-2);
  border-bottom: 1px solid var(--lp-line); padding: .4rem .5rem; }
.lp-try td { padding: .45rem .5rem; border-bottom: 1px dashed var(--lp-line); vertical-align: top; color: var(--lp-ink); }
.lp-try input { position: absolute; opacity: 0; pointer-events: none; }
.lp-try label { display: block; cursor: pointer; border: 1.5px solid var(--lp-line); background: #fff; border-radius: .8rem;
  padding: .7rem 1rem; margin: .5rem 0; font-weight: 500; color: var(--lp-ink); transition: border-color .15s, background .15s; }
.lp-try label:hover { border-color: var(--lp-green-2); }
.lp-try .fb { display: none; margin-top: 1rem; border-radius: .9rem; padding: 1rem 1.15rem; line-height: 1.6; font-size: .95rem; }
.lp-try .fb.ok { background: #e6f1e1; border: 1.5px solid var(--lp-green-2); }
.lp-try .fb.no { background: #fbeee6; border: 1.5px solid #c9673a; }
#lp-o3:checked ~ label[for="lp-o3"] { border-color: var(--lp-green-2); background: #e6f1e1; }
#lp-o1:checked ~ label[for="lp-o1"], #lp-o2:checked ~ label[for="lp-o2"], #lp-o4:checked ~ label[for="lp-o4"] {
  border-color: #c9673a; background: #fbeee6; }
#lp-o3:checked ~ .fb.ok, #lp-o1:checked ~ .fb.no, #lp-o2:checked ~ .fb.no, #lp-o4:checked ~ .fb.no { display: block; }

/* Steps */
.lp-steps { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1rem; counter-reset: s; }
.lp-step { border-top: 3px solid var(--lp-green); padding: 1.1rem .2rem 0; }
.lp-step::before { counter-increment: s; content: "0" counter(s); font-family: var(--lp-serif); font-style: italic;
  font-size: 2rem; color: var(--lp-green-2); }
.lp-step h3 { font-family: var(--lp-serif); font-size: 1.2rem; margin: .3rem 0 .35rem; padding: 0; }
.lp-step p { color: var(--lp-muted); margin: 0; line-height: 1.6; }

/* Pricing */
.lp-price { background: var(--lp-card); border: 1px solid var(--lp-line); border-radius: 1.2rem; padding: 1.5rem; height: 100%; }
.lp-price.hot { background: var(--lp-green); color: #eef3e8; border-color: var(--lp-green); position: relative; }
.lp-price.hot .lp-badge { position: absolute; top: -.75rem; right: 1.2rem; background: var(--lp-lime); color: var(--lp-ink);
  font-size: .72rem; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; padding: .3rem .7rem; border-radius: 999px; }
.lp-price h3 { font-family: var(--lp-serif); font-size: 1.3rem; margin: 0 0 .1rem; padding: 0; color: inherit; }
.lp-price .code { font-size: .82rem; opacity: .75; }
.lp-price .amt { font-family: var(--lp-serif); font-size: 2.5rem; font-weight: 700; margin: .7rem 0 .1rem; }
.lp-price .amt small { font-family: Inter, sans-serif; font-size: .9rem; font-weight: 500; opacity: .75; }
.lp-price ul { list-style: none; padding: 0; margin: 1rem 0 0; line-height: 1.6; font-size: .94rem; }
.lp-price li { padding: .28rem 0 .28rem 1.5rem; position: relative; }
.lp-price li::before { content: "✓"; position: absolute; left: 0; font-weight: 700; color: var(--lp-green-2); }
.lp-price.hot li::before { color: var(--lp-lime); }
.lp-price.soon { opacity: .7; }
.lp-price.soon .amt { font-size: 1.5rem; }

/* FAQ */
.lp-faq details { border-bottom: 1px solid var(--lp-line); padding: 1rem .2rem; }
.lp-faq summary { cursor: pointer; font-weight: 600; font-size: 1.04rem; color: var(--lp-ink); list-style: none; }
.lp-faq summary::-webkit-details-marker { display: none; }
.lp-faq summary::after { content: "+"; float: right; font-size: 1.3rem; color: var(--lp-green-2); line-height: 1; }
.lp-faq details[open] summary::after { content: "–"; }
.lp-faq details p { color: var(--lp-muted); margin: .6rem 0 0; line-height: 1.65; }

/* Final call to action: a keyed Streamlit container painted as a green band */
.st-key-lp-final { background: var(--lp-green); border-radius: 1.6rem; padding: 3rem 2rem 2.6rem; margin: 4.5rem 0 1rem;
  text-align: center; align-items: center; }
.lp-final-h { font-family: var(--lp-serif); font-weight: 800; color: #fff; font-size: clamp(1.9rem, 3.8vw, 2.9rem);
  line-height: 1.12; margin: 0 0 .6rem; }
.lp-final-h em { color: var(--lp-lime); }
.lp-final-p { color: #cfdcc9; font-size: 1.05rem; margin: 0 auto .4rem; max-width: 36rem; }
.lp-foot { text-align: center; color: var(--lp-muted); font-size: .82rem; margin: 1.5rem 0 .5rem; }

@media (max-width: 640px) {
  .lp-preview { transform: none; }
  .lp-bar { grid-template-columns: 7rem 1fr 2.2rem; }
  .st-key-lp-final { padding: 2.2rem 1.1rem; }
}
</style>
"""


# --- sections --------------------------------------------------------------------------

def _years(s: SubjectStats) -> str:
    if not s.first_year:
        return ""
    return str(s.first_year) if s.first_year == s.last_year else f"{s.first_year}–{s.last_year}"


def _hero_copy(total: int, papers: int, years: str) -> str:
    span = f" ({years})" if years else ""
    return f"""
<p class="lp-eyebrow">UGC NET · Yoga (100) · Paper 1 · IKS (103)</p>
<p class="lp-maker">Built by a doctoral fellow in the science of yoga</p>
<h1 class="lp-h1">Every question NTA has asked.<em>Every answer explained.</em></h1>
<p class="lp-lead">Practise <b>{total} real previous-year questions</b> from <b>{papers} UGC NET papers</b>{span}, each mapped
to its syllabus unit and micro-topic. Every option gets an explanation, so you learn why the wrong answers are wrong too.</p>
"""


PREVIEW = """
<div class="lp-preview">
  <div class="lp-preview-top"><span class="lp-chip">Yoga · Unit 4 · Patañjala Yoga Sūtra</span><span>Match List I with List II</span></div>
  <p class="lp-q">Match each kleśa with the way the Yoga Sūtra defines it.</p>
  <div class="lp-opt">(1) A-IV, B-II, C-III, D-I</div>
  <div class="lp-opt right">(3) A-II, B-IV, C-III, D-I</div>
  <div class="lp-insight"><b>Trend insight</b>The kleśa block (YS 2.2–2.13) is a closed, countable set, so NTA tests it
    through Match-the-List and Sequence items. Trap: <i>sukhānuśayī</i> (rāga) vs <i>duḥkhānuśayī</i> (dveṣa).</div>
  <div class="lp-bars">
    <div class="lp-bar"><span>Patañjala Yoga Sūtra</span><i style="--w:86%;--c:#2f6b4f"></i><span>86%</span></div>
    <div class="lp-bar"><span>Hatha Yoga texts</span><i style="--w:68%;--c:#eda100"></i><span>68%</span></div>
    <div class="lp-bar"><span>Yoga Upanishads</span><i style="--w:44%;--c:#c9673a"></i><span>44%</span></div>
  </div>
</div>
"""


def _stats_strip(yoga: SubjectStats, total_papers: int, topics: int) -> str:
    items = [
        (f"{yoga.questions}", "Yoga (100) previous-year questions"),
        (f"{total_papers}", "full exam papers, tagged by year"),
        (f"{topics}", "micro-topics tracked for you"),
        (f"₹{SUBJECT_PRICE_INR}", "a month per subject. Cancel anytime"),
    ]
    return '<div class="lp-stats">' + "".join(
        f'<div class="lp-stat"><strong>{escape(n)}</strong><span>{escape(t)}</span></div>' for n, t in items) + "</div>"


VERSUS = """
<div class="lp-section">
  <h2 class="lp-h2">Stop collecting PDFs. <em>Start closing gaps.</em></h2>
  <p class="lp-sub">Most NET preparation is a folder of question papers and an answer key. You find out what you got
  wrong, never why, and the same topic catches you again next attempt.</p>
  <div class="lp-vs">
    <div class="old"><h4>The usual way</h4><ul>
      <li>Scanned papers with a bare answer key</li>
      <li>No idea which topics NTA keeps repeating</li>
      <li>Mistakes forgotten by next week</li>
      <li>Progress lives in a notebook</li></ul></div>
    <div class="new"><h4>With NET PYQ Practice</h4><ul>
      <li>An explanation for every option, not just the key</li>
      <li>Trend insight for each micro-topic: targets, traps, prep move</li>
      <li>Wrong answers come back until you get them right</li>
      <li>Accuracy by unit and topic, saved to your account</li></ul></div>
  </div>
</div>
"""


def _features() -> str:
    cards = [
        ("paper", "Real papers, not guesswork",
         "Questions from official UGC NET papers, tagged by exam session, unit and micro-topic. Filter by year to sit a full paper."),
        ("bulb", "Explanations that teach",
         "Why the right answer is right, why each distractor fails, and the key facts from the knowledge base for that topic."),
        ("trend", "Know what the examiner wants",
         "Trend insight on every topic: how NTA frames it, the traps it sets, and one prep move that pays off."),
        ("loop", "A mistake-review loop",
         "Every question you miss lands in Review Mistakes. Clear the list and you've closed your weakest gaps."),
        ("chart", "Analytics that tell you what to revise",
         "Accuracy by unit and micro-topic. Weak topics show in red, needs-revision in amber, so you always know where to spend the next hour."),
        ("grid", "Every NTA format",
         "Single answer, Match List I with List II, Assertion–Reason, multiple statements and sequence questions, exactly as they appear in the exam."),
    ]
    body = "".join(f'<div class="lp-card"><div class="lp-ico {i}"></div><h3>{escape(t)}</h3><p>{escape(d)}</p></div>'
                   for i, t, d in cards)
    return f"""
<div class="lp-section">
  <p class="lp-eyebrow">What you get</p>
  <h2 class="lp-h2">Everything you need to <em>crack the paper</em>, in one place.</h2>
  <div class="lp-grid">{body}</div>
</div>
"""


TRY = """
<div class="lp-section">
  <p class="lp-eyebrow">Try one now · no sign-in</p>
  <h2 class="lp-h2">See how it works <em>before you sign up.</em></h2>
  <p class="lp-sub">A question in NTA's Match-the-List format. Pick an answer to see the explanation.</p>
  <div class="lp-try">
    <p class="lp-q">Match List I (kleśa) with List II (how the Yoga Sūtra defines it).</p>
    <table>
      <tr><th>List I: Kleśa</th><th>List II: Definition</th></tr>
      <tr><td>A. Avidyā</td><td>I. Clinging to life, flowing by its own momentum, present even in the learned</td></tr>
      <tr><td>B. Asmitā</td><td>II. Taking the impermanent, impure, painful and non-self to be permanent, pure, pleasant and the self</td></tr>
      <tr><td>C. Rāga</td><td>III. That which follows in the wake of pleasure</td></tr>
      <tr><td>D. Abhiniveśa</td><td>IV. The power of the seer and the power of seeing appearing as a single self</td></tr>
    </table>
    <input type="radio" name="lp-q" id="lp-o1"><input type="radio" name="lp-q" id="lp-o2">
    <input type="radio" name="lp-q" id="lp-o3"><input type="radio" name="lp-q" id="lp-o4">
    <label for="lp-o1">(1) A-IV, B-II, C-III, D-I</label>
    <label for="lp-o2">(2) A-II, B-III, C-IV, D-I</label>
    <label for="lp-o3">(3) A-II, B-IV, C-III, D-I</label>
    <label for="lp-o4">(4) A-I, B-IV, C-II, D-III</label>
    <div class="fb ok"><b>Correct: (3).</b> Avidyā is defined in YS 2.5 as mistaking the impermanent for the permanent (II);
      asmitā in 2.6 as seer and instrument appearing as one (IV); rāga in 2.7 as what follows pleasure (III); abhiniveśa
      in 2.9 as the will to live that grips even the learned (I). Notice that dveṣa was left out of List I: a favourite
      way to build distractors.<br><br><i>Inside the app, every question also shows a trend insight, key facts and your topic accuracy.</i></div>
    <div class="fb no"><b>Not quite. The answer is (3) A-II, B-IV, C-III, D-I.</b> The classic trap is swapping avidyā and
      asmitā, since both describe a misidentification: avidyā is the general error (YS 2.5), asmitā the specific fusion of
      seer and instrument (2.6). Inside the app, this question would now wait for you in <b>Review Mistakes</b>.</div>
  </div>
</div>
"""

STEPS = """
<div class="lp-section">
  <p class="lp-eyebrow">How it works</p>
  <h2 class="lp-h2">From sign-in to <em>first question</em> in under a minute.</h2>
  <div class="lp-steps">
    <div class="lp-step"><h3>Sign in with Google</h3><p>One tap. No form, no password. Your progress is saved to your account.</p></div>
    <div class="lp-step"><h3>Try the free questions</h3><p>Practise the sample questions with full explanations and analytics, free.</p></div>
    <div class="lp-step"><h3>Unlock your subject</h3><p>Pay by UPI, card or net banking on Razorpay's secure page. Every real paper for that subject opens straight away.</p></div>
  </div>
</div>
"""


def _price_card(subject: str, s: SubjectStats, hot: bool) -> str:
    info = SUBJECTS[subject]
    general = not info.code.isdigit()          # Paper 1 has no subject code
    title = info.code if general else info.name
    sub = "Teaching &amp; Research Aptitude" if general else f"Code {escape(info.code)}"
    if not s.questions:
        return (f'<div class="lp-price soon"><h3>{escape(title)}</h3><div class="code">{sub}</div>'
                '<div class="amt">Coming soon</div><ul><li>Real papers are being added</li>'
                '<li>Free sample questions available now</li></ul></div>')
    years = _years(s)
    span = f" ({years})" if years else ""
    paper_word = "paper" if s.papers == 1 else "papers"
    return f"""<div class="lp-price{' hot' if hot else ''}">{'<span class="lp-badge">Most questions</span>' if hot else ''}
<h3>{escape(title)}</h3><div class="code">{sub}</div>
<div class="amt">₹{SUBJECT_PRICE_INR}<small> / month</small></div>
<ul><li>{s.questions} real questions from {s.papers} {paper_word}{span}</li><li>{s.topics} micro-topics with trend insight</li>
<li>Explanations, review loop and analytics</li><li>Cancel anytime, keep access to period end</li></ul></div>"""


FREE_CARD = """<div class="lp-price"><h3>Free</h3><div class="code">For everyone who signs in</div>
<div class="amt">₹0</div><ul><li>Sample questions in every NTA format</li><li>Full explanations and trend insight</li>
<li>Progress saved to your account</li><li>No card needed</li></ul></div>"""


def _faq(years_by_subject: dict[str, str]) -> str:
    covered = "; ".join(f"{SUBJECTS[k].name}: {v}" for k, v in years_by_subject.items() if v) or "being added"
    qa = [
        ("Are these the real UGC NET questions?",
         "Yes. Every question in a paid subject comes from an actual UGC NET paper, checked against the official "
         "answer key, and is tagged with its exam session. The free samples are written in NTA's pattern and are "
         "marked as such. We are not affiliated with NTA or UGC."),
        ("Which exam sessions are covered?", f"Right now: {covered}. New papers are added to your subject at no extra cost."),
        ("How do I pay, and can I cancel?",
         f"₹{SUBJECT_PRICE_INR} a month per subject, paid by UPI, debit or credit card, or net banking on Razorpay's "
         "secure page. It renews monthly until you cancel on the Subscription page, and you keep access until the end "
         "of the month you paid for."),
        ("Do I need a separate plan for Paper 1?",
         "Each subject is its own plan, so you pay only for what you're preparing. Most candidates take Paper 1 "
         "plus one Paper 2 subject."),
        ("Can I use it on my phone?",
         "Yes. It works in any browser, and because progress is saved to your Google sign-in you can switch between "
         "phone and laptop and carry on where you left off."),
    ]
    body = "".join(f"<details><summary>{escape(q)}</summary><p>{escape(a)}</p></details>" for q, a in qa)
    return f'<div class="lp-section lp-faq"><p class="lp-eyebrow">Questions</p><h2 class="lp-h2">Before you <em>start</em></h2>{body}</div>'


# --- page ------------------------------------------------------------------------------

def _signin(key: str, label: str = "Start free with Google") -> None:
    st.button(label, key=key, icon=":material/login:", on_click=st.login, args=("google",))


def render() -> None:
    bank = state.get_full_bank()
    stats = {s: _stats(bank, s) for s in SUBJECTS}
    live = sellable_subjects(bank)
    sellable = [q for s in live for q in sellable_questions(bank, s)]
    total_papers = len({(q.subject, q.session_label) for q in sellable})
    topics = len({q.micro_topic for q in sellable})
    years = [q.exam_year for q in sellable if q.exam_year]
    span = f"{min(years)}–{max(years)}" if years and min(years) != max(years) else (str(years[0]) if years else "")
    biggest = max(live, key=lambda s: stats[s].questions, default=None)
    yoga = stats.get("yoga", SubjectStats(0, 0, 0, None, None))

    st.html(CSS + _icon_css())

    left, right = st.columns([1.15, 1], gap="large", vertical_alignment="center")
    with left:
        st.html(_hero_copy(len(sellable), total_papers, span))
        _signin("lp-signin-hero")
        st.html('<p class="lp-fine"><span>Free sample questions</span><span>No card to start</span>'
                '<span>Works on phone</span></p>')
    with right:
        st.html(PREVIEW)

    st.html(_stats_strip(yoga, total_papers, topics))
    st.html(VERSUS)
    st.html(_features())
    st.html(TRY)
    st.html(STEPS)

    st.html('<div class="lp-section"><p class="lp-eyebrow">Pricing</p><h2 class="lp-h2">Pay only for the subject '
            '<em>you\'re taking.</em></h2><p class="lp-sub">One simple monthly plan per subject. No bundles, no '
            'lock-in.</p></div>')
    order = ["free", *SUBJECTS]
    cols = st.columns(len(order), gap="small")
    for col, key in zip(cols, order):
        with col:
            st.html(FREE_CARD if key == "free" else _price_card(key, stats[key], key == biggest))
    _signin("lp-signin-price", "Start free, upgrade when ready")

    st.html(_faq({s: _years(stats[s]) for s in SUBJECTS}))

    with st.container(key="lp-final"):
        st.html('<h2 class="lp-final-h">The best predictor of the next paper<br><em>is every paper before it.</em></h2>'
                '<p class="lp-final-p">Written and checked by a doctoral fellow in the science of yoga. Sign in, try the free questions, and see your weak topics within your first session.</p>')
        _signin("lp-signin-final", "Start practising free")
    st.html('<p class="lp-foot">Sign-in uses only your Google name and email, to save your progress. '
            'Not affiliated with the National Testing Agency (NTA) or the University Grants Commission (UGC). '
            'See Pricing, Privacy Policy and Terms in the menu above.</p>')
