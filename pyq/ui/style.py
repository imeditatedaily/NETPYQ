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
</style>
"""


def inject() -> None:
    st.markdown(CSS, unsafe_allow_html=True)
