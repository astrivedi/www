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

test('snapshot is complete, unique, acyclic, connected, and fully represented in SVG', () => {
  const data = JSON.parse(readFileSync(new URL('../genealogy/data.json', import.meta.url)));
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
  assert.equal(seen.size, nodes.size);
  assert.ok(data.nodes.some(n => n.advisors.length > 1));
});
