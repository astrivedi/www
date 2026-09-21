import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {pathsToRoot, normalizeName} from '../genealogy.mjs';

test('all paths survive branching and shared ancestors; unrelated branches are excluded', () => {
  const nodes = [
    {id:'me',advisors:['a','b']}, {id:'a',advisors:['shared','other']},
    {id:'b',advisors:['shared']}, {id:'shared',advisors:['older']},
    {id:'other',advisors:[]}, {id:'older',advisors:[]}
  ];
  const path = pathsToRoot(nodes, 'me', 'shared');
  assert.deepEqual([...path.people].sort(), ['a','b','me','shared']);
  assert.deepEqual([...path.edges].sort(), ['edge-a-me','edge-b-me','edge-shared-a','edge-shared-b']);
  assert.deepEqual([...pathsToRoot(nodes,'me','me').people], ['me']);
  assert.equal(pathsToRoot(nodes, 'me', 'missing').people.size, 0);
});

test('name search handles accents and case', () => {
  assert.equal(normalizeName('VÄISÄLÄ'), normalizeName('Vaisala'));
});

test('graduate selection traces supervision in the correct direction', () => {
  const nodes = [{id:'advisor',advisors:[]},{id:'me',advisors:['advisor']},{id:'graduate',advisors:['me']}];
  const path = pathsToRoot(nodes, 'graduate', 'me');
  assert.deepEqual([...path.people].sort(), ['graduate','me']);
  assert.deepEqual([...path.edges], ['edge-me-graduate']);
});

test('snapshot includes ancestors and graduates once, is acyclic, and matches the SVG', () => {
  const data = JSON.parse(readFileSync(new URL('../../assets/genealogy/data.json', import.meta.url)));
  const svg = readFileSync(new URL('../../assets/genealogy/ancestry.svg', import.meta.url), 'utf8').replaceAll('&#45;', '-');
  const page = readFileSync(new URL('../../genealogy/index.html', import.meta.url), 'utf8');
  assert.match(page, /<svg\s+id="ancestry-graph"/);
  const nodes = new Map(data.nodes.map(n => [n.id,n]));
  assert.equal(nodes.size, data.nodes.length);
  assert.equal(data.complete, true);
  const seen = new Set(), visiting = new Set();
  function visit(id) {
    assert.ok(!visiting.has(id), `cycle at ${id}`);
    if (seen.has(id)) return;
    visiting.add(id);
    const n = nodes.get(id);
    assert.ok(n, `missing record ${id}`);
    assert.ok(n.name);
    assert.ok(svg.includes(`id="person-${id}"`));
    for (const a of n.advisors) {
      assert.ok(svg.includes(`id="edge-${a}-${id}"`));
      visit(a);
    }
    visiting.delete(id); seen.add(id);
  }
  visit(data.root);
  const graduates = data.nodes.filter(n => n.kind === 'graduate');
  assert.equal(graduates.length, 8);
  for (const graduate of graduates) {
    assert.deepEqual(graduate.advisors, [data.root]);
    visit(graduate.id);
  }
  assert.equal(seen.size, nodes.size);
  assert.ok(data.nodes.some(n => n.advisors.length > 1));
  for (const n of data.nodes) {
    if (n.wikipedia) {
      assert.ok(n.wikipedia.startsWith('https://en.wikipedia.org/wiki/'));
      assert.ok(n.wikidata.startsWith('https://www.wikidata.org/entity/Q'));
      assert.ok(page.includes(n.wikipedia));
    }
    if (n.id.startsWith('local-')) assert.match(n.source_label, /local alumni record/);
  }
  assert.equal(nodes.get('60985').wikipedia, 'https://en.wikipedia.org/wiki/Gottfried_Wilhelm_Leibniz');
  assert.ok(graduates.some(n => n.other_advisors.length > 0));
});
