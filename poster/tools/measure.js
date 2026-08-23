// Injected into a copy of index.html and read back via --dump-dom.
function runMeasure() {
  const ROWS = [128, 236, 216, 202, 142, 100, 13];
  const MM = 96 / 25.4;                       // CSS px per mm, fixed by spec
  const out = { pageW: document.body.getBoundingClientRect().width / MM,
                pageH: document.body.getBoundingClientRect().height / MM,
                scrollW: document.body.scrollWidth / MM,
                scrollH: document.body.scrollHeight / MM,
                bands: [], safe: [], type: [], fonts: {} };

  // an element inside an overflow:hidden ancestor cannot spill, so it must not
  // count against the band -- otherwise a deliberately cropped image reads as
  // an overflow it is not.
  function clipped(el, stop) {
    for (let n = el.parentElement; n && n !== stop; n = n.parentElement) {
      const o = getComputedStyle(n);
      if (o.overflow !== 'visible' || o.overflowY !== 'visible') return true;
    }
    return false;
  }

  const bands = [...document.querySelectorAll('.poster > *')];
  bands.forEach((b, i) => {
    const br = b.getBoundingClientRect();
    let bottom = br.top, worst = null, right = br.left;
    b.querySelectorAll('*').forEach(el => {
      const r = el.getBoundingClientRect();
      if (!r.width && !r.height) return;
      if (clipped(el, b)) return;
      if (r.bottom > bottom) { bottom = r.bottom; worst = el; }
      if (r.right > right) right = r.right;
    });
    out.bands.push({
      band: String(b.className || b.tagName).replace('band ', '').trim(),
      rowMM: ROWS[i],
      boxMM: +(br.height / MM).toFixed(1),
      contentMM: +((bottom - br.top) / MM).toFixed(1),
      // against the declared row, so a band that hard-codes its own height
      // cannot report zero overflow while spilling into the next band
      overMM: +(((bottom - br.top) / MM) - ROWS[i]).toFixed(1),
      overRightMM: +((right - br.right) / MM).toFixed(1),
      worst: worst ? worst.tagName + '.' + String(worst.className).slice(0, 30) : ''
    });
  });

  // direct children of each band, so an overflowing column is named
  out.cols = [];
  bands.forEach(b => {
    [...b.children].forEach(c => {
      const cr = c.getBoundingClientRect();
      let bot = cr.top;
      c.querySelectorAll('*').forEach(el => {
        const r = el.getBoundingClientRect();
        if ((!r.width && !r.height) || clipped(el, c)) return;
        if (r.bottom > bot) bot = r.bottom;
      });
      out.cols.push({ band: String(b.className).replace('band ', '').trim(),
        child: c.tagName + '.' + String(c.className).slice(0, 18),
        hMM: +((bot - cr.top) / MM).toFixed(1) });
    });
  });

  // safe-margin containment: 28 mm on all sides of an 841 x 1189 page
  const LO = 28 * MM, HIX = (841 - 28) * MM, HIY = (1189 - 28) * MM;
  document.querySelectorAll('.poster *').forEach(el => {
    const r = el.getBoundingClientRect();
    if (!r.width && !r.height) return;
    if (clipped(el, document.querySelector('.poster'))) return;
    // inline text boxes report the font's full ascent/descent, which overshoots
    // the visible glyphs; 2 mm of tolerance keeps that from reading as a breach
    const T = getComputedStyle(el).display.startsWith('inline') ? 2 * MM : 0.5;
    if (r.left < LO - T || r.top < LO - T || r.right > HIX + T || r.bottom > HIY + T) {
      out.safe.push({ el: el.tagName + '.' + String(el.className).slice(0, 26),
        l: +(r.left / MM).toFixed(1), t: +(r.top / MM).toFixed(1),
        r: +(r.right / MM).toFixed(1), b: +(r.bottom / MM).toFixed(1) });
    }
  });

  // smallest rendered type
  const sizes = [];
  document.querySelectorAll('.poster *').forEach(el => {
    const hasText = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
    if (!hasText) return;
    const cs = getComputedStyle(el);
    const pt = parseFloat(cs.fontSize) * 72 / 96;
    sizes.push({ pt: +pt.toFixed(1), sel: el.tagName + '.' + String(el.className).slice(0, 26),
                 text: el.textContent.trim().slice(0, 34) });
  });
  sizes.sort((a, b) => a.pt - b.pt);
  out.type = sizes.slice(0, 8);

  // did the three families actually load?
  ['Source Serif 4', 'IBM Plex Sans', 'IBM Plex Mono'].forEach(f => {
    out.fonts[f] = document.fonts.check(`30pt "${f}"`);
  });

  // word count, excluding the author block and affiliations per the brief
  const clone = document.querySelector('.poster').cloneNode(true);
  clone.querySelectorAll('.authors, .affils').forEach(n => n.remove());
  out.words = clone.textContent.trim().split(/\s+/).filter(Boolean).length;

  // deep dump for whichever band children overflow, so the culprit is named
  out.deep = [];
  bands.forEach((b, i) => {
    [...b.children].forEach(c => {
      const cr = c.getBoundingClientRect();
      let bot = cr.top;
      c.querySelectorAll('*').forEach(el => {
        const r = el.getBoundingClientRect();
        if ((!r.width && !r.height) || clipped(el, c)) return;
        if (r.bottom > bot) bot = r.bottom;
      });
      if ((bot - cr.top) / MM <= ROWS[i] + 0.3) return;
      const kids = [...c.children].map(k => {
        const r = k.getBoundingClientRect();
        const cs = getComputedStyle(k);
        return { el: k.tagName + '.' + String(k.className).slice(0, 20),
          hMM: +(r.height / MM).toFixed(1),
          mt: +(parseFloat(cs.marginTop) / MM).toFixed(1),
          mb: +(parseFloat(cs.marginBottom) / MM).toFixed(1),
          txt: k.textContent.trim().slice(0, 26) };
      });
      out.deep.push({ band: String(b.className).replace('band ', '').trim(),
        totalMM: +((bot - cr.top) / MM).toFixed(1), rowMM: ROWS[i], kids });
    });
  });

  // every number rendered on the poster, for provenance checking against §9
  // per leaf element, so adjacent table cells cannot merge into a fake number
  const nums = new Set();
  document.querySelectorAll('.poster *').forEach(el => {
    [...el.childNodes].forEach(n => {
      if (n.nodeType !== 3) return;
      (n.textContent.match(/\d+(?:[.,]\d+)*%?/g) || []).forEach(v => nums.add(v));
    });
  });
  out.numbers = [...nums].sort();

  // measure of body copy, in characters, per rendered line
  out.measure = [];
  document.querySelectorAll('.poster p, .poster li, .poster dd').forEach(el => {
    const cs = getComputedStyle(el);
    const pt = parseFloat(cs.fontSize) * 72 / 96;
    if (pt < 24) return;
    const txt = el.textContent.replace(/\s+/g, ' ').trim();
    if (txt.length < 25) return;
    const lines = Math.max(1, Math.round(el.getBoundingClientRect().height /
                  (parseFloat(cs.lineHeight) || parseFloat(cs.fontSize) * 1.4)));
    out.measure.push({ chars: Math.round(txt.length / lines), lines,
      pt: +pt.toFixed(0), sel: el.tagName + '.' + String(el.className).slice(0, 20),
      txt: txt.slice(0, 30) });
  });

  // per-band word counts
  out.bandWords = [];
  bands.forEach(b => {
    const c = b.cloneNode(true);
    c.querySelectorAll('.authors, .affils').forEach(n => n.remove());
    out.bandWords.push({ band: String(b.className).replace('band ', '').trim(),
      words: c.textContent.trim().split(/\s+/).filter(Boolean).length });
  });

  const pre = document.createElement('pre');
  pre.id = 'MEASURE';
  pre.textContent = JSON.stringify(out, null, 1);
  document.body.appendChild(pre);
}

// Fonts must be resolved first: their metrics drive every height measured
// above, and document.fonts.check() is simply false until loading completes.
if (document.fonts && document.fonts.ready) {
  document.fonts.ready.then(() => requestAnimationFrame(runMeasure));
} else {
  runMeasure();
}
