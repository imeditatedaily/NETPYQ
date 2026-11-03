"""Public pages anyone can open without signing in: pricing and the policies
Google (OAuth consent screen) and Razorpay (account activation) ask for.

Business details come from the [business] section of secrets:

    [business]
    name = "Your legal name or business name"
    email = "support@example.com"
    phone = "+91 ..."
    address = "City, State, India"

Missing values fall back to the first admin email and "India".
"""

import streamlit as st

from ..access import free_paper_label
from ..config import PASS_DAYS, PASSES, SUBJECT_PRICE_INR

APP_NAME = "UGC NET PYQ Practice"
UPDATED = "1 November 2026"


def _biz(key: str, default: str = "") -> str:
    try:
        value = st.secrets["business"][key]
        return str(value) if value else default
    except Exception:
        return default


def details() -> dict[str, str]:
    try:
        admins = list(st.secrets.get("admin_emails", []))
    except Exception:
        admins = []
    email = _biz("email", admins[0] if admins else "")
    return {
        "name": _biz("name", f"the operator of {APP_NAME}"),
        "email": email,
        "phone": _biz("phone"),
        "address": _biz("address", "India"),
    }


def _footer() -> None:
    d = details()
    st.divider()
    st.caption(f"{APP_NAME} is operated by {d['name']}, {d['address']}. Contact: {d['email']}"
               + (f", {d['phone']}" if d["phone"] else "") + f". Last updated {UPDATED}. "
               "Not affiliated with the National Testing Agency (NTA) or the University Grants Commission (UGC).")


def pricing() -> None:
    st.title("Pricing")
    st.markdown(f"""
{APP_NAME} is an online practice service for the UGC NET exam: real previous-year questions mapped to the
syllabus, a detailed explanation for every answer, a mistake-review loop and topic-wise performance analytics.

| Plan | Price | What you get |
|---|---|---|
| Free | ₹0 | Sign in with Google: two full real papers ({free_paper_label()}) and the sample questions |
| Exam pass, one subject | **₹{PASSES['yoga'][1]:,} once** | {PASS_DAYS // 30} months of every previous-year question for that subject, mock tests, explanations, review and analytics. Does not renew |
| Exam pass, Paper 1 + Yoga | **₹{PASSES['combo'][1]:,} once** | The same for both papers, for {PASS_DAYS // 30} months. Does not renew |
| Monthly, one subject | **₹{SUBJECT_PRICE_INR} per month** | Every previous-year question loaded for that subject (for example Yoga, code 100), renewed monthly until you cancel |

- An exam pass is a single payment and gives access for {PASS_DAYS} days from the day it is paid.
- Each monthly plan covers one subject. Subscribe to as many as you need.
- Prices are in Indian rupees and include any applicable taxes.
- Payment is by UPI, debit/credit card or net banking through Razorpay. The subscription renews every
  month until you cancel it on the Subscription page, and runs for at most 12 months.
- **No refunds.** Payments are final once made. Try the free paper first.
- Access starts as soon as the payment is confirmed.
""")
    _footer()


def privacy() -> None:
    d = details()
    st.title("Privacy Policy")
    st.markdown(f"""
This policy explains what {APP_NAME} ("we", "the service") collects, why, and your choices. It is written to
meet India's Digital Personal Data Protection Act, 2023.

**What we collect**

- **Your Google account name and email address**, when you sign in with Google. We do not receive your
  Google password or any other Google data.
- **Your practice history**: which questions you answered, the option you chose, whether it was correct, and
  when. This powers your score, review list and analytics.
- **Subscription records**: which subject you subscribed to, the Razorpay subscription ID, its status and
  the date your paid period ends.

**What we do not collect.** Card numbers, UPI IDs, bank details and other payment information are entered
on Razorpay's secure page and handled by Razorpay, never by us.

**How we use it.** Only to sign you in, keep your progress, unlock the subjects you pay for, provide
support, and keep the service secure. We do not sell your data or use it for advertising.

**Who processes it for us.** Google (sign-in), Razorpay (payments), Supabase (database) and Render
(hosting). Some of these providers may store data outside India.

**How long we keep it.** For as long as your account is in use. Payment records may be kept longer where the
law requires.

**Your rights.** You can see your progress in the app at any time, clear it with
*Clear my progress*, and ask us for a copy of your data, or to correct or delete it, by writing to **{d['email']}**. We reply
within 30 days.

**Cookies.** We use one cookie to keep you signed in. No advertising or tracking cookies.

**Grievance officer.** {d['name']}, {d['email']}{', ' + d['phone'] if d['phone'] else ''}.

We may update this policy; the date below shows the latest version.
""")
    _footer()


def terms() -> None:
    d = details()
    st.title("Terms and Conditions")
    st.markdown(f"""
By signing in to or paying for {APP_NAME} you agree to these terms.

1. **The service.** Online practice with UGC NET previous-year questions, explanations and analytics. It
   is a study aid. We work to keep answers and explanations accurate, but some answers are marked
   *unverified* where no official key exists, and we cannot guarantee any exam result.
2. **Your account.** You sign in with your own Google account. A subscription is for one person: do not
   share your account or copy, download in bulk, resell or republish the questions or explanations.
3. **Subscriptions and payment.** An exam pass is a single payment for {PASS_DAYS} days of access and does not
   renew. A monthly plan costs ₹{SUBJECT_PRICE_INR} per subject per month, charged through Razorpay and renewed
   automatically every month (for at most 12 months) until you cancel. **Payments are
   non-refundable**, except for billing errors. See the Pricing and the Cancellation and Refund Policy pages.
4. **Availability.** We aim to keep the service running but it may occasionally be unavailable for
   maintenance or reasons outside our control.
5. **Changes.** We may change these terms or prices with notice on this site. A price change applies from
   your next billing period.
6. **Ending access.** We may suspend accounts that break these terms (for example, sharing or copying
   content).
7. **Liability.** To the extent the law allows, our total liability is limited to the amount you paid in the
   last month.
8. **Not affiliated.** We are independent and not connected with the NTA or UGC.
9. **Law.** These terms are governed by the laws of India.

Questions: **{d['email']}**.
""")
    _footer()


def refund() -> None:
    d = details()
    st.title("Cancellation and Refund Policy")
    st.markdown(f"""
**Exam passes** are a single payment and never renew, so there is nothing to cancel. Access ends {PASS_DAYS}
days after payment.

**Cancelling a monthly plan.** You can cancel a subscription at any time on the **Subscription** page (*Cancel renewal*)
or by writing to {d['email']}. No further payments are taken, and you keep access until the end of the month
you have already paid for.

**No refunds.** Access to the full question bank starts the moment your payment is confirmed, so **all
payments are final and non-refundable**, including partly used months. Please try the free paper
before you subscribe. Cancelling stops future payments; it does not refund the current month.

**Billing errors.** The only exception is a mistake in the charge itself: if you were charged twice for the
same subject and month, charged after you cancelled, or paid but the subject never unlocked and we could not
fix it, write to **{d['email']}** with your sign-in email and the Razorpay payment ID. We return the wrong
charge to the original payment method within **5–7 business days**.
""")
    _footer()


def shipping() -> None:
    st.title("Shipping and Delivery Policy")
    st.markdown(f"""
{APP_NAME} is a purely online service. **Nothing is shipped.** After payment is confirmed, the subject is
unlocked in your account straight away, usually within a minute. If it isn't, press *I've paid: check now*
on the Subscription page, or contact us and we will fix it (or, if we can't, return the payment).
""")
    _footer()


def contact() -> None:
    d = details()
    st.title("Contact Us")
    st.markdown(f"""
- **Operated by:** {d['name']}
- **Email:** {d['email']}
{('- **Phone:** ' + d['phone']) if d['phone'] else ''}
- **Address:** {d['address']}

We reply to emails within 2 working days.
""")
    _footer()


PAGES = [
    ("pricing", pricing, "Pricing", ":material/sell:"),
    ("privacy", privacy, "Privacy Policy", ":material/shield:"),
    ("terms", terms, "Terms", ":material/gavel:"),
    ("refund", refund, "Cancellation & Refunds", ":material/currency_rupee:"),
    ("shipping", shipping, "Shipping & Delivery", ":material/local_shipping:"),
    ("contact", contact, "Contact Us", ":material/mail:"),
]


def st_pages() -> list:
    return [st.Page(fn, title=title, icon=icon, url_path=path) for path, fn, title, icon in PAGES]
