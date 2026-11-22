// Usage: call Playwright browser_run_code_unsafe with filename=<this file> (no `require` is available there) (after loading the page at 1440x900
// and scrolling through it once). Returns a JSON audit: fonts, sizes, brand colour, section metrics and a
// role map keyed by Elementor element IDs. Nothing here is page-specific.
async (page) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.evaluate(async () => {            // scroll through once so lazy/animated content settles
    const H = document.documentElement.scrollHeight;
    for (let y = 0; y < H; y += 900) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 120)); }
    window.scrollTo(0, 0);
  });
  return await page.evaluate(() => {
    const idOf = el => { for (const c of el.classList) { const m = c.match(/^elementor-element-([a-z0-9]+)$/); if (m) return m[1]; } return null; };
    const rgb = s => { const m = (s || '').match(/rgba?\(([^)]+)\)/); if (!m) return null; const p = m[1].split(',').map(x => parseFloat(x)); return { r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1 }; };
    const hex = c => '#' + [c.r, c.g, c.b].map(v => Math.round(v).toString(16).padStart(2, '0')).join('');
    const hsl = c => { const r = c.r / 255, g = c.g / 255, b = c.b / 255, mx = Math.max(r, g, b), mn = Math.min(r, g, b), l = (mx + mn) / 2; let h = 0, s = 0; if (mx !== mn) { const d = mx - mn; s = l > .5 ? d / (2 - mx - mn) : d / (mx + mn); h = mx === r ? ((g - b) / d + (g < b ? 6 : 0)) : mx === g ? (b - r) / d + 2 : (r - g) / d + 4; h *= 60; } return { h, s, l }; };
    const fam = el => getComputedStyle(el).fontFamily.split(',')[0].replace(/["']/g, '').trim();
    const solid = c => c && c.a > 0.5;

    const roots = [...document.querySelectorAll('[data-elementor-type="wp-page"] > .e-con, .elementor-location-single > .e-con, .elementor > .e-con')];
    const rootSet = new Set(roots);
    const inRootBg = el => {                    // is el inside a card (non-root container with a solid bg or blur)?
      let p = el.parentElement, depth = 0;
      while (p && depth < 4) {
        if (p.classList && p.classList.contains('e-con') && !rootSet.has(p)) {
          const cs = getComputedStyle(p), c = rgb(cs.backgroundColor);
          if (solid(c) || (cs.backdropFilter && cs.backdropFilter !== 'none')) return true;
        }
        p = p.parentElement; depth++;
      }
      return false;
    };

    const fontCount = {}, sizeSet = new Set(), colourVotes = {};
    const vote = (c, w) => { if (!c || c.a < .5) return; const h = hsl(c); if (h.s > .35 && h.l > .12 && h.l < .7) { const k = hex(c); colourVotes[k] = (colourVotes[k] || 0) + w; } };

    const roles = { hero: [], sectionTitle: [], lede: [], cardTitle: [], subhead: [], eyebrow: [], meta: [], centeredBody: [] };
    const unclassified = [];
    const headings = [...document.querySelectorAll('.elementor-widget-heading')].filter(w => w.getBoundingClientRect().width > 0);
    const infos = headings.map(w => {
      const t = w.querySelector('.elementor-heading-title') || w, cs = getComputedStyle(t), col = rgb(cs.color) || { r: 0, g: 0, b: 0, a: 1 }, hh = hsl(col);
      return { id: idOf(w), text: (t.textContent || '').replace(/\s+/g, ' ').trim(), fs: parseFloat(cs.fontSize), light: hh.l > .75, neutralDark: hh.s < .15 && hh.l < .2, rootIdx: roots.findIndex(r => r.contains(w)), col };
    });
    const heroCandidates = infos.filter(i => i.rootIdx <= 1);
    const heroFs = heroCandidates.length ? Math.max(...heroCandidates.map(i => i.fs)) : 0;
    const flags = {};                          // per-id extra flags the builder needs
    infos.forEach(i => {
      if (!i.id) return;
      if (i.light || i.neutralDark) flags[i.id] = { light: i.light, neutralDark: i.neutralDark };
      sizeSet.add(i.fs); vote(i.col, 2);
      if (heroFs && i.fs === heroFs && i.rootIdx <= 1 && i.fs >= 36) roles.hero.push(i.id);
      else if (i.fs >= 28 && i.text.length > 70) roles.lede.push(i.id);
      else if (i.fs >= 36) roles.sectionTitle.push(i.id);
      else if (i.fs >= 20) roles.cardTitle.push(i.id);
      else if (i.fs >= 13) roles.subhead.push(i.id);
      else unclassified.push({ id: i.id, why: 'heading smaller than 13px', text: i.text.slice(0, 30) });
    });

    document.querySelectorAll('.elementor-widget-icon-list').forEach(w => {
      const items = w.querySelectorAll('.elementor-icon-list-item');
      if (items.length !== 1) return;
      const span = w.querySelector('.elementor-icon-list-text'); if (!span) return;
      const txt = span.textContent.trim(), fs = parseFloat(getComputedStyle(span).fontSize), id = idOf(w);
      if (!id || w.getBoundingClientRect().width === 0) return;
      if (txt.length < 40 && fs <= 16 && !inRootBg(w)) roles.eyebrow.push(id); else if (txt.length < 40) roles.meta.push(id);
    });

    // centred body copy (text-editor widgets whose text is centre-aligned): the builder caps their measure AND centres the block
    document.querySelectorAll('.elementor-widget-text-editor').forEach(w => {
      const id = idOf(w); if (!id || w.getBoundingClientRect().width === 0) return;
      const t = w.querySelector('p') || w;
      if (getComputedStyle(t).textAlign === 'center' || getComputedStyle(w).textAlign === 'center') roles.centeredBody.push(id);
    });

    document.querySelectorAll('.elementor-widget-text-editor, .elementor-widget-heading, .elementor-widget-icon-list, .elementor-widget-button, .elementor-nav-menu, .elementor-counter').forEach(w => {
      const t = w.querySelector('p, .elementor-heading-title, .elementor-icon-list-text, .elementor-button, a, .elementor-counter-title') || w;
      const f = fam(t); fontCount[f] = (fontCount[f] || 0) + 1;
    });
    document.querySelectorAll('.elementor-button').forEach(b => { vote(rgb(getComputedStyle(b).backgroundColor), 3); });

    let seenHero = false;
    const sections = roots.map((r, i) => {
      const cs = getComputedStyle(r), bg = rgb(cs.backgroundColor), h = Math.round(r.getBoundingClientRect().height);
      if (solid(bg)) vote(bg, 1);
      const hasImg = (cs.backgroundImage && cs.backgroundImage !== 'none') || !!r.querySelector(':scope > .elementor-background-video-container, :scope > .elementor-background-overlay');
      const hh = bg ? hsl(bg) : null;
      return { id: idOf(r), index: i, height: h, padTop: parseFloat(cs.paddingTop), padBottom: parseFloat(cs.paddingBottom), padLeft: parseFloat(cs.paddingLeft), padRight: parseFloat(cs.paddingRight),
        bg: solid(bg) ? hex(bg) : null, bgLum: hh ? +hh.l.toFixed(2) : null, bgSat: hh ? +hh.s.toFixed(2) : null, hasBgMedia: !!hasImg, minHeight: cs.minHeight,
        kind: (r.closest('[data-elementor-type]') || {}).getAttribute && r.closest('[data-elementor-type]').getAttribute('data-elementor-type') !== 'wp-page' ? 'template' : (h >= window.innerHeight * .85 && (hasImg || cs.minHeight !== '0px') && i <= 2 && !seenHero ? (seenHero = true, 'hero') : 'content') };
    });
    const brand = Object.entries(colourVotes).sort((a, b) => b[1] - a[1])[0];
    const bodySizes = [...document.querySelectorAll('.elementor-widget-text-editor p')].map(p => parseFloat(getComputedStyle(p).fontSize));
    return {
      url: location.href, viewport: innerWidth + 'x' + innerHeight, fonts: fontCount, distinctHeadingSizes: [...sizeSet].sort((a, b) => b - a),
      bodySizes: [...new Set(bodySizes)], inferredBrand: brand ? brand[0] : null, colourVotes: Object.fromEntries(Object.entries(colourVotes).sort((a, b) => b[1] - a[1]).slice(0, 5)), roles, flags, sections, unclassified
    };
  });
}
