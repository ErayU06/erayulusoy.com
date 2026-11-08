/* Eray Ulusoy — site behaviour (no third-party scripts) */
(() => {
  'use strict';
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* scroll progress line */
  const bar = document.getElementById('progressBar');
  let ticking = false;
  const setBar = () => { const max = document.documentElement.scrollHeight - innerHeight; bar.style.transform = `scaleX(${max > 0 ? Math.min(1, scrollY / max) : 0})`; ticking = false; };
  addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(setBar); } }, { passive: true });
  addEventListener('resize', setBar); setBar();

  /* nav: transparent over hero, solid after */
  const nav = document.getElementById('nav');
  const onScroll = () => nav.classList.toggle('solid', scrollY > 40);
  addEventListener('scroll', onScroll, { passive: true }); onScroll();

  /* mobile menu */
  const mb = document.getElementById('menuBtn'), mm = document.getElementById('mobileMenu');
  const setMenu = open => { mm.hidden = !open; mb.setAttribute('aria-expanded', open); document.body.style.overflow = open ? 'hidden' : ''; nav.classList.toggle('solid', open || scrollY > 40); };
  mb.addEventListener('click', () => setMenu(mm.hidden));
  mm.querySelectorAll('a').forEach(a => a.addEventListener('click', () => setMenu(false)));

  /* marquee */
  const words = ['HTML & CSS', 'JavaScript', 'TypeScript', 'Node.js', 'Python', 'PostgreSQL', 'Docker', 'Linux', 'AWS', 'Amazon S3', 'Cloudflare', 'Git'];
  document.getElementById('marquee').innerHTML = [...words, ...words].map(w => `<span>${w}</span>`).join('');

  /* hero brief: types itself */
  const out = document.getElementById('briefOut');
  let lines = [];
  try { lines = JSON.parse(out.dataset.lines || '[]'); } catch (e) { lines = []; }
  const esc = s => s.replace(/[&<>]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' })[c]);
  const total = lines.reduce((n, l) => n + l[1].length, 0);
  const flat = lines.map(l => l[1]).join('');
  const draw = n => {
    let left = n, h = '';
    for (const [c, t] of lines) { if (left <= 0) break; const p = t.slice(0, left); left -= p.length; h += c ? `<span class="${c}">${esc(p)}</span>` : esc(p); }
    out.innerHTML = h + '<span class="caret"></span>';
  };
  if (reduce) draw(total); else {
    let i = 0; draw(0);
    const tick = () => { i++; draw(i); if (i < total) setTimeout(tick, flat[i - 1] === '\n' ? 320 : flat[i - 1] === '.' ? 9 : 26 + Math.random() * 30); };
    setTimeout(tick, 1500);
  }

  /* hero particle field: fine gold / ivory dust that drifts and parts around the pointer */
  const particleField = canvas => {
    const ctx = canvas.getContext('2d');
    const host = canvas.parentElement;
    const COLORS = ['212,188,138', '184,155,100', '245,241,232', '150,162,196'];
    let W, H, P = [], running = true;
    const m = { x: -1e4, y: -1e4, active: false };
    const rnd = (a, b) => a + Math.random() * (b - a);
    const gauss = () => (Math.random() + Math.random() + Math.random() - 1.5) / 1.5;
    const add = (x, y, o) => {
      if (x < -20 || x > W + 20 || y < -20 || y > H + 20) return;
      const r = Math.random();
      const c = o.c != null ? o.c : r < .5 ? 0 : r < .68 ? 1 : r < .88 ? 2 : 3;
      P.push({ hx: x, hy: y, x, y, vx: 0, vy: 0, c, a: o.a != null ? o.a : rnd(.25, .85), s: o.s || (Math.random() < .18 ? 1.7 : 1.15),
        ph: Math.random() * 6.283, sp: rnd(.2, .7), amp: rnd(.6, 3) });
    };
    const build = () => {
      P = [];
      const mobile = W < 700;
      const k = Math.min(1.25, (W * H) / (1440 * 900));
      const dust = Math.round((mobile ? 6000 : 15000) * Math.max(.5, k));
      /* a smooth swirling field the strands follow */
      const s1 = rnd(0, 6.28), s2 = rnd(0, 6.28), s3 = rnd(0, 6.28), f = rnd(.0028, .0042);
      const field = (x, y) => (Math.sin(x * f + s1) * Math.cos(y * f * 1.3 + s2) + .6 * Math.sin((x - y) * f * .7 + s3) + .35 * Math.cos((x + y * 1.6) * f * 2.1 + s1)) * 3.4;
      const left = mobile ? .02 : .3;
      /* dust: heavier toward the right, in uneven clumps */
      const clumps = Array.from({ length: mobile ? 10 : 22 }, () => ({ x: W * rnd(left, 1.04), y: H * rnd(-.08, 1.08), rx: rnd(60, 300), ry: rnd(40, 200), rot: rnd(0, 3.14) }));
      for (let i = 0; i < dust; i++) {
        const q = Math.random();
        if (q < .6) {
          const c = clumps[(Math.random() * clumps.length) | 0];
          const gx = gauss() * c.rx, gy = gauss() * c.ry;
          add(c.x + gx * Math.cos(c.rot) - gy * Math.sin(c.rot), c.y + gx * Math.sin(c.rot) + gy * Math.cos(c.rot), { a: rnd(.3, 1) });
        } else add(W * Math.pow(Math.random(), .4), H * Math.random(), { a: rnd(.2, .7) });
      }
      /* strands: particles laid along the swirling field, thick in the middle, frayed at the ends */
      const strands = mobile ? 34 : 90;
      for (let l = 0; l < strands; l++) {
        let x = W * rnd(left, 1.02), y = H * rnd(-.05, 1.05);
        const steps = rnd(60, 260) | 0, width = rnd(1.5, 9), dens = rnd(1.2, 3.2), c = Math.random() < .72 ? 0 : Math.random() < .5 ? 2 : 3;
        for (let i = 0; i < steps; i++) {
          const ang = field(x, y);
          x += Math.cos(ang) * 2.2; y += Math.sin(ang) * 2.2;
          const taper = Math.sin((i / steps) * Math.PI);
          const n = Math.random() < dens - Math.floor(dens) ? Math.ceil(dens) : Math.floor(dens);
          for (let k = 0; k < n; k++) add(x + gauss() * width * taper * 2, y + gauss() * width * taper * 2, { c: Math.random() < .85 ? c : 1, a: rnd(.45, 1), s: Math.random() < .3 ? 1.6 : 1.15 });
        }
      }
      /* bright scattered fragments: tiny broken bursts */
      for (let l = 0; l < (mobile ? 18 : 46); l++) {
        const cx = W * rnd(left + .05, 1), cy = H * rnd(.15, .95), r = rnd(4, 18), n = (r * rnd(2, 4)) | 0;
        for (let i = 0; i < n; i++) { const th = Math.random() * 6.283, rr = r * Math.pow(Math.random(), .6); add(cx + Math.cos(th) * rr * rnd(.4, 1.6), cy + Math.sin(th) * rr, { c: 0, a: rnd(.7, 1), s: 1.5 }); }
      }
    };
    let grid = new Map(), CELL = 60, statics = [], scaleX = 1, scaleY = 1;
    const LV = 10;
    const STYLES = COLORS.map(c => Array.from({ length: LV + 1 }, (_, i) => `rgba(${c},${(i / LV).toFixed(2)})`));
    const size = () => {
      const r = canvas.getBoundingClientRect(), d = Math.min(devicePixelRatio || 1, 1.5);
      W = canvas.offsetWidth; H = canvas.offsetHeight; canvas.width = W * d; canvas.height = H * d; ctx.setTransform(d, 0, 0, d, 0, 0);
      build();
      /* pre-sort particles into colour/alpha buckets once, and index them on a grid */
      statics = Array.from({ length: COLORS.length * (LV + 1) }, () => []);
      grid = new Map();
      for (const p of P) {
        statics[p.c * (LV + 1) + Math.min(LV, Math.round(p.a * LV))].push(p);
        const key = ((p.hx / CELL) | 0) + ',' + ((p.hy / CELL) | 0);
        let g = grid.get(key); if (!g) grid.set(key, g = []); g.push(p);
      }
      active.clear(); paintBase(); draw();
    };
    const R = 120, R2 = R * R;
    const active = new Set();
    const base = document.createElement('canvas'), bctx = base.getContext('2d');
    const paintBase = () => {
      const d = canvas.width / W;
      base.width = canvas.width; base.height = canvas.height; bctx.setTransform(d, 0, 0, d, 0, 0);
      for (let k = 0; k < statics.length; k++) {
        const b = statics[k]; if (!b.length) continue;
        bctx.fillStyle = STYLES[(k / (LV + 1)) | 0][k % (LV + 1)];
        for (let j = 0; j < b.length; j++) { const p = b[j]; bctx.fillRect(p.hx, p.hy, p.s, p.s); }
      }
    };
    /* the resting field is one cached image; only particles the pointer disturbs are redrawn */
    const draw = () => {
      ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.clearRect(0, 0, canvas.width, canvas.height); ctx.drawImage(base, 0, 0);
      const d = canvas.width / W; ctx.setTransform(d, 0, 0, d, 0, 0);
      if (!active.size) return;
      for (const p of active) ctx.clearRect(p.hx - .4, p.hy - .4, p.s + .8, p.s + .8);
      for (const p of active) {
        let a = p.a;
        if (m.active) { const dx = p.x - m.x, dy = p.y - m.y, g = 1 - Math.sqrt(dx * dx + dy * dy) / (R * 1.5); if (g > 0) a += g * .5; }
        ctx.fillStyle = STYLES[p.c][Math.min(LV, Math.round(a * LV))];
        ctx.fillRect(p.x, p.y, p.s, p.s);
      }
    };
    let looping = false;
    const step = () => {
      if (m.active) {
        const c0 = ((m.x - R) / CELL) | 0, c1 = ((m.x + R) / CELL) | 0, r0 = ((m.y - R) / CELL) | 0, r1 = ((m.y + R) / CELL) | 0;
        for (let cx = c0; cx <= c1; cx++) for (let cy = r0; cy <= r1; cy++) { const g = grid.get(cx + ',' + cy); if (g) for (const p of g) active.add(p); }
      }
      for (const p of active) {
        let fx = (p.hx - p.x) * .03, fy = (p.hy - p.y) * .03;
        const dx = p.x - m.x, dy = p.y - m.y, d2 = dx * dx + dy * dy;
        if (m.active && d2 < R2) { const d = Math.sqrt(d2) || .1, f = (1 - d / R) * 2.6; fx += (dx - dy * .35) / d * f; fy += (dy + dx * .35) / d * f; }
        p.vx = (p.vx + fx) * .88; p.vy = (p.vy + fy) * .88; p.x += p.vx; p.y += p.vy;
        if ((!m.active || d2 > R2 * 1.4) && Math.abs(p.x - p.hx) < .3 && Math.abs(p.y - p.hy) < .3 && Math.abs(p.vx) + Math.abs(p.vy) < .05) { p.x = p.hx; p.y = p.hy; p.vx = p.vy = 0; active.delete(p); }
      }
      draw();
      if (running && (m.active || active.size)) requestAnimationFrame(step); else looping = false;
    };
    const kick = () => { if (!looping && !reduce && running) { looping = true; requestAnimationFrame(step); } };
    size();
    let rt; addEventListener('resize', () => { clearTimeout(rt); rt = setTimeout(size, 150); });
    host.addEventListener('pointermove', e => {
      const r = canvas.getBoundingClientRect();
      m.x = (e.clientX - r.left) * (W / r.width); m.y = (e.clientY - r.top) * (H / r.height); m.active = true; kick();
    });
    host.addEventListener('pointerleave', () => { m.active = false; kick(); });
    if ('IntersectionObserver' in window) new IntersectionObserver(es => es.forEach(en => { running = en.isIntersecting; if (running) kick(); })).observe(canvas);
  };
  particleField(document.getElementById('constellation'));

  /* subtle parallax on hero canvas */
  const cons = document.getElementById('constellation');
  if (!reduce) addEventListener('scroll', () => { if (scrollY < innerHeight) cons.style.transform = `translateY(${scrollY * .25}px)`; }, { passive: true });

  /* scroll reveals: items already on screen stay put; later ones lift in */
  if (!reduce && 'IntersectionObserver' in window) {
    const io = new IntersectionObserver(es => es.forEach(en => {
      if (!en.isIntersecting) return;
      const el = en.target; const sib = [...el.parentElement.children].filter(c => c.classList.contains('rv'));
      const delay = Math.max(0, sib.indexOf(el)) * 110;
      setTimeout(() => { el.classList.remove('pre'); el.classList.add('in'); }, delay);
      io.unobserve(el);
    }), { threshold: .14, rootMargin: '0px 0px -40px 0px' });
    document.querySelectorAll('.rv, .rule.draw, #steps, #sig').forEach(el => {
      if (el.getBoundingClientRect().top > innerHeight * .92) { if (el.classList.contains('rv')) el.classList.add('pre'); io.observe(el); }
      else el.classList.add('in');
    });
  } else document.querySelectorAll('.rv, .rule.draw, #steps, #sig').forEach(el => el.classList.add('in'));

  /* ---- effects (original code) ---- */
  const wrapWords = (root, make) => {
    const walk = node => [...node.childNodes].forEach(n => {
      if (n.nodeType === 3) {
        const frag = document.createDocumentFragment();
        n.textContent.split(/(\s+)/).forEach(part => {
          if (!part) return;
          frag.appendChild(/^\s+$/.test(part) ? document.createTextNode(part) : make(part));
        });
        n.replaceWith(frag);
      } else if (n.nodeType === 1 && n.tagName !== 'BR') walk(n);
    });
    walk(root);
  };

  /* headings rise word by word */
  if (!reduce && 'IntersectionObserver' in window) {
    const heads = document.querySelectorAll('main h2:not(.label), .work-head h3');
    const hio = new IntersectionObserver(es => es.forEach(en => {
      if (en.isIntersecting) { en.target.classList.add('shown'); hio.unobserve(en.target); }
    }), { threshold: .3 });
    heads.forEach(h => {
      let i = 0;
      wrapWords(h, word => {
        const w = document.createElement('span'); w.className = 'w';
        const inner = document.createElement('span'); inner.textContent = word;
        inner.style.transitionDelay = `${(i++) * 55 + 120}ms`;
        w.appendChild(inner); return w;
      });
      h.classList.add('split');
      requestAnimationFrame(() => hio.observe(h));
    });
  }

  /* the perspective quote fills in word by word as it scrolls past */
  const quote = document.querySelector('.intro blockquote');
  if (quote && !reduce) {
    const qw = [];
    wrapWords(quote, word => { const s = document.createElement('span'); s.className = 'qw'; s.textContent = word; qw.push(s); return s; });
    let qt = false;
    const fill = () => {
      qt = false;
      const r = quote.getBoundingClientRect(), vh = innerHeight;
      const p = Math.min(1, Math.max(0, (vh * .82 - r.top) / (r.height + vh * .3)));
      const n = Math.round(p * qw.length);
      qw.forEach((w, i) => w.classList.toggle('lit', i < n));
    };
    addEventListener('scroll', () => { if (!qt) { qt = true; requestAnimationFrame(fill); } }, { passive: true });
    addEventListener('resize', fill); fill();
  }

  /* fact numbers roll into place */
  const facts = document.querySelector('.facts');
  if (facts && !reduce && 'IntersectionObserver' in window) {
    const strips = [];
    const originals = [];
    facts.querySelectorAll('.fact b').forEach(b => {
      originals.push([b, b.innerHTML]);
      b.setAttribute('aria-label', b.textContent.trim());
      const walk = node => [...node.childNodes].forEach(n => {
        if (n.nodeType === 3) {
          const frag = document.createDocumentFragment();
          [...n.textContent].forEach(ch => {
            if (!/\d/.test(ch)) { frag.appendChild(document.createTextNode(ch)); return; }
            const roll = document.createElement('span'); roll.className = 'roll'; roll.setAttribute('aria-hidden', 'true');
            const strip = document.createElement('span');
            for (let k = 0; k < 20; k++) { const d = document.createElement('span'); d.textContent = k % 10; strip.appendChild(d); }
            roll.appendChild(strip); frag.appendChild(roll);
            strips.push([strip, 10 + +ch]);
          });
          n.replaceWith(frag);
        } else if (n.nodeType === 1) walk(n);
      });
      walk(b);
    });
    const fio = new IntersectionObserver(es => {
      if (!es.some(e => e.isIntersecting)) return;
      strips.forEach(([s, to], i) => setTimeout(() => { s.style.transform = `translateY(-${to * 1.15}em)`; }, 250 + i * 140));
      setTimeout(() => originals.forEach(([el, html]) => { el.innerHTML = html; el.removeAttribute('aria-label'); }), 250 + strips.length * 140 + 2400);
      fio.disconnect();
    }, { threshold: .4 });
    fio.observe(facts);
  }

  /* approach cards: earlier cards ease back as the next one slides over */
  const cards = [...document.querySelectorAll('.steps.stack .step')];
  if (cards.length && !reduce) {
    let ct = false;
    const stack = () => {
      ct = false;
      cards.forEach((c, i) => {
        const next = cards[i + 1];
        if (!next) return;
        const a = c.getBoundingClientRect(), b = next.getBoundingClientRect();
        const p = Math.min(1, Math.max(0, 1 - (b.top - a.top - 26) / a.height));
        c.style.transform = `scale(${1 - p * .05})`;
        c.style.filter = `brightness(${1 - p * .35})`;
      });
    };
    addEventListener('scroll', () => { if (!ct) { ct = true; requestAnimationFrame(stack); } }, { passive: true });
    addEventListener('resize', stack); stack();
  }

  /* copy email */
  const cb = document.getElementById('copyMail'), addr = document.getElementById('mailAddr');
  cb.addEventListener('click', () => {
    const ok = () => { cb.textContent = cb.dataset.done; setTimeout(() => cb.textContent = cb.dataset.label, 1800); };
    const sel = () => { const r = document.createRange(); r.selectNodeContents(addr); const g = getSelection(); g.removeAllRanges(); g.addRange(r); cb.textContent = cb.dataset.done; };
    try { navigator.clipboard.writeText(addr.textContent).then(ok, sel); } catch (e) { sel(); }
  });

  /* language switch: remember the visitor's explicit choice */
  document.querySelectorAll('[data-lang-link]').forEach(a => a.addEventListener('click', () => {
    try { localStorage.setItem('lang', a.dataset.langLink); } catch (e) {}
  }));

  /* form: paste your Formspree form ID below (e.g. 'xyzabcd') to start receiving enquiries by email */
  const FORMSPREE_ID = 'mwlvgwnw';
  const form = document.getElementById('enquiry'), note = document.getElementById('formNote');
  const t = (k, first) => (form.dataset[k] || '').replace('{name}', first || '');
  form.addEventListener('submit', async e => {
    e.preventDefault();
    const name = form.elements.name, email = form.elements.email;
    if (!name.value.trim()) { note.textContent = t('msgName'); name.focus(); return; }
    if (!email.validity.valid || !email.value.trim()) { note.textContent = t('msgEmail'); email.focus(); return; }
    const first = name.value.trim().split(/\s+/)[0].slice(0, 40);
    if (!FORMSPREE_ID) { note.textContent = t('msgOffline', first); return; }
    if (form.elements._gotcha && form.elements._gotcha.value) return;
    const btn = form.querySelector('button[type=submit]'); btn.disabled = true; note.textContent = t('msgSending');
    try {
      const res = await fetch(`https://formspree.io/f/${encodeURIComponent(FORMSPREE_ID)}`, { method: 'POST', body: new FormData(form), headers: { Accept: 'application/json' } });
      if (!res.ok) throw new Error(res.status);
      form.reset(); note.textContent = t('msgSent', first);
    } catch (err) {
      note.textContent = t('msgError');
    } finally { btn.disabled = false; }
  });

})();
