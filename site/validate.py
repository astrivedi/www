"""Check the generated site without a browser or network dependencies."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
class Document(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.tags=[]; self.refs=[]; self.ids=[]; self.scripts=[]; self.script=None
        self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs); self.tags.append((tag,a))
        if 'id' in a: self.ids.append(a['id'])
        for k in ('href','src'):
            if k in a: self.refs.append(a[k])
        if tag=='script':
            assert a.get('type')=='application/ld+json', 'Executable JavaScript'
            self.script=''
        if tag=='img': assert a.get('alt') and a.get('width') and a.get('height')
    def handle_data(self,data):
        if self.script is not None: self.script+=data
    def handle_endtag(self,tag):
        if tag=='script':
            self.scripts.append(json.loads(self.script)); self.script=None

docs={p:Document(p.read_text()) for p in ROOT.rglob('*.html') if 'site' not in p.relative_to(ROOT).parts and '.git' not in p.relative_to(ROOT).parts}
errors=[]
for p,d in docs.items():
    def count(tag): return sum(t==tag for t,a in d.tags)
    for tag in ('html','head','body','main','h1','title'):
        if count(tag)!=1: errors.append(f'{p}: expected one {tag}, found {count(tag)}')
    for name in ('description',):
        if not any(t=='meta' and a.get('name')==name and a.get('content') for t,a in d.tags): errors.append(f'{p}: missing {name}')
    if not any(t=='link' and a.get('rel')=='canonical' for t,a in d.tags): errors.append(f'{p}: no canonical')
    if len(d.ids)!=len(set(d.ids)): errors.append(f'{p}: duplicate IDs')
    if not d.scripts: errors.append(f'{p}: no JSON-LD')
    text=p.read_text()
    for marker in ('{{','{%','contentReference'):
        if marker in text: errors.append(f'{p}: template residue {marker}')
    for ref in d.refs:
        u=urlsplit(ref)
        if u.scheme or u.netloc: continue
        target=(ROOT/unquote(u.path).lstrip('/')) if u.path.startswith('/') else p.parent/unquote(u.path)
        if not u.path: target=p
        if target.is_dir(): target=target/'index.html'
        if not target.is_file(): errors.append(f'{p}: broken link {ref}'); continue
        if target.stat().st_size==0: errors.append(f'{p}: empty linked file {ref}')
        if u.fragment and target in docs and unquote(u.fragment) not in docs[target].ids: errors.append(f'{p}: missing anchor {ref}')
for route in ('','research','publications','students','teaching','talks','cv'):
    assert (ROOT/route/'index.html').is_file()
ET.parse(ROOT/'sitemap.xml')
assert (ROOT/'robots.txt').read_text().startswith('User-agent: *')
assert len(list((ROOT/'papers').glob('*/index.html')))==12
if errors: raise SystemExit('\n'.join(errors))
print(f'PASS: {len(docs)} pages; internal links and anchors; metadata; JSON-LD; one H1 per page; no executable JavaScript; sitemap; nonempty linked assets.')
print(f'Homepage: {(ROOT/"index.html").stat().st_size:,} bytes; CSS: {(ROOT/"assets/site.css").stat().st_size:,} bytes.')
