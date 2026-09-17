"""Generate offline graph layout, vector exports, and accessible page content."""
import html
import json
from pathlib import Path
import re
import subprocess
import textwrap

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'genealogy'
OUT = ROOT.parent / 'assets/genealogy'


def main():
    data = json.loads((SOURCE / 'data.json').read_text())
    nodes = {n['id']: n for n in data['nodes']}
    assert data['complete'] and data['root'] in nodes
    for n in nodes.values():
        assert all(a in nodes for a in n['advisors'])
    OUT.mkdir(parents=True, exist_ok=True)
    quote = lambda s: json.dumps(s, ensure_ascii=False)
    lines = ['digraph genealogy {',
             'graph [rankdir=TB, bgcolor="white", pad="0.3", nodesep="0.3", ranksep="0.65", label="Academic ancestry of Ashutosh Trivedi · Mathematics Genealogy Project", labelloc=b, fontname="Helvetica", fontsize=13];',
             'node [shape=box, style="rounded,filled", fillcolor="#f5f7f8", color="#c5d0d8", fontcolor="#242424", fontname="Helvetica", fontsize=13, margin="0.16,0.12"];',
             'edge [color="#9aaab6", arrowsize=0.6];']
    for n in nodes.values():
        label = '\n'.join(textwrap.wrap(n['name'], 32))
        if n['degree']:
            label += '\n' + '\n'.join(textwrap.wrap(n['degree'], 42))
        attrs = f'id="person-{n["id"]}", label={quote(label)}, tooltip={quote(n["name"])}'
        if n['id'] == data['root']:
            attrs += ', fillcolor="#dcebf5", color="#245a80", penwidth=2'
        lines.append(f'"{n["id"]}" [{attrs}];')
        for a in n['advisors']:
            lines.append(f'"{a}" -> "{n["id"]}" [id="edge-{a}-{n["id"]}"];')
    lines.append('}')
    dot = '\n'.join(lines)
    for fmt in ('svg', 'pdf'):
        subprocess.run(['dot', f'-T{fmt}', '-o', str(OUT / f'ancestry.{fmt}')], input=dot, text=True, check=True)
    (OUT / 'data.json').write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    svg = (OUT / 'ancestry.svg').read_text()
    svg = svg[svg.index('<svg'):]
    svg = re.sub(r'\s(?:width|height)="[^"]*"', '', svg, count=2)
    svg = re.sub(r'<svg\b', '<svg id="ancestry-graph" role="group" aria-label="Complete academic ancestry; arrows run from advisor to student" tabindex="0"', svg, count=1)
    svg = re.sub(r'<title>.*?</title>', '', svg, flags=re.S)
    esc = html.escape
    rows, options = [], []
    for n in sorted(nodes.values(), key=lambda n: n['name'].casefold()):
        options.append(f'<option value="{esc(n["name"], quote=True)}"></option>')
        advisors = ', '.join(f'<a href="#record-{a}">{esc(nodes[a]["name"])}</a>' for a in n['advisors']) or 'No advisor recorded in MGP'
        rows.append(f'<tr id="record-{n["id"]}"><th scope="row"><a href="{n["url"]}">{esc(n["name"])}</a></th><td>{esc(n["degree"]) or "Not recorded"}</td><td>{advisors}</td></tr>')
    connections = sum(len(n['advisors']) for n in nodes.values())
    oldest = min(n['retrieved'] for n in nodes.values())
    newest = max(n['retrieved'] for n in nodes.values())
    dates = oldest if oldest == newest else f'{oldest}–{newest}'
    embedded_data = json.dumps(data, ensure_ascii=False).replace('<', '\\u003c')
    content = f'''<p class="back"><a href="/students/">People</a> / Academic genealogy</p>
<h1>Academic genealogy</h1>
<p>My academic ancestry, tracing the mentorship connections from earlier generations of scholars to my Ph.D. at Warwick. Every recorded advisor branch is included; shared ancestors appear once.</p>
<p class="genealogy-meta">{len(nodes)} people · {connections} advisor–student connections · Records retrieved {dates}</p>
<section id="genealogy" aria-label="Explore academic ancestry">
<div class="genealogy-controls" hidden>
<form id="genealogy-search"><label for="ancestor-search">Find a person</label><div class="genealogy-search-row"><input id="ancestor-search" list="ancestor-names" type="search" autocomplete="off" placeholder="Name"/><datalist id="ancestor-names">{''.join(options)}</datalist><button type="submit">Find</button></div></form>
<div class="genealogy-buttons"><button type="button" id="zoom-in" aria-label="Zoom in">+</button><button type="button" id="zoom-out" aria-label="Zoom out">−</button><button type="button" id="fit-graph">Whole graph</button><button type="button" id="focus-root">Start with me</button><button type="button" id="clear-path">Clear highlight</button><button type="button" id="expand-graph">Full screen</button></div>
</div>
<p class="genealogy-help">Oldest generations above, Ashutosh Trivedi below. Arrows point from advisor to student. <span class="interactive-help" hidden>Drag to pan; use +/− or pinch to zoom. Select a person to highlight every path to me. Arrow keys pan the focused graph.</span></p>
<div class="genealogy-stage">{svg}<div class="genealogy-overview" hidden><span>Overview</span><svg id="ancestry-overview" aria-label="Ancestry overview"></svg></div></div>
<p id="genealogy-selection" aria-live="polite">Select a name to explore its connections.</p>
</section>
<p class="genealogy-downloads">Download the complete graph: <a href="/assets/genealogy/ancestry.svg" download>SVG</a> · <a href="/assets/genealogy/ancestry.pdf" download>PDF</a> · <a href="/assets/genealogy/data.json" download>Source data</a></p>
<details><summary>People and advisor relationships — text view</summary><div class="genealogy-table"><table><thead><tr><th scope="col">Person / MGP record</th><th scope="col">Degree</th><th scope="col">Advisors</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div></details>
<h2>About these records</h2>
<p>Source: the <a href="https://www.mathgenealogy.org/id.php?id=136067">Mathematics Genealogy Project</a>. This is the complete recorded advisor ancestry reachable from my entry, not a claim that the historical record is complete. Earlier relationships can reflect mentorship rather than modern doctoral supervision. Degree descriptions follow MGP; blank fields and missing advisors have not been inferred.</p>
<p>My <a href="/students/#phd-alumni">PhD alumni</a> are listed separately on the People page, including graduates not yet recorded in MGP.</p>
<script id="genealogy-data" type="application/json">{embedded_data}</script>'''
    (SOURCE / 'page.html').write_text(content)
    print(f'Rendered {len(nodes)} people and {connections} connections.')


if __name__ == '__main__':
    main()
