"""Razorpay Subscriptions over its REST API. Nothing here imports Streamlit.

The app never sees card or UPI details: it creates a subscription, sends the
user to Razorpay's own payment page (short_url), and later asks Razorpay for
the subscription's status. No webhook is needed.
"""

from dataclasses import dataclass, replace

import requests

from .access import Subscription

API = "https://api.razorpay.com/v1"

# Billing cycles per subscription. After a year it completes and the user can
# subscribe again from the Subscription page.
TOTAL_CYCLES = 12


class PaymentError(Exception):
    pass


@dataclass(frozen=True)
class Razorpay:
    key_id: str
    key_secret: str
    timeout: float = 20.0

    def _call(self, method: str, path: str, payload: dict | None = None) -> dict:
        try:
            resp = requests.request(method, f"{API}{path}", json=payload, auth=(self.key_id, self.key_secret),
                                    timeout=self.timeout)
        except requests.RequestException as e:
            raise PaymentError(f"could not reach Razorpay: {e}") from e
        try:
            data = resp.json()
        except ValueError:
            data = {}
        if not resp.ok:
            detail = (data.get("error") or {}).get("description") or resp.text[:200]
            raise PaymentError(f"Razorpay said: {detail}")
        return data

    def create_subscription(self, plan_id: str, email: str, subject: str) -> Subscription:
        data = self._call("POST", "/subscriptions", {
            "plan_id": plan_id,
            "total_count": TOTAL_CYCLES,
            "quantity": 1,
            "customer_notify": 1,
            "notes": {"email": email, "subject": subject},
        })
        return Subscription(razorpay_id=data["id"], email=email, subject=subject, status=data.get("status", "created"),
                            current_end=data.get("current_end"), short_url=data.get("short_url", ""))

    def refresh(self, sub: Subscription) -> Subscription:
        data = self._call("GET", f"/subscriptions/{sub.razorpay_id}")
        return replace(sub, status=data.get("status", sub.status), current_end=data.get("current_end") or sub.current_end,
                       short_url=data.get("short_url") or sub.short_url)

    def cancel_at_period_end(self, sub: Subscription) -> Subscription:
        data = self._call("POST", f"/subscriptions/{sub.razorpay_id}/cancel", {"cancel_at_cycle_end": 1})
        return replace(sub, status=data.get("status", sub.status), current_end=data.get("current_end") or sub.current_end)


# States Razorpay will not move out of: no point asking again.
FINAL_STATES = frozenset({"cancelled", "completed", "expired"})


def needs_refresh(sub: Subscription, now: float) -> bool:
    if sub.status in FINAL_STATES:
        return False
    if sub.status == "active":
        return sub.current_end is None or now >= sub.current_end   # renewal due: did it go through?
    return True
