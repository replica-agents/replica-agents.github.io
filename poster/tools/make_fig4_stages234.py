#!/usr/bin/env python3
"""
Vector rebuild of Fig. 4, stages 2-4.

Each viewBox matches the corresponding panel's pixel box in
static/images/replica-agents-maindiag-final.png so the outputs can be
overlaid 1:1 on crops of the original.

  stage 2  1176 x 1350      stage 3  691 x 1350      stage 4  1120 x 1350

Strings follow the original, with four of its typographic errors corrected at
the author's request (2026-08-21):
  "Tags. CSS"                     -> "Tags, CSS"     (all five stage-2 boxes)
  "(A .list)"                     -> "(A_list)"      (stage 2, List-Agent)
  "Evaluates Textual Continuity <" -> trailing "<" dropped (stage 3, 3B);
                                     the "<" was a truncated string, not content
  "Sementic"                      -> "Semantic"      (stage 1, see make_fig4_stage1.py)
Sub-HTML fragment and auxiliary-context subscripts read as H_v / C_v,
confirmed against the paper's own notation for v in T_layout.

Label sizes are auto-fitted to their containers, so nothing overruns a card.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from fig4_lib import (PANEL, defs, defs_blue, text, lines, sub, badge, card,
                      whitebox, polyline, tool_icon, agent_icon, brain_agent_icon,
                      html_doc_icon, browser_icon, loop_arrow,
                      ftext, flines, fsub)

OUT = pathlib.Path(__file__).resolve().parents[1] / 'assets' / 'figures'


def head(W, H, pal, hx, hw, t1, t2, s1=54, s2=50):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
            f'width="{W}" height="{H}">',
            defs().replace('</defs>', defs_blue() + '</defs>'),
            f'<rect x="6" y="6" width="{W-12}" height="{H-12}" rx="34" '
            f'fill="{pal["fill"]}" stroke="{pal["edge"]}" stroke-width="7"/>',
            f'<rect x="{hx}" y="34" width="{hw}" height="168" rx="34" fill="{pal["head"]}"/>',
            ftext(hx + hw / 2, 108, t1, hw - 60, s1, '700'),
            ftext(hx + hw / 2, 172, t2, hw - 60, s2, '400')]


# ---------------------------------------------------------------- stage 2
def stage2():
    W, H = 1176, 1350
    P = PANEL['loc']
    o = head(W, H, P, 24, W - 48, 'Stage 2: Localise:', 'Layout-Aware HTML Generation')

    # router agent, and the trunk line that runs right through the panel
    o.append(polyline([(-70, 358), (446, 358)]))
    o.append(polyline([(560, 358), (W + 46, 358)], head=False))
    o.append(badge(432, 268, '2A', P['badge'], 52, 50))
    o.append(agent_icon(548, 354, 0.96))
    o.append(ftext(560, 470, 'Router Agent', 340, 48, '700'))
    o.append(fsub(560, 524, '(Routing Policy π, A', 'route)', 420, 42, '400'))

    names = [('Text-Agent', 'text'), ('Table-Agent', 'table'), ('Image-Agent', 'img'),
             ('Form-Agent', 'form'), ('List-Agent', 'list')]
    cx = [140, 372, 604, 836, 1064]
    cw, inner = 210, 194

    o.append(polyline([(560, 532), (560, 566)], head=False))
    o.append(polyline([(cx[0], 566), (cx[-1], 566)], head=False))
    for x in cx:
        o.append(polyline([(x, 566), (x, 594)]))

    for x, (nm, sfx) in zip(cx, names):
        o.append(card(x - cw / 2, 598, cw, 254, P, 24))
        o.append(agent_icon(x, 662, 0.58))
        o.append(ftext(x, 770, nm, inner, 36, '700'))
        o.append(fsub(x, 822, '(A', sfx + ')', inner, 34, '400'))
        o.append(polyline([(x, 852), (x, 888)]))
        o.append(whitebox(x - cw / 2, 892, cw, 232, 24))
        o.append(ftext(x, 936, 'Sub-HTML', inner, 32, '700'))
        o.append(fsub(x, 976, 'Fragment (H', 'v)', inner, 32, '700'))
        o.append(flines(x, 1024, ['(Tags, CSS,', 'Spatial Data,'], inner, 30, '400', 1.18))
        o.append(fsub(x, 1098, 'Aux. Context C', 'v)', inner, 30, '400'))
        o.append(polyline([(x, 1124), (x, 1158)], head=False))

    o.append(badge(34, 604, '2B', P['badge'], 52, 50))

    # collection bus
    o.append(polyline([(cx[0], 1158), (cx[-1], 1158)], head=False))
    o.append(polyline([(604, 1158), (604, 1196)]))
    o.append(whitebox(238, 1200, 736, 98, 26))
    o.append(ftext(606, 1264, 'Collection of Sub-HTML Fragments', 700, 46, '700'))
    o.append(flines(112, 1184, ['Auxiliary', 'Context'], 190, 37, '700', 1.14))
    o.append(flines(112, 1278, ['(OCR,', 'Attributes)'], 190, 34, '400', 1.14))
    o.append(polyline([(190, 1246), (232, 1246)]))
    o.append(polyline([(974, 1248), (W + 46, 1248)], head=False))
    o.append(badge(604, 1330, '2C', P['badge'], 48, 46))
    o.append('</svg>')
    return W, H, '\n'.join(o)


# ---------------------------------------------------------------- stage 3
def stage3():
    W, H = 691, 1350
    P = PANEL['asm']
    o = head(W, H, P, 18, W - 36, 'Stage 3: Assemble:',
             'Position- & Reading-Aware Merge', 48, 44)

    # 3B reading-order agent
    o.append(card(92, 278, 552, 226, P, 26))
    o.append(brain_agent_icon(180, 390, 0.94))
    o.append(ftext(452, 334, 'Reading-Order', 330, 44, '700'))
    o.append(fsub(452, 384, 'Agent (A', 'ro)', 330, 44, '700'))
    o.append(ftext(452, 428, 'Contextual Coherence &', 340, 34, '700'))
    o.append(ftext(452, 468, 'Evaluates Textual Continuity', 340, 34, '700'))
    o.append(badge(68, 286, '3B', P['badge'], 52, 50))

    # incoming from stage 2, and the merge <-> reading-order loop
    o.append(polyline([(-46, 358), (48, 358), (48, 566), (124, 566)], head=False))
    o.append(polyline([(214, 590), (214, 512)]))
    o.append(polyline([(316, 512), (316, 590)]))

    # 3A position-aware merge
    o.append(card(92, 594, 288, 352, P, 26))
    o.append(tool_icon(250, 688, 1.20))
    o.append(flines(236, 818, ['Position-Aware', 'Merge'], 262, 42, '700', 1.16))
    o.append(fsub(236, 916, '(Tool, T', 'pos)', 262, 40, '400'))
    o.append(badge(120, 654, '3A', P['badge'], 52, 50))

    # initial HTML document
    o.append(polyline([(384, 720), (444, 720)]))
    o.append(html_doc_icon(548, 706, 150, 194))
    o.append(flines(548, 846, ['Initial HTML', 'Document'], 250, 42, '700', 1.16))
    o.append(ftext(548, 948, '(H)', 250, 40, '700'))

    # the collection of fragments arriving from stage 2, from below
    o.append(polyline([(-46, 1248), (214, 1248), (214, 960)]))
    o.append('</svg>')
    return W, H, '\n'.join(o)


# ---------------------------------------------------------------- stage 4
def stage4():
    W, H = 1120, 1350
    P = PANEL['ref']
    o = head(W, H, P, 44, W - 88, 'Stage 4: Refine:', 'Visual Fidelity Enhancements')

    # 4A font-size optimisation
    o.append(card(52, 296, 224, 344, P, 26))
    o.append(tool_icon(164, 388, 1.06))
    o.append(flines(164, 512, ['Font-Size', 'Optimization'], 208, 42, '700', 1.16))
    o.append(fsub(164, 604, '(Tool, T', 'font)', 208, 40, '400'))
    o.append(badge(48, 302, '4A', P['badge'], 50, 48))

    # 4B background restoration
    o.append(card(52, 800, 224, 344, P, 26))
    o.append(tool_icon(164, 890, 1.06))
    o.append(flines(164, 1014, ['Background', 'Restoration'], 208, 42, '700', 1.16))
    o.append(fsub(164, 1108, '(Tool, T', 'bg)', 208, 40, '400'))
    o.append(badge(48, 806, '4B', P['badge'], 50, 48))

    # both tools feed the reflection agent
    o.append(polyline([(280, 468), (322, 468), (322, 700)], head=False))
    o.append(polyline([(280, 972), (322, 972), (322, 700)], head=False))
    o.append(polyline([(322, 700), (374, 700)]))

    # 4C reflection agent + visual alignment loop
    o.append(card(384, 396, 340, 748, P, 30))
    o.append(agent_icon(554, 516, 1.04))
    o.append(ftext(554, 668, 'Reflection Agent', 310, 44, '700'))
    o.append(fsub(554, 716, '(Iterative Verification, A', 'ref)', 316, 38, '400'))
    o.append(badge(408, 432, '4C', P['badge'], 50, 48))
    o.append(html_doc_icon(458, 806, 98, 130, 'HTML'))
    o.append(browser_icon(640, 806, 136, 116))
    o.append(loop_arrow('M514,774 q34,-26 62,-4'))
    o.append(loop_arrow('M676,870 q26,50 -22,80'))
    o.append(loop_arrow('M458,968 q-46,-40 -12,-86'))
    o.append(ftext(560, 942, 'VLM', 200, 46, '700'))
    o.append(flines(560, 1000, ['Visual', 'Alignment Loop'], 300, 42, '400', 1.16))

    # final output
    o.append(polyline([(728, 700), (778, 700)]))
    o.append(browser_icon(940, 640, 296, 232))
    o.append(flines(940, 826, ['High-Fidelity', 'Final HTML', 'Document'], 290, 46, '700', 1.16))
    o.append('</svg>')
    return W, H, '\n'.join(o)


if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    for n, fn in ((2, stage2), (3, stage3), (4, stage4)):
        w, h, svg = fn()
        (OUT / f'fig4-stage{n}.svg').write_text(svg, encoding='utf-8')
        print(f'wrote fig4-stage{n}.svg  ({w}x{h} viewBox)')
