from pybtex.database.input import bibtex
from collections import defaultdict
import html
import uuid

# Load BibTeX file
bib_data = bibtex.Parser().parse_file('publications.bib')

# Organize entries by year
publications_by_year = defaultdict(list)
for key, entry in bib_data.entries.items():
    year = entry.fields.get('year', 'Unknown')
    authors = ', '.join(str(person) for person in entry.persons.get('author', []))
    title = entry.fields.get('title', 'No title').strip('{}')
    venue = entry.fields.get('booktitle') or entry.fields.get('journal') or 'Unknown venue'
    abstract = entry.fields.get('abstract', '')
    bibtex_str = entry.to_string('bibtex')
    link = entry.fields.get('url') or entry.fields.get('pdf') or entry.fields.get('doi')
    if link and not link.startswith('http'):
        link = 'https://doi.org/' + link

    publications_by_year[year].append({
        'authors': authors,
        'title': title,
        'venue': venue,
        'abstract': abstract,
        'bibtex': bibtex_str,
        'link': link
    })

# HTML + CSS + JS header
html_output = ['''<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Publications</title>
  <style>
    body {
      font-family: sans-serif;
      margin: 2rem;
      max-width: 900px;
    }
    h2 {
      border-bottom: 2px solid #ccc;
      padding-bottom: 0.3em;
      margin-top: 2em;
    }
    .publication {
      margin-bottom: 1.5em;
    }
    .buttons {
      margin-top: 0.3em;
    }
    .button {
      background-color: #01579B;
      color: white;
      border: none;
      padding: 0.2em 0.6em;
      margin-right: 0.5em;
      cursor: pointer;
      font-size: 0.9em;
    }
    .button:hover {
      background-color: #014172;
    }
    .hidden-content {
      display: none;
      margin-top: 0.5em;
      padding: 0.5em;
      background-color: #f3f3f3;
      border-left: 3px solid #ccc;
      font-size: 0.9em;
      white-space: pre-wrap;
    }
    a {
      color: #01579B;
      text-decoration: none;
    }
    a:hover {
      text-decoration: underline;
    }
  </style>
  <script>
    function toggle(id) {
      var e = document.getElementById(id);
      if (e.style.display === "block") {
        e.style.display = "none";
      } else {
        e.style.display = "block";
      }
    }
  </script>
</head>
<body>
<h1>Publications</h1>
''']

# Generate publication list grouped by year
for year in sorted(publications_by_year.keys(), reverse=True):
    html_output.append(f'<h2>{year}</h2>')
    for pub in publications_by_year[year]:
        uid = str(uuid.uuid4()).replace("-", "")[:8]
        authors = html.escape(pub['authors'])
        title = html.escape(pub['title'])
        venue = html.escape(pub['venue'])
        abstract = html.escape(pub['abstract']) if pub['abstract'] else 'Abstract not available.'
        bibtex = html.escape(pub['bibtex'])
        link = pub['link']

        html_output.append('<div class="publication">')
        if link:
            html_output.append(f'<a href="{link}" target="_blank"><strong>{title}</strong></a><br>')
        else:
            html_output.append(f'<strong>{title}</strong><br>')
        html_output.append(f'{authors}<br>{venue}<br>')
        
        # Add buttons
        html_output.append(f'''
        <div class="buttons">
          <button class="button" onclick="toggle('abs-{uid}')">Abs</button>
          <button class="button" onclick="toggle('bib-{uid}')">Bib</button>''')
        if link:
            html_output.append(f'<a class="button" href="{link}" target="_blank">URL</a>')
        html_output.append('</div>')
        
        # Add hidden content
        html_output.append(f'<div id="abs-{uid}" class="hidden-content">{abstract}</div>')
        html_output.append(f'<div id="bib-{uid}" class="hidden-content">{bibtex}</div>')
        html_output.append('</div>')

# Close HTML
html_output.append('</body></html>')

# Write to file
with open("publications_generated.html", "w") as f:
    f.write("\n".join(html_output))
