"""Refresh English Wikipedia links by exact MGP IDs in Wikidata, never by name."""
import datetime
import json
from pathlib import Path
import subprocess
from urllib.parse import urlencode

ROOT = Path(__file__).resolve().parent / 'genealogy'


def main():
    nodes = json.loads((ROOT / 'data.json').read_text())['nodes']
    nodes += json.loads((ROOT / 'graduates.json').read_text())['nodes']
    ids = {n['id'] for n in nodes if n['id'].isdigit()}
    values = ' '.join(json.dumps(ident) for ident in sorted(ids))
    query = ('SELECT ?person ?id ?article WHERE { VALUES ?id { ' + values +
             ' } ?person wdt:P549 ?id. ?article schema:about ?person; '
             'schema:isPartOf <https://en.wikipedia.org/>. }')
    url = 'https://query.wikidata.org/sparql?' + urlencode({'query': query, 'format': 'json'})
    result = subprocess.run(['curl', '-fsSL', '--retry', '2', '--max-time', '60', url],
                            capture_output=True, text=True, check=True)
    links = {}
    for row in json.loads(result.stdout)['results']['bindings']:
        ident, article = row['id']['value'], row['article']['value']
        assert ident in ids and article.startswith('https://en.wikipedia.org/wiki/')
        if ident in links and links[ident]['url'] != article:
            raise ValueError(f'Ambiguous Wikipedia identity for MGP {ident}')
        links[ident] = {'url': article, 'wikidata': row['person']['value'].replace('http:', 'https:')}
    if not links:
        raise ValueError('No Wikipedia matches returned; preserving the previous snapshot')
    snapshot = {'source': 'https://query.wikidata.org/',
                'match': 'Wikidata P549 (Mathematics Genealogy Project ID) and English Wikipedia sitelink',
                'retrieved': datetime.date.today().isoformat(), 'links': links}
    (ROOT / 'wikipedia.json').write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + '\n')
    print(f'Saved {len(links)} Wikipedia links matched by exact MGP ID.')


if __name__ == '__main__':
    main()
