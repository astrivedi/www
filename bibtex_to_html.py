from pybtex.database.input import bibtex
from collections import defaultdict
import html

# Load BibTeX file
bib_data = bibtex.Parser().parse_file('publications.bib')

# Organize entries by year
publications_by_year = defaultdict(list)
for key, entry in bib_data.entries.items():
    year = entry.fields.get('year', 'Unknown')
    authors = ', '.join(str(person) for person in entry.persons.get('author', []))
    title = entry.fields.get('title', 'No title').strip('{}')
    venue = entry.fields.get('booktitle') or entry.fields.get('journal') or 'Unknown venue'
    link = entry.fields.get('url') or entry.fields.get('doi')
    if link and not link.startswith('http'):
        link = 'https://doi.org/' + link
    publications_by_year[year].append({
        'authors': authors,
        'title': title,
        'venue': venue,
        'link': link
    })

# Generate HTML
html_output = []
for year in sorted(publications_by_year.keys(), reverse=True):
    html_output.append(f"""
<div class="accordion-item">
  <h3 class="accordion-header">
    <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
            data-bs-target="#collapse{year}" aria-expanded="false" aria-controls="collapse{year}">
      {year}
    </button>
  </h3>
  <div id="collapse{year}" class="accordion-collapse collapse" aria-labelledby="heading{year}"
       data-bs-parent="#accordionExample">
    <div class="accordion-body">
      <ul class="list-style-icon-angle-double">
""")
    for pub in publications_by_year[year]:
        authors = html.escape(pub['authors'])
        title = html.escape(pub['title'])
        venue = html.escape(pub['venue'])
        link = pub['link']
        if link:
            html_output.append(f'<li><a href="{link}" target="_blank">{title}</a><br>{authors}<br>{venue}</li>')
        else:
            html_output.append(f'<li>{title}<br>{authors}<br>{venue}</li>')
    html_output.append("</ul></div></div></div>")

# Write to file
with open("publications_generated.html", "w") as f:
    f.write("\n".join(html_output))
