#!/usr/bin/env python3
"""
Compose the four rebuilt stage panels into the complete Fig. 4.

Output viewBox is 4682 x 1478, matching the pixel box of
static/images/replica-agents-maindiag-final.png, so the rebuild can be
overlaid 1:1 on the original.

Panel x-offsets were measured off the original by scanning for each panel's
sampled fill colour; the inter-stage chevrons sit in the gaps between them.

Two outputs:
  fig4-full.svg          the complete figure
  fig4-full-nochev.svg   same, without the chevrons, for a poster layout that
                         draws its own continuous stage-to-stage connector
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from fig4_lib import PANEL, chevron

OUT = pathlib.Path(__file__).resolve().parents[1] / 'assets' / 'figures'
W, H = 4682, 1478
TOP = 21

# (stage, x offset in the full figure, panel width)
PLACE = [(1, 19, 1517), (2, 1601, 1176), (3, 2809, 691), (4, 3540, 1120)]
# (x, width, palette key of the stage the chevron leaves)
CHEV = [(1512, 116, 'seg'), (2752, 86, 'loc'), (3474, 100, 'asm')]


def inner(path):
    """Strip the outer <svg> wrapper so the content can be nested."""
    s = (OUT / path).read_text(encoding='utf-8')
    s = re.sub(r'^<svg[^>]*>', '', s.strip())
    s = re.sub(r'</svg>$', '', s.strip())
    return s


def build(with_chevrons=True):
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
         f'width="{W}" height="{H}">',
         f'<rect width="{W}" height="{H}" fill="#FFFFFF"/>']
    for n, x, w in PLACE:
        o.append(f'<svg x="{x}" y="{TOP}" width="{w}" height="1350" '
                 f'viewBox="0 0 {w} 1350" overflow="visible">')
        o.append(inner(f'fig4-stage{n}.svg'))
        o.append('</svg>')
    # chevrons last: in the original they sit over both neighbouring panels
    if with_chevrons:
        for x, w, key in CHEV:
            o.append(chevron(x, 606, w, 196, PANEL[key]))
    o.append('</svg>')
    return '\n'.join(o)


if __name__ == '__main__':
    (OUT / 'fig4-full.svg').write_text(build(True), encoding='utf-8')
    (OUT / 'fig4-full-nochev.svg').write_text(build(False), encoding='utf-8')
    for f in ('fig4-full.svg', 'fig4-full-nochev.svg'):
        print(f'wrote {f}  ({W}x{H} viewBox, {(OUT/f).stat().st_size//1024} KB)')
