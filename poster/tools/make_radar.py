#!/usr/bin/env python3
"""
Generate Fig. 1B (radar) as true vector SVG.

Data and colours supplied by the author (2026-08-21), superseding any value
derived from Table 2. Axis order is [TE, LS, PS, VF]; the plot places
TE right, LS top, PS left, VF bottom, matching the orientation of the
original 512x582 raster in static/images/teaser/image-2.png.

Writes two files into poster/assets/figures/:
  fig1b-radar.svg          labelled, type sized for a ~170 mm placed width
  fig1b-radar-plot.svg     geometry only, no text -- the poster sets its own
                           labels in poster type (same approach the brief
                           mandates for every other figure)
"""
import math
import pathlib

DATA = {
    'REPLICA (OURS)': [90, 80, 79, 93],
    'GPT-5':          [82, 51, 32, 86],
    'Marker':         [75, 39, 26, 74],
    'Qwen3-VL-30B':   [68, 41, 26, 43],
}
COLORS = {
    'REPLICA (OURS)': '#FF0F0F',
    'GPT-5':          '#F5B041',
    'Marker':         '#003D0B',
    'Qwen3-VL-30B':   '#940BE3',
}
AXES = ['TE', 'LS', 'PS', 'VF']
# angle in degrees, measured CCW from east: TE right, LS top, PS left, VF bottom
ANGLE = [0, 90, 180, 270]

# --- geometry, in a 1000 x 1000 viewBox -------------------------------------
CX, CY, R = 500.0, 470.0, 330.0
RINGS = [0.2, 0.4, 0.6, 0.8, 1.0]

# Draw order: largest area first so smaller series stay readable on top.
ORDER = ['REPLICA (OURS)', 'GPT-5', 'Marker', 'Qwen3-VL-30B']


def pt(value, angle_deg):
    """Map a 0..1 value on a given axis to an (x, y) in viewBox space."""
    a = math.radians(angle_deg)
    return (CX + R * value * math.cos(a), CY - R * value * math.sin(a))


def poly(values):
    pts = [pt(v / 100.0, ANGLE[i]) for i, v in enumerate(values)]
    return ' '.join(f'{x:.2f},{y:.2f}' for x, y in pts)


def build(with_text: bool) -> str:
    o = []
    o.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1080" '
             'width="1000" height="1080" role="img">')
    o.append('<title>Fig. 1B - REPLICA vs baselines on TE / LS / PS / VF</title>')

    # rings
    o.append('<g fill="none" stroke="#B9BEC6" stroke-width="1.6">')
    for ring in RINGS[:-1]:
        o.append(f'<circle cx="{CX}" cy="{CY}" r="{R*ring:.2f}"/>')
    o.append('</g>')
    o.append(f'<circle cx="{CX}" cy="{CY}" r="{R:.2f}" fill="none" '
             f'stroke="#6C7480" stroke-width="2.6"/>')

    # spokes
    o.append('<g stroke="#B9BEC6" stroke-width="1.6">')
    for a in ANGLE:
        x, y = pt(1.0, a)
        o.append(f'<line x1="{CX}" y1="{CY}" x2="{x:.2f}" y2="{y:.2f}"/>')
    o.append('</g>')

    # series
    for name in ORDER:
        c = COLORS[name]
        o.append(f'<polygon points="{poly(DATA[name])}" fill="{c}" '
                 f'fill-opacity="0.13" stroke="{c}" stroke-width="5" '
                 f'stroke-linejoin="round"/>')
    for name in ORDER:
        c = COLORS[name]
        for i, v in enumerate(DATA[name]):
            x, y = pt(v / 100.0, ANGLE[i])
            o.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="9" fill="#FFFFFF" '
                     f'stroke="{c}" stroke-width="5"/>')

    if with_text:
        # axis labels - 54 units ~= 26 pt at a 170 mm placed width
        o.append('<g font-family="IBM Plex Sans, Inter, Helvetica, sans-serif" '
                 'font-size="54" font-weight="600" fill="#14181F">')
        lab = {
            'TE': (CX + R + 32, CY + 18, 'start'),
            'LS': (CX, CY - R - 36, 'middle'),
            'PS': (CX - R - 32, CY + 18, 'end'),
            'VF': (CX, CY + R + 72, 'middle'),
        }
        for k, (x, y, anchor) in lab.items():
            o.append(f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}">{k}</text>')
        o.append('</g>')

        # ring callouts - only 0.5 and 1.0, so every glyph clears 24 pt
        o.append('<g font-family="IBM Plex Mono, monospace" font-size="50" '
                 'fill="#5B6472" font-variant-numeric="tabular-nums">')
        for ring, txt in ((0.5, '0.5'), (1.0, '1.0')):
            x, y = pt(ring, 50)
            o.append(f'<text x="{x-4:.1f}" y="{y-16:.1f}" text-anchor="middle">{txt}</text>')
        o.append('</g>')

        # legend, two columns beneath the plot
        o.append('<g font-family="IBM Plex Sans, Inter, Helvetica, sans-serif" '
                 'font-size="50" fill="#14181F">')
        cols = [(70, 968), (580, 968), (70, 1048), (580, 1048)]
        for (x, y), name in zip(cols, ORDER):
            c = COLORS[name]
            o.append(f'<circle cx="{x}" cy="{y-16}" r="13" fill="#FFFFFF" '
                     f'stroke="{c}" stroke-width="7"/>')
            o.append(f'<line x1="{x-30}" y1="{y-16}" x2="{x+30}" y2="{y-16}" '
                     f'stroke="{c}" stroke-width="6"/>')
            o.append(f'<text x="{x+48}" y="{y}">{name}</text>')
        o.append('</g>')

    o.append('</svg>')
    return '\n'.join(o)


if __name__ == '__main__':
    out = pathlib.Path(__file__).resolve().parent.parent / 'assets' / 'figures'
    out.mkdir(parents=True, exist_ok=True)
    (out / 'fig1b-radar.svg').write_text(build(True), encoding='utf-8')
    (out / 'fig1b-radar-plot.svg').write_text(build(False), encoding='utf-8')
    print('wrote fig1b-radar.svg and fig1b-radar-plot.svg')
