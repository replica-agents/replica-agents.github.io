#!/usr/bin/env bash
# Measure the print build inside the same headless Chrome that renders the PDF.
# The preview pane cannot be used: it renders a scaled snapshot, so the fixed-mm
# layout is not honoured there.
set -uo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
TMP="$ROOT/poster/_measure.html"

python3 - "$ROOT" <<'PY'
import sys, pathlib
root = pathlib.Path(sys.argv[1])
html = (root/'poster'/'index.html').read_text()
html = html.replace('</body>', '<script src="tools/measure.js"></script></body>')
(root/'poster'/'_measure.html').write_text(html)
PY

# The measurement waits on document.fonts.ready, so it lands after --dump-dom
# occasionally. Retry rather than emit a truncated result.
for attempt in 1 2 3 4; do
  OUT="$("$CHROME" --headless --disable-gpu --hide-scrollbars \
        --run-all-compositor-stages-before-draw \
        --virtual-time-budget=25000 --window-size=3178,4493 \
        --dump-dom "file://$TMP" 2>/dev/null \
    | python3 -c "
import sys, re, html
d = sys.stdin.read()
m = re.search(r'<pre id=\"MEASURE\">(.*?)</pre>', d, re.S)
print(html.unescape(m.group(1)) if m else '')
")"
  if [ -n "$(printf '%s' "$OUT" | tr -d '[:space:]')" ]; then
    printf '%s\n' "$OUT"
    rm -f "$TMP"
    exit 0
  fi
done
rm -f "$TMP"
echo "MEASURE BLOCK NOT FOUND after 4 attempts" >&2
exit 1
