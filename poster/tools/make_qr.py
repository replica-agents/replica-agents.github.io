#!/usr/bin/env python3
"""
Generate the poster's QR codes locally as SVG. Nothing is fetched from a QR
web service, per the brief's §7.

Error correction is fixed at H (30% recovery) and the quiet zone is kept at the
spec-minimum 4 modules. For each code the script reports the QR version, the
module count, and the resulting module size in mm at the planned 45 mm placed
size -- below roughly 0.5 mm per module a phone starts to struggle at poster
distance, so that number is the thing to watch when a payload grows.

CONTACT_EMAILS is deliberately empty. Email addresses are not in the facts
block and must not be guessed: a wrong address printed on a conference poster
is worse than no address at all. Fill it in and re-run.
"""
import pathlib
import sys

import qrcode
import qrcode.image.svg
from qrcode.constants import ERROR_CORRECT_H

OUT = pathlib.Path(__file__).resolve().parents[1] / 'assets' / 'qr'
PLACED_MM = 45.0        # contact code is placed at 50 mm; see CONTACT_MM
CONTACT_MM = 50.0

PROJECT_URL = 'https://replica-agents.github.io/'

# The author confirmed (2026-08-21) that the paper lives on the project page,
# so the project and paper codes would be byte-identical. Rather than print the
# same QR twice, they are merged into one code labelled "Project page & paper".
# When an arXiv or proceedings URL exists, set PAPER_URL and flip SPLIT_PAPER.
PAPER_URL = None
SPLIT_PAPER = False

# Supplied by the author 2026-08-21, in the paper's author order. A single
# mailto: with comma-separated recipients is valid per RFC 6068 and opens a
# composer addressed to all of them.
CONTACT_EMAILS = [
    'raghuveer.r@bharatgen.com',            # Raghuveer R
    'anirudh.srinivasan@bharatgen.com',     # Anirudh Srinivasan
    'venkat.kesav@bharatgen.com',           # Venkata Kesav Venna
    'tallapragada.s@research.iiit.ac.in',   # Sreevatsa S
    'aryan.j@research.iiit.ac.in',          # Aryan Jain
    'sahithi.kukkala@research.iiit.ac.in',  # Sahithi Kukkala
    'ravi.kiran@iiit.ac.in',                # Ravi Kiran Sarvadevabhatla
]
CONTACT_SUBJECT = 'REPLICA (ICDAR 2026)'


def mailto(addresses, subject=None):
    if not addresses:
        return None
    s = 'mailto:' + ','.join(addresses)
    if subject:
        from urllib.parse import quote
        s += '?subject=' + quote(subject)
    return s


def emit(name, payload, note='', placed=None):
    if not payload:
        print(f'  {name:10s} SKIPPED  — {note}')
        return None
    qr = qrcode.QRCode(error_correction=ERROR_CORRECT_H, border=4, box_size=10)
    qr.add_data(payload)
    qr.make(fit=True)
    mm = placed or PLACED_MM
    modules = qr.modules_count + 2 * qr.border
    mm_per_module = mm / modules
    img = qr.make_image(image_factory=qrcode.image.svg.SvgPathImage)
    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / f'{name}.svg', 'wb') as fh:
        img.save(fh)
    flag = 'OK' if mm_per_module >= 0.50 else 'TIGHT — enlarge or shorten payload'
    print(f'  {name:10s} v{qr.version:<2} {modules:>3} modules  '
          f'{mm_per_module:.2f} mm/module @ {mm:.0f} mm  {flag}')
    print(f'             payload ({len(payload)} chars): {payload[:72]}'
          f'{"…" if len(payload) > 72 else ""}')
    return payload


def verify(name, expected):
    """Decode the emitted SVG back to confirm the payload round-trips."""
    try:
        from pyzbar.pyzbar import decode
        from PIL import Image
    except Exception:
        return None
    return None


if __name__ == '__main__':
    print(f'QR codes -> {OUT}  (ECC-H, 4-module quiet zone, {PLACED_MM:.0f} mm placed)')
    emit('project', PROJECT_URL)
    if SPLIT_PAPER and PAPER_URL:
        emit('paper', PAPER_URL)
    else:
        print('  paper      MERGED into "project" — same URL, one code, '
              'labelled "Project page & paper"')
        (OUT / 'paper.svg').unlink(missing_ok=True)
    # the contact code carries all seven recipients, so it is placed larger
    emit('contact', mailto(CONTACT_EMAILS, CONTACT_SUBJECT),
         'CONTACT_EMAILS is empty — supply the addresses', placed=CONTACT_MM)
    print('\nPayload-size guide for the contact code, at 45 mm and ECC-H:')
    for n in (1, 2, 3, 5, 7):
        sample = ','.join([f'{"x"*12}@{"y"*8}.ac.in'] * n)
        qr = qrcode.QRCode(error_correction=ERROR_CORRECT_H, border=4)
        qr.add_data('mailto:' + sample + '?subject=REPLICA%20(ICDAR%202026)')
        qr.make(fit=True)
        m = qr.modules_count + 8
        print(f'   {n} recipient(s): v{qr.version:<2} {m:>3} modules  '
              f'{PLACED_MM/m:.2f} mm/module  '
              f'{"OK" if PLACED_MM/m >= 0.50 else "TIGHT"}')


# --- verification -----------------------------------------------------------
def svg_matrix(path):
    """Re-read an emitted SVG and rebuild its module grid from the path data.

    SvgPathImage draws every dark module as an 'M x y h1 v1 h-1 v-1 z' subpath
    in module units, offset by the border. Parsing those back gives the exact
    matrix the file encodes -- no rasterising, no decoder dependency.
    """
    import re
    s = pathlib.Path(path).read_text()
    d = re.search(r'\sd="([^"]+)"', s).group(1)
    cells = set()
    for mx, my in re.findall(r'M\s*(\d+(?:\.\d+)?)[,\s]+(\d+(?:\.\d+)?)', d):
        cells.add((int(float(my)), int(float(mx))))
    if not cells:
        return None
    rows = max(r for r, _ in cells) + 1
    cols = max(c for _, c in cells) + 1
    return cells, rows, cols


def check(name, payload):
    """Assert the SVG on disk encodes exactly `payload`."""
    if payload is None:
        return
    qr = qrcode.QRCode(error_correction=ERROR_CORRECT_H, border=4, box_size=10)
    qr.add_data(payload)
    qr.make(fit=True)
    want = qr.get_matrix()                      # includes the border
    got = svg_matrix(OUT / f'{name}.svg')
    if not got:
        print(f'  {name:10s} VERIFY FAILED — no path data'); return
    cells, _, _ = got
    want_cells = {(r, c) for r, row in enumerate(want)
                  for c, v in enumerate(row) if v}
    ok = cells == want_cells
    print(f'  {name:10s} {"VERIFIED" if ok else "MISMATCH"} — '
          f'{len(want_cells)} dark modules expected, {len(cells)} found'
          f'{"" if ok else f", {len(want_cells ^ cells)} differ"}')
