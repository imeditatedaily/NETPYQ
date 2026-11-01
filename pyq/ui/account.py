"""Sign-in with Google, the signed-in user's data, and their subscriptions.

Settings come from Streamlit secrets (.streamlit/secrets.toml locally, the
app's Secrets box on Community Cloud). See SETUP.md for every key.

Development mode (NETPYQ_DEV_MODE=1, or dev_mode = true in secrets) skips
sign-in, uses a local SQLite file and gives full access. Without it, the app
refuses to run until sign-in and the database are configured, so a deploy
with missing secrets never gives the questions away.
"""

import os
import time

import streamlit as st

from .. import store
from ..access import Subscription, unlocked_subjects
from .. import config
from ..payments import PaymentError, Razorpay, needs_refresh
from . import state

DEV_EMAIL = "dev@localhost"


# --- settings ----------------------------------------------------------------------------

def _secret(*path, default=None):
    try:
        node = st.secrets
        for key in path:
            node = node[key]
        return node
    except Exception:   # no secrets file, or key missing
        return default


def dev_mode() -> bool:
    return os.environ.get("NETPYQ_DEV_MODE") == "1" or bool(_secret("dev_mode", default=False))


def admin_emails() -> set[str]:
    return {e.strip().lower() for e in (_secret("admin_emails", default=[]) or [])}


def plan_ids() -> dict[str, str]:
    return dict(_secret("razorpay", "plans", default={}) or {})


def razorpay() -> Razorpay | None:
    key_id, key_secret = _secret("razorpay", "key_id"), _secret("razorpay", "key_secret")
    return Razorpay(key_id, key_secret) if key_id and key_secret else None


@st.cache_resource(show_spinner=False)
def _engine(url: str):
    return store.make_engine(url)


def engine():
    url = _secret("database", "url")
    if not url:
        config.LOCAL_DB_FILE.parent.mkdir(parents=True, exist_ok=True)
        url = f"sqlite:///{config.LOCAL_DB_FILE}"
    return _engine(url)


# --- the gate ----------------------------------------------------------------------------

def _setup_missing() -> list[str]:
    missing = []
    if _secret("auth") is None:
        missing.append("Google sign-in ([auth] section)")
    if not _secret("database", "url"):
        missing.append("the database ([database] url)")
    return missing


def _login_screen() -> None:
    from . import landing
    landing.render()


def gate() -> str:
    """Returns the signed-in user's email, or draws the sign-in screen and stops."""
    if dev_mode():
        email = DEV_EMAIL
    else:
        if missing := _setup_missing():
            st.error("This app isn't fully set up yet. Missing: " + "; ".join(missing) + ". See SETUP.md.",
                     icon=":material/construction:")
            st.stop()
        if not st.user.is_logged_in:
            # Signed out: the sign-in screen plus the public pricing and policy pages.
            from . import legal
            home = st.Page(_login_screen, title="Sign in", icon=":material/login:", default=True)
            st.navigation([home, *legal.st_pages()], position="top").run()
            st.stop()
        email = str(st.user.email).strip().lower()
    _start_user_session(email)
    return email


def _start_user_session(email: str) -> None:
    """Loads this user's saved answers and subscriptions once per browser session."""
    ss = st.session_state
    if ss.get("user") == email:
        return
    ss.user = email
    ss.is_admin = dev_mode() or email in admin_emails()
    ss.run, ss.review = None, None
    try:
        ss.log = store.load_answers(engine(), email)
    except Exception as e:  # the app still works; answers just aren't saved
        ss.log = []
        state.notice(f"Could not load your saved progress: {e}", ":material/error:")
    sync_subscriptions(force=False)


# --- subscriptions -----------------------------------------------------------------------

def subscriptions() -> list[Subscription]:
    return st.session_state.get("subs", [])


def sync_subscriptions(force: bool = True) -> None:
    """Reads this user's subscriptions and asks Razorpay about any whose status may have moved."""
    ss = st.session_state
    now = time.time()
    try:
        subs = store.list_subscriptions(engine(), ss.user)
    except Exception as e:
        state.notice(f"Could not read your subscriptions: {e}", ":material/error:")
        subs = []
    client = razorpay()
    if client:
        fresh = []
        for sub in subs:
            if force or needs_refresh(sub, now):
                try:
                    updated = client.refresh(sub)
                    if updated != sub:
                        sub = store.save_subscription(engine(), updated)
                except PaymentError as e:
                    state.notice(f"Could not check a payment with Razorpay: {e}", ":material/error:")
            fresh.append(sub)
        subs = fresh
    ss.subs = subs
    ss.unlocked = unlocked_subjects(subs, now)


def start_subscription(subject: str) -> None:
    """Callback: creates a Razorpay subscription and remembers its payment link."""
    ss = st.session_state
    client, plan = razorpay(), plan_ids().get(subject)
    if not client or not plan:
        state.notice("Payments for this subject aren't set up yet.", ":material/error:")
        return
    try:
        sub = client.create_subscription(plan, ss.user, subject)
        store.save_subscription(engine(), sub)
    except Exception as e:
        state.notice(f"Could not start the payment: {e}", ":material/error:")
        return
    sync_subscriptions(force=False)
    state.notice("Payment page ready: open it below to pay.", ":material/payments:")


def cancel_subscription(razorpay_id: str) -> None:
    client = razorpay()
    sub = next((s for s in subscriptions() if s.razorpay_id == razorpay_id), None)
    if not client or not sub:
        return
    try:
        store.save_subscription(engine(), client.cancel_at_period_end(sub))
    except Exception as e:
        state.notice(f"Could not cancel: {e}", ":material/error:")
        return
    sync_subscriptions(force=False)
    state.notice("Renewal cancelled. You keep access until the end of the period you paid for.", ":material/check:")


def check_payments() -> None:
    sync_subscriptions(force=True)
    state.notice("Checked your payments with Razorpay.", ":material/sync:")


# --- saving answers ----------------------------------------------------------------------

def save_answer(answer) -> None:
    try:
        store.add_answer(engine(), st.session_state.user, answer)
    except Exception as e:
        state.notice(f"This answer couldn't be saved to your account: {e}", ":material/error:")


def save_all_answers(log) -> None:
    try:
        store.replace_answers(engine(), st.session_state.user, log)
    except Exception as e:
        state.notice(f"Your progress couldn't be saved to your account: {e}", ":material/error:")
