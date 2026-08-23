#!/usr/bin/env python3
"""
Shared vocabulary for the vector rebuild of Fig. 4.

Every colour here was sampled directly off static/images/replica-agents-maindiag-final.png
at full resolution (modal colour of a clean interior region), not guessed.

Icon note: the wrench+gear "Tool" glyph and the "Agent" robot in the original are
clipart rasters whose best available resolution is ~67x65 px. They cannot be
reproduced pixel-exactly at any size. The versions here are redrawn vector
equivalents matched to the originals' silhouette, proportion and palette.
"""

# --- sampled palette --------------------------------------------------------
PANEL = {
    'seg': dict(fill='#DBE7EF', head='#B9CCDE', edge='#46617C', badge='#4A6BA5',
                card='#E7F0F8', chev='#C3D2E2', chevedge='#6C8AAC'),
    'loc': dict(fill='#D9E7CB', head='#BED7A1', edge='#6D9468', badge='#689558',
                card='#E4EFD8', chev='#C9DEB9', chevedge='#7BA76B'),
    'asm': dict(fill='#F5E8B2', head='#F0DC84', edge='#C9A83F', badge='#E9C136',
                card='#F7EDBE', chev='#F0D97A', chevedge='#CDA53E'),
    'ref': dict(fill='#F3E3CF', head='#EAC19F', edge='#B4753F', badge='#C67736',
                card='#F6E9DA', chev='#F0CBA6', chevedge='#C08A5C'),
}
BADGE_1A = '#B01F1E'      # the one red badge in the original
BADGE_1B = '#37507F'      # 1B is a darker navy than 1C/1D/1E in the original
INK = '#101418'
RULE = '#101418'

TOOL_STEEL = '#D8D8D2'    # wrench body
TOOL_BLUE = '#4A6FA8'     # wrench handle
BOT_LINE = '#101418'
BOT_FILL = '#FFFFFF'
BOT_TINT = '#EDEFE6'


def esc(s):
    return (s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))


def text(x, y, s, size=40, weight='700', anchor='middle', fill=INK,
         family='Arial, Helvetica, sans-serif', style=''):
    st = f' font-style="{style}"' if style else ''
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"{st}>{esc(s)}</text>')


def lines(x, y, rows, size=40, weight='700', lh=1.14, anchor='middle', fill=INK):
    """Stacked centred text lines, the way every label in Fig. 4 is set."""
    out = []
    for i, r in enumerate(rows):
        if isinstance(r, tuple):
            s, w, sz = r
        else:
            s, w, sz = r, weight, size
        out.append(text(x, y + i * size * lh, s, sz, w, anchor, fill))
    return '\n'.join(out)


def sub(x, y, base, subscript, size=40, weight='700', anchor='middle'):
    """Renders e.g. T_type as T with a small lowered 'type'."""
    return (f'<text x="{x}" y="{y}" font-family="Arial, Helvetica, sans-serif" '
            f'font-size="{size}" font-weight="{weight}" fill="{INK}" '
            f'text-anchor="{anchor}">{esc(base)}'
            f'<tspan font-size="{size*0.68:.0f}" dy="{size*0.22:.0f}">{esc(subscript)}</tspan></text>')


def _dark(hexc, k=0.45):
    r = int(hexc[1:3], 16); g = int(hexc[3:5], 16); b = int(hexc[5:7], 16)
    return '#%02X%02X%02X' % (int(r * k), int(g * k), int(b * k))


def badge(cx, cy, label, color, r=54, fs=52):
    """Filled disc with the dark ring the original uses, white numeral."""
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}" '
            f'stroke="{_dark(color)}" stroke-width="{max(5.0, r*0.155):.1f}"/>'
            + text(cx, cy + fs * 0.35, label, fs, '700', 'middle', '#FFFFFF'))


def card(x, y, w, h, pal, rx=26, sw=5):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
            f'fill="{pal["card"]}" stroke="{pal["edge"]}" stroke-width="{sw}"/>')


def whitebox(x, y, w, h, rx=26, sw=5):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
            f'fill="#FFFFFF" stroke="{RULE}" stroke-width="{sw}"/>')


def chevron(x, y, w, h, pal):
    """The fat inter-stage arrow between panels."""
    n = w * 0.46
    d = (f'M{x},{y+h*0.26} H{x+n} V{y} L{x+w},{y+h/2} L{x+n},{y+h} '
         f'V{y+h*0.74} H{x} Z')
    return (f'<path d="{d}" fill="{pal["chev"]}" stroke="{pal["chevedge"]}" '
            f'stroke-width="6" stroke-linejoin="round"/>')


def arrow(x1, y1, x2, y2, w=7, head=26):
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{RULE}" '
            f'stroke-width="{w}" marker-end="url(#ah)"/>')


def polyline(pts, w=7, head=True):
    p = ' '.join(f'{x},{y}' for x, y in pts)
    m = ' marker-end="url(#ah)"' if head else ''
    return (f'<polyline points="{p}" fill="none" stroke="{RULE}" '
            f'stroke-width="{w}" stroke-linejoin="miter"{m}/>')


def defs():
    return '''<defs>
<marker id="ah" viewBox="0 0 12 12" refX="9.5" refY="6" markerWidth="5.2"
        markerHeight="5.2" orient="auto-start-reverse" markerUnits="strokeWidth">
  <path d="M0,0.6 L11.5,6 L0,11.4 z" fill="%s"/>
</marker>
</defs>''' % RULE


# --- redrawn icons ----------------------------------------------------------
import math

def _jaw(cx, cy, ro, ri, gap_deg):
    """Thick C opening upward -- an open-end spanner head."""
    half = math.radians(gap_deg / 2)
    def P(r, a):
        return (cx + r * math.sin(a), cy - r * math.cos(a))
    a0, a1 = half, 2 * math.pi - half
    o0, o1, i1, i0 = P(ro, a0), P(ro, a1), P(ri, a1), P(ri, a0)
    return (f"M{o0[0]:.2f},{o0[1]:.2f} A{ro},{ro} 0 1 1 {o1[0]:.2f},{o1[1]:.2f} "
            f"L{i1[0]:.2f},{i1[1]:.2f} A{ri},{ri} 0 1 0 {i0[0]:.2f},{i0[1]:.2f} Z")


def _gear(cx, cy, r, teeth=8, depth=0.32):
    d = []
    for i in range(teeth):
        a = 2 * math.pi * i / teeth
        w = math.radians(360 / teeth * 0.30)
        ring = [(r, a - w), (r * (1 + depth), a - w * 0.62),
                (r * (1 + depth), a + w * 0.62), (r, a + w)]
        for k, (rr, aa) in enumerate(ring):
            x, y = cx + rr * math.sin(aa), cy - rr * math.cos(aa)
            d.append(("M" if (i == 0 and k == 0) else "L") + f"{x:.2f},{y:.2f}")
    return " ".join(d) + " Z"


def _spanner(fill):
    """One spanner, pointing up, drawn in a 0..40 x 0..122 box."""
    return (f'<g stroke="{BOT_LINE}" stroke-width="5.5" stroke-linejoin="round">'
            f'<path d="{_jaw(20,19,18,9.5,62)}" fill="{fill}"/>'
            f'<rect x="11" y="29" width="18" height="78" rx="8" fill="{fill}"/>'
            f'</g>')


def tool_icon(cx, cy, s=1.0):
    """Two crossed spanners plus a gear -- the original's 'Tool' clipart."""
    k = s * 1.06
    return (f'<g transform="translate({cx},{cy}) scale({k})">'
            f'<g transform="rotate(-38) translate(-20,-62)">{_spanner(TOOL_STEEL)}</g>'
            f'<g transform="rotate(38) translate(-20,-62)">{_spanner(TOOL_BLUE)}</g>'
            f'<path d="{_gear(8,36,15)}" fill="{TOOL_STEEL}" stroke="{BOT_LINE}" '
            f'stroke-width="5" stroke-linejoin="round"/>'
            f'<circle cx="8" cy="36" r="6.5" fill="{BOT_TINT}" stroke="{BOT_LINE}" '
            f'stroke-width="4"/>'
            f'</g>')


def agent_icon(cx, cy, s=1.0):
    """Rounded 'assistant' robot, matched to the original's silhouette."""
    return (f'<g transform="translate({cx},{cy}) scale({s})">'
            f'<g stroke="{BOT_LINE}" stroke-width="7" stroke-linejoin="round" '
            f'stroke-linecap="round" fill="{BOT_FILL}">'
            f'<path d="M0,-88 v16" fill="none"/>'
            f'<circle cx="0" cy="-92" r="9" fill="{BOT_LINE}" stroke="none"/>'
            f'<rect x="-54" y="-74" width="108" height="78" rx="32" fill="{BOT_TINT}"/>'
            f'<path d="M-30,-40 a13,12 0 0 1 24,0" fill="none"/>'
            f'<path d="M6,-40 a13,12 0 0 1 24,0" fill="none"/>'
            f'<rect x="-42" y="14" width="84" height="60" rx="18" fill="{BOT_FILL}"/>'
            f'<rect x="-13" y="32" width="26" height="28" rx="9" fill="{BOT_TINT}"/>'
            f'<rect x="-70" y="22" width="22" height="42" rx="11" fill="{BOT_TINT}"/>'
            f'<rect x="48" y="22" width="22" height="42" rx="11" fill="{BOT_TINT}"/>'
            f'</g></g>')


def doc_icon(x, y, w, h):
    """The 'Input Document' page thumbnail."""
    ln = ''.join(
        f'<rect x="{x+w*0.10}" y="{y+h*(0.36+i*0.075)}" width="{w*0.80}" '
        f'height="{h*0.028}" fill="#7C8794"/>' for i in range(4))
    ln2 = ''.join(
        f'<rect x="{x+w*0.10}" y="{y+h*(0.70+i*0.075)}" width="{w*0.36}" '
        f'height="{h*0.028}" fill="#7C8794"/>' for i in range(3))
    return f'''
<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#FFFFFF" stroke="{BOT_LINE}" stroke-width="5"/>
<rect x="{x+w*0.10}" y="{y+h*0.08}" width="{w*0.46}" height="{h*0.22}" fill="#CFE3F5" stroke="#5B7FA8" stroke-width="3"/>
<path d="M{x+w*0.12},{y+h*0.28} L{x+w*0.24},{y+h*0.15} L{x+w*0.34},{y+h*0.28} z" fill="#8FBF7A"/>
<circle cx="{x+w*0.44}" cy="{y+h*0.15}" r="{h*0.028}" fill="#E8B84B"/>
<rect x="{x+w*0.62}" y="{y+h*0.08}" width="{w*0.28}" height="{h*0.030}" fill="#7C8794"/>
<rect x="{x+w*0.62}" y="{y+h*0.15}" width="{w*0.28}" height="{h*0.030}" fill="#7C8794"/>
<rect x="{x+w*0.62}" y="{y+h*0.22}" width="{w*0.28}" height="{h*0.030}" fill="#7C8794"/>
{ln}{ln2}
<rect x="{x+w*0.54}" y="{y+h*0.66}" width="{w*0.36}" height="{h*0.22}" fill="#BCD3EA" stroke="#5B7FA8" stroke-width="3"/>'''


def tree_icon(cx, cy, w=250, h=230):
    """The T_layout tree: 1 root, 3 children, 4 leaves."""
    r = w * 0.072
    x0, y0 = cx - w / 2, cy - h / 2
    root = (cx, y0 + r)
    mids = [(x0 + w * 0.20, y0 + h * 0.52), (x0 + w * 0.50, y0 + h * 0.52),
            (x0 + w * 0.80, y0 + h * 0.52)]
    leaves = [(x0 + w * 0.10, y0 + h - r), (x0 + w * 0.32, y0 + h - r),
              (x0 + w * 0.62, y0 + h - r), (x0 + w * 0.88, y0 + h - r)]
    seg = []
    for m in mids:
        seg.append(f'<path d="M{root[0]},{root[1]} V{(root[1]+m[1])/2} H{m[0]} V{m[1]}" '
                   f'fill="none" stroke="{BOT_LINE}" stroke-width="5"/>')
    for i, l in enumerate(leaves):
        m = mids[0] if i < 2 else mids[2]
        seg.append(f'<path d="M{m[0]},{m[1]} V{(m[1]+l[1])/2} H{l[0]} V{l[1]}" '
                   f'fill="none" stroke="{BOT_LINE}" stroke-width="5"/>')
    dots = ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#9AA6B2" '
                   f'stroke="{BOT_LINE}" stroke-width="4"/>'
                   for x, y in [root] + mids + leaves)
    return ''.join(seg) + dots


# --- icons used only by stages 3 and 4 --------------------------------------
def brain_agent_icon(cx, cy, s=1.0):
    """The Reading-Order agent: robot whose crown is a visible brain."""
    return (f'<g transform="translate({cx},{cy}) scale({s})">'
            f'<g stroke="{BOT_LINE}" stroke-width="6" stroke-linejoin="round" '
            f'stroke-linecap="round" fill="{BOT_FILL}">'
            f'<path d="M-44,-52 a44,40 0 0 1 88,0 a30,26 0 0 1 -6,20 H-38 '
            f'a30,26 0 0 1 -6,-20 z" fill="#BFD3E4"/>'
            f'<g fill="none" stroke="{BOT_LINE}" stroke-width="4">'
            f'<path d="M0,-90 V-32"/>'
            f'<path d="M-13,-84 q-16,10 -12,26 q-14,8 -8,24"/>'
            f'<path d="M13,-84 q16,10 12,26 q14,8 8,24"/>'
            f'<path d="M-30,-58 q10,-6 16,2"/>'
            f'<path d="M30,-58 q-10,-6 -16,2"/>'
            f'</g>'
            f'<rect x="-42" y="-32" width="84" height="52" rx="20" fill="{BOT_TINT}"/>'
            f'<circle cx="-16" cy="-10" r="6.5" fill="{BOT_LINE}" stroke="none"/>'
            f'<circle cx="16" cy="-10" r="6.5" fill="{BOT_LINE}" stroke="none"/>'
            f'<path d="M-12,6 a14,10 0 0 0 24,0" fill="none" stroke-width="5"/>'
            f'<rect x="-34" y="30" width="68" height="48" rx="16" fill="{BOT_FILL}"/>'
            f'<circle cx="0" cy="54" r="11" fill="#C9AFA0"/>'
            f'<rect x="-58" y="36" width="18" height="36" rx="9" fill="{BOT_TINT}"/>'
            f'<rect x="40" y="36" width="18" height="36" rx="9" fill="{BOT_TINT}"/>'
            f'</g></g>')


def html_doc_icon(cx, cy, w=150, h=190, label='HTML'):
    """Page with a folded corner, 'HTML' caption, list rules and </>."""
    x, y = cx - w / 2, cy - h / 2
    f = w * 0.26
    d = (f'M{x},{y} H{x+w-f} L{x+w},{y+f} V{y+h} H{x} Z')
    fold = f'M{x+w-f},{y} V{y+f} H{x+w}'
    rules = ''.join(
        f'<rect x="{x+w*0.22}" y="{y+h*(0.40+i*0.10)}" width="{w*0.56}" '
        f'height="{h*0.038}" fill="{BOT_LINE}"/>' for i in range(3))
    dots = ''.join(
        f'<circle cx="{x+w*0.14}" cy="{y+h*(0.42+i*0.10)}" r="{w*0.032}" '
        f'fill="{BOT_LINE}"/>' for i in range(3))
    return (f'<path d="{d}" fill="#FFFFFF" stroke="{BOT_LINE}" stroke-width="5" '
            f'stroke-linejoin="round"/>'
            f'<path d="{fold}" fill="none" stroke="{BOT_LINE}" stroke-width="5"/>'
            + text(cx - w * 0.10, y + h * 0.26, label, w * 0.20, '700')
            + rules + dots
            + text(cx, y + h * 0.94, '</>', w * 0.22, '700'))


def browser_icon(cx, cy, w=300, h=230):
    """Browser chrome with a rendered page inside -- the 'final HTML' thumbnail."""
    x, y = cx - w / 2, cy - h / 2
    bar = h * 0.135
    dots = ''.join(f'<circle cx="{x+w*(0.045+i*0.045)}" cy="{y+bar/2}" '
                   f'r="{bar*0.16}" fill="{c}"/>'
                   for i, c in enumerate(['#E06C5F', '#E3B341', '#79B563']))
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#FFFFFF" '
            f'stroke="{BOT_LINE}" stroke-width="5"/>'
            f'<path d="M{x},{y+bar} H{x+w}" stroke="{BOT_LINE}" stroke-width="4"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{bar}" rx="10" fill="#CBDCEC"/>'
            f'<rect x="{x}" y="{y+bar*0.5}" width="{w}" height="{bar*0.5}" fill="#CBDCEC"/>'
            + dots +
            f'<rect x="{x+w*0.05}" y="{y+bar*1.35}" width="{w*0.42}" height="{h*0.30}" '
            f'fill="#CFE3F5" stroke="#6E90B4" stroke-width="3"/>'
            f'<path d="M{x+w*0.08},{y+bar*1.35+h*0.30} L{x+w*0.20},{y+bar*1.35+h*0.11} '
            f'L{x+w*0.32},{y+bar*1.35+h*0.30} z" fill="#7FB36A"/>'
            f'<circle cx="{x+w*0.36}" cy="{y+bar*1.35+h*0.09}" r="{h*0.030}" fill="#E8B84B"/>'
            f'<rect x="{x+w*0.54}" y="{y+bar*1.35}" width="{w*0.40}" height="{h*0.10}" fill="#D8534B"/>'
            + ''.join(f'<rect x="{x+w*0.54}" y="{y+bar*1.35+h*(0.15+i*0.055)}" '
                      f'width="{w*0.40}" height="{h*0.030}" fill="#9AA6B2"/>' for i in range(3))
            + ''.join(f'<rect x="{x+w*0.05}" y="{y+bar*1.35+h*(0.36+i*0.055)}" '
                      f'width="{w*0.46}" height="{h*0.030}" fill="#9AA6B2"/>' for i in range(3))
            + f'<rect x="{x+w*0.56}" y="{y+bar*1.35+h*0.36}" width="{w*0.36}" '
              f'height="{h*0.24}" fill="#F0C64E"/>')


def loop_arrow(d, w=16, color='#5B7FB5'):
    return (f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w}" '
            f'stroke-linecap="round" marker-end="url(#ahb)"/>')


def defs_blue():
    return ('<marker id="ahb" viewBox="0 0 12 12" refX="8" refY="6" markerWidth="3.4" '
            'markerHeight="3.4" orient="auto-start-reverse" markerUnits="strokeWidth">'
            '<path d="M0,0.6 L11.5,6 L0,11.4 z" fill="#5B7FB5"/></marker>')


# --- text fitting -----------------------------------------------------------
# Approximate Arial advance widths, as a fraction of font-size. Good to a few
# percent, which is all that is needed to stop labels overrunning their boxes.
_NARROW = set("ijltI.,;:'!|()[]{}/\\ ")
_WIDE = set("MWmw@")


def _adv(ch, bold):
    if ch in _NARROW:
        w = 0.30
    elif ch in _WIDE:
        w = 0.86
    elif ch.isupper() or ch.isdigit():
        w = 0.65
    else:
        w = 0.53
    return w * (1.06 if bold else 1.0)


def measure(s, size, bold=True):
    return size * sum(_adv(c, bold) for c in s)


def fit_size(s, maxw, size, bold=True, floor=18):
    """Largest size <= `size` at which `s` fits in `maxw`."""
    w = measure(s, size, bold)
    if w <= maxw:
        return size
    return max(floor, size * maxw / w)


def ftext(x, y, s, maxw, size=40, weight='700', anchor='middle', fill=INK):
    sz = fit_size(s, maxw, size, weight != '400')
    return text(x, y, s, sz, weight, anchor, fill)


def flines(x, y, rows, maxw, size=40, weight='700', lh=1.14, anchor='middle'):
    """Stacked lines, all shrunk together to the size the widest one allows."""
    bold = weight != '400'
    sz = min(fit_size(r, maxw, size, bold) for r in rows)
    return '\n'.join(text(x, y + i * sz * lh, r, sz, weight, anchor) for i, r in enumerate(rows))


def fsub(x, y, base, subscript, maxw, size=40, weight='700', anchor='middle'):
    """Subscripted label that shrinks to fit maxw."""
    bold = weight != '400'
    approx = base + subscript
    sz = fit_size(approx, maxw, size, bold)
    return sub(x, y, base, subscript, sz, weight, anchor)
