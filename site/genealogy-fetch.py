"""Refresh the complete MGP advisor closure; cache records and fail on missing pages.

Usage: python3 site/genealogy-fetch.py [--refresh]
Only this explicit refresh command accesses the network; normal builds are offline.
"""
import datetime
import html
import json
from pathlib import Path
import re
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
CACHE = ROOT / 'cache/genealogy'
DEST = ROOT / 'genealogy/data.json'


def clean(value):
    return ' '.join(html.unescape(re.sub(r'<[^>]*>', ' ', value)).split())


def parse(page, ident):
    heading = re.search(r'<h2\b[^>]*>(.*?)</h2>', page, re.S)
    if not heading or 'Advisor' not in page:
        # The oldest records can explicitly have no advisor listed.
        if not heading or 'Mathematics Genealogy Project' not in page or 'Dissertation:' not in page:
            raise ValueError(f'Unrecognized MGP record {ident}')
    advisor_blocks = re.findall(r'<p\b[^>]*>\s*Advisor.*?</p>', page, re.S)
    advisors = list(dict.fromkeys(re.findall(r'id\.php\?id=(\d+)', ''.join(advisor_blocks))))
    degree = re.search(r'<div style="line-height: 30px;.*?</div>', page, re.S)
    thesis = re.search(r'id="thesisTitle"[^>]*>(.*?)</span>', page, re.S)
    return {'id': ident, 'name': clean(heading[1]), 'degree': clean(degree[0]) if degree else '',
            'thesis': clean(thesis[1]) if thesis else '', 'advisors': advisors,
            'url': f'https://www.mathgenealogy.org/id.php?id={ident}'}


def main():
    CACHE.mkdir(parents=True, exist_ok=True)
    pending, nodes = ['136067'], {}
    while pending:
        ident = pending.pop(0)
        if ident in nodes:
            continue
        cached = CACHE / f'{ident}.html'
        if not cached.exists() or '--refresh' in sys.argv:
            result = subprocess.run(['curl', '-fsSL', '--retry', '2', '--max-time', '40',
                                     f'https://www.mathgenealogy.org/id.php?id={ident}'],
                                    capture_output=True, text=True, check=True)
            parse(result.stdout, ident)
            cached.write_text(result.stdout)
            time.sleep(0.5)
        record = parse(cached.read_text(), ident)
        record['retrieved'] = datetime.datetime.fromtimestamp(cached.stat().st_mtime, datetime.timezone.utc).date().isoformat()
        nodes[ident] = record
        pending.extend(a for a in record['advisors'] if a not in nodes)
        print(f'{len(nodes)}: {record["name"]} ({len(pending)} pending)', flush=True)
    # Validate closure and acyclicity rather than silently dropping unusual links.
    visiting, visited = set(), set()
    def visit(ident):
        if ident in visiting:
            raise ValueError(f'Cycle in MGP records at {ident}')
        if ident in visited:
            return
        visiting.add(ident)
        for advisor in nodes[ident]['advisors']:
            visit(advisor)
        visiting.remove(ident)
        visited.add(ident)
    visit('136067')
    DEST.parent.mkdir(parents=True, exist_ok=True)
    DEST.write_text(json.dumps({'root': '136067', 'source': 'Mathematics Genealogy Project',
                               'complete': True, 'nodes': list(nodes.values())}, ensure_ascii=False, indent=2) + '\n')
    print(f'Saved complete ancestor closure: {len(nodes)} people.')


if __name__ == '__main__':
    main()
