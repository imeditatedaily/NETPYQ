"""Content protection for paying students' content: no copying, saving or printing,
and a watermark carrying the viewer's email on every page.

A web page cannot truly stop a screenshot or a phone camera. What this does:
  * deters: text can't be selected or copied, right-click, Ctrl/Cmd+C/S/P/U and
    the devtools shortcuts are blocked, printing produces a blank page, table
    download buttons are hidden, and the page blurs when the window loses focus
    (which is what most desktop snipping tools cause);
  * traces: a faint, repeated watermark with the viewer's email sits over every
    page, so any screenshot that is shared shows whose account it came from.

Admins see the app unprotected.
"""

from html import escape
from urllib.parse import quote

import streamlit as st

CSS = """
<style>
/* No selecting or dragging text and images in the app. Inputs stay usable. */
.stApp, .stApp * { -webkit-user-select: none !important; user-select: none !important; -webkit-touch-callout: none !important; }
.stApp input, .stApp textarea { -webkit-user-select: text !important; user-select: text !important; }
.stApp img { -webkit-user-drag: none; pointer-events: none; }

/* Tables and charts: no "Download as CSV" / "Save as PNG" toolbars. */
[data-testid="stElementToolbar"], .vega-embed details, .vega-actions { display: none !important; }

/* Printing or "Save as PDF" gives a blank page. */
@media print { body * { display: none !important; } body::after { content: "Printing is disabled."; display: block !important; } }

/* Blurred while the window is not in focus (set by the script below). */
body.np-shield .stApp { filter: blur(14px); }

.np-watermark {
  position: fixed; inset: 0; z-index: 999999; pointer-events: none;
  background-image: url("data:image/svg+xml;utf8,__SVG__");
  background-repeat: repeat; opacity: .09;
}
</style>
"""

JS = """
<script>
(() => {
  const w = window.parent && window.parent.document ? window.parent : window;
  const d = w.document;
  if (w.__npProtect) return;          // the script reruns with every Streamlit rerun
  w.__npProtect = true;
  const stop = e => { e.preventDefault(); e.stopPropagation(); return false; };
  ["contextmenu", "copy", "cut", "dragstart", "selectstart"].forEach(t =>
    d.addEventListener(t, e => {
      const el = e.target;
      if (el && (el.tagName === "INPUT" || el.tagName === "TEXTAREA") && t !== "contextmenu") return;
      return stop(e);
    }, true));
  d.addEventListener("keydown", e => {
    const k = (e.key || "").toLowerCase(), mod = e.ctrlKey || e.metaKey;
    if ((mod && ["c", "x", "s", "p", "u", "a"].includes(k) && !["INPUT", "TEXTAREA"].includes(e.target.tagName))
        || (mod && e.shiftKey && ["i", "j", "c", "s"].includes(k))
        || k === "f12" || k === "printscreen") return stop(e);
  }, true);
  d.addEventListener("keyup", e => {
    if ((e.key || "").toLowerCase() === "printscreen") {
      try { w.navigator.clipboard.writeText(""); } catch (_) {}
      d.body.classList.add("np-shield"); setTimeout(() => d.body.classList.remove("np-shield"), 1500);
    }
  }, true);
  w.addEventListener("blur", () => d.body.classList.add("np-shield"));
  w.addEventListener("focus", () => d.body.classList.remove("np-shield"));
  w.addEventListener("beforeprint", () => d.body.classList.add("np-shield"));
  w.addEventListener("afterprint", () => d.body.classList.remove("np-shield"));
})();
</script>
"""


def _watermark_svg(text: str) -> str:
    t = escape(text, quote=True)
    svg = (f"<svg xmlns='http://www.w3.org/2000/svg' width='360' height='200'>"
           f"<text x='20' y='120' transform='rotate(-25 180 100)' font-family='sans-serif' font-size='15' "
           f"fill='#161b15'>{t}</text></svg>")
    return quote(svg, safe="/:=' ")


def apply() -> None:
    """Call once per run, after sign-in. Does nothing for admins."""
    ss = st.session_state
    if ss.get("is_admin"):
        return
    user = ss.get("user") or "UGC NET PYQ Practice"
    st.html(CSS.replace("__SVG__", _watermark_svg(user)) + '<div class="np-watermark"></div>' + JS,
            unsafe_allow_javascript=True)
