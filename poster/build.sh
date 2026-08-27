#!/usr/bin/env bash
# Render the poster to a print-ready A0 PDF plus proof rasters.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
mkdir -p "$ROOT/out"

"$CHROME" --headless --disable-gpu --no-pdf-header-footer \
  --virtual-time-budget=20000 \
  --print-to-pdf="$ROOT/out/REPLICA_ICDAR2026_A0.pdf" \
  "file://$ROOT/poster/index.html"

# Chrome maps CSS physical units at 96 dpi, so the exact A0 canvas is
# 3179 x 4494 CSS pixels. Capture that canvas without a surplus viewport,
# then resample the proof to true 100 dpi below.
"$CHROME" --headless --disable-gpu --hide-scrollbars \
  --force-device-scale-factor=1 --window-size=3179,4494 \
  --virtual-time-budget=20000 \
  --screenshot="$ROOT/out/REPLICA_ICDAR2026_proof_100dpi.png" \
  "file://$ROOT/poster/index.html"

python3 - "$ROOT" <<'PY'
import sys, pathlib
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
root = pathlib.Path(sys.argv[1])
p = root / 'out' / 'REPLICA_ICDAR2026_proof_100dpi.png'
im = Image.open(p)
im = im.resize((3311, 4681), Image.LANCZOS)
im.save(p)
im.resize((500, round(500 * im.height / im.width)), Image.LANCZOS).save(
    root / 'out' / 'REPLICA_ICDAR2026_squint.png')
print(f'proof {im.width}x{im.height}  squint 500x{round(500*im.height/im.width)}')
PY
echo "done -> $ROOT/out"
