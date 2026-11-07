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
    let W, H, P = [], running = true, t = 0;
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
      const dust = Math.round((mobile ? 4200 : 10500) * Math.max(.5, k));
      /* dust: heavier toward the right, in soft clumps */
      const clumps = Array.from({ length: mobile ? 8 : 16 }, () => ({ x: W * rnd(mobile ? .05 : .36, 1.02), y: H * rnd(-.05, 1.05), r: rnd(80, 240) }));
      for (let i = 0; i < dust; i++) {
        if (Math.random() < .66) { const c = clumps[i % clumps.length]; add(c.x + gauss() * c.r * 1.6, c.y + gauss() * c.r, { a: rnd(.35, 1) }); }
        else add(W * Math.pow(Math.random(), .45), H * Math.random(), { a: rnd(.25, .75) });
      }
      /* long faint arcs sweeping across */
      const arcs = mobile ? [[W * 1.05, -H * .1, W * .8]] : [[W * .98, -H * .2, W * .42], [W * 1.08, H * .55, W * .3], [-W * .2, H * 1.6, W * .78]];
      arcs.forEach(([cx, cy, R], j) => {
        const n = Math.round(R * 4.5);
        for (let i = 0; i < n; i++) { const th = Math.random() * 6.283, rr = R + gauss() * 7; add(cx + Math.cos(th) * rr, cy + Math.sin(th) * rr, { c: j === 1 ? 2 : 0, a: rnd(.3, .8) }); }
      });
      /* small bright loops scattered in the cloud */
      const loops = mobile ? 7 : 18;
      for (let l = 0; l < loops; l++) {
        const cx = W * rnd(mobile ? .15 : .45, .97), cy = H * rnd(.2, .92), rx = rnd(8, 34), ry = rx * rnd(.35, 1), rot = Math.random() * 3.14;
        const n = Math.round(rx * 6);
        for (let i = 0; i < n; i++) {
          const th = (i / n) * 6.283, ex = Math.cos(th) * rx + gauss() * 1.2, ey = Math.sin(th) * ry + gauss() * 1.2;
          add(cx + ex * Math.cos(rot) - ey * Math.sin(rot), cy + ex * Math.sin(rot) + ey * Math.cos(rot), { c: 0, a: rnd(.75, 1), s: 1.5 });
        }
      }
      /* short curved strokes, like threads */
      for (let l = 0; l < (mobile ? 10 : 26); l++) {
        let x = W * rnd(mobile ? .1 : .45, 1), y = H * Math.random(), ang = Math.random() * 6.283;
        const len = rnd(30, 110), turn = rnd(-.04, .04);
        for (let i = 0; i < len; i += 1.4) { x += Math.cos(ang) * 1.4; y += Math.sin(ang) * 1.4; ang += turn; add(x + gauss(), y + gauss(), { c: Math.random() < .7 ? 0 : 2, a: rnd(.5, .9), s: 1.3 }); }
      }
    };
    const size = () => {
      const r = canvas.getBoundingClientRect(), d = Math.min(devicePixelRatio || 1, 2);
      W = r.width; H = r.height; canvas.width = W * d; canvas.height = H * d; ctx.setTransform(d, 0, 0, d, 0, 0);
      build();
    };
    const R = 150, R2 = R * R, G2 = (R * 1.6) * (R * 1.6), LV = 10;
    const STYLES = COLORS.map(c => Array.from({ length: LV + 1 }, (_, i) => `rgba(${c},${(i / LV).toFixed(2)})`));
    const buckets = Array.from({ length: COLORS.length * (LV + 1) }, () => []);
    const frame = () => {
      t += .016;
      ctx.clearRect(0, 0, W, H);
      for (const b of buckets) b.length = 0;
      const mx = m.x, my = m.y, act = m.active;
      for (let i = 0; i < P.length; i++) {
        const p = P[i];
        let a = p.a;
        if (!reduce) {
          const ox = p.hx + Math.cos(t * p.sp + p.ph) * p.amp, oy = p.hy + Math.sin(t * p.sp * 1.3 + p.ph) * p.amp;
          let fx = (ox - p.x) * .018, fy = (oy - p.y) * .018;
          if (act) {
            const dx = p.x - mx, dy = p.y - my, d2 = dx * dx + dy * dy;
            if (d2 < G2) {
              const d = Math.sqrt(d2) || .1;
              a += (1 - d / (R * 1.6)) * .5;
              if (d2 < R2) { const f = (1 - d / R) * 2.4; fx += (dx + -dy * .35) / d * f; fy += (dy + dx * .35) / d * f; }
            }
          }
          p.vx = (p.vx + fx) * .9; p.vy = (p.vy + fy) * .9; p.x += p.vx; p.y += p.vy;
        }
        buckets[p.c * (LV + 1) + Math.min(LV, Math.round(a * LV))].push(p);
      }
      for (let k = 0; k < buckets.length; k++) {
        const b = buckets[k]; if (!b.length) continue;
        ctx.fillStyle = STYLES[(k / (LV + 1)) | 0][k % (LV + 1)];
        for (let j = 0; j < b.length; j++) { const p = b[j]; ctx.fillRect(p.x, p.y, p.s, p.s); }
      }
      if (!reduce && running) requestAnimationFrame(frame);
    };
    size(); frame();
    let rt; addEventListener('resize', () => { clearTimeout(rt); rt = setTimeout(() => { size(); if (reduce) frame(); }, 150); });
    host.addEventListener('pointermove', e => { const r = canvas.getBoundingClientRect(); m.x = e.clientX - r.left; m.y = e.clientY - r.top; m.active = true; });
    host.addEventListener('pointerleave', () => { m.active = false; });
    if (!reduce && 'IntersectionObserver' in window) new IntersectionObserver(es => es.forEach(en => { const was = running; running = en.isIntersecting; if (running && !was) frame(); })).observe(canvas);
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
