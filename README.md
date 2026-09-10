# Ashutosh Trivedi — academic homepage

Static HTML and CSS for https://ashutoshtrivedi.com. The root directory is the complete website, ready for GitHub Pages using **Deploy from a branch**, with **main / (root)**. `.nojekyll` disables Jekyll processing. The existing `CNAME` is retained. This review branch does not publish or change GitHub Pages settings.

## Edit and build

- `site/build.rb`: shared layout, homepage, Research, publication rendering, news selection, and supporting pages.
- `site/source/group.md`: People page.
- `site/source/teaching.md`: Teaching page.
- `site/source/_data/news.yml`: news; `featured: true` selects homepage highlights (up to four). Optional `datetime` supports approximate dates.
- `site/source/_papers/*.md`: publication metadata and abstracts.
- `site/source/assets/`: manuscripts, citations, CV, and original photographs.
- `site/site.css`: the authored stylesheet. It is copied to `assets/site.css` during generation.

With Ruby and Kramdown installed, run from the repository root:

```sh
ruby site/build.rb
python3 site/validate.py
python3 -m http.server 8765 --bind 127.0.0.1
```

For a clean Ruby environment, run `bundle install` inside `site`, then `bundle exec ruby build.rb`. Commit both source and generated files. Hosting itself needs no Ruby, build service, JavaScript, external fonts, or framework. Edit source files rather than generated HTML.

Legacy Jekyll source is retained under `site/source` for reference; its layouts are no longer used. Old generated `_site` output is excluded. Git history retains prior versions.

## Routes and metadata

Main routes: `/`, `/research/`, `/publications/`, `/students/`, `/teaching/`, `/talks/`, `/cv/`. People uses `/students/` to retain permanent links. Existing paper, news, biography, contact, tag, and CV URLs remain available. `/group/` points to `/students/` with the latter as canonical; an HTTP redirect can be configured if the host supports one.

Pages include descriptive titles, canonical URLs, Open Graph metadata, existing Person/ProfilePage JSON-LD, semantic headings, and ordinary links. Paper pages include citation metadata. `sitemap.xml` and `robots.txt` target the permanent domain.

## Validation

`site/validate.py` checks all generated pages for internal links and anchors, missing or empty assets, unique IDs, document structure, headings, canonical URLs, JSON-LD, template residue, and sitemap XML. Research was additionally inspected at desktop and mobile widths. Publication records are the supplied archive's records; newer papers currently announced in News have external links and have not yet been added to the full bibliography.
