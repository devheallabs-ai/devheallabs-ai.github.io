(function () {
  'use strict';
  const form = document.getElementById('enquiry-form');
  if (form) {
    if (new URLSearchParams(location.search).get('interest') === 'dummu') form.elements.interest.value = 'Dummu demonstration';
    form.addEventListener('submit', function (event) {
      event.preventDefault();
      if (!form.reportValidity()) return;
      const data = new FormData(form);
      const text = ['DevHeal enquiry', '', 'Name: ' + data.get('name'), 'Work email: ' + data.get('email'), 'Company: ' + data.get('company'), 'Interest: ' + data.get('interest'), '', 'Business challenge:', data.get('challenge'), '', 'Preferred times and timezone: ' + (data.get('availability') || 'To be discussed')].join('\n');
      document.getElementById('enquiry-text').value = text;
      document.getElementById('enquiry-email').href = 'mailto:sales@devheallabs.com?subject=' + encodeURIComponent('DevHeal enquiry: ' + data.get('interest')) + '&body=' + encodeURIComponent(text);
      document.getElementById('copy-status').textContent = '';
      const result = document.getElementById('enquiry-result'); result.hidden = false; result.scrollIntoView({block:'nearest'});
    });
    document.getElementById('copy-enquiry').addEventListener('click', async function () {
      const text = document.getElementById('enquiry-text');
      try { await navigator.clipboard.writeText(text.value); document.getElementById('copy-status').textContent = 'Enquiry copied. Paste it into an email to sales@devheallabs.com.'; }
      catch (_) { text.focus(); text.select(); document.getElementById('copy-status').textContent = 'Select and copy the enquiry text above, then paste it into your email.'; }
    });
  }
  const steps = [
    ['Describe the goal', 'Describe a repeatable task in plain English: investigate a service alert, collect the relevant context, and propose the next action for review.', 'Business intent → Agent definition'],
    ['Set the boundaries', 'Review the generated definition. Choose allowed tools, namespace access, and the approvals needed before an agent can act.', 'Agent definition → Tools + policy + approval'],
    ['Review and act', 'Inspect the proposed action and its context. Apply policy checks and the required approval before execution, then retain the audit evidence.', 'Proposed action → Approval → Execution record'],
    ['Learn from outcomes', 'Use resolution success, elapsed time, tool efficiency, and operator feedback to inform future diagnostic choices within the same governance boundaries.', 'Recorded outcome → Feedback → Updated recommendations']
  ];
  document.querySelectorAll('[data-step]').forEach(function (button) {
    button.addEventListener('click', function () {
      const step = steps[Number(button.dataset.step)];
      document.querySelectorAll('[data-step]').forEach(function (item) { item.setAttribute('aria-pressed', String(item === button)); });
      document.getElementById('walk-title').textContent = step[0];
      document.getElementById('walk-copy').textContent = step[1];
      document.getElementById('walk-artifact').textContent = step[2];
    });
  });
})();
