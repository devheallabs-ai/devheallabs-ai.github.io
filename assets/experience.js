(function () {
  'use strict';
  document.querySelectorAll('[data-panel-group]').forEach(function (group) {
    var buttons = Array.from(group.querySelectorAll('[data-panel]'));
    var panels = buttons.map(function (button) { return document.getElementById(button.dataset.panel); });
    if (!buttons.length || panels.some(function (panel) { return !panel; })) return;
    function select(index, focus) {
      buttons.forEach(function (button, i) {
        button.setAttribute('aria-pressed', String(i === index));
        panels[i].hidden = i !== index;
      });
      if (focus) buttons[index].focus();
    }
    buttons.forEach(function (button, index) {
      button.addEventListener('click', function () { select(index, false); });
      button.addEventListener('keydown', function (event) {
        var next;
        if (event.key === 'ArrowRight') next = (index + 1) % buttons.length;
        if (event.key === 'ArrowLeft') next = (index + buttons.length - 1) % buttons.length;
        if (event.key === 'Home') next = 0;
        if (event.key === 'End') next = buttons.length - 1;
        if (next !== undefined) { event.preventDefault(); select(next, true); }
      });
    });
    select(0, false);
  });
  // Content remains visible if animation or JavaScript is unavailable.
  var reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (!reduced && 'IntersectionObserver' in window && Element.prototype.animate) {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.animate([{ opacity: 0.6, transform: 'translateY(12px)' }, { opacity: 1, transform: 'translateY(0)' }], { duration: 380, easing: 'ease-out' });
        observer.unobserve(entry.target);
      });
    }, { threshold: 0.12 });
    document.querySelectorAll('.business-refresh section:not(.business-intro) .sec-title').forEach(function (title) { observer.observe(title); });
  }
})();
