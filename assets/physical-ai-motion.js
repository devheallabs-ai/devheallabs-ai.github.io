(function () {
  'use strict';
  var preference = window.matchMedia('(prefers-reduced-motion: reduce)');
  var cards = document.querySelectorAll('.motion-card');
  function play(card) {
    if (preference.matches) return;
    card.classList.remove('is-playing');
    void card.offsetWidth;
    card.classList.add('is-playing');
  }
  var observer = 'IntersectionObserver' in window ? new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) { play(entry.target); observer.unobserve(entry.target); }
    });
  }, { threshold: 0.25 }) : null;
  cards.forEach(function (card) {
    var button = card.querySelector('.motion-replay');
    button.hidden = preference.matches;
    button.addEventListener('click', function () { play(card); });
    if (observer) observer.observe(card);
  });
  preference.addEventListener('change', function () {
    cards.forEach(function (card) {
      card.classList.remove('is-playing');
      card.querySelector('.motion-replay').hidden = preference.matches;
    });
  });
})();
