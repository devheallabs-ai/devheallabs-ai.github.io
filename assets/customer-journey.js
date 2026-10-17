(function () {
  'use strict';

  // 1. Contact Form Enquiry Handler & URL Parameter Pre-Selection
  var form = document.getElementById('enquiry-form');
  if (form) {
    var query = new URLSearchParams(location.search);
    var param = query.get('interest');
    if (query.get('offer') === 'collaboration' && form.elements.request) form.elements.request.value = 'Partnership discussion';
    if (query.get('offer') === 'pilot' && form.elements.request) form.elements.request.value = 'Free pilot';
    var map = {
      'partnership': 'Partnership & collaboration',
      'steadystate': 'SteadyState platform demonstration',
      'dummu': 'SteadyState platform demonstration',
      'nova': 'Nova model demonstration',
      'podotl': 'Podotl intelligence demonstration',
      'agentproving': 'D-AgentProving assurance demonstration',
      'twinvoke': 'D-TwinVoke digital twin early access',
      'services': 'Custom AI engineering & integration',
      'private-ai': 'Private & local CPU inference (NC AI)'
    };
    if (param && map[param] && form.elements.interest) {
      form.elements.interest.value = map[param];
    }
    form.addEventListener('submit', function (event) {
      event.preventDefault();
      if (!form.reportValidity()) return;
      var data = new FormData(form);
      var text = [
        'DevHeal Labs AI — Enterprise Workflow Enquiry',
        '',
        'Name: ' + data.get('name'),
        'Work email: ' + data.get('email'),
        'Company: ' + data.get('company'),
        'Primary interest: ' + data.get('interest'),
        'Request: ' + (data.get('request') || 'Product demonstration'),
        '',
        'Target workflow & infrastructure environment:',
        data.get('challenge'),
        '',
        'Preferred times & timezone: ' + (data.get('availability') || 'To be discussed')
      ].join('\n');
      document.getElementById('enquiry-text').value = text;
      document.getElementById('enquiry-email').href =
        'mailto:sales@devheallabs.com?subject=' +
        encodeURIComponent('DevHeal enquiry: ' + data.get('interest')) +
        '&body=' +
        encodeURIComponent(text);
      document.getElementById('copy-status').textContent = '';
      var result = document.getElementById('enquiry-result');
      result.hidden = false;
      result.scrollIntoView({ block: 'nearest' });
    });
    var copyBtn = document.getElementById('copy-enquiry');
    if (copyBtn) {
      copyBtn.addEventListener('click', async function () {
        var text = document.getElementById('enquiry-text');
        try {
          await navigator.clipboard.writeText(text.value);
          document.getElementById('copy-status').textContent =
            'Enquiry copied. Paste it into an email to sales@devheallabs.com.';
        } catch (_) {
          text.focus();
          text.select();
          document.getElementById('copy-status').textContent =
            'Select and copy the enquiry text above, then paste it into your email.';
        }
      });
    }
  }

  // 2. Interactive Homepage Hero Console Tabs
  var consoleTabs = document.querySelectorAll('[data-console-tab]');
  if (consoleTabs.length) {
    consoleTabs.forEach(function (tab) {
      tab.addEventListener('click', function () {
        var targetId = tab.getAttribute('data-console-tab');
        consoleTabs.forEach(function (t) {
          t.setAttribute('aria-selected', String(t === tab));
        });
        document.querySelectorAll('[data-console-pane]').forEach(function (pane) {
          pane.hidden = pane.getAttribute('data-console-pane') !== targetId;
        });
      });
    });
  }

  // 3. Interactive SteadyState SRE Incident & Governance Console Walkthrough
  var steps = [
    [
      '01 · Ingest Alert & Correlate Cluster Context',
      'SteadyState ingests PagerDuty/Prometheus alerts, correlates recent Kubernetes deployments, pod OOM events, and upstream service dependencies, and computes a diagnostic confidence score.',
      '[ALERT #INC-4821] namespace=prod-payments pod=checkout-api-7d9f8b\nSignal Correlation: OOMKilled (exit 137) after deploy v2.14.3 (+42% heap)\nRecommended Action: Rollback deployment/checkout-api -> rev 2.14.2 (Confidence: 0.94)'
    ],
    [
      '02 · Enforce AGP Policy & Blast-Radius Pre-Flight',
      'Before any cluster mutation can occur, the Agent Governance Protocol (AGP) verifies namespace RBAC boundaries, active change-freeze windows, and dry-run simulation results.',
      '[AGP POLICY GATE] Evaluating action: kubectl rollout undo deployment/checkout-api\n✓ Namespace boundary: prod-payments (Allowed)\n✓ Change freeze check: No active freeze window\n✓ Dry-run preflight: 3/3 replicas healthy in staging twin\n⚠ Execution Policy: Consequential prod write requires Two-Person Approval (Entra ID)'
    ],
    [
      '03 · Two-Person Approval & Cryptographic Execution',
      'On-call SREs review the exact proposed diff and preflight evidence via Slack/Teams or the SteadyState console. Single-use Microsoft Entra ID approvals unlock bounded execution.',
      '[APPROVAL GATE] Required: 2 of 2 (Role: SRE-Prod-Approver via Microsoft Entra ID)\n✓ Approved by: a.sharma@enterprise.example (14:22:09 UTC)\n✓ Approved by: r.patel@enterprise.example (14:22:41 UTC)\n[EXECUTING] Rollback rev 2.14.2 applied -> Pod readiness 3/3 in 18s'
    ],
    [
      '04 · Hash-Chained Audit Receipt & RL Policy Update',
      'Every signal, policy check, approval signature, and execution outcome is written to a tamper-evident SHA-256 hash-chained ledger, updating diagnostic weights within fixed governance boundaries.',
      '[MERKLE AUDIT RECEIPT #8f92a1c4] prev_hash=3b7e90...8a12 | sig=VERIFIED\nOutcome: MTTR reduced from 47m baseline -> 4m 12s (SLO recovered)\nRL Policy Update: Diagnostic weight for OOM-post-deploy +0.03 (Authority boundary unchanged)'
    ]
  ];
  document.querySelectorAll('[data-step]').forEach(function (button) {
    button.addEventListener('click', function () {
      var step = steps[Number(button.dataset.step)];
      if (!step) return;
      document.querySelectorAll('[data-step]').forEach(function (item) {
        item.setAttribute('aria-pressed', String(item === button));
      });
      var titleEl = document.getElementById('walk-title');
      var copyEl = document.getElementById('walk-copy');
      var artEl = document.getElementById('walk-artifact');
      if (titleEl) titleEl.textContent = step[0];
      if (copyEl) copyEl.textContent = step[1];
      if (artEl) artEl.textContent = step[2];
    });
  });
})();
