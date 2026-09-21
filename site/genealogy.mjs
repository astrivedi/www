// Return all branches from an ancestor to the focal person, including merges.
export function pathsToRoot(nodes, root, ancestor) {
  const byId = new Map(nodes.map(n => [n.id, n]));
  const memo = new Map();
  const reaches = id => {
    if (memo.has(id)) return memo.get(id);
    const result = id === ancestor || byId.get(id).advisors.some(reaches);
    memo.set(id, result);
    return result;
  };
  const people = new Set(), edges = new Set();
  const visit = id => {
    if (!reaches(id) || people.has(id)) return;
    people.add(id);
    if (id === ancestor) return;
    for (const advisor of byId.get(id).advisors) {
      if (reaches(advisor)) { edges.add(`edge-${advisor}-${id}`); visit(advisor); }
    }
  };
  visit(root);
  return { people, edges };
}

export const normalizeName = name => name.normalize('NFD').replace(/\p{M}/gu, '').toLocaleLowerCase();

function init() {
  const container = document.getElementById('genealogy');
  if (!container) return;
  const data = JSON.parse(document.getElementById('genealogy-data').textContent);
  const nodes = new Map(data.nodes.map(n => [n.id, n]));
  const svg = document.getElementById('ancestry-graph');
  const stage = container.querySelector('.genealogy-stage');
  const detail = document.getElementById('genealogy-selection');
  const nodeElements = [...svg.querySelectorAll('.node')];
  const edgeElements = [...svg.querySelectorAll('.edge')];
  const full = svg.getAttribute('viewBox').split(/\s+/).map(Number);
  let view = [...full], selected = null;
  let moved = false;
  const overview = document.getElementById('ancestry-overview');
  overview.setAttribute('viewBox', full.join(' '));
  const miniature = svg.querySelector('g.graph').cloneNode(true);
  miniature.removeAttribute('id');
  miniature.querySelectorAll('[id]').forEach(el => el.removeAttribute('id'));
  miniature.querySelectorAll('text,title').forEach(el => el.remove());
  overview.append(miniature);
  const frame = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
  frame.classList.add('overview-viewport');
  overview.append(frame);

  function update() {
    // Keep at least part of the graph in view, even after a long drag.
    view[0] = Math.max(full[0] - view[2] * .8, Math.min(full[0] + full[2] - view[2] * .2, view[0]));
    view[1] = Math.max(full[1] - view[3] * .8, Math.min(full[1] + full[3] - view[3] * .2, view[1]));
    svg.setAttribute('viewBox', view.join(' '));
    ['x', 'y', 'width', 'height'].forEach((a, i) => frame.setAttribute(a, view[i]));
    const pixelScale = Math.min(svg.clientWidth / view[2], svg.clientHeight / view[3]);
    svg.classList.toggle('hide-labels', pixelScale < .55);
  }
  function fit() {
    // Use the viewport aspect ratio so dragging and centering are predictable.
    const ratio = svg.clientWidth / svg.clientHeight;
    const width = Math.max(full[2], full[3] * ratio);
    const height = width / ratio;
    view = [full[0] + (full[2] - width) / 2, full[1] + (full[3] - height) / 2, width, height];
    update();
  }
  function point(clientX, clientY) {
    return new DOMPoint(clientX, clientY).matrixTransform(svg.getScreenCTM().inverse());
  }
  function zoom(factor, at = null) {
    const minWidth = Math.min(240, full[2]);
    const width = Math.max(minWidth, Math.min(Math.max(full[2], full[3] * svg.clientWidth / svg.clientHeight) * 1.5, view[2] * factor));
    const applied = width / view[2];
    const anchor = at || {x: view[0] + view[2] / 2, y: view[1] + view[3] / 2};
    view = [anchor.x - (anchor.x - view[0]) * applied, anchor.y - (anchor.y - view[1]) * applied, width, view[3] * applied];
    update();
  }
  function center(id) {
    const el = document.getElementById(`person-${id}`);
    const box = el.getBBox();
    const local = new DOMPoint(box.x + box.width / 2, box.y + box.height / 2);
    const at = local.matrixTransform(el.getCTM()).matrixTransform(svg.getCTM().inverse());
    const width = svg.clientWidth < 600
      ? Math.max(box.width * 1.12, svg.clientWidth * 1.05)
      : Math.max(box.width * 2.5, Math.min(850, svg.clientWidth * 1.2));
    const height = width * svg.clientHeight / svg.clientWidth;
    view = [at.x - width / 2, at.y - height / 2, width, height];
    update();
  }
  function highlight(id) {
    const path = !id || id === data.root ? null : nodes.get(id).kind === 'graduate'
      ? pathsToRoot(data.nodes, id, data.root) : pathsToRoot(data.nodes, data.root, id);
    nodeElements.forEach(el => {
      const ident = el.id.replace('person-', '');
      el.classList.toggle('dimmed', !!path && !path.people.has(ident));
      el.classList.toggle('selected', ident === id);
      el.setAttribute('aria-pressed', String(ident === selected));
    });
    edgeElements.forEach(el => {
      el.classList.toggle('dimmed', !!path && !path.edges.has(el.id));
      el.classList.toggle('highlighted', !!path && path.edges.has(el.id));
    });
  }
  function select(id, navigate = false) {
    selected = id;
    highlight(id);
    const record = nodes.get(id);
    detail.replaceChildren();
    const name = document.createElement('strong'); name.textContent = record.name;
    detail.append(name, ` · ${record.degree || 'Degree not recorded'}. `);
    if (record.thesis) detail.append(`Dissertation: ${record.thesis}. `);
    if (record.other_advisors?.length) {
      detail.append('Co-advised with ');
      record.other_advisors.forEach((advisor, i) => {
        if (i) detail.append(', ');
        const a = document.createElement('a'); a.href = advisor.url; a.textContent = advisor.name;
        detail.append(a);
      });
      detail.append('. ');
    }
    const link = document.createElement('a'); link.href = record.url; link.textContent = record.source_label || 'MGP record';
    detail.append(link);
    if (record.wikipedia) {
      const wiki = document.createElement('a'); wiki.href = record.wikipedia; wiki.textContent = 'Wikipedia';
      wiki.target = '_blank'; wiki.rel = 'noopener noreferrer';
      detail.append(' · ', wiki);
    }
    if (navigate) center(id);
  }
  function activate(id, navigate = false) {
    select(id, navigate);
    const wikipedia = nodes.get(id).wikipedia;
    if (wikipedia) window.open(wikipedia, '_blank', 'noopener,noreferrer');
  }
  nodeElements.forEach(el => {
    const id = el.id.replace('person-', '');
    el.classList.toggle('graduate', nodes.get(id).kind === 'graduate');
    el.setAttribute('role', 'button');
    el.setAttribute('tabindex', '0');
    el.setAttribute('aria-label', `${nodes.get(id).name}. ${nodes.get(id).degree}. Show connections${nodes.get(id).wikipedia ? ' and open Wikipedia in a new tab' : ''}.`);
    el.addEventListener('click', () => { if (!moved) activate(id); });
    el.addEventListener('keydown', event => {
      if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); event.stopPropagation(); activate(id, true); }
    });
    el.addEventListener('focus', () => { if (el.matches(':focus-visible')) center(id); highlight(id); });
    el.addEventListener('blur', () => highlight(selected));
    el.addEventListener('pointerenter', event => { if (event.pointerType === 'mouse') highlight(id); });
    el.addEventListener('pointerleave', () => highlight(selected));
  });
  document.querySelectorAll('.genealogy-graduates [data-person]').forEach(link => {
    link.addEventListener('click', event => {
      event.preventDefault();
      svg.focus({preventScroll: true});
      select(link.dataset.person, true);
      stage.scrollIntoView({block: 'center'});
    });
  });
  // Open the text alternative for fragment links, including no-script navigation.
  function revealRecord() {
    if (location.hash.startsWith('#record-')) document.getElementById('genealogy-text-view').open = true;
  }
  window.addEventListener('hashchange', revealRecord);
  revealRecord();
  document.getElementById('genealogy-search').addEventListener('submit', event => {
    event.preventDefault();
    const query = normalizeName(document.getElementById('ancestor-search').value.trim());
    const matches = data.nodes.filter(n => normalizeName(n.name).includes(query));
    const exact = matches.find(n => normalizeName(n.name) === query);
    if (query && (exact || matches.length === 1)) select((exact || matches[0]).id, true);
    else detail.textContent = !query ? 'Enter a name to find an ancestor.' : matches.length ? `${matches.length} matches. Choose a full name from the suggestions.` : 'No matching person in this ancestry.';
  });
  document.getElementById('zoom-in').onclick = () => zoom(.7);
  document.getElementById('zoom-out').onclick = () => zoom(1 / .7);
  document.getElementById('fit-graph').onclick = fit;
  document.getElementById('focus-root').onclick = () => select(data.root, true);
  document.getElementById('clear-path').onclick = () => {
    selected = null; highlight(null); detail.textContent = 'Select a name to explore its connections.';
  };
  const expand = document.getElementById('expand-graph');
  expand.hidden = !container.requestFullscreen;
  expand.onclick = async () => {
    try {
      if (document.fullscreenElement) await document.exitFullscreen();
      else await container.requestFullscreen();
    } catch { detail.textContent = 'Full screen is unavailable in this browser. Use the SVG download for a larger view.'; }
  };
  document.addEventListener('fullscreenchange', () => {
    expand.textContent = document.fullscreenElement ? 'Exit full screen' : 'Full screen';
    fit();
  });
  svg.addEventListener('keydown', event => {
    const delta = {ArrowLeft: [-.12, 0], ArrowRight: [.12, 0], ArrowUp: [0, -.12], ArrowDown: [0, .12]}[event.key];
    if (delta) { event.preventDefault(); view[0] += delta[0] * view[2]; view[1] += delta[1] * view[3]; update(); }
    else if (event.key === '+' || event.key === '=') { event.preventDefault(); zoom(.7); }
    else if (event.key === '-') { event.preventDefault(); zoom(1 / .7); }
    else if (event.key === 'Home') { event.preventDefault(); fit(); }
    else if (event.key === 'Escape') { selected = null; highlight(null); }
  });
  // Ordinary wheel scroll still scrolls the page; modified wheel zooms the graph.
  svg.addEventListener('wheel', event => {
    if (!event.ctrlKey && !event.metaKey) return;
    event.preventDefault();
    zoom(Math.exp(Math.max(-.4, Math.min(.4, event.deltaY * .005))), point(event.clientX, event.clientY));
  }, {passive: false});
  const pointers = new Map();
  svg.addEventListener('pointerdown', event => {
    if (event.button !== 0) return;
    moved = false;
    pointers.set(event.pointerId, {x: event.clientX, y: event.clientY});
    // Capture on the original target to preserve node clicks after release.
    event.target.setPointerCapture(event.pointerId);
  });
  svg.addEventListener('pointermove', event => {
    if (!pointers.has(event.pointerId)) return;
    const old = pointers.get(event.pointerId), next = {x: event.clientX, y: event.clientY};
    if (Math.hypot(next.x - old.x, next.y - old.y) > 2) moved = true;
    if (pointers.size === 2) {
      const other = [...pointers.entries()].find(([id]) => id !== event.pointerId)[1];
      const before = Math.hypot(old.x - other.x, old.y - other.y);
      const after = Math.hypot(next.x - other.x, next.y - other.y);
      if (before && after) zoom(before / after, point((next.x + other.x) / 2, (next.y + other.y) / 2));
    } else {
      const start = point(old.x, old.y), end = point(next.x, next.y);
      view[0] += start.x - end.x; view[1] += start.y - end.y; update();
    }
    pointers.set(event.pointerId, next);
  });
  for (const type of ['pointerup', 'pointercancel', 'lostpointercapture']) svg.addEventListener(type, event => pointers.delete(event.pointerId));
  container.querySelectorAll('.genealogy-controls, .genealogy-overview, .interactive-help').forEach(el => el.hidden = false);
  container.classList.add('is-interactive');
  let previousSize = [svg.clientWidth, svg.clientHeight];
  new ResizeObserver(() => {
    const size = [svg.clientWidth, svg.clientHeight];
    if (size[0] === previousSize[0] && size[1] === previousSize[1]) return;
    const cx = view[0] + view[2] / 2, cy = view[1] + view[3] / 2;
    const width = view[2] * size[0] / previousSize[0];
    const height = width * size[1] / size[0];
    view = [cx - width / 2, cy - height / 2, width, height];
    previousSize = size;
    update();
  }).observe(stage);
  highlight(null);
  fit();
}

if (typeof document !== 'undefined') init();
