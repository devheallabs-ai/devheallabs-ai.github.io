(function () {
  'use strict';
  const dialog = document.getElementById('diagram-viewer');
  if (!dialog || typeof dialog.showModal !== 'function') return;
  const image = document.getElementById('diagram-image');
  const title = document.getElementById('diagram-title');
  const scaleLabel = document.getElementById('diagram-scale');
  let scale = 1, baseWidth = 600, opener;
  function resize() {
    image.style.width = Math.round(baseWidth * scale) + 'px';
    scaleLabel.value = Math.round(scale * 100) + '%';
    dialog.querySelector('[data-zoom="out"]').disabled = scale <= 1;
    dialog.querySelector('[data-zoom="in"]').disabled = scale >= 3;
  }
  document.querySelectorAll('[data-diagram]').forEach(button => {
    button.addEventListener('click', () => {
      opener = button; scale = 1;
      title.textContent = button.dataset.title;
      image.alt = button.dataset.title;
      image.src = button.dataset.diagram;
      dialog.showModal();
      baseWidth = Math.min(600, dialog.querySelector('.diagram-scroll').clientWidth - 24);
      resize();
    });
  });
  dialog.querySelectorAll('[data-zoom]').forEach(button => {
    button.addEventListener('click', () => {
      scale = Math.max(1, Math.min(3, scale + (button.dataset.zoom === 'in' ? .25 : -.25)));
      resize();
    });
  });
  document.getElementById('diagram-close').addEventListener('click', () => dialog.close());
  dialog.addEventListener('close', () => { if (opener) opener.focus(); });
}());
