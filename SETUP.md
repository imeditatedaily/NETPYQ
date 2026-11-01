# Going live: sign-in, saved progress and ₹500/month subscriptions

The code is ready. These steps create the accounts it needs. Do them in this
order; each one gives you a few values to paste into **one secrets file** at the
end (step 6). Never put those values in GitHub.

| Step | What | Cost | Time |
|---|---|---|---|
| 1 | Make the GitHub repo private | free | 1 min |
| 2 | Database (Supabase) | free plan | 5 min |
| 3 | Hosting (Render) | free plan sleeps when idle; a paid plan stays on | 10 min |
| 4 | Google sign-in (Google Cloud) | free | 10 min |
| 5 | Payments (Razorpay) | a fee per payment, no monthly fee | 15 min + KYC review |
| 6 | Paste the secrets and test | | 10 min |

> **Why not Streamlit Community Cloud?** Its terms do not allow business or
> commercial use, so a paid app can't be hosted there. Render runs the same app.

## 1. Make the repo private

Anyone can currently download every question from GitHub for free.

GitHub → **imeditatedaily/NETPYQ** → **Settings** → **General** → scroll to
**Danger Zone** → **Change visibility** → **Make private**.

## 2. Database: Supabase (keeps every user's progress and subscriptions)

1. Go to **supabase.com** → **Start your project** → sign in with GitHub.
2. **New project**. Name: `netpyq`. Region: **Mumbai (ap-south-1)**. Choose a
   database password and **write it down**.
3. When the project is ready, click **Connect** (top of the page).
4. Under **Session pooler**, copy the connection string. It looks like
   `postgresql://postgres.abcd:[YOUR-PASSWORD]@aws-0-ap-south-1.pooler.supabase.com:5432/postgres`.
   Replace `[YOUR-PASSWORD]` with your password. This is your **database url**.

   Use the *Session pooler* one, not *Direct connection*: the direct one needs
   IPv6, which many hosts don't have.

The app creates its two tables (`answers`, `subscriptions`) by itself on first run.

## 3. Hosting: Render

1. Go to **render.com** → **Get Started** → sign in with GitHub as
   **imeditatedaily**, and allow Render to see the **NETPYQ** repository.
2. **New** → **Blueprint** → choose **NETPYQ** → **Apply**. Render reads
   `render.yaml` from the repo (Python 3.14, Singapore region, always-on plan).
   To start free, change the plan to **Free** before applying: the app then
   sleeps after a few idle minutes and takes about a minute to wake.
3. When it's created, note the app's address, for example
   `https://netpyq.onrender.com`. This is your **app URL**. (You can add your own
   domain later under **Settings → Custom Domains**.)

The first deploy will show "This app isn't fully set up yet". That's expected
until step 6.

## 4. Google sign-in: Google Cloud

1. Go to **console.cloud.google.com** and sign in with your Gmail.
2. Top bar → project picker → **New project** → name `netpyq` → **Create**, then select it.
3. Menu → **APIs & Services** → **OAuth consent screen** (also called
   **Google Auth Platform**) → **Get started**.
   - App name: `UGC NET PYQ Practice`; support email: yours.
   - Audience: **External**.
   - Finish, then open **Audience** and click **Publish app** so that *any*
     Gmail user can sign in, not only test users. The app asks only for name and
     email, so Google doesn't need to review it.
4. **Clients** → **Create client** → type **Web application** → name `netpyq`.
   Under **Authorized redirect URIs** add:
   - `https://YOUR-APP-URL/oauth2callback` (for example `https://netpyq.onrender.com/oauth2callback`)
   - `http://localhost:8501/oauth2callback` (only if you'll test on your computer)
5. **Create**. Copy the **Client ID** and **Client secret**.

## 5. Payments: Razorpay

1. Sign up at **razorpay.com** and complete **account activation (KYC)**: PAN,
   bank account and business details. For a website, Razorpay checks that it has
   **Terms & Conditions, Privacy Policy, Cancellation & Refund Policy, Contact Us
   and Pricing** pages. Ask Claude to add these pages to the app; they need your
   legal name, address, phone and email.
2. Turn on **Subscriptions** (Dashboard → Products / Subscriptions). If you want
   **UPI Autopay**, ask Razorpay support to enable it on your account.
3. Start in **Test mode** (switch at the top of the dashboard).
4. **Subscriptions → Plans → Create plan**, once per subject you want to sell:
   - Plan name: `Yoga (100) – monthly`; billing frequency: **every 1 month**;
     amount: **₹500**.
   - Copy the **Plan ID** (`plan_…`).
   - Right now only **Yoga** has real papers to sell. IKS and Paper 1 show
     "Coming soon" until real papers are added, so their plans can wait.
5. **Account & Settings → API Keys → Generate key**. Copy the **Key ID**
   (`rzp_test_…`) and **Key Secret**.

Subscriptions run for 12 months, then end; the student can subscribe again from
the Subscription page.

## 6. Paste the secrets and test

In Render → your **netpyq** service → **Environment** → **Secret Files** →
**Add Secret File**. Filename: `secrets.toml`. Contents (fill in your values):

```toml
# Emails that get full access free, plus the Admin page and Source Library.
admin_emails = ["vridhiitl@gmail.com"]

[auth]
redirect_uri = "https://YOUR-APP-URL/oauth2callback"
cookie_secret = "TYPE-40-OR-MORE-RANDOM-LETTERS-AND-NUMBERS-HERE"

[auth.google]
client_id = "….apps.googleusercontent.com"
client_secret = "GOCSPX-…"
server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration"

[database]
url = "postgresql://postgres.abcd:YOURPASSWORD@aws-0-ap-south-1.pooler.supabase.com:5432/postgres"

[razorpay]
key_id = "rzp_test_…"
key_secret = "…"

[razorpay.plans]
yoga = "plan_…"
# iks = "plan_…"       # add when IKS papers are in
# paper1 = "plan_…"    # add when official Paper 1 papers are in
```

Save. Render redeploys. Then test:

1. Open the app URL in a private/incognito window and **Sign in with Google**
   with an email that is *not* in `admin_emails`. You should see the free sample
   questions and a "See plans" banner.
2. **Subscription → Subscribe for ₹500/month (Yoga)** → **Pay ₹500 on Razorpay**.
   In test mode, pay with a Razorpay test card or test UPI ID (listed in
   Razorpay's docs under *Test card details*).
3. Back in the app, press **I've paid: check now**. Yoga unlocks.
4. Answer a question, refresh the page: your progress is still there.
5. Sign in with your admin email and open **Admin**: the test subscription is listed.

**Going live:** in Razorpay switch to **Live mode**, create the same plans
again (live plans have new IDs), generate **live** API keys, and replace
`key_id`, `key_secret` and the plan IDs in the secret file.

## Running it on your computer

```bash
pip install -r requirements-dev.txt
NETPYQ_DEV_MODE=1 streamlit run streamlit_app.py    # no sign-in, full access, local SQLite file
pytest
```

Without `NETPYQ_DEV_MODE=1` (or `dev_mode = true` in `.streamlit/secrets.toml`),
the app refuses to start until sign-in and the database are set up, so a deploy
with missing secrets never gives the questions away.

## How access works

- Everyone who signs in gets the 4 free sample questions.
- Each subject (Yoga, IKS, Paper 1) unlocks with its own ₹500/month plan,
  offered only once that subject has real papers.
- Questions transcribed from a published book (currently all six Paper 1
  papers from Madaan's Pearson book, and Yoga Nov 2017 and July 2018 from a
  solved-papers collection) are never shown to subscribers; only
  admins see them.
- The Source Library lists your own Drive files and notes, so only admins see it.
- Access follows Razorpay's status: unlocked while **active**; after a
  cancellation or failed renewal, unlocked until the end of the month already paid for.
