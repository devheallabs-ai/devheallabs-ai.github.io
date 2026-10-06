const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const root = path.resolve(__dirname, '../..');
const release = path.join(root, 'dh-adom/releases/1.0.0');
const pages = ['', 'whitepaper', 'specification', 'architecture', 'implementation', 'evaluation', 'security', 'research', 'downloads'];
test('every publication link, image and paper fragment resolves', () => {
  for (const page of pages) {
    const file = path.join(root, 'dh-adom', page, 'index.html');
    const html = fs.readFileSync(file, 'utf8');
    assert.equal((html.match(/<h1>/g) || []).length, 1, page);
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
    assert.equal(hash(path.join(release, name)), hash(path.join(root, '.github/dh-adom/source/01-White-Paper', name)), name);
  }
});
