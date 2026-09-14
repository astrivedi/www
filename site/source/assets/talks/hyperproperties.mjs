// Finite teaching models. These functions do not verify the research systems.
export function privacy(p, leak) {
  return { outputs: [p, p + Number(leak)], holds: !leak };
}
export function opacity(sensor, alternative) {
  const secret = ['P', 'Q', 'P'];
  const other = sensor === 'coarse' ? ['P', 'Q', 'P'] : ['P', 'R', 'P'];
  return { secret, other: alternative ? other : null, matches: alternative && secret.every((x, i) => x === other[i]) };
}
export function fairness(score, biased) {
  return { decisions: [score >= 60, score >= (biased ? 70 : 60)], violations: biased ? 10 : 0 };
}
export function benefits(bug) {
  return { values: [10, bug ? 8 : 12], holds: !bug };
}

if (typeof document !== 'undefined') {
  for (const example of document.querySelectorAll('[data-example]')) {
    const controls = example.querySelector('.talk-controls');
    const result = example.querySelector('[data-result]');
    const rows = example.querySelector('[data-rows]');
    const field = name => controls.querySelector(`[name="${name}"]`);
    const table = values => rows.replaceChildren(...values.map(values => {
      const row = document.createElement('tr');
      for (const value of values) {
        const cell = document.createElement('td');
        cell.textContent = value;
        row.append(cell);
      }
      return row;
    }));
    function update() {
      switch (example.dataset.example) {
        case 'privacy': {
          const p = Number(field('public').value);
          const model = privacy(p, field('leak').checked);
          table([[0, p, model.outputs[0]], [1, p, model.outputs[1]]]);
          result.textContent = model.holds
            ? `Both outputs are ${p}. With O = p, all four public-input cases satisfy noninterference in this finite model.`
            : `The outputs differ: ${p} versus ${p + 1}. Changing the secret changes the observation. Each of the four public-input cases is a counterexample.`;
          break;
        }
        case 'opacity': {
          const model = opacity(field('sensor').value, field('alternative').checked);
          table([['Secret', model.secret.join(' → ')], ['Nonsecret', model.other ? model.other.join(' → ') : 'No route included']]);
          result.textContent = model.matches
            ? 'A matching nonsecret route exists for the illustrated secret route.'
            : 'No matching nonsecret route exists in the illustrated model. This observation sequence distinguishes the secret start.';
          break;
        }
        case 'fairness': {
          const score = Number(field('score').value);
          const model = fairness(score, field('biased').checked);
          example.querySelector('[data-score]').textContent = score;
          table(model.decisions.map((accept, i) => [i ? 'B' : 'A', score, accept ? 'Accept' : 'Reject']));
          result.textContent = (model.decisions[0] === model.decisions[1]
            ? `The outcomes agree at score ${score}. ` : `The outcomes differ at score ${score}. `)
            + (model.violations ? 'Scores 60–69 violate the specified equality relation in this finite model.'
              : 'All 101 integer scores satisfy the specified equality relation in this finite model.');
          break;
        }
        case 'benefits': {
          const model = benefits(field('bug').checked);
          table([['Not eligible', model.values[0]], ['Eligible', model.values[1]]]);
          result.textContent = model.holds
            ? '12 ≥ 10: the eligibility change respects the stated relation.'
            : '8 < 10: gaining eligibility reduces the benefit. This pair violates the stated relation.';
          break;
        }
      }
    }
    controls.hidden = false;
    controls.addEventListener('input', update);
    controls.addEventListener('change', update);
    update();
  }
}
