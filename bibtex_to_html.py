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

# HTML & CSS header
html_output = ['''<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Publications</title>
  <style>
    body {
      font-family: sans-serif;
      margin: 2rem;
      max-width: 800px;
    }
    .publication-list h2 {
      border-bottom: 2px solid #ddd;
      padding-bottom: 0.3em;
      margin-top: 2em;
    }
    .publication-list ol {
      list-style-type: decimal;
      padding-left: 1.5em;
    }
    .publication-list li {
      margin-bottom: 1em;
      line-height: 1.5;
    }
    a {
      color: #01579B;
      text-decoration: none;
    }
    a:hover {
      text-decoration: underline;
    }
  </style>
</head>
<body>
<div class="publication-list">
''']

# Generate publication list grouped by year
for year in sorted(publications_by_year.keys(), reverse=True):
    html_output.append(f'<h2>{year}</h2>\n<ol>')
    for pub in publications_by_year[year]:
        authors = html.escape(pub['authors'])
        title = html.escape(pub['title'])
        venue = html.escape(pub['venue'])
        link = pub['link']
        if link:
            html_output.append(f'<li><a href="{link}" target="_blank">{title}</a><br>{authors}<br>{venue}</li>')
        else:
            html_output.append(f'<li>{title}<br>{authors}<br>{venue}</li>')
    html_output.append('</ol>')

# Close HTML tags
html_output.append('</div>\n</body>\n</html>')

# Write to file
with open("publications_generated.html", "w") as f:
    f.write("\n".join(html_output))
