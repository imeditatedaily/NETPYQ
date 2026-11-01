"""One-time exam passes (Razorpay payment links) and the visit-to-payment funnel."""

from pyq import config, store
from pyq.access import Subscription, unlocked_subjects
from pyq.payments import Razorpay, needs_refresh
from tests.test_accounts import FakeResponse

DAY = 86400


def test_a_paid_combo_pass_unlocks_both_subjects_until_it_ends():
    p = Subscription("plink_1", "x@gmail.com", "paper1+yoga", "paid", current_end=1000 * DAY)
    assert p.is_pass and p.subjects == ("paper1", "yoga") and not p.renews
    assert unlocked_subjects([p], 999 * DAY) == {"paper1", "yoga"}
    assert unlocked_subjects([p], 1000 * DAY) == set()
    unpaid = Subscription("plink_2", "x@gmail.com", "yoga", "created", short_url="https://rzp.io/l/x")
    assert unpaid.awaiting_payment and not unpaid.grants_access(0)


def test_passes_are_checked_only_until_paid():
    assert needs_refresh(Subscription("plink_1", "x", "yoga", "created"), 0)
    assert not needs_refresh(Subscription("plink_1", "x", "yoga", "paid", current_end=5), 0)
    assert not needs_refresh(Subscription("plink_1", "x", "yoga", "expired"), 0)


def test_razorpay_payment_link_round_trip(monkeypatch):
    calls = []

    def fake_request(method, url, json=None, auth=None, timeout=None):
        calls.append((method, url, json))
        if method == "POST" and url.endswith("/payment_links"):
            return FakeResponse(200, {"id": "plink_A", "status": "created", "short_url": "https://rzp.io/l/abc"})
        return FakeResponse(200, {"id": "plink_A", "status": "paid", "payments": [{"created_at": 100 * DAY}]})

    monkeypatch.setattr("pyq.payments.requests.request", fake_request)
    rzp = Razorpay("k", "s")
    name, price, subjects = config.PASSES["combo"]
    p = rzp.create_pass(price, "x@gmail.com", subjects, name, callback_url="https://example.com/plans")
    body = calls[0][2]
    assert body["amount"] == price * 100 and body["notes"]["subject"] == "paper1+yoga"
    assert body["callback_url"] == "https://example.com/plans" and not body["accept_partial"]
    assert (p.razorpay_id, p.status, p.subject) == ("plink_A", "created", "paper1+yoga")

    paid = rzp.refresh(p)       # refresh() sends passes to the payment-links API
    assert calls[-1][1].endswith("/payment_links/plink_A")
    assert paid.status == "paid" and paid.current_end == 100 * DAY + config.PASS_DAYS * DAY
    assert rzp.refresh(paid).current_end == paid.current_end    # the end date never moves


def test_funnel_counts_people_per_step(tmp_path):
    eng = store.make_engine(f"sqlite:///{tmp_path / 'f.db'}")
    for v in ("v1", "v2", "v3", "v4"):
        store.add_event(eng, "visit", v)
    store.add_event(eng, "signin", "v5", "a@x.com")
    store.add_event(eng, "signin", "v6", "a@x.com")        # the same person twice
    store.add_event(eng, "signin", "v7", "b@x.com")
    store.add_event(eng, "plans", "v7", "b@x.com")
    store.add_event(eng, "checkout", "v7", "b@x.com", "combo")
    paid = Subscription("plink_9", "b@x.com", "paper1+yoga", "paid", current_end=5, created_at="2026-11-01")
    steps = {e: n for e, _, n in store.funnel(store.list_events(eng), [paid])}
    assert steps == {"visit": 4, "signin": 2, "plans": 1, "checkout": 1, "paid": 1}
