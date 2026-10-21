/* Eray Ulusoy — site behaviour (no third-party scripts) */
(() => {
  'use strict';
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

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

  /* constellation: slow gold network, reacts gently to the pointer */
  const makeField = (canvas, opts) => {
    const ctx = canvas.getContext('2d');
    let W, H, pts = [];
    const m = { x: -1e4, y: -1e4 };
    const size = () => {
      const r = canvas.getBoundingClientRect(), d = Math.min(devicePixelRatio || 1, 2);
      W = r.width; H = r.height; canvas.width = W * d; canvas.height = H * d; ctx.setTransform(d, 0, 0, d, 0, 0);
      const n = Math.round(Math.min(opts.max, Math.max(opts.min, W * H / opts.density)));
      pts = Array.from({ length: n }, () => ({ x: Math.random() * W, y: Math.random() * H, vx: (Math.random() - .5) * opts.speed, vy: (Math.random() - .5) * opts.speed, r: Math.random() < .08 ? 2.2 : 1 }));
    };
    const frame = () => {
      ctx.clearRect(0, 0, W, H);
      for (const p of pts) {
        if (!reduce) { p.x += p.vx; p.y += p.vy; if (p.x < 0 || p.x > W) p.vx *= -1; if (p.y < 0 || p.y > H) p.vy *= -1; }
      }
      for (let i = 0; i < pts.length; i++) for (let j = i + 1; j < pts.length; j++) {
        const a = pts[i], b = pts[j], d = Math.hypot(a.x - b.x, a.y - b.y);
        if (d < opts.link) {
          const near = Math.hypot((a.x + b.x) / 2 - m.x, (a.y + b.y) / 2 - m.y) < 180;
          ctx.strokeStyle = `rgba(184,155,100,${(1 - d / opts.link) * (near ? .55 : opts.alpha)})`;
          ctx.lineWidth = .6; ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke();
        }
      }
      for (const p of pts) {
        const near = Math.hypot(p.x - m.x, p.y - m.y) < 140;
        ctx.fillStyle = p.r > 2 ? 'rgba(212,188,138,.9)' : `rgba(245,241,232,${near ? .8 : .35})`;
        ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2); ctx.fill();
        if (p.r > 2) { ctx.strokeStyle = 'rgba(184,155,100,.35)'; ctx.beginPath(); ctx.arc(p.x, p.y, 7, 0, Math.PI * 2); ctx.stroke(); }
      }
      if (!reduce && running) requestAnimationFrame(frame);
    };
    let running = true;
    size(); frame();
    addEventListener('resize', () => { size(); if (reduce) frame(); });
    const host = canvas.parentElement;
    host.addEventListener('pointermove', e => { const r = canvas.getBoundingClientRect(); m.x = e.clientX - r.left; m.y = e.clientY - r.top; });
    host.addEventListener('pointerleave', () => { m.x = m.y = -1e4; });
    if (!reduce && 'IntersectionObserver' in window) new IntersectionObserver(es => es.forEach(en => { const was = running; running = en.isIntersecting; if (running && !was) frame(); })).observe(canvas);
  };
  makeField(document.getElementById('constellation'), { min: 30, max: 80, density: 14000, speed: .18, link: 160, alpha: .22 });

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
