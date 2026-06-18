// KESI SA — JS di base.
// Interattività leggera gestita da Alpine.js nei template; HTMX per i cambi
// di stato server-driven.

// ── Luxury Animations ────────────────────────────────────────────────────────
(function () {
  'use strict';

  // ── 1. Scroll reveal with stagger ──────────────────────────────────────────
  const REVEAL_SELECTORS = [
    '.section-head',
    '.cards > .card',
    '.feature-grid > .feature',
    '.stats > .stat',
    '.tech-grid > .tech-card',
    '.ref-grid > .ref-card',
    '.tl-item',
    '.pg-main',
    '.pg-item',
    '.ba-item',
    '.contatti-founder-img',
    '.contatti-info',
    '.manifesto > .container > *',
    '.scanner-section > *',
    '.founder-grid > *',
    '.tech-detail-grid > *',
    '.scanner-hw-item',
  ];

  // Track stagger index per parent so siblings animate in sequence
  const staggerMap = new Map();
  REVEAL_SELECTORS.forEach(sel => {
    document.querySelectorAll(sel).forEach(el => {
      const parent = el.parentElement;
      const idx = staggerMap.get(parent) || 0;
      staggerMap.set(parent, idx + 1);
      el.classList.add('reveal');
      el.style.setProperty('--reveal-delay', idx * 55 + 'ms');
    });
  });

  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('revealed');
        revealObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.10, rootMargin: '0px 0px -30px 0px' });

  document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));

  // ── 2. Stat counter animation ───────────────────────────────────────────────
  function countUp(el) {
    const text = el.textContent.trim();
    const match = text.match(/^(\d+(?:\.\d+)?)(.*)/);
    if (!match) return;
    const target = parseFloat(match[1]);
    const suffix = match[2];
    const dur = 1800;
    const t0 = performance.now();
    (function tick(now) {
      const p = Math.min((now - t0) / dur, 1);
      const eased = 1 - Math.pow(2, -10 * p); // easeOutExpo
      el.textContent = Math.round(eased * target) + suffix;
      if (p < 1) requestAnimationFrame(tick);
    })(performance.now());
  }

  const statsEl = document.querySelector('.stats');
  if (statsEl) {
    const statsObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          statsEl.querySelectorAll('.stat-value').forEach(countUp);
          statsObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.5 });
    statsObserver.observe(statsEl);
  }

  // ── 3. Header glass effect on scroll ───────────────────────────────────────
  const header = document.querySelector('.site-header');
  if (header) {
    window.addEventListener('scroll', () => {
      header.classList.toggle('scrolled', window.scrollY > 24);
    }, { passive: true });
  }

  // ── 4. Stats sine-wave canvas ──────────────────────────────────────────────
  const waveCanvas = document.querySelector('.stats-wave-canvas');
  if (waveCanvas) {
    const ctx = waveCanvas.getContext('2d');
    let phase = 0;
    const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    function resizeWave() {
      waveCanvas.width  = waveCanvas.offsetWidth;
      waveCanvas.height = waveCanvas.offsetHeight;
    }

    function drawWaves() {
      const w = waveCanvas.width;
      const h = waveCanvas.height;
      if (!w || !h) { if (!reduced) requestAnimationFrame(drawWaves); return; }

      ctx.clearRect(0, 0, w, h);

      const numLines = 32;
      const amplitude = 9;
      const freq = 0.0082;

      for (let i = 0; i < numLines; i++) {
        const baseY = h * (i / (numLines - 1));
        const linePhase = i * 0.36 - phase;

        ctx.beginPath();
        ctx.lineWidth = 1;
        ctx.strokeStyle = 'rgba(0,0,0,0.052)';

        for (let x = 0; x <= w; x += 2) {
          const y = baseY + Math.sin(x * freq + linePhase) * amplitude;
          x === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
        }
        ctx.stroke();
      }

      phase += 0.014; // drift left → right
      if (!reduced) requestAnimationFrame(drawWaves);
    }

    resizeWave();
    drawWaves();
    window.addEventListener('resize', resizeWave, { passive: true });
  }

  // ── 5. Cursor spotlight on dark sections ───────────────────────────────────
  document.querySelectorAll('.cta').forEach(section => {
    const spot = document.createElement('div');
    spot.className = 'cursor-spotlight';
    spot.setAttribute('aria-hidden', 'true');

    const hasWave = !!section.querySelector('.hero-wave');
    const WAVE_H = 130; // matches .hero-wave height in CSS
    if (hasWave) spot.classList.add('cursor-spotlight--wave');

    section.appendChild(spot);

    section.addEventListener('mousemove', e => {
      const rect = section.getBoundingClientRect();
      const relX = e.clientX - rect.left;
      const relY = e.clientY - rect.top;

      if (hasWave) {
        // Hide spotlight when cursor is inside the wave's white ellipse.
        // Wave: clip-path: ellipse(90% 100% at 50% 100%) on a WAVE_H-tall box at bottom.
        const waveTop = rect.height - WAVE_H;
        if (relY >= waveTop) {
          const rx = rect.width * 0.90;
          const ry = WAVE_H;
          const cx = rect.width * 0.50;
          const cy = rect.height; // ellipse centre is at the very bottom edge
          const dx = relX - cx;
          const dy = relY - cy;
          if ((dx * dx) / (rx * rx) + (dy * dy) / (ry * ry) <= 1) {
            spot.style.opacity = '0';
            return;
          }
        }
      }

      const x = (relX / rect.width * 100).toFixed(1);
      const y = (relY / rect.height * 100).toFixed(1);
      spot.style.setProperty('--cx', x + '%');
      spot.style.setProperty('--cy', y + '%');
      spot.style.opacity = '1';
    }, { passive: true });

    section.addEventListener('mouseleave', () => {
      spot.style.opacity = '0';
    });
  });

})();

// ── Ambient floating sine curves ─────────────────────────────────────────────
(function () {
  'use strict';
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  const cv = document.createElement('canvas');
  cv.style.cssText = [
    'position:fixed', 'top:0', 'left:0',
    'width:100%', 'height:100%',
    'pointer-events:none',
    'z-index:-1',
  ].join(';');
  cv.setAttribute('aria-hidden', 'true');
  document.body.appendChild(cv);

  const ctx = cv.getContext('2d');
  let W, H;
  const resize = () => {
    W = cv.width  = window.innerWidth;
    H = cv.height = window.innerHeight;
  };
  resize();
  window.addEventListener('resize', resize, { passive: true });

  // Reduce to 1 curve while user is scrolling
  let scrolling = false, scrollT;
  window.addEventListener('scroll', () => {
    scrolling = true;
    clearTimeout(scrollT);
    scrollT = setTimeout(() => { scrolling = false; }, 700);
  }, { passive: true });

  const curves = [];
  let nextSpawn = performance.now() + 600;

  function spawn() {
    const fromLeft = Math.random() > 0.5;
    const angle    = (Math.random() * 40 - 20) * (Math.PI / 180); // ±20° diagonal
    const spd      = (0.28 + Math.random() * 0.38) * 3;
    const vy_sign  = Math.random() < 0.5 ? 1 : -1;
    curves.push({
      x:     fromLeft ? -200 : W + 200,
      y:     window.scrollY + H * (0.06 + Math.random() * 0.88), // document-relative Y
      vx:    (fromLeft ? 1 : -1) * spd * Math.cos(angle),
      vy:    spd * Math.sin(Math.abs(angle)) * vy_sign,
      phase: Math.random() * Math.PI * 2,
      amp:   13 + Math.random() * 20,          // px amplitude of the sine
      freq:  0.010 + Math.random() * 0.009,    // spatial frequency
      half:  85 + Math.random() * 85,          // half-length of visible segment
      lw:    0.8 + Math.random() * 0.9,        // stroke width
    });
  }

  function drawCurve(c) {
    // Fade based on horizontal distance from screen edges
    const edgeA = Math.max(0, Math.min(1,
      (c.x + 200) / 260,
      (W + 200 - c.x) / 260
    ));
    if (edgeA < 0.01) return;

    const travelAngle = Math.atan2(c.vy, c.vx);
    const STEPS = 46;

    ctx.save();
    ctx.translate(c.x, c.y - window.scrollY); // convert doc-Y → viewport-Y
    ctx.rotate(travelAngle);
    ctx.lineWidth = c.lw;
    ctx.lineCap   = 'round';

    for (let i = 0; i < STEPS; i++) {
      const t0 = (i / STEPS) * 2 - 1;       // −1 … +1
      const t1 = ((i + 1) / STEPS) * 2 - 1;
      const tmid = (t0 + t1) * 0.5;

      // Cosine-shaped tip fade: bright in centre, zero at both ends
      const tipA = Math.pow(Math.cos(tmid * Math.PI * 0.5), 2);
      const alpha = tipA * edgeA * 0.70;
      if (alpha < 0.005) continue;

      const x0 = t0 * c.half;
      const y0 = Math.sin(x0 * c.freq + c.phase) * c.amp;
      const x1 = t1 * c.half;
      const y1 = Math.sin(x1 * c.freq + c.phase) * c.amp;

      ctx.beginPath();
      ctx.moveTo(x0, y0);
      ctx.lineTo(x1, y1);
      ctx.strokeStyle = `rgba(247,147,29,${alpha.toFixed(3)})`;
      ctx.stroke();
    }

    ctx.restore();
  }

  function loop(now) {
    ctx.clearRect(0, 0, W, H);

    const limit = scrolling ? 1 : 5;

    if (curves.length < limit && now >= nextSpawn) {
      spawn();
      nextSpawn = now + 800 + Math.random() * 2600; // 0.8–3.4 s between spawns
    }
    // Drop oldest if user started scrolling while 5 were active
    while (curves.length > limit) curves.shift();

    for (let i = curves.length - 1; i >= 0; i--) {
      const c = curves[i];
      c.x     += c.vx;
      c.y     += c.vy;
      c.phase += 0.048; // 3× phase drift keeps the wave flowing at the new speed

      drawCurve(c);

      const viewY = c.y - window.scrollY;
      if (c.x < -400 || c.x > W + 400 || viewY < -400 || viewY > H + 400) curves.splice(i, 1);
    }

    requestAnimationFrame(loop);
  }

  // Short delay before first frame so the page has settled
  setTimeout(() => requestAnimationFrame(loop), 500);
})();
