import test from 'node:test';
import assert from 'node:assert/strict';
import {privacy, opacity, fairness, benefits} from '../source/assets/talks/hyperproperties.mjs';

test('noninterference claim agrees with every pair in the finite domain', () => {
  for (const leak of [false, true]) {
    for (let p = 0; p <= 3; p++) {
      const m = privacy(p, leak);
      assert.equal(m.holds, m.outputs[0] === m.outputs[1]);
    }
  }
});
test('opacity needs an existing route with all observations matching', () => {
  assert.equal(opacity('coarse', true).matches, true);
  assert.equal(opacity('distinguish', true).matches, false);
  assert.equal(opacity('coarse', false).matches, false);
  assert.equal(opacity('distinguish', false).matches, false);
});
test('fairness counterexamples are exactly integer scores 60 through 69', () => {
  for (const biased of [false, true]) {
    const witnesses = Array.from({length:101}, (_,i)=>i).filter(score => {
      const [a,b] = fairness(score,biased).decisions;
      return a !== b;
    });
    assert.deepEqual(witnesses, biased ? [60,61,62,63,64,65,66,67,68,69] : []);
    assert.equal(fairness(65,biased).violations, witnesses.length);
  }
});
test('the subtraction mutation violates the monotonicity requirement', () => {
  for (const bug of [false,true]) {
    const m=benefits(bug);
    assert.equal(m.holds,m.values[1]>=m.values[0]);
  }
});
