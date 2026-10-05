const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const source = fs.readFileSync(path.join(__dirname, '../../assets/site.js'), 'utf8');
const reveal = source.match(/function revealFragment\(\) \{[\s\S]*?\n  \}/)[0];
test('deep links expand every enclosing architecture disclosure before scrolling', () => {
  const outer = { tagName: 'DETAILS', open: false, parentElement: null };
  const inner = { tagName: 'DETAILS', open: false, parentElement: outer };
  let scrolled = false;
  const target = { tagName: 'DIV', parentElement: inner, scrollIntoView() { assert.equal(outer.open, true); assert.equal(inner.open, true); scrolled = true; } };
  const ctx = { location: { hash: '#recovery-engine' }, document: { getElementById: id => id === 'recovery-engine' ? target : null }, requestAnimationFrame: fn => fn() };
  vm.createContext(ctx); vm.runInContext(reveal, ctx); ctx.revealFragment(); assert.equal(scrolled, true);
});
test('malformed and missing fragments do not interrupt navigation initialization', () => {
  for (const hash of ['#%ZZ', '#missing', '']) {
    const ctx = { location: { hash }, document: { getElementById: () => null } };
    vm.createContext(ctx); vm.runInContext(reveal, ctx); assert.doesNotThrow(() => ctx.revealFragment());
  }
});
