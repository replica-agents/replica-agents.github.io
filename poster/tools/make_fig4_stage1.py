#!/usr/bin/env python3
"""
Vector rebuild of Fig. 4, Stage 1 (Segment) -- fidelity proof.

viewBox is 1517 x 1350, matching the Stage 1 panel's pixel box in
static/images/replica-agents-maindiag-final.png, so the output can be
overlaid 1:1 on a crop of the original for comparison.

The original's "Sementic" is corrected to "Semantic" here, at the author's
request (2026-08-21). See make_fig4_stages234.py for the other three fixes.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from fig4_lib import (PANEL, BADGE_1A, BADGE_1B, INK, defs, text, lines, sub,
                      badge, polyline, tool_icon, agent_icon, doc_icon, tree_icon)

W, H = 1517, 1350
P = PANEL['seg']
o = []
o.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
         f'width="{W}" height="{H}">')
o.append(defs())

# panel + header pill
o.append(f'<rect x="6" y="6" width="{W-12}" height="{H-12}" rx="34" '
         f'fill="{P["fill"]}" stroke="{P["edge"]}" stroke-width="7"/>')
o.append(f'<rect x="586" y="34" width="{W-586-34}" height="168" rx="34" '
         f'fill="{P["head"]}"/>')
o.append(text(1030, 108, 'Stage 1: Segment:', 54, '700'))
o.append(text(1030, 172, 'Hierarchical Semantic Layout Detection', 50, '400'))

# input document
o.append(doc_icon(76, 46, 182, 262))
o.append(lines(400, 96, ['Input', 'Document', 'Image or', 'PDF (I)'], 48, '400', 1.20))
o.append(polyline([(167, 316), (167, 486)]))

# 1A  document-type analyser
o.append(tool_icon(176, 588, 1.20))
o.append(lines(178, 696, ['Document-Type', 'Analyzer'], 45, '700', 1.14))
o.append(sub(178, 794, '(Tool, T', 'type)', 43, '400'))
o.append(badge(176, 898, '1A', BADGE_1A, 56, 54))

# branch: analyser -> digital / scanned
o.append(polyline([(258, 592), (334, 592)], head=False))
o.append(polyline([(334, 470), (334, 916)], head=False))
o.append(polyline([(334, 470), (556, 470)]))
o.append(polyline([(334, 916), (512, 916)]))
o.append(text(430, 424, 'Digital', 46, '700'))
o.append(text(444, 528, '(δ=digital)', 44, '400'))
o.append(text(438, 992, 'Scanned', 46, '700'))
o.append(text(446, 1054, '(δ=scanned)', 44, '400'))

# 1E  digitally-born PDF extraction
o.append(tool_icon(658, 450, 1.12))
o.append(badge(778, 348, '1E', P['badge'], 52, 50))
o.append(lines(668, 560, ['Digitally-Born', 'PDF Extraction'], 45, '700', 1.14))
o.append(sub(668, 660, '(Tool, T', 'pet)', 43, '400'))
o.append(polyline([(742, 470), (972, 470)]))

# structured PDF objects
o.append(f'<rect x="984" y="330" width="234" height="322" rx="18" '
         f'fill="#E7F0F8" stroke="{P["edge"]}" stroke-width="5"/>')
o.append(lines(1101, 384, ['Structured', 'PDF', 'Objects'], 46, '700', 1.14))
o.append(lines(1101, 546, ['(Bboxes,', 'Content,', 'Metadata)'], 44, '400', 1.14))

# 1B  geometric proposal generation
o.append(tool_icon(600, 852, 1.02))
o.append(tool_icon(600, 1012, 1.02))
o.append(badge(540, 1168, '1B', BADGE_1B, 48, 46))
o.append(lines(696, 1148, ['Geometric', 'Proposal', 'Generation'], 40, '700', 1.13))
o.append(text(696, 1288, '(Tool)', 40, '400'))
o.append(polyline([(676, 856), (712, 856), (712, 1010), (676, 1010)], head=False))
o.append(polyline([(712, 933), (806, 933)]))

# 1C labeling agent
o.append(badge(806, 794, '1C', P['badge'], 50, 48))
o.append(agent_icon(892, 880, 1.02))
o.append(lines(892, 1004, ['Labeling', 'Agent'], 44, '700', 1.14))
o.append(lines(892, 1104, ['(SoM', 'Prompting,'], 38, '400', 1.14))
o.append(sub(892, 1192, 'A', 'lab)', 40, '700'))

# 1D grouping agent
o.append(polyline([(956, 880), (1046, 880)]))
o.append(badge(1028, 794, '1D', P['badge'], 50, 48))
o.append(agent_icon(1118, 880, 1.02))
o.append(lines(1118, 1004, ['Grouping', 'Agent'], 44, '700', 1.14))
o.append(lines(1112, 1104, ['(Spatial &', 'Semantic'], 37, '400', 1.14))
o.append(sub(1104, 1192, 'Reasoning, A', 'grp)', 37, '400'))

# feed into the layout tree
o.append(polyline([(1218, 492), (1262, 492), (1262, 736)], head=False))
o.append(polyline([(1186, 880), (1262, 880), (1262, 736)], head=False))
o.append(polyline([(1262, 736), (1300, 736)]))

# T_layout
o.append(tree_icon(1352, 726, 196, 184))
o.append(lines(1352, 930, ['Hierarchical', 'Layout Tree'], 41, '700', 1.14))
o.append(sub(1352, 1024, '(T', 'layout)', 39, '400'))
o.append(lines(1352, 1078, ['(Nodes:', 'Geometry,', 'Type, Hierarchy,', 'Order)'], 36, '400', 1.14))

# T_layout output: up and right, on into Stage 2's Router Agent.
# Runs past the panel edge; the composite relies on overflow:visible.
o.append(polyline([(1352, 630), (1352, 358), (1596, 358)], head=False))

o.append('</svg>')

out = pathlib.Path(__file__).resolve().parents[1] / 'assets' / 'figures'
out.mkdir(parents=True, exist_ok=True)
(out / 'fig4-stage1.svg').write_text('\n'.join(o), encoding='utf-8')
print(f'wrote fig4-stage1.svg  ({W}x{H} viewBox)')
