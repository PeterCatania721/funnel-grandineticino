/**
 * Grandineticino.ch — upload foto (form hero + form bottom) + mobile UX.
 */
(function () {
  'use strict';

  var MAX_BYTES = 20 * 1024 * 1024;

  document.querySelectorAll('a[href^="#"]').forEach(function (link) {
    link.addEventListener('click', function (e) {
      var hash = this.getAttribute('href');
      if (!hash || hash.length < 2) return;
      var target = document.getElementById(hash.slice(1));
      if (!target) return;
      e.preventDefault();
      var header = document.querySelector('.funnel-header');
      var offset = header ? header.offsetHeight + 12 : 72;
      var top = target.getBoundingClientRect().top + window.scrollY - offset;
      window.scrollTo({ top: Math.max(0, top), behavior: 'smooth' });
    });
  });

  document.querySelectorAll('.funnel-form').forEach(function (form) {
    var input = form.querySelector('.funnel-upload-input');
    var grid = form.querySelector('.funnel-preview-grid');
    var submit = form.querySelector('button[type="submit"]');
    if (!input || !grid || !submit) return;

    var files = [];

    input.addEventListener('change', function () {
      Array.from(this.files).forEach(function (f) {
        if (files.length < 15) files.push(f);
      });
      syncInput();
      render();
    });

    form.addEventListener('submit', function (e) {
      if (totalBytes() > MAX_BYTES) e.preventDefault();
    });

    function totalBytes() {
      return files.reduce(function (sum, f) { return sum + f.size; }, 0);
    }

    function fmtSize(bytes) {
      if (bytes >= 1024 * 1024) return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
      return Math.round(bytes / 1024) + ' KB';
    }

    function syncInput() {
      var dt = new DataTransfer();
      files.forEach(function (f) { dt.items.add(f); });
      input.files = dt.files;
      input.required = files.length === 0;
    }

    function render() {
      grid.innerHTML = '';
      var total = totalBytes();
      var overLimit = total > MAX_BYTES;

      if (files.length > 0) {
        var bar = document.createElement('div');
        bar.className = 'prev-size-bar' + (overLimit ? ' prev-size-bar--over' : '');
        var pct = Math.min(total / MAX_BYTES * 100, 100);
        bar.innerHTML =
          '<div class="prev-size-track"><div class="prev-size-fill" style="width:' + pct + '%"></div></div>' +
          '<span class="prev-size-label">' + fmtSize(total) + ' / 20 MB</span>';

        if (overLimit) {
          var warn = document.createElement('p');
          warn.className = 'prev-size-warning';
          warn.textContent = 'Totale allegati troppo grande per l\'invio via email. Rimuovi alcuni file fino a tornare sotto i 20 MB.';
          bar.appendChild(warn);
        }

        grid.appendChild(bar);
        submit.disabled = overLimit;
        submit.style.opacity = overLimit ? '0.45' : '';
        submit.style.cursor = overLimit ? 'not-allowed' : '';
      } else {
        submit.disabled = false;
        submit.style.opacity = '';
        submit.style.cursor = '';
      }

      files.forEach(function (f, idx) {
        var item = document.createElement('div');
        item.className = 'prev-preview-item';

        if (f.type.startsWith('image/')) {
          var img = document.createElement('img');
          img.className = 'prev-preview-thumb';
          img.alt = f.name;
          var reader = new FileReader();
          reader.onload = function (e) { img.src = e.target.result; };
          reader.readAsDataURL(f);
          item.appendChild(img);
        } else {
          var icon = document.createElement('div');
          icon.className = 'prev-preview-icon';
          icon.textContent = f.name.split('.').pop().toUpperCase();
          item.appendChild(icon);
        }

        var name = document.createElement('span');
        name.className = 'prev-preview-name';
        name.textContent = f.name;
        item.appendChild(name);

        var size = document.createElement('span');
        size.className = 'prev-preview-size';
        size.textContent = fmtSize(f.size);
        item.appendChild(size);

        var btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'prev-preview-del';
        btn.setAttribute('aria-label', 'Rimuovi ' + f.name);
        btn.innerHTML = '&times;';
        btn.addEventListener('click', function () {
          files.splice(idx, 1);
          syncInput();
          render();
        });
        item.appendChild(btn);
        grid.appendChild(item);
      });
    }
  });
})();
