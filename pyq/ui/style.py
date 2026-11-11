"""The app's colour theme on top of Streamlit's: the same forest green, cream,
lime and amber as the sign-in page, so the two feel like one product."""

import streamlit as st

CSS = """
<style>
:root {
  --g: #1d4433; --g2: #2f6b4f; --lime: #d8f45a; --amber: #eda100; --rust: #c9673a;
  --cream: #f5f0e4; --card: #fbf8f0; --line: #ddd4bf; --ink: #161b15; --muted: #5c6258;
}

/* A coloured band across the top of every page. */
.stMainBlockContainer::before {
  content: ""; display: block; height: .45rem; border-radius: 999px; margin: -0.6rem 0 1.4rem;
  background: linear-gradient(90deg, var(--g) 0%, var(--g2) 40%, var(--lime) 75%, var(--amber) 100%);
}

/* Page titles: serif, green, with a lime underline. */
h1 { color: var(--g) !important; }
.stMainBlockContainer h1::after {
  content: ""; display: block; width: 4.5rem; height: .32rem; margin-top: .45rem;
  background: var(--lime); border-radius: 999px;
}
h2, h3 { color: var(--g2) !important; }

/* Cards: every bordered container gets the sign-in page's card look. */
[data-testid="stVerticalBlockBorderWrapper"]:has(> div > [data-testid="stVerticalBlock"]) {
  border-radius: 1.1rem;
}
.stMainBlockContainer [data-testid="stVerticalBlockBorderWrapper"] {
  background: var(--card);
  box-shadow: 0 1px 0 rgba(29, 68, 51, .04), 0 6px 18px -12px rgba(29, 68, 51, .25);
}

/* Buttons: primary = green with lime text on hover, secondary = outlined green. */
.stButton button[kind="primary"], .stFormSubmitButton button[kind="primary"] {
  background: var(--g); border-color: var(--g); color: #fff; font-weight: 600;
}
.stButton button[kind="primary"]:hover, .stFormSubmitButton button[kind="primary"]:hover {
  background: #163628; border-color: #163628; color: var(--lime);
}
.stMainBlockContainer .stButton button[kind="secondary"] {
  border: 1.5px solid var(--g2); color: var(--g); background: #fff; font-weight: 500;
}
.stMainBlockContainer .stButton button[kind="secondary"]:hover {
  background: #eaf1e1; border-color: var(--g); color: var(--g);
}

/* Metrics: little coloured tiles. */
[data-testid="stMetric"] {
  background: linear-gradient(135deg, #eaf1e1 0%, #f7f9e8 100%);
  border: 1px solid #cfe0c3; border-left: .35rem solid var(--g2);
  border-radius: .9rem; padding: .7rem .9rem;
}
[data-testid="stMetricValue"] { color: var(--g); font-weight: 700; }

/* Segmented controls and tabs: the selected item is green with lime text. */
[data-testid="stButtonGroup"] button[aria-checked="true"], [data-testid="stButtonGroup"] button[kind="segmented_controlActive"] {
  background: var(--g) !important; color: var(--lime) !important; border-color: var(--g) !important;
}
.stTabs [aria-selected="true"] { color: var(--g) !important; }
.stTabs [data-baseweb="tab-highlight"] { background: var(--lime) !important; height: .25rem; }

/* Expanders as soft cards. */
[data-testid="stExpander"] details { background: var(--card); border-radius: .9rem; border-color: var(--line); }
[data-testid="stExpander"] summary:hover { color: var(--g); }

/* Progress bars in brand colours. */
[data-testid="stProgress"] [role="progressbar"] > div > div { background: linear-gradient(90deg, var(--g2), var(--lime)) !important; }

/* Alerts a touch warmer. */
[data-testid="stAlertContentSuccess"] { color: var(--g); }

/* Sidebar: deep green with a lime edge. */
[data-testid="stSidebar"] { border-right: .3rem solid var(--lime); }
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 { color: var(--lime) !important; }
[data-testid="stSidebar"] [data-testid="stMetric"] {
  background: rgba(216, 244, 90, .08); border: 1px solid #3d6b55; border-left: .35rem solid var(--lime);
}
[data-testid="stSidebar"] [data-testid="stMetricValue"] { color: var(--lime); }
[data-testid="stSidebar"] .stButton button { border-color: var(--lime); color: var(--cream); background: transparent; }
[data-testid="stSidebar"] .stButton button:hover { background: var(--lime); color: var(--ink); }

/* Study Notes: a readable column, like a printed page. */
.st-key-nt-body { max-width: 52rem; padding: 1.4rem 1.8rem !important; background: #fffdf7 !important; }
.st-key-nt-body p, .st-key-nt-body li { font-size: 1.06rem; line-height: 1.85; }
.st-key-nt-body h2 { margin-top: 1.6rem; border-bottom: 2px solid var(--lime, #d8f45a); padding-bottom: .2rem; }
.st-key-nt-body blockquote { border-left: .3rem solid var(--g2, #2f6b4f); background: #f3f7ea; padding: .4rem .9rem; }

/* Sanskrit Texts: the lines are set larger than body copy so conjuncts stay readable. */
.st-key-tx-lines p { font-size: 1.14rem; line-height: 1.95; }
.st-key-tx-lines p strong { font-size: .85rem; color: var(--g1, #1d4433); letter-spacing: .02em; }

/* Trend Insight: the one amber box on the page (keyed containers get a st-key-* class). */
[class*="st-key-trend-"] {
  background: linear-gradient(135deg, rgba(237, 161, 0, .14), rgba(216, 244, 90, .12));
  border: 2px solid var(--amber);
  border-radius: 1rem;
  padding: 1rem 1.25rem 1.25rem;
}
/* The Knowledge Base box after an answer: lime-tinted. */
[class*="st-key-kb-"] { background: linear-gradient(135deg, #f1f7dd, var(--card)) !important; border-left: .35rem solid var(--g2); }
/* Locked teasers. */
[class*="st-key-locked-"] { background: linear-gradient(135deg, #1d4433, #2f6b4f) !important; color: var(--cream); }
[class*="st-key-locked-"] p, [class*="st-key-locked-"] [data-testid="stCaptionContainer"] { color: var(--cream) !important; }
/* The highlighted exam pass on the Subscription page. */
[class*="st-key-pass-card-"][class*="-hot"] {
  background: #eaf1e1;
  border: 2px solid var(--g) !important;
}

/* Practice: the score strip as small chips instead of big tiles. */
.st-key-practice-strip [data-testid="stMetric"] { padding: .35rem .7rem; border-left-width: .25rem; min-width: 6.5rem; flex: 1 1 0; }
.st-key-practice-strip [data-testid="stMetricValue"] { font-size: 1.15rem; }
.st-key-practice-strip [data-testid="stMetricLabel"] p { font-size: .75rem; }

/* Answer options as big, tappable cards. */
[data-testid="stForm"] [data-testid="stElementContainer"]:has([data-testid="stRadio"]),
[data-testid="stForm"] [data-testid="stRadio"], [data-testid="stForm"] [data-testid="stRadio"] > div { width: 100% !important; }
[data-testid="stForm"] [data-testid="stRadioGroup"] { gap: .55rem; width: 100%; align-items: stretch; }
[data-testid="stForm"] [data-testid="stRadioGroup"] > div { width: 100%; }
[data-testid="stForm"] [data-testid="stRadioOption"] {
  width: 100%; margin: 0; padding: .8rem 1rem; border: 1.5px solid var(--line); border-radius: .9rem;
  background: #fff; cursor: pointer; transition: border-color .15s, background .15s;
}
[data-testid="stForm"] [data-testid="stRadioOption"]:hover { border-color: var(--g2); background: #f3f7ec; }
[data-testid="stForm"] [data-testid="stRadioOption"]:has(input:checked) {
  border-color: var(--g); background: #eaf1e1; box-shadow: inset .3rem 0 0 var(--g);
}
[data-testid="stForm"] [data-testid="stRadioOption"] p { font-size: 1.02rem; }

/* After submitting: each option as a coloured card. */
[class*="st-key-opt-"] { border-radius: .9rem; padding: .6rem 1rem; margin-bottom: .1rem; border: 1.5px solid var(--line); background: #fff; }
[class*="st-key-opt-right-"] { border-color: #2e8b57; background: #e6f4ea; }
[class*="st-key-opt-right-"] p { color: #1b5e3a; }
[class*="st-key-opt-wrong-"] { border-color: #c0392b; background: #fdecea; }
[class*="st-key-opt-wrong-"] p { color: #8e2a20; }
[class*="st-key-opt-plain-"] p { color: var(--muted); }
[class*="st-key-explain-"] { border-left: .3rem solid var(--lime); padding: .2rem 0 .2rem 1rem; margin-top: .6rem; }

/* On phones the Next / Skip row sticks to the bottom of the screen. */
@media (max-width: 640px) {
  .st-key-practice-nav {
    position: sticky; bottom: 0; z-index: 20; background: var(--cream);
    padding: .6rem .4rem; border-top: 2px solid var(--lime); margin: 0 -1rem; justify-content: center;
  }
  .st-key-practice-strip [data-testid="stMetric"] { min-width: 4.6rem; }
}

/* Home dashboard cards. */
[class*="st-key-home-card-"] { border-radius: 1.1rem; padding: 1.1rem 1.2rem; background: var(--card); border: 1px solid var(--line);
  box-shadow: 0 6px 18px -12px rgba(29, 68, 51, .3); height: 100%; }
.st-key-home-card-continue { background: linear-gradient(135deg, var(--g), var(--g2)); border: 0; }
.st-key-home-card-continue p, .st-key-home-card-continue h3, .st-key-home-card-continue h4 { color: var(--cream) !important; }
.st-key-home-card-continue button { background: var(--lime) !important; color: var(--ink) !important; border: 0 !important; }
.st-key-home-card-continue button p { color: var(--ink) !important; }
[class*="st-key-home-subject-"] { border-radius: 1rem; padding: 1rem 1.1rem; border: 2px solid var(--line); background: #fff; }
[class*="st-key-home-subject-"][class*="-open"] { border-color: var(--g2); background: linear-gradient(135deg, #f1f7dd, #fff); }
</style>
"""

FOCUS = """
<style>
[data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"], [data-testid="stExpandSidebarButton"] { display: none !important; }
.stMainBlockContainer { max-width: 860px; margin: 0 auto; }
</style>
"""


def focus_mode() -> None:
    """Practice without the sidebar: just the question, centred."""
    st.markdown(FOCUS, unsafe_allow_html=True)


def inject() -> None:
    st.markdown(CSS, unsafe_allow_html=True)
