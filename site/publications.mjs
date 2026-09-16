export function normalize(value) {
  return value.normalize('NFKD').replace(/\p{M}/gu, '').toLocaleLowerCase().replace(/[^\p{L}\p{N}]+/gu, ' ').trim();
}
export function matchesPublication(text, topics, query, topic) {
  const terms = normalize(query).split(/\s+/).filter(Boolean);
  const searchable = normalize(text);
  return (!topic || topics.includes(topic)) && terms.every(term => searchable.includes(term));
}

if (typeof document !== 'undefined') {
  const form = document.querySelector('#publication-filters');
  if (form) {
    const search = form.querySelector('#paper-search');
    const topic = form.querySelector('#paper-topic');
    const sections = [...document.querySelectorAll('.publication-year')];
    const papers = [...document.querySelectorAll('.publication-year .publication')].map(element => ({
      element, text: element.textContent, topics: element.dataset.topics.split(' ')
    }));
    const yearLinks = [...document.querySelectorAll('.year-nav a')];
    function update() {
      let count = 0;
      for (const paper of papers) {
        paper.element.hidden = !matchesPublication(paper.text, paper.topics, search.value, topic.value);
        if (!paper.element.hidden) count++;
      }
      sections.forEach((section, index) => {
        section.hidden = ![...section.querySelectorAll('.publication')].some(p => !p.hidden);
        yearLinks[index].hidden = section.hidden;
      });
      document.querySelector('.year-nav').hidden = count === 0;
      form.querySelector('#publication-count').textContent = `${count} of ${papers.length} publications`;
      document.querySelector('#publication-empty').hidden = count > 0;
    }
    form.addEventListener('submit', event => event.preventDefault());
    search.addEventListener('input', update);
    topic.addEventListener('change', update);
    form.addEventListener('reset', () => { search.value = ''; topic.value = ''; update(); });
    form.hidden = false;
    update();
  }
}
