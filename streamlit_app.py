"""UGC NET PYQ practice: Paper 1, Yoga (100) and Indian Knowledge System (103).

Users sign in with Google; each subject unlocks with a monthly Razorpay plan.

Run locally without sign-in or payments:  NETPYQ_DEV_MODE=1 streamlit run streamlit_app.py
"""

import streamlit as st

from pyq.filters import ALL
from pyq.syllabus import SUBJECTS
from pyq.ui import (account, admin_page, analytics_page, bank_page, knowledge_page, legal, library_page, plans_page,
                    practice_page, review_page, sidebar, state, style)

st.set_page_config(page_title="UGC NET PYQ Practice", page_icon=":material/insights:", layout="wide")
style.inject()
state.init()
account.gate()            # stops here with the sign-in screen until the user is signed in
admin = st.session_state.is_admin

PAGES = {
    # The default page always lives at "/", so it takes no url_path.
    "practice": st.Page(practice_page.render, title="Practice", icon=":material/quiz:", default=True),
    "review": st.Page(review_page.render, title="Review Mistakes", icon=":material/replay:", url_path="review"),
    "analytics": st.Page(analytics_page.render, title="Performance Analytics", icon=":material/monitoring:", url_path="analytics"),
    "knowledge": st.Page(knowledge_page.render, title="Knowledge Base", icon=":material/school:", url_path="knowledge"),
    "bank": st.Page(bank_page.render, title="Question Bank", icon=":material/table_chart:", url_path="bank"),
    "plans": st.Page(plans_page.render, title="Subscription", icon=":material/workspace_premium:", url_path="plans"),
}
if admin:   # the Source Library lists the owner's own Drive files and notes
    PAGES["library"] = st.Page(library_page.render, title="Source Library", icon=":material/menu_book:", url_path="library")
    PAGES["admin"] = st.Page(admin_page.render, title="Admin", icon=":material/admin_panel_settings:", url_path="admin")

# Pricing and policies stay reachable after sign-in, in a "Help" menu.
HELP = dict(zip((p[0] for p in legal.PAGES), legal.st_pages()))
page = st.navigation({"": list(PAGES.values()), "Help": list(HELP.values())}, position="top")

# Buttons ask for a page change through a callback (state.go); act on it here.
if (target := st.session_state.pop("goto", None)) and (target in PAGES or target in HELP):
    st.switch_page(PAGES.get(target) or HELP[target])

bank = state.get_bank()
sidebar.render(bank)
state.show_notice()

# Tell a user who hasn't unlocked the subject they're looking at how to get it.
if not admin and page.url_path not in ("plans", *HELP):
    subject, unlocked = st.session_state.f_subject, st.session_state.unlocked
    if subject != ALL and subject not in unlocked:
        with st.container(border=True, horizontal=True, vertical_alignment="center"):
            st.markdown(f":material/lock: **{SUBJECTS[subject].display}** is locked. You can try the free sample "
                        "questions; subscribe to practise every real paper.")
            st.button("See plans", icon=":material/workspace_premium:", on_click=state.go, args=("plans",))
    elif subject == ALL and not unlocked:
        with st.container(border=True, horizontal=True, vertical_alignment="center"):
            st.markdown(":material/lock: You're using the **free sample questions**. Subscribe to a subject to "
                        "practise its real previous-year papers.")
            st.button("See plans", icon=":material/workspace_premium:", on_click=state.go, args=("plans",))

page.run()
