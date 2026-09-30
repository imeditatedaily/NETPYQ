"""UGC NET PYQ Analytical Dashboard: Paper 1, Yoga (100) and Indian Knowledge System (103).

Run locally:  streamlit run streamlit_app.py
"""

import streamlit as st

from pyq.ui import analytics_page, bank_page, library_page, practice_page, review_page, sidebar, state, style

st.set_page_config(page_title="UGC NET PYQ Analytics", page_icon=":material/insights:", layout="wide")
style.inject()
state.init()

PAGES = {
    # The default page always lives at "/", so it takes no url_path.
    "practice": st.Page(practice_page.render, title="Practice", icon=":material/quiz:", default=True),
    "review": st.Page(review_page.render, title="Review Mistakes", icon=":material/replay:", url_path="review"),
    "analytics": st.Page(analytics_page.render, title="Performance Analytics", icon=":material/monitoring:", url_path="analytics"),
    "bank": st.Page(bank_page.render, title="Question Bank", icon=":material/table_chart:", url_path="bank"),
    "library": st.Page(library_page.render, title="Source Library", icon=":material/menu_book:", url_path="library"),
}

page = st.navigation(list(PAGES.values()), position="top")

# Buttons ask for a page change through a callback (state.go); act on it here.
if target := st.session_state.pop("goto", None):
    st.switch_page(PAGES[target])

bank = state.get_bank()
sidebar.render(bank)
state.show_notice()
page.run()
