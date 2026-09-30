# Source Library

PDFs in this folder appear on the app's **Source Library** page. `catalog.json`
gives each one a title, author, year, the syllabus units it serves, and its
licence. Entries with `"file": null` are recommended texts not added yet. Put
the PDF here and set `file` to its name.

A PDF without a catalog entry still appears, as "uncatalogued".

Only add texts you are free to share: public-domain translations, open-access
papers, official documents, or your own notes. `kind` is one of `syllabus`, `primary`,
`study`, `paper` or `notes`. Use `notes` for your own or AI-generated material, so it is never
mistaken for a source.

Copyrighted books and coaching notes can still be catalogued with `"file": null` and
a `where` that says where you keep them (for example your Google Drive), so they
show up under their syllabus units without being published in this repository.
