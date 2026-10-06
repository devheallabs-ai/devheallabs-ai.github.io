const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const root = path.resolve(__dirname, '../..');
const release = path.join(root, 'dh-adom/releases/1.1.0');
const pages = ['', 'whitepaper', 'specification', 'architecture', 'implementation', 'evaluation', 'security', 'research', 'downloads', 'adoption', 'schemas', 'conformance'];
test('every publication link, image and paper fragment resolves', () => {
  for (const page of pages) {
    const file = path.join(root, 'dh-adom', page, 'index.html');
    const html = fs.readFileSync(file, 'utf8');
    assert.equal((html.match(/<h1>/g) || []).length, 1, page);
    assert.ok(!html.includes('Autonomous Twin') && !html.includes('devheallabs.in'), page);
    const ids = [...html.matchAll(/\bid="([^"]+)"/g)].map(m => m[1]);
    assert.equal(new Set(ids).size, ids.length, `duplicate IDs: ${page}`);
    for (const [, ref] of html.matchAll(/(?:href|src)="([^"]+)"/g)) {
      if (ref.startsWith('#')) { assert.ok(ids.includes(ref.slice(1)), ref); continue; }
      if (!ref.startsWith('/')) continue;
      const pathname = ref.split(/[?#]/)[0];
      const target = path.join(root, pathname);
      assert.ok(fs.existsSync(target), `${page}: ${ref}`);
      if (pathname.endsWith('/')) assert.ok(fs.existsSync(path.join(target, 'index.html')), ref);
    }
  }
});
test('download checksums match the delivered files and original papers', () => {
  const hash = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
  const checksums = JSON.parse(fs.readFileSync(path.join(release, 'checksums.json')));
  for (const [name, expected] of Object.entries(checksums)) assert.equal(hash(path.join(release, name)), expected, name);
  for (const name of ['DH-ADOM_White_Paper_v1.0.pdf', 'DH-ADOM_White_Paper_v1.1-illustrated.docx']) {
    assert.equal(hash(path.join(root, 'dh-adom/releases/1.0.0', name)), hash(path.join(root, '.github/dh-adom/originals', name)), name);
  }
});
test('conformance mapping covers every requirement without claiming certification', () => {
  const map = JSON.parse(fs.readFileSync(path.join(root, 'dh-adom/source/05-Conformance-Validation-Suite/coverage.json')));
  assert.equal(map.requirements.length, 20);
  assert.equal(new Set(map.requirements.map(r => r.id)).size, 20);
  for (const requirement of map.requirements) {
    assert.ok(fs.existsSync(path.join(root, 'dh-adom/source', requirement.source)));
    assert.ok(requirement.validation && requirement.observed);
    assert.notEqual(requirement.status, 'PASS');
  }
});
test('current paper preserves multiline contracts and semantic conformance tables', () => {
  const paper = fs.readFileSync(path.join(root, 'dh-adom/whitepaper/index.html'), 'utf8');
  assert.match(paper, /DelegationContract:\r?\n/);
  const spec = fs.readFileSync(path.join(root, 'dh-adom/specification/index.html'), 'utf8');
  assert.match(spec, /<th scope="col">ID<\/th>/);
  assert.doesNotMatch(spec, /<p>\| CR-/);
});
