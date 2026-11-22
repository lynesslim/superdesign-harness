#!/usr/bin/env python3
"""Build a page-scoped override stylesheet from an audit.json (see audit.js).
Derives colour roles from ONE brand colour, a type scale from base+ratio, and maps roles to selectors by
Elementor element id. Nothing here is page-specific; every value can be overridden by a flag."""
import argparse, colorsys, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))

def hex2rgb(h): h = h.lstrip('#'); return tuple(int(h[i:i+2], 16) / 255 for i in (0, 2, 4))
def rgb2hex(r, g, b): return '#%02X%02X%02X' % tuple(round(max(0, min(1, v)) * 255) for v in (r, g, b))
def from_hsl(h, s, l): r, g, b = colorsys.hls_to_rgb(h, l, s); return rgb2hex(r, g, b)
def lum(hexc):
    def f(v): return v / 12.92 if v <= .03928 else ((v + .055) / 1.055) ** 2.4
    r, g, b = map(f, hex2rgb(hexc)); return .2126 * r + .7152 * g + .0722 * b
def contrast(a, b): la, lb = sorted((lum(a), lum(b)), reverse=True); return (la + .05) / (lb + .05)

def derive_colours(brand):
    h, l, s = colorsys.rgb_to_hls(*hex2rgb(brand))
    s = max(s, .35)
    t = {'brand': brand.upper(),
         'ink': from_hsl(h, min(s, .6), .11), 'deep': from_hsl(h, min(s, .6), .19),
         'body': from_hsl(h, min(s, .30), .27), 'paper': from_hsl(h, .35, .97),
         'mist': from_hsl(h, .30, .945), 'sky': from_hsl(h, .60, .90), 'skyText': from_hsl(h, .55, .82)}
    return t

def sel(page, ids, suffix=''):
    return ',\n'.join('body.page-id-%s .elementor-element-%s%s' % (page, i, suffix) for i in ids)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--audit', required=True); ap.add_argument('--page-id', required=True)
    ap.add_argument('--pairing', default='auto'); ap.add_argument('--brand')
    ap.add_argument('--base', type=float, default=16.5, help='body px'); ap.add_argument('--ratio', type=float, default=1.25)
    ap.add_argument('--gutter', default='clamp(24px,4.4vw,64px)'); ap.add_argument('--section', default='clamp(64px,7vw,104px)')
    ap.add_argument('--brand-section', choices=['keep', 'deep'], default='keep', help='what to do with a saturated brand-coloured section background')
    ap.add_argument('--out', required=True); ap.add_argument('--tokens-out')
    a = ap.parse_args()

    audit = json.load(open(a.audit)); roles = audit['roles']; flags = audit.get('flags', {}); P = a.page_id
    brand = (a.brand or audit.get('inferredBrand'))
    if not brand: sys.exit('No brand colour: pass --brand #hex (audit could not infer one).')
    c = derive_colours(brand)

    pairings = json.load(open(os.path.join(HERE, '..', 'references', 'font-pairings.json')))
    key = a.pairing if a.pairing != 'auto' else 'editorial'
    if key not in pairings: sys.exit('Unknown pairing %r. Options: %s' % (key, ', '.join(pairings)))
    f = pairings[key]; D = "'%s',serif" % f['display']; B = "'%s',sans-serif" % f['body']
    if key in ('geometric', 'friendly', 'technical'): D = "'%s',sans-serif" % f['display']
    link = 'https://fonts.googleapis.com/css2?family=%s:wght@%s&family=%s:wght@%s&display=swap' % (
        f['display'].replace(' ', '+'), f['displayWeights'], f['body'].replace(' ', '+'), f['bodyWeights'])

    r = a.ratio; base = a.base
    rem = lambda px: '%.4g' % (px / 16)
    card = base * r ** 2; card_min = base * 1.2  # card title range (min..max px)
    tokens = {'brand': c, 'pairing': key, 'fonts': {'display': f['display'], 'body': f['body']}, 'baseBodyPx': base, 'ratio': r,
              'sizes': {'body': base, 'cardTitle': [round(card_min, 1), round(card, 1)], 'sectionTitle': 'clamp(2.125rem,1.2rem+2.8vw,3.5rem)', 'hero': 'clamp(2.5rem,1rem+4.1vw,4.25rem)'},
              'gutter': a.gutter, 'sectionPadding': a.section,
              'contrast': {'body_on_paper': round(contrast(c['body'], c['paper']), 2), 'ink_on_paper': round(contrast(c['ink'], c['paper']), 2), 'skyText_on_deep': round(contrast(c['skyText'], c['deep']), 2)}}
    if a.tokens_out: json.dump(tokens, open(a.tokens_out, 'w'), indent=2)

    dt = f['displayTracking']; S = 'body.page-id-%s' % P
    css = []
    css.append(":root{--i-ink:%(ink)s;--i-deep:%(deep)s;--i-brand:%(brand)s;--i-paper:%(paper)s;--i-mist:%(mist)s;--i-sky:%(sky)s;--i-body:%(body)s}" % c)
    css.append(":root{--i-gut:%s;--i-sec:%s}" % (a.gutter, a.section))
    css.append("%s{font-family:%s!important;color:var(--i-body)}" % (S, B))
    css.append("%s .elementor-widget-text-editor,%s .elementor-widget-text-editor p,%s .elementor-widget-text-editor li{font-family:%s!important;font-size:clamp(1rem,.95rem + .15vw,%srem)!important;line-height:1.65!important;letter-spacing:0!important;font-weight:400!important}" % (S, S, S, B, rem(base)))
    # !important: Elementor's per-element `max-width:100%` otherwise wins and lines run 120+ characters
    css.append("%s .elementor-widget-text-editor{max-width:62ch!important}" % S)
    if roles.get('centeredBody'):  # centred copy: shorter measure, and centre the capped block so it stays under its heading
        css.append("%s{max-width:58ch!important;margin-left:auto!important;margin-right:auto!important;text-wrap:pretty}" % sel(P, roles['centeredBody']))
        # a custom "initial" widget width (e.g. 60%) leaves ~25 characters per line on phones: let centred copy use the full column there
        css.append("@media(max-width:767px){%s{width:100%%!important}}" % sel(P, roles['centeredBody']))
    css.append("%s .elementor-heading-title{font-family:%s!important;font-weight:600!important;font-size:clamp(%srem,1.05rem + .6vw,%srem)!important;line-height:1.2!important;letter-spacing:-.02em!important}" % (S, B, rem(base * 1.2), rem(card)))
    def role_rule(ids, props):
        if ids: css.append('%s{%s}' % (sel(P, ids, ' .elementor-heading-title'), props))
    role_rule(roles['hero'], "font-family:%s!important;font-weight:400!important;font-size:clamp(2.5rem,1rem + 4.1vw,4.25rem)!important;line-height:1.04!important;letter-spacing:%sem!important" % (D, dt - .005))
    role_rule(roles['sectionTitle'], "font-family:%s!important;font-weight:400!important;font-size:clamp(2.125rem,1.2rem + 2.8vw,3.5rem)!important;line-height:1.08!important;letter-spacing:%sem!important" % (D, dt))
    role_rule(roles['lede'], "font-family:%s!important;font-weight:400!important;font-size:clamp(1.625rem,1.1rem + 1.7vw,2.5rem)!important;line-height:1.18!important;letter-spacing:%sem!important" % (D, dt + .005))
    light_sub = [i for i in roles['subhead'] if flags.get(i, {}).get('light')]; dark_sub = [i for i in roles['subhead'] if i not in light_sub]
    role_rule(roles['subhead'], "font-size:1.0625rem!important;font-weight:500!important;letter-spacing:-.01em!important;line-height:1.4!important")
    role_rule(light_sub, "color:%s!important" % c['skyText'])
    ink_ids = [i for g in ('sectionTitle', 'cardTitle', 'subhead') for i in roles[g] if flags.get(i, {}).get('neutralDark')]
    role_rule(ink_ids, "color:var(--i-ink)!important")
    if roles['eyebrow']:
        css.append("%s{font-family:%s!important;font-size:.8125rem!important;font-weight:600!important;letter-spacing:.1em!important;text-transform:uppercase!important;line-height:1.3!important}" % (sel(P, roles['eyebrow'], ' .elementor-icon-list-text'), B))
    if roles['meta']:
        css.append("%s{font-family:%s!important;font-size:.875rem!important;font-weight:500!important;letter-spacing:0!important}" % (sel(P, roles['meta'], ' .elementor-icon-list-text'), B))
    css.append("%s .elementor-counter-number-wrapper{font-family:%s!important;font-weight:400!important;font-size:clamp(3rem,2rem + 3vw,4.5rem)!important;line-height:1!important;letter-spacing:%sem!important}" % (S, D, dt))
    css.append("%s .elementor-counter-title,%s .elementor-item,%s .e-n-menu-title-text,%s .elementor-nav-menu a{font-family:%s!important;font-weight:500!important;letter-spacing:0!important}" % (S, S, S, S, B))
    css.append("%s .elementor-button{font-family:%s!important;font-weight:600!important;font-size:.9375rem!important;letter-spacing:0!important;border-radius:999px!important;padding:15px 28px!important;min-height:48px}" % (S, B))

    # catch-alls so no old font survives: any icon-list text not given a role, and custom (SuperComponent) widget markup
    css.insert(5, "%s .elementor-icon-list-text{font-family:%s!important;letter-spacing:0}" % (S, B))
    css.append("%s .elementor-widget-supercomponent *:not(i):not(svg):not(path){font-family:%s!important}" % (S, B))
    css.append("%s .elementor-widget-supercomponent :is(h1,h2,h3,h4,h5,h6){font-weight:600!important;font-size:clamp(%srem,1rem + .5vw,%srem)!important;line-height:1.2!important;letter-spacing:-.02em!important}" % (S, rem(base * 1.15), rem(base * 1.4)))
    css.append("%s .elementor-widget-supercomponent p{font-size:.9375rem!important;line-height:1.55!important;letter-spacing:0!important}" % S)
    # native Icon Box widgets (title + description) are not headings/text-editors, so give them the card-title / body roles
    css.append("%s .elementor-icon-box-title,%s .elementor-icon-box-title *{font-family:%s!important;font-weight:600!important;font-size:clamp(%srem,1rem + .5vw,%srem)!important;line-height:1.2!important;letter-spacing:-.02em!important}" % (S, S, B, rem(base * 1.15), rem(base * 1.4)))
    css.append("%s .elementor-icon-box-description{font-family:%s!important;font-size:.9375rem!important;line-height:1.6!important;letter-spacing:0!important}" % (S, B))

    # section backgrounds + spacing (derived from audit.sections, not hardcoded)
    light_i = 0
    for s in audit['sections']:
        if not s['id']: continue
        sid = s['id']; sc = '%s .elementor-element-%s' % (S, sid)
        if s['kind'] == 'content':
            css.append("%s{padding-left:var(--i-gut)!important;padding-right:var(--i-gut)!important;padding-top:var(--i-sec)!important;padding-bottom:var(--i-sec)!important}" % sc)
        if s['bg'] and not s['hasBgMedia'] and s['bgLum'] is not None:
            if s['bgLum'] > .85 and s['bgSat'] < .12 and s['bg'].upper() != '#FFFFFF':
                css.append("%s{background-color:var(--i-%s)!important}" % (sc, 'paper' if light_i % 2 == 0 else 'mist')); light_i += 1
            elif s['bgLum'] < .3:
                css.append("%s{background-color:var(--i-deep)!important}" % sc)
            elif s['bgSat'] > .35 and a.brand_section == 'deep':
                css.append("%s{background-color:var(--i-deep)!important}" % sc)
    body = '\n'.join(css)
    open(a.out, 'w').write('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="%s"><style>\n%s\n</style>' % (link, body))
    print(json.dumps({'out': a.out, 'brand': c['brand'], 'pairing': key, 'contrast': tokens['contrast'],
                      'roleCounts': {k: len(v) for k, v in roles.items()}, 'sections': len(audit['sections'])}, indent=1))

if __name__ == '__main__': main()
