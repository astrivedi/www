# Ashutosh Trivedi — academic homepage

Static HTML and CSS for https://ashutoshtrivedi.com. The root directory is the complete website, ready for GitHub Pages using **Deploy from a branch**, with **main / (root)**. `.nojekyll` disables Jekyll processing. The existing `CNAME` is retained. This review branch does not publish or change GitHub Pages settings.

## Edit and build

- `site/build.rb`: shared layout, homepage, Research, publication rendering, news selection, and supporting pages.
- `site/source/group.md`: People page.
- `site/source/teaching.md`: Teaching page.
- `site/source/_data/news.yml`: news; `featured: true` selects homepage highlights (up to four). Optional `datetime` supports approximate dates; `summary` supplies shorter homepage wording.
- `site/source/_papers/*.md`: publication metadata and abstracts.
- `site/source/assets/`: manuscripts, citations, CV, and original photographs.
- `site/publications.mjs`: progressive publication search and topic filtering. Topic rules are defined in `site/build.rb`.
- `site/source/assets/img/group/`: optimized group photographs; captions are in `site/source/group.md`.
- `site/site.css`: the authored stylesheet. It is copied to `assets/site.css` during generation.

With Ruby and Kramdown installed, run from the repository root:

```sh
ruby site/build.rb
python3 site/validate.py
python3 -m http.server 8765 --bind 127.0.0.1
```

For a clean Ruby environment, run `bundle install` inside `site`, then `bundle exec ruby build.rb`. Commit both source and generated files. Hosting itself needs no Ruby, build service, external fonts, or framework. Publication search and topic filters use a small JavaScript module; the complete bibliography remains available without JavaScript. Edit source files rather than generated HTML.

Legacy Jekyll source is retained under `site/source` for reference; its layouts are no longer used. Old generated `_site` output is excluded. Git history retains prior versions.

## Academic genealogy

`/genealogy/` displays the full cached MGP advisor ancestry of record 136067 and his eight PhD graduates. Shared ancestors appear once and every listed ancestral advisor is retained. Graduate branches show his supervision; other MGP-listed advisors are named in details, without adding their ancestries. Local alumni additions are labeled separately from MGP records.

- Refresh public records explicitly: `python3 site/genealogy-fetch.py --refresh`. Fetches are sequential, delayed, retried, and cached under ignored `site/cache/genealogy/`. Without `--refresh`, existing cached records are reused. A failed fetch or a cycle prevents replacement of the complete snapshot.
- `site/genealogy/data.json` is the versioned snapshot, with per-record retrieval dates and source URLs. No network requests are made by the webpage or normal build.
- `site/genealogy/graduates.json` maintains the graduated PhD students, source labels, and co-advisor metadata. The ancestry refresh does not overwrite this file. Mateo Perez and Shadi Tasdighi-Kalat are locally sourced from the People page.
- Refresh English Wikipedia links with `python3 site/genealogy-wikipedia.py`. This matches exact MGP IDs through Wikidata P549, rejects ambiguous matches, and stores results in `site/genealogy/wikipedia.json`. Links appear in selected-person details and the text table; exported PDF/SVG nodes link to Wikipedia where available, otherwise to their source record.
- `site/genealogy-render.py` uses Graphviz `dot` (required for builds) to generate SVG/PDF exports and the accessible page markup. The regular Ruby build invokes it. Python 3 requires no extra packages.
- `site/genealogy.mjs` provides pan, pinch/modified-wheel zoom, keyboard navigation, search, overview, and highlighting of all paths to the focal person. `site/genealogy.css` styles the view. The static graph, text table, and downloads work without JavaScript.
- Verify: `node --test site/tests/genealogy.test.mjs`, `python3 site/tests/genealogy_fetch_test.py`, then `python3 site/validate.py`.

The ancestor closure is complete relative to MGP's recorded links, not the historical record; terminal nodes mean no advisor was recorded. Historical mentorship is not relabeled as a modern doctorate. Rebuild and commit the source snapshot together with generated pages and assets.

## Routes and metadata

Main routes: `/`, `/research/`, `/publications/`, `/students/`, `/teaching/`, `/talks/`, `/cv/`. People uses `/students/` to retain permanent links. Existing paper, news, biography, contact, tag, and CV URLs remain available. `/group/` points to `/students/` with the latter as canonical; an HTTP redirect can be configured if the host supports one.

Pages include descriptive titles, canonical URLs, Open Graph metadata, existing Person/ProfilePage JSON-LD, semantic headings, and ordinary links. Paper pages include citation metadata. `sitemap.xml` and `robots.txt` target the permanent domain.

## Validation

`site/validate.py` checks all generated pages for internal links and anchors, missing or empty assets, unique IDs, document structure, headings, canonical URLs, JSON-LD, template residue, and sitemap XML. Research was additionally inspected at desktop and mobile widths. Publication records are the supplied archive's records; newer papers currently announced in News have external links and have not yet been added to the full bibliography.
