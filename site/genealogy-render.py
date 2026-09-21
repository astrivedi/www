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
    graduates = json.loads((SOURCE / 'graduates.json').read_text())['nodes']
    wikipedia = json.loads((SOURCE / 'wikipedia.json').read_text())
    data['ancestor_count'] = len(data['nodes']) - 1
    data['wikipedia_retrieved'] = wikipedia['retrieved']
    data['scope'] = 'Complete recorded advisor ancestry of Ashutosh Trivedi, plus his PhD graduates. Graduate edges show his supervision; other recorded advisors are separate metadata.'
    for n in data['nodes']:
        n['kind'] = 'self' if n['id'] == data['root'] else 'ancestor'
    data['nodes'].extend(graduates)
    for n in data['nodes']:
        if n['id'] in wikipedia['links']:
            n['wikipedia'] = wikipedia['links'][n['id']]['url']
            n['wikidata'] = wikipedia['links'][n['id']]['wikidata']
    nodes = {n['id']: n for n in data['nodes']}
    assert data['complete'] and data['root'] in nodes
    for n in nodes.values():
        assert all(a in nodes for a in n['advisors'])
    OUT.mkdir(parents=True, exist_ok=True)
    quote = lambda s: json.dumps(s, ensure_ascii=False)
    lines = ['digraph genealogy {',
             'graph [rankdir=TB, bgcolor="white", pad="0.3", nodesep="0.3", ranksep="0.65", label="Academic genealogy of Ashutosh Trivedi · MGP and local alumni records", labelloc=b, fontname="Helvetica", fontsize=13];',
             'node [shape=box, style="rounded,filled", fillcolor="#f5f7f8", color="#c5d0d8", fontcolor="#242424", fontname="Helvetica", fontsize=13, margin="0.16,0.12"];',
             'edge [color="#9aaab6", arrowsize=0.6];']
    for n in nodes.values():
        label = '\n'.join(textwrap.wrap(n['name'], 32))
        if n['degree']:
            label += '\n' + '\n'.join(textwrap.wrap(n['degree'], 42))
        attrs = f'id="person-{n["id"]}", label={quote(label)}, tooltip={quote(n["name"])}'
        attrs += f', URL={quote(n.get("wikipedia", n["url"]))}, target="_blank"'
        if n.get('kind') == 'graduate':
            attrs += ', fillcolor="#e4f1ea", color="#648271"'
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
    svg = re.sub(r'<svg\b', '<svg id="ancestry-graph" role="group" aria-label="Academic ancestry and PhD graduates; arrows run from advisor to student" tabindex="0"', svg, count=1)
    # Exported nodes link to biographies; in-page nodes select details instead.
    svg = re.sub(r'\s(?:xlink:href|href|target)="[^"]*"', '', svg)
    svg = re.sub(r'<title>.*?</title>', '', svg, flags=re.S)
    esc = html.escape
    rows, options = [], []
    for n in sorted(nodes.values(), key=lambda n: n['name'].casefold()):
        options.append(f'<option value="{esc(n["name"], quote=True)}"></option>')
        advisors = ', '.join(f'<a href="#record-{a}">{esc(nodes[a]["name"])}</a>' for a in n['advisors']) or 'No advisor recorded in MGP'
        other = n.get('other_advisors', [])
        if other:
            advisors += ', ' + ', '.join(f'<a href="{esc(a["url"], quote=True)}">{esc(a["name"])}</a> (co-advisor)' for a in other)
        biography = f'<br/><a href="{esc(n["wikipedia"], quote=True)}">Wikipedia</a>' if n.get('wikipedia') else ''
        local = '<br/><small>Local alumni record</small>' if n['id'].startswith('local-') else ''
        rows.append(f'<tr id="record-{n["id"]}"><th scope="row"><a href="{n["url"]}">{esc(n["name"])}</a>{biography}{local}</th><td>{esc(n["degree"]) or "Not recorded"}</td><td>{advisors}</td></tr>')
    graduate_list = ''.join(f'<li><a href="#record-{n["id"]}" data-person="{n["id"]}">{esc(n["name"])}</a><span>{esc(n["degree"])}</span></li>' for n in graduates)
    biography_count = sum(bool(n.get('wikipedia')) for n in nodes.values())
    connections = sum(len(n['advisors']) for n in nodes.values())
    oldest = min(n['retrieved'] for n in nodes.values())
    newest = max(n['retrieved'] for n in nodes.values())
    dates = oldest if oldest == newest else f'{oldest}–{newest}'
    embedded_data = json.dumps(data, ensure_ascii=False).replace('<', '\\u003c')
    content = f'''<p class="back"><a href="/students/">People</a> / Academic genealogy</p>
<h1>Academic genealogy</h1>
<p>From earlier generations of scholars to my Ph.D. at Warwick and the students I have supervised. Every recorded branch of my advisor ancestry is included; shared ancestors appear once.</p>
<p class="genealogy-meta">{len(nodes)} people · {connections} connections · {len(graduates)} PhD graduates · {biography_count} Wikipedia links<br/>Records retrieved {dates}</p>
<section id="genealogy" aria-label="Explore academic ancestry">
<div class="genealogy-controls" hidden>
<form id="genealogy-search"><label for="ancestor-search">Find a person</label><div class="genealogy-search-row"><input id="ancestor-search" list="ancestor-names" type="search" autocomplete="off" placeholder="Name"/><datalist id="ancestor-names">{''.join(options)}</datalist><button type="submit">Find</button></div></form>
<div class="genealogy-buttons"><button type="button" id="zoom-in" aria-label="Zoom in">+</button><button type="button" id="zoom-out" aria-label="Zoom out">−</button><button type="button" id="fit-graph">Whole graph</button><button type="button" id="focus-root">Start with me</button><button type="button" id="clear-path">Clear highlight</button><button type="button" id="expand-graph">Full screen</button></div>
</div>
<p class="genealogy-help">Ancestors above me; PhD graduates below, shaded green. Arrows point from advisor to student. <span class="interactive-help" hidden>Drag to pan; use +/− or pinch to zoom. Click a person to highlight their connections and open Wikipedia in a new tab, when available. Arrow keys pan the focused graph.</span></p>
<div class="genealogy-stage">{svg}<div class="genealogy-overview" hidden><span>Overview</span><svg id="ancestry-overview" aria-label="Ancestry overview"></svg></div></div>
<p id="genealogy-selection" aria-live="polite">Select a name to explore its connections.</p>
</section>
<p class="genealogy-downloads">Download the complete graph: <a href="/assets/genealogy/ancestry.svg" download>SVG</a> · <a href="/assets/genealogy/ancestry.pdf" download>PDF</a> · <a href="/assets/genealogy/data.json" download>Source data</a></p>
<section aria-labelledby="phd-graduates"><h2 id="phd-graduates">PhD graduates</h2><p class="genealogy-help">Select a graduate to see their connection in the graph.</p><ul class="genealogy-graduates">{graduate_list}</ul></section>
<details id="genealogy-text-view"><summary>People and advisor relationships — text view</summary><div class="genealogy-table"><table><thead><tr><th scope="col">Person / links</th><th scope="col">Degree</th><th scope="col">Advisors</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div></details>
<h2>About these records</h2>
<p>Source: the <a href="https://www.mathgenealogy.org/id.php?id=136067">Mathematics Genealogy Project</a>. This is the complete recorded advisor ancestry reachable from my entry, not a claim that the historical record is complete. Earlier relationships can reflect mentorship rather than modern doctoral supervision. Degree descriptions follow MGP; blank fields and missing advisors have not been inferred.</p>
<p>Graduate branches show my supervision. Other advisors recorded by MGP are named in the selected person's details and text view; their ancestries are outside this graph. Mateo Perez and Shadi Tasdighi-Kalat are included from my <a href="/students/#phd-alumni">local alumni records</a>, rather than MGP.</p>
<p>English Wikipedia links are matched through <a href="https://www.wikidata.org/wiki/Property:P549">Wikidata's Mathematics Genealogy IDs</a>, checked {wikipedia['retrieved']}. No link is inferred from a name alone. Linked biographies provide context; MGP remains the source for the recorded ancestry.</p>
<script id="genealogy-data" type="application/json">{embedded_data}</script>'''
    (SOURCE / 'page.html').write_text(content)
    print(f'Rendered {len(nodes)} people and {connections} connections.')


if __name__ == '__main__':
    main()
