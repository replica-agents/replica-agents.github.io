#!/usr/bin/env python3
"""
Render the Fid-HTML reconstructions in static/images/qual/*.html to PNG via
headless Chrome, at a device-scale-factor chosen so each output clears
~1800 px on its long edge (>= 300 dpi at a 125 mm placed width).

The HTML files are read-only inputs; nothing outside poster/ is written.
Text in these documents is real DOM text, so supersampling yields genuine
extra detail rather than an upscale. The page background is an embedded
raster and is the one element that does not gain detail past its own size.
"""
import re
import pathlib
import subprocess
import sys

REPO = pathlib.Path(__file__).resolve().parents[2]
QUAL = REPO / 'static' / 'images' / 'qual'
OUT = REPO / 'poster' / 'assets' / 'figures'
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

# html stem -> output slot name
PAIRS = {
    '17935_corrected':        'qual-newspaper-render',
    '00000127_corrected':     'qual-magazine-render',
    '00000087_corrected':     'qual-techmag-render',
    '00000269_corrected':     'qual-interview-render',
    'X51005621482_corrected': 'qual-receipt-render',
    'X51005230605_corrected': 'qual-fuelreceipt-render',
    'LoRaLay_1_corrected':    'qual-korean-render',
    'RVLCDIP_4_corrected':    'qual-letter-render',
    'IndicDLP_1_corrected':   'qual-gazette-render',
    'IndicDLP_2_corrected':   'qual-indicmag-render',
    '20005_html':             'qual-factsoflife-render',
}
TARGET_LONG_EDGE = 1800
MAX_SCALE = 4          # beyond this Chrome gets unreliable on very tall pages
MAX_PIXELS = 60_000_000


def page_box(path: pathlib.Path):
    """Read the declared body width/height in CSS px."""
    head = path.read_text(errors='replace')[:4000]
    w = re.search(r'width:\s*(\d+)px', head)
    h = re.search(r'height:\s*(\d+)px', head)
    if not (w and h):
        return None
    return int(w.group(1)), int(h.group(1))


def main():
    if not pathlib.Path(CHROME).exists():
        sys.exit(f'Chrome not found at {CHROME}')
    OUT.mkdir(parents=True, exist_ok=True)
    for stem, slot in PAIRS.items():
        src = QUAL / f'{stem}.html'
        if not src.exists():
            print(f'  SKIP  {stem}: not on disk')
            continue
        box = page_box(src)
        if not box:
            print(f'  SKIP  {stem}: no declared body box')
            continue
        w, h = box
        scale = min(MAX_SCALE, max(1, round(TARGET_LONG_EDGE / max(w, h) + 0.49)))
        while w * h * scale * scale > MAX_PIXELS and scale > 1:
            scale -= 1
        dest = OUT / f'{slot}.png'
        cmd = [CHROME, '--headless', '--disable-gpu', '--hide-scrollbars',
               '--default-background-color=00000000',
               f'--force-device-scale-factor={scale}',
               f'--window-size={w},{h}',
               '--virtual-time-budget=20000',
               f'--screenshot={dest}', src.as_uri()]
        subprocess.run(cmd, capture_output=True, timeout=300)
        if dest.exists():
            from PIL import Image
            Image.MAX_IMAGE_PIXELS = None
            im = Image.open(dest)
            print(f'  OK    {slot:26s} css {w}x{h} @{scale}x -> {im.width}x{im.height}')
        else:
            print(f'  FAIL  {slot}: no output')


if __name__ == '__main__':
    main()
