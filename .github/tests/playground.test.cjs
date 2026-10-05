const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const html = fs.readFileSync(path.join(__dirname, '../../playground/index.html'), 'utf8');
const script = html.match(/<script>([\s\S]*?)<\/script>/)[1];
function harness(overrides = {}) {
  const nodes = new Map();
  const context = {
    editor: { value: 'show "hello"', selectionStart: 0 },
    location: { origin: 'https://devheallabs.com', pathname: '/playground/' },
    document: { getElementById(id) {
      if (!nodes.has(id)) nodes.set(id, { value: '', textContent: '', innerHTML: '',
        classList: { values: new Set(), add(v) { this.values.add(v); }, remove(v) { this.values.delete(v); }, contains(v) { return this.values.has(v); }, toggle() {} },
        setAttribute() {} });
      return nodes.get(id);
    } },
    output: [], status: null, showTab() {}, clearOutput() {}, updateStatus() {}, notify() {},
    setStatus(type, text) { context.status = { type, text }; },
    renderOutput(text, error) { context.output.push({ text, error }); },
    btoa: value => Buffer.from(value, 'binary').toString('base64'),
    unescape, encodeURIComponent, AbortSignal, Date,
    PLAYGROUND_API: 'https://example.invalid/run', ...overrides
  };
  vm.createContext(context);
  for (const name of ['formatCode', 'generateShareUrl', 'runCode']) {
    const fn = script.match(new RegExp('(?:async )?function ' + name + '\\([^]*?\\n}'))[0];
    vm.runInContext(fn, context);
  }
  return context;
}
test('all inline JavaScript parses', () => new vm.Script(script));
test('normalization preserves branches, loops and multiline text', () => {
  const code = 'if ready:\r\n    show "ready"\r\nelse:\r\n    show "waiting"\r\nshow "done"\r\n';
  const ctx = harness(); ctx.editor.value = code; ctx.formatCode();
  assert.equal(ctx.editor.value, code.replace(/\r\n/g, '\n'));
  const multiline = 'show """\n  text with spaces  \n    indented content\n"""';
  ctx.editor.value = multiline; ctx.formatCode(); assert.equal(ctx.editor.value, multiline);
});
test('share links round-trip Unicode, plus, slash, quotes and multiline code', () => {
  for (const code of ['show "࠾"', 'show "తెలుగు 😀 + / ="\nshow "next"', '']) {
    const ctx = harness(); ctx.editor.value = code; ctx.generateShareUrl();
    const encoded = new URL(ctx.document.getElementById('shareUrl').value).searchParams.get('code');
    assert.equal(Buffer.from(encoded, 'base64').toString('utf8'), code);
  }
});
test('HTTP failures cannot report successful execution', async () => {
  const ctx = harness({ fetch: async () => ({ ok: false, status: 500, json: async () => ({ message: 'failure' }) }) });
  await ctx.runCode(); assert.equal(ctx.status.type, 'error'); assert.match(ctx.output[0].text, /HTTP 500/);
  assert.equal(ctx.document.getElementById('runBtn').classList.contains('running'), false);
});
test('malformed payloads, JSON failures and timeouts release the Run button', async () => {
  for (const fetch of [
    async () => ({ ok: true, json: async () => ({ message: 'unexpected' }) }),
    async () => ({ ok: true, json: async () => ({ output: 42 }) }),
    async () => ({ ok: true, json: async () => { throw new SyntaxError('Invalid JSON'); } }),
    async () => { const error = new Error('timeout'); error.name = 'TimeoutError'; throw error; }
  ]) {
    const ctx = harness({ fetch }); await ctx.runCode(); assert.equal(ctx.status.type, 'error');
    assert.equal(ctx.document.getElementById('runBtn').classList.contains('running'), false);
  }
});
test('successful, empty and program-error responses retain correct status', async () => {
  for (const [data, type] of [[{ output: 'hello' }, 'ok'], [{ output: '' }, 'ok'], [{ error: 'Syntax error' }, 'error']]) {
    const ctx = harness({ fetch: async () => ({ ok: true, json: async () => data }) });
    await ctx.runCode(); assert.equal(ctx.status.type, type);
  }
});
test('Tab and Shift+Tab are not intercepted by the editor', () => {
  const handler = script.match(/editor.addEventListener\('keydown', (e => \{[\s\S]*?\n\})\);/)[1];
  const ctx = harness(); vm.runInContext('handler = ' + handler, ctx);
  for (const shiftKey of [false, true]) {
    let prevented = false; ctx.handler({ key: 'Tab', shiftKey, preventDefault() { prevented = true; } });
    assert.equal(prevented, false);
  }
});
test('interactive cards and panel tabs use native keyboard controls', () => {
  assert.doesNotMatch(html, /<div[^>]+class="(?:dropdown-item|deploy-option|output-tab)[^"]*"[^>]+onclick=/);
  assert.equal((html.match(/role="tab" aria-controls=/g) || []).length, 3);
  assert.equal((html.match(/role="tabpanel" aria-labelledby=/g) || []).length, 3);
  assert.match(script, /const el = document.createElement\('button'\)/);
});

test('unconfigured runner downloads source without a network request', async () => {
  let downloaded = false;
  const ctx = harness({ PLAYGROUND_API: '', downloadCode() { downloaded = true; }, fetch() { throw new Error('Unexpected request'); } });
  await ctx.runCode(); assert.equal(downloaded, true);
});
