"""Source Library: study texts mapped to syllabus units, with the PDFs you have added."""

import streamlit as st

from ..filters import ALL
from ..library import KINDS, Source
from ..syllabus import SUBJECTS, UNIT_INDEX
from . import state


def _unit_order(source: Source) -> tuple:
    if not source.units:
        return (99, 99, source.title)
    subject, no = UNIT_INDEX[source.units[0]]
    return (list(SUBJECTS).index(subject.id), no, source.title)


def _pdf_viewer(source: Source) -> None:
    try:
        st.pdf(source.path, height=600)
    except Exception:  # the optional streamlit-pdf component is missing or failed to load
        st.info("The in-app reader is unavailable here. Download the PDF instead.", icon=":material/picture_as_pdf:")


def _clear_focus() -> None:
    st.session_state["lib_focus"] = None


def _card(source: Source) -> None:
    with st.container(border=True):
        with st.container(horizontal=True, gap="small"):
            st.badge(KINDS[source.kind], color="violet" if source.kind == "notes" else "gray")
            if source.available:
                st.badge("In your library", icon=":material/check:", color="green")
            else:
                st.badge("Not added yet", icon=":material/add:", color="gray")
        st.markdown(f"**{source.title}**")
        byline = " · ".join(b for b in (source.author, source.year) if b)
        if byline:
            st.caption(byline)
        if source.units:
            st.caption("Units: " + "; ".join(source.units))
        if source.note:
            st.markdown(source.note)
        details = []
        if source.licence:
            details.append(f"**Licence:** {source.licence}")
        if source.where:
            details.append(f"**{'Source' if source.available else 'Where to get it'}:** {source.where}")
        if details:
            st.caption("  \n".join(details))
        if source.available:
            with st.container(horizontal=True):
                st.download_button("Download PDF", source.path.read_bytes(), file_name=source.path.name,
                                   mime="application/pdf", icon=":material/download:", on_click="ignore",
                                   key=f"dl-{source.id}")
                read = st.toggle("Read here", key=f"read-{source.id}")
            if read:
                _pdf_viewer(source)


def render() -> None:
    library = state.get_library()
    ss = st.session_state
    st.title("Source Library", anchor=False)
    st.caption("Primary texts and studies for each syllabus unit. PDFs you add to the `sources/` folder show up here; "
               "entries marked *Not added yet* are public-domain texts worth adding.")

    # A "Study this in" link from a question opens the library on that question's
    # unit, and it stays there until cleared.
    focus_unit = ss.get("lib_focus")
    unit_filter = focus_unit or (ss.f_unit if ss.f_unit != ALL else None)
    subject = ss.f_subject

    c1, c2 = st.columns([1, 2])
    show = c1.segmented_control("Show", ["All", "In your library", "Not added yet"], default="All",
                                key="lib_show", required=True)
    query = c2.text_input("Search titles and authors", key="lib_query", placeholder="e.g. Pradipika, Clark, Sushruta")

    sources = sorted(library.sources, key=_unit_order)
    if unit_filter:
        with st.container(border=True, horizontal=True, vertical_alignment="center"):
            st.markdown(f":material/filter_alt: Showing sources for **{unit_filter}**.")
            if focus_unit:
                st.button("Show all units", on_click=_clear_focus)
            else:
                st.caption("Clear the unit filter in the sidebar to see everything.")
        sources = [s for s in sources if unit_filter in s.units]
    elif subject != ALL:
        sources = [s for s in sources if not s.units or any(UNIT_INDEX[u][0].id == subject for u in s.units)]
    if show == "In your library":
        sources = [s for s in sources if s.available]
    elif show == "Not added yet":
        sources = [s for s in sources if not s.available]
    if query:
        needle = query.casefold()
        sources = [s for s in sources if needle in f"{s.title} {s.author} {s.note}".casefold()]

    have = sum(s.available for s in library.sources)
    st.caption(f"{len(sources)} shown · {have} of {len(library.sources)} catalogued sources are in your library")
    for source in sources:
        _card(source)

    for problem in library.problems:
        st.warning(problem, icon=":material/warning:")

    with st.expander("How to add a PDF"):
        st.markdown(
            "1. Put the PDF in the `sources/` folder of the repository.\n"
            "2. Add an entry to `sources/catalog.json` with its `file` name and the syllabus `units` it serves "
            "(or fill in `file` on an existing *Not added yet* entry).\n"
            "3. Commit and push. Streamlit Community Cloud redeploys and the PDF appears here.\n\n"
            "A PDF without a catalog entry still appears, marked *uncatalogued*. Only add texts you have the right to "
            "share: public-domain translations, open-access papers, or your own notes."
        )
