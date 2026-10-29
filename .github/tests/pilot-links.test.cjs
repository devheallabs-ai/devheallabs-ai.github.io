const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname, '../..');

function pages(dir) {
  return fs.readdirSync(dir, { withFileTypes: true }).flatMap(entry => {
    if (entry.name.startsWith('.') || entry.name === 'node_modules') return [];
    const file = path.join(dir, entry.name);
    return entry.isDirectory() ? pages(file) : file.endsWith('.html') ? [file] : [];
  });
}

test('every Start a free pilot button opens the SteadyState sandbox', () => {
  let count = 0;
  for (const file of pages(root)) {
    const html = fs.readFileSync(file, 'utf8');
    for (const [anchor] of html.matchAll(/<a\b[^>]*>[\s\S]*?<\/a>/g)) {
      const label = anchor.replace(/<[^>]+>/g, '').trim();
      if (!label.startsWith('Start a free pilot')) continue;
      assert.match(anchor, /href="https:\/\/sandbox\.devheallabs\.com\/"/, file);
      count++;
    }
  }
  assert.ok(count >= 58, 'shared navigation and homepage pilot buttons are covered');
});

test('other products retain their own pilot enquiry routes', () => {
  for (const [file, interest] of [['physical-ai/index.html', 'physical-ai'], ['agentproving/index.html', 'agentproving'], ['products/nova/index.html', 'nova']]) {
    assert.ok(fs.readFileSync(path.join(root, file), 'utf8').includes(`/contact/?interest=${interest}&amp;offer=pilot`), file);
  }
});
