#!/usr/bin/env python3
"""
Ink-coverage check, §10 item 17.

The brief asks for "no single flood-filled region larger than ~150 x 150 mm at
greater than 40% saturation". My first attempt measured the fraction of
saturated pixels inside a sliding 150 mm window, which is a different and much
stricter thing -- a window scattered with saturated photo pixels scored the
same as a solid block of ink. This version does what the brief actually says:
finds connected components of heavily-saturated pixels and reports the largest
one's bounding box.
"""
import pathlib
import sys

import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None
SAT_LIMIT = 0.40
SIDE_MM = 150


def main(path):
    im = Image.open(path).convert('RGB')
    W, H = im.size
    # resample to exactly 1 px per mm so component sizes are in mm directly
    im = im.resize((841, 1189), Image.LANCZOS)
    a = np.asarray(im).astype(np.float32) / 255.0
    mx, mn = a.max(2), a.min(2)
    sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0.0)
    heavy = sat > SAT_LIMIT
    print(f'{path}: {W}x{H}px -> 841x1189 mm grid')
    print(f'  pixels above {SAT_LIMIT:.0%} saturation: {heavy.mean()*100:.1f}% of the page')

    # connected components, 4-neighbour, iterative so it cannot blow the stack
    lab = np.zeros(heavy.shape, np.int32)
    cur = 0
    best = (0, None)
    ys, xs = np.nonzero(heavy)
    for sy, sx in zip(ys, xs):
        if lab[sy, sx]:
            continue
        cur += 1
        stack = [(sy, sx)]
        lab[sy, sx] = cur
        y0 = y1 = sy
        x0 = x1 = sx
        n = 0
        while stack:
            y, x = stack.pop()
            n += 1
            y0, y1 = min(y0, y), max(y1, y)
            x0, x1 = min(x0, x), max(x1, x)
            for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                ny, nx = y + dy, x + dx
                if 0 <= ny < 1189 and 0 <= nx < 841 and heavy[ny, nx] and not lab[ny, nx]:
                    lab[ny, nx] = cur
                    stack.append((ny, nx))
        if n > best[0]:
            best = (n, (x0, y0, x1, y1))
    n, box = best
    if not box:
        print('  no saturated region at all'); return 0
    w, h = box[2] - box[0] + 1, box[3] - box[1] + 1
    print(f'  largest saturated component: {n} mm^2, bounding box {w} x {h} mm '
          f'at ({box[0]}, {box[1]})')
    fail = w > SIDE_MM and h > SIDE_MM
    print(f'  verdict: {"FAIL" if fail else "PASS"} '
          f'(limit is a flood-filled region larger than {SIDE_MM} x {SIDE_MM} mm)')
    return 1 if fail else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1
                  else 'out/REPLICA_ICDAR2026_proof_100dpi.png'))
