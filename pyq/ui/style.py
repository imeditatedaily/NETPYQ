"""The few styles Streamlit's theme does not cover."""

import streamlit as st

CSS = """
<style>
/* Trend Insight: the one highlighted box on the page (keyed containers get a st-key-* class). */
[class*="st-key-trend-"] {
  background: rgba(237, 161, 0, 0.10);
  border: 2px solid #eda100;
  border-radius: 0.75rem;
  padding: 1rem 1.25rem 1.25rem;
}
/* The highlighted exam pass on the Subscription page. */
[class*="st-key-pass-card-"][class*="-hot"] {
  background: #eaf1e1;
  border: 2px solid #1d4433 !important;
}
</style>
"""


def inject() -> None:
    st.markdown(CSS, unsafe_allow_html=True)
