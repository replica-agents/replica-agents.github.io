# REPLICA ICDAR 2026 poster — asset inventory (pass 0)

**Status: inventory only. No poster code written. Waiting on your review of §B before the plan pass.**

Scope of what I touched: I created `poster/` and **copied** files into `poster/assets/`. No file
outside `poster/` was created, renamed, moved, edited or deleted. `git status` confirms the only
modified tracked files are the two `.DS_Store` entries that were already dirty before I started.
`slides.html` and `index.html` are byte-identical to how I found them.

---

## 0. What the repo actually contains

135 image assets, 133 of them under `static/images/`. Tooling available on this machine:
PyMuPDF, Pillow, `qrcode`, and Google Chrome (headless). **No** draw.io CLI, Inkscape, ImageMagick,
poppler, or Node. There are **no `.drawio` files, no LaTeX source, and no `figures/` submission
directory** anywhere in the repo or in git history — I checked all branches.

Three PDFs and one SVG looked like vector sources. Only one of them actually is:

| File | Verdict | What it really is |
|---|---|---|
| `static/images/fidhtml_diag_horizontal.pdf` | **Real vector** | Fig. 3. Verified at 6× zoom — glyph outlines, crisp at any scale. Only the two small bar charts inside the left-hand document are embedded rasters (1107×883, 855×808). |
| `static/images/Teaser_v2.pdf` / `.svg` | **Hybrid, mostly raster** | Fig. 1. The browser chrome, labels and leader lines are vector. The five page renders **and the radar plot** are embedded rasters. See §C1. |
| `static/images/replica-agents-maindiag-final.pdf` | **Not vector** | Fig. 4. `get_text()` returns 0 characters — every label is a separate tiny embedded PNG (105×32, 41×24, 182×27 …). It is a raster montage in a PDF wrapper. |

---

## A. Mapping table — every §6 slot

Effective dpi below is **not** the naive `pixels / placed size`. For every raster I ran a
downscale→upscale round-trip and found the scale at which detail stops changing; the "Eff. px"
column is the real information content, and Effective dpi is computed from that. Where the two
differ, the file has been upscaled or soft-exported and the nominal number is a lie.

| Slot | Repo path found | Format | Actual px | Eff. px | Placed mm | Eff. dpi | Verdict | Notes |
|---|---|---|---|---|---|---|---|---|
| `hero-source.png` | `static/images/demo/newspaper/S1_raw.png` | PNG RGB | 2136×3515 | 2136 | 120 w | 452 | **PRINT-OK** | Telugu newspaper, `manatelangana.news`. Clean, no annotation, no chrome. Deck label: "Raw document (image or PDF)". |
| `hero-render.png` | `static/images/demo/newspaper/S4_final.png` | PNG RGBA | 4272×7030 | 4272 | 120 w | 904 | **PRINT-OK** | Exactly 2× the source, identical aspect. Deck label: "High-fidelity final HTML (output)". **No browser chrome baked in** — good, the poster draws its own. |
| `hero-boxes.png` | `static/images/demo/newspaper/S1_tree.png` | PNG RGBA | 2136×3515 | 2136 | 120 w | 452 | **PRINT-OK** | Pixel-aligned to the source. Caveat in §C2 — these are filled translucent tints, not outlined boxes, and there are no SoM numerals. |
| `fig1a-replica.png` | `static/images/teaser/13031_rendered.png` | PNG RGBA | 3843×5086 | 3843 | 104 w | 939 | **PRINT-OK** | Page render only. Chrome + TE/LS/PS/VF chips are vector in `Teaser_v2.pdf`; poster re-sets them per §6. |
| `fig1a-gpt5.png` | `static/images/teaser/13031_rendered_gpt5.png` | PNG RGBA | 2545×3400 | 2545 | 104 w | 622 | **PRINT-OK** | Visible failure at 1 m: body text far too small, heading colour lost. |
| `fig1a-qwen.png` | `static/images/teaser/13031_rendered_qwen.png` | PNG RGBA | 3118×5439 | 3118 | 104 w | 762 | **PRINT-OK** | Aspect is 0.573, not 3:4 — the page **overflows**, which *is* the failure. Do not crop it to match the others. |
| `fig1a-marker.png` | `static/images/teaser/13031_rendered_marker.png` | PNG RGBA | 2173×2792 | 2173 | 104 w | 531 | **PRINT-OK** | Fully linearised to one column. The clearest annotatable failure of the four. |
| *(bonus)* `fig1a-source.png` | `static/images/teaser/base_doc.png` | PNG RGB | 1570×2065 | 1570 | 104 w | 383 | **PRINT-OK** | The Fig. 1A input page. Not in your §6 manifest but you need it to make the strip read. |
| `fig1b-radar.svg` | `static/images/teaser/image-2.png` | PNG RGBA | 512×582 | 512 | 90 w | **144** | **REJECT** | See §C1. It is a raster in the PDF too. Copied as `fig1b-radar__REJECT_512px.png` for reference only. |
| `fig3-input.png` | `static/images/fidhtml_diag_horizontal.pdf` p1 | **SVG** | — | — | 150 w | — | **VECTOR** | Re-exported by me → `fig3-input.svg` (clip 0,20→630,620). Baked "Input Document" caption excluded so the poster sets its own type. |
| `fig3-fidhtml.png` | `static/images/fidhtml_diag_horizontal.pdf` p1 | **SVG** | — | — | 150 w | — | **VECTOR** | Re-exported → `fig3-fidhtml.svg` (clip 630,0→1860,660). Includes all six ①–⑥ callouts. Verified by rendering at 1740×990 in Chrome. |
| `fig4-stage1.svg` | `static/images/stages/stage1.png` | PNG RGB | 839×766 | 671 | 190 w | **90** | **REJECT — vector required** | See §C3. |
| `fig4-stage2.svg` | `static/images/stages/stage2.png` | PNG RGB | 672×787 | 537 | 190 w | **72** | **REJECT — vector required** | |
| `fig4-stage3.svg` | `static/images/stages/stage3.png` | PNG RGB | 389×754 | 311 | 190 w | **42** | **REJECT — vector required** | Also clipped at its right edge. |
| `fig4-stage4.svg` | `static/images/stages/stage4.png` | PNG RGB | 636×754 | 508 | 190 w | **68** | **REJECT — vector required** | |
| `fig2-app-a.png` | `static/images/downstream/app_A_translation.png` | PNG RGBA | 1432×984 | 1432 | 75 w | 485 | **PRINT-OK** | Layout-Preserving Translation. |
| `fig2-app-b.png` | `static/images/downstream/app_B_preservation.png` | PNG RGBA | 1480×1160 | 1480 | 75 w | 501 | **PRINT-OK** | Document Preservation. |
| `fig2-app-c.png` | `static/images/downstream/app_C_indexing.png` | PNG RGBA | 1632×1120 | 1632 | 75 w | 553 | **PRINT-OK** | Indexing & Searchability. |
| `fig2-app-d.png` | `static/images/downstream/app_D_grounded.png` | PNG RGBA | 3302×1423 | 3302 | 75 w | 1118 | **PRINT-OK** | Grounded Document Intelligence. Aspect 2.32:1, not 4:3. |
| `fig2-app-e.png` | `static/images/downstream/app_E_chunking.png` | PNG RGBA | 1896×1456 | 1896 | 75 w | 642 | **PRINT-OK** | Semantic Chunking. Has baked labels + a ❌/✅ pair — see §C4. |
| `fig2-app-f.png` | `static/images/downstream/app_F_retrieval.png` | PNG RGBA | 4160×1496 | 4160 | 75 w | 1409 | **PRINT-OK** | Position-Aware Retrieval. Baked label + violet Ⓕ badge — see §C4. |
| *(bonus)* `fig2-full.png` | `static/images/applications.png` | PNG RGBA | 14250×5420 | 11400 | 380 w | 762 | **PRINT-OK** | The whole radial Fig. 2 including the central REPLICA→Fid-HTML flow, which the six tiles omit. |
| `qual-1.png` (source half) | `static/images/demo/newspaper/S1_raw.png` | PNG RGB | 2136×3515 | 2136 | 125 w | 434 | **PRINT-OK** | Historic-style newspaper. Render half exists — as **live HTML**, not an image. See §B4. |
| `qual-2.png` (source half) | `static/images/qual/00000127.png` | PNG RGB | 2412×3526 | 2412 | 125 w | 490 | **PRINT-OK** | Automotive magazine spread. Pairs with `00000127_corrected.html`. |
| `qual-3.png` (source half) | `static/images/qual/00000087.png` | PNG RGB | 2374×3254 | 2374 | 125 w | 482 | **PRINT-OK** | Tech magazine article. Pairs with `00000087_corrected.html`. |
| *(bonus)* `qual-factsoflife-src.png` | `static/images/qual/20005.png` | PNG RGBA | 3372×4880 | 1686 | 125 w | 343 | **PRINT-OK** | Note: soft, real detail is ~1686 px. Still fine at 125 mm. |
| `assets/logos/icdar26.png` | *(official file not in repo)* | — | — | — | 110 w | — | **MISSING** | The repo's `icdar_logo.png` is 366×138 → **85 dpi, REJECT**. See §B1. |
| *(alternative)* ICDAR logo | `Thesis Slides Sreevatsa.pptx` → `image29.png` | PNG | 2048×773 | 1638 | 110 w | 378 | **PRINT-OK** | Copied as `icdar26-vienna-2048.png`. Same Vienna 2026 lockup, 5.6× larger. Usable if the official download is a problem. |
| `assets/logos/bharatgen.png` | `static/images/logos/bgen_logo.png` | PNG P | 457×110 | 457 | 60 w | **193** | **REJECT** | Has the strapline "GenAI for Bharat, by Bharat" in it — fine text, so MARGINAL is not available. |
| `assets/logos/iiith.png` | `static/images/logos/iiith_logo.jpeg` | **JPEG** | 313×161 | 313 | 45 w | **177** | **REJECT** | JPEG artefacts on a logo, baked white background, and it contains three lines of small type. |
| *(QR codes)* | `static/images/qr_projectpage.png` 330×330 | PNG | — | — | 45 | — | n/a | Ignore it — §7 says generate locally at error-correction H. `qrcode` is installed, so this is a non-issue. |

**Summary: 19 slots PRINT-OK, 2 VECTOR, 7 REJECT, 1 MISSING.**

### Preliminary colour samples (from §3 — sample, don't guess)

Sampled off `replica-agents-maindiag-final.png` and `applications.png`:

| Token | Sampled | Source |
|---|---|---|
| `--seg` panel fill | `#DCE8F0` | Fig. 4 Stage 1 band |
| `--loc` panel fill | `#C0D8A4` | Fig. 4 Stage 2 band |
| `--asm` panel fill | `#EEDB83` | Fig. 4 Stage 3 band |
| `--ref` panel fill | `#EAC09C` | Fig. 4 Stage 4 band |
| `--seg` accent | ~`#546D87` | most-saturated recurring in Stage 1 |
| `--loc` accent | ~`#669750` | Stage 2 |
| `--ref` accent | ~`#C7793A` | Stage 4 |
| `--mark` violet | `#7F00FF` | Fig. 2 SoM badges A–F |

Two warnings. **These accents were sampled off a blurred upscale**, so they are approximate — a
vector Fig. 4 would also fix the palette. And `#7F00FF` is a fully-saturated electric violet that
sits right on the edge your §2 anti-brief warns about; I'd desaturate it for print and will propose
a specific value in `POSTER_PLAN.md`.

---

## B. Re-export list — what I need from you, in priority order

### B1. Fig. 4, the pipeline — the one that actually blocks the poster
**This is the only item that stops the centrepiece band from being built.**

Every version of Fig. 4 in existence here is a raster, and they are all soft:

| Candidate | Native | Effective | dpi @ 785 mm | dpi for one stage @ 190 mm |
|---|---|---|---|---|
| `replica-agents-maindiag-final.png` | 4682×1478 | 3121 | 101 | 104 |
| paper PDF p6 embedded image | 2810×888 | 2248 | 73 | 75 |
| `replica_maindiag.png` | 2600×820 | 2080 | 67 | 69 |
| `stages/stage1–4.png` | ≤839 wide | ≤671 | — | 42–90 |

`replica-agents-maindiag-final.png` is a **1.8× upscale** — I compared 200 % crops against the
2600 px version and against a 4682 px render of the PDF, and all three have the same blur halo
around the letterforms with no additional detail in the larger one. Your §4 hard rule applies and
it is also just true: **all four stage slots are REJECT — vector required.**

**What I need:** the original editable file for Fig. 4 — the PowerPoint, Illustrator, draw.io or
Figma document it was authored in. It is not in this repo. I checked `Thesis Slides Sreevatsa.pptx`
too: it contains the diagram only as `image27.png`, 2048×647, i.e. worse than what we already have,
and its media folder has no EMF/WMF/SVG at all.

- **Format:** SVG per stage — `fig4-stage1.svg` … `fig4-stage4.svg`, transparent background.
- **If only a single combined export is possible:** one SVG of the whole diagram is fine, I'll split it.
- **If no vector source exists at all:** say so and I will rebuild all four stage panels from
  scratch in HTML/CSS from the §5 sub-step table. That is genuinely the better outcome — your §6
  already asks me to re-set every label in poster type, and it gets you the agent-vs-tool
  shape distinction that the current figure does not make. It costs me a few hours, not a day.

### B2. Fig. 1B, the radar plot
Only a **512×582 PNG** exists. It is embedded as a raster inside `Teaser_v2.pdf` at a placed size of
3832×4356 pt — a 7.5× blow-up — and `Teaser_v2.svg` contains the identical 512 px bitmap. There is
no vector version anywhere.

**What I need:** the plotting script's output re-saved as PDF or SVG (matplotlib: `savefig('radar.pdf')`).

I deliberately did **not** regenerate it from Table 2. The radar's axes are TE/LS/PS/VF, and §9
gives me WRR/CRR/NTED/LPS/GPS/VFS — deriving TE from `mean(WRR,CRR)` or LS from `1−NTED` would be
interpolation, which §9 forbids. **If you'd rather I rebuild the radar as vector, send me the four
TE/LS/PS/VF values per method and I'll plot it directly.**

### B3. Logos
All three institutional logos are below 200 dpi at any sane placed size, and all three contain fine
type that rules out a MARGINAL pass.

- **ICDAR:** `https://icdar2026.org/wp-content/uploads/2025/08/icdar26-logo-transparent.png` — your
  §1 says download it. I have not fetched anything from the network in this pass. Say the word and
  I'll pull it into `poster/assets/logos/`. Fallback already staged: `icdar26-vienna-2048.png`
  (2048×773, 378 dpi at 110 mm), lifted from your thesis deck.
- **BharatGen:** need ≥ 1200 px wide, SVG preferred, transparent.
- **IIIT Hyderabad:** need ≥ 900 px wide, SVG preferred, transparent. The current file is a **JPEG** — a
  lossy logo with a baked white box, which will show as a hard white slab on the cool screen ground.

### B4. Source/render pairs for the hero seam — decision, not a re-export
`static/images/qual/` holds ten source PNGs **and their Fid-HTML reconstructions as live `.html`
files** (`00000087_corrected.html`, `IndicDLP_1_corrected.html`, …). Chrome is installed here, so I
can render any of them headlessly at whatever resolution I want — output that is effectively
vector-quality rather than a re-scaled screenshot. That is strictly better than any PNG pair.

**Confirm you want me to do this** and I'll generate the render halves myself; it needs no work from you.

### B5. Two missing files in the deck (not poster-blocking)
Listed here because you'd want to know, not because I need them. See §D.

---

## C. Ambiguities and things I want you to look at

### C1. The radar plot is a raster hiding inside a vector file
Worth stating plainly because it is counter-intuitive: `Teaser_v2.pdf` renders beautifully and *is*
partly vector — chrome, labels, leader lines, and the TE/LS/PS/VF chip rows all have real paths. But
`page.get_image_rects()` shows the radar is `image-2.png`, 512×582, stretched across 3832×4356 pt.
It looks sharp in a 1400 px preview purely because at that size it happens to be near 1:1. Anyone
eyeballing the PDF would reasonably conclude the radar is vector. It isn't.

Related: the SVG's 21 embedded images are the 6 real rasters plus **15 emoji bitmaps at ~226 px** —
the ✓/✗ marks in the chip rows. The poster should set those as type, not import them.

### C2. `hero-boxes` is not quite what §6 asks for
`newspaper/S1_tree.png` is pixel-aligned to `S1_raw.png` and is the right asset, but:
- the regions are **filled translucent tints, not outlined boxes**, and the underlying page text is
  washed out beneath them;
- there are **no SoM numerals** on it — the SoM marks in the deck are drawn in the DOM, not baked in.

So it gives you region *geometry* but not the "detection boxes + SoM marks" look. Two options, your
call: (a) use it as-is as a tinted underlay and draw outlines + SoM badges in CSS on top — I'd need
no new assets; or (b) you export a version with 1-px outlines and numerals.

For reference on the intended look I copied two gov-document assets:
`seam-boxcrop-ref.png` (outlined boxes, correct style, but only a header strip) and
`seam-fragments-ref.png` (the stacked sub-HTML fragment cards). **Neither is directly usable** —
both have baked titles and white backgrounds. They are style references for the seam only.

### C3. `stages/stage1–4.png` are separate crops, not a cumulative build-up
I checked for the build-up trap you flagged: they are *not* additive reveals, they're four genuine
side-by-side crops. Unfortunately that doesn't help — they're crops of the already-soft master, at
389–839 px, with white slab backgrounds, and `stage3.png` is **clipped at its right edge** (the
outgoing arrow into Stage 4 is cut). Rejected on resolution regardless.

### C4. Baked-in labels on two Fig. 2 tiles
`fig2-app-e` has "Document / Chunking ❌ / Semantic Chunking ✅" baked into the pixels, and
`fig2-app-f` has "Position-Aware Document Retrieval" plus a violet Ⓕ badge baked in. Your §6 says to
crop tiles individually and set labels in poster type — these two will show **doubled labels** unless
I crop the baked text off. The crops are feasible (both tiles have room) but they change the aspect
ratios. Flagging rather than deciding.

Separately: the six tiles' aspect ratios run from 1.30:1 to 2.78:1, nowhere near the ~4:3 your
manifest assumes. A six-tile row of equal boxes will letterbox badly. `fig2-full.png` is staged as
an alternative — it also carries the central REPLICA → Fid-HTML flow that the individual tiles drop.

### C5. Which document should carry the hero seam
I picked the Telugu newspaper because it is the only document where the source, the box overlay and
the final render are all present, all high-resolution, and all in the same aspect. For completeness,
what I rejected:

- **gov** — `S1_tree.png` is a **pre-annotated slide variant**: it has "Nested Hierarchical Layout
  Tree" baked in as a caption and a different crop (1892×2756 vs the source's 1908×2552), so it does
  not overlay. `S4_final.png` also has browser chrome baked in.
- **magazine** — clean triple, but the source is only 900×1251. Too small.
- **financial** — a receipt at 936×2915. The aspect ratio would wreck the hero band.

If you'd rather the hero were an English-language document for an international audience, say so —
the magazine (Chinese) and gov (Hindi/English) options are both too low-resolution, so that would
become a new export request.

### C6. Fig. 3 exists twice and I'm using the better one
`Doc2Web-Pipeline-ExplainingFid-HTML.png` (5164×2082, RGBA, transparent, **orphaned**) is the same
Fig. 3 as a raster, without the baked captions. It's a decent asset, but the vector SVG I exported
beats it. Copied as `fig3-full-transparent.png` in case you want the raster.

Note the naming: "Doc2Web" is presumably the paper's former title. Harmless, but the poster must not
inherit it anywhere.

---

## D. Repo hygiene — reported only, nothing changed

**Two genuinely broken references in `slides.html`:**
- L775 → `static/images/vfdr_samples.png` — **does not exist.** It has an `onerror` handler that
  replaces it with a visible "VFDR-Bench samples figure not yet added" box, so **anyone presenting
  this deck today sees a placeholder on the VFDR-Bench slide.** Worth fixing before the talk. The
  poster's Band E needs this same figure, so it's a shared gap.
- L966 → `static/images/logos/cvit_logo.png` — **does not exist.** Fails silently
  (`onerror="this.style.display='none'"`), so the closing slide shows two logos where three were intended.

**One broken reference in `index.html`:** L10 → `static/images/favicon.png` doesn't exist. The
comment on L9 already admits it's a placeholder.

**`index_old.html` is entirely broken** — all seven of its image paths are root-relative
(`bgen_logo.png`, `Teaser_v2.png`, `applications.png` …) but the assets live under `static/images/`.
It's a legacy file and nothing links to it. `Teaser_v2.png` doesn't exist in any location.

**50 orphaned assets, ~14 MB.** The bulk is 48 files under `static/images/demo/*/` —
`S1_analyzer`, `S1_detect`, `S1_labeling`, `S1_grouping`, `S1_digital`, `S1_pdfobjects`,
`S2_collection`, `S2_specialists`, `S4_bg`, `S4_font`, `S4_reflection` — each **byte-identical
across all four document folders** (verified by MD5) and referenced nowhere. The deck draws those
sub-stage panels in the DOM instead. Also orphaned: the three vector-ish PDFs, `Teaser_v2.svg`, and
`Doc2Web-Pipeline-ExplainingFid-HTML.png`. The PDFs and SVG are your only real figure sources —
**don't delete those** even though nothing references them.

**Redundant duplicates that are referenced:** `replica-agents-maindiag-final.png` exists identically
at the repo root and under `static/images/` (7.5 MB each). Within each demo folder,
`S1_raw` = `S3_reading` = `thumb` = the named original are all the same bytes (3–4 copies of a file
up to 8 MB), and `S3_final` = `S4_initial`. Roughly 40 MB of exact duplication. All of it is load-bearing
for the deck as currently written — I mention it only as cleanup you might want later.

**One thing that surprised me:** `S3_reading.png` is byte-identical to the raw page in every folder.
It is *not* a reading-order-annotated image; the arrows are drawn in the DOM. If you ever wanted a
static reading-order figure for the poster, it does not exist and would need generating.

---

## E. What is staged in `poster/` right now

```
poster/assets/figures/
  hero-source.png  hero-render.png  hero-boxes.png          ← the seam triple, PRINT-OK
  fig1a-{replica,gpt5,qwen,marker,source}.png               ← PRINT-OK
  fig1b-radar__REJECT_512px.png                             ← reference only, do not place
  fig3-{full,input,fidhtml}.svg                             ← VECTOR, re-exported by me
  fig3-full-transparent.png                                 ← raster alternative
  fig4-full__REJECT_paperraster_2810px.png                  ← best Fig. 4 in existence, still REJECT
  fig2-app-{a..f}.png  fig2-full.png                        ← PRINT-OK
  qual-{newspaper,magazine,financial,factsoflife}-src.png   ← source halves; renders need §B4
  seam-{boxcrop,fragments}-ref.png                          ← style references, not placeable
poster/assets/logos/
  icdar26-vienna.png (REJECT)  icdar26-vienna-2048.png (PRINT-OK)
  bharatgen.png (REJECT)  iiith.jpeg (REJECT)
poster/_slotcalc.json                                       ← machine-readable dpi audit
```

Files marked REJECT are kept deliberately, with the verdict in the filename, so they cannot be
placed by accident.

---

## Stopping here

The four things I need from you, shortest first:

1. **Fig. 4 vector source — or permission to rebuild all four stage panels from scratch.** This is the blocker.
2. **Fig. 1B radar as PDF/SVG — or the four TE/LS/PS/VF values per method** so I can plot it.
3. **Higher-resolution BharatGen and IIIT-H logos**, and a yes/no on fetching the official ICDAR logo over the network.
4. **Confirm I should render the `qual/*_corrected.html` files myself** for the source/render pairs.

Answer those and I'll write `POSTER_PLAN.md`. I have not started the plan pass.

---

# Addendum — 2026-08-21, after author input

## Resolved

**B2 Fig. 1B radar — DONE, now vector.** Built from the values you supplied via
`poster/tools/make_radar.py` → `fig1b-radar.svg` (labelled) and `fig1b-radar-plot.svg`
(geometry only, for the poster to label in its own type). Every series polygon matches the
original 512 px raster's geometry exactly. Axis order read as `[TE, LS, PS, VF]`, plotted
TE right / LS top / PS left / VF bottom to match the original orientation.
**Placement constraint: ≥ 170 mm wide**, below which the legend drops under the 24 pt floor.

*One thing to check, not a blocker:* for REPLICA and Marker your TE values equal
`mean(WRR, CRR)` from Table 2 (90 ≈ mean(.88,.93); 75 = mean(.68,.82)), and LS/PS/VF match
`1−NTED` / `mean(GPS,LPS)` / `VFS` for all four methods. But GPT-5's TE is 82 where Table 2
implies 72, and Qwen3-VL's is 68 where Table 2 implies 72.5. I used your numbers verbatim.
Flagging only because the poster shows the radar and Table 2 side by side.

**B4 Fid-HTML render halves — DONE.** `poster/tools/render_qual.py` renders all eleven
`qual/*.html` reconstructions through headless Chrome at a scale chosen to clear ~1800 px on
the long edge. All eleven succeeded; spot-checked four against their sources and the
reconstructions are near-indistinguishable. Best pairs for the §6 `qual-1/2/3` slots:
the Cadillac magazine spread, the historic newspaper, and the PREMIO tax invoice.

**cvit_logo.png — received, deck reference now resolves.** 160×55, RGBA. That is **90 dpi at
45 mm**, so it fixes the slide deck but is **REJECT** for the poster footer. Copied as
`poster/assets/logos/cvit.png`. If CVIT should appear on the poster I need a bigger file;
if the footer only needs BharatGen + IIIT-H per §5, ignore this.

## Fig. 4 — proof built, one decision left

`poster/tools/make_fig4_stage1.py` + `fig4_lib.py` produce `fig4-stage1.svg`, a full vector
rebuild of the Segment panel. Colours were sampled at full resolution off the original
(`#D9E6EE` panel, `#B9CCDF` header, `#4A6BA5` badges, `#B01F1E` for 1A, `#37507F` for 1B —
note the original's own badge palette is inconsistent). Structure, connectors, badges and
every label string are reproduced exactly, including the original's `Sementic` typo, which
I left as-is pending your call.

**What I cannot reproduce exactly: the icons.** The wrench-and-gear "Tool" glyph and the
robot "Agent" glyph are clipart rasters whose best available resolution is ~67×65 px
(≈63 dpi at poster size). There is no vector original anywhere in the repo, the paper PDF,
or the thesis deck. Mine are redrawn vector equivalents — same silhouette, proportion and
palette, visibly the same character, but not pixel-identical.

## New finding: what the Fig. 4 PDF actually contains

`replica-agents-maindiag-final.pdf` is not one diagram. It is **five stacked versions** —
four superseded drafts sitting underneath the current figure, each a full rasterised copy at
1101–1376 px. That is why the file is 5.6 MB and carries 25 embedded images.

The drafts are visibly older: they say *Layout Detection Ensemble (Tool, T_det)*,
*Assemble-Agent (Position-Aware Merge, A_pos)* and *Reading-Order Computation (Tool, T_ro)*
where the current version says *Geometric Proposal Generation*, *Position-Aware Merge (Tool,
T_pos)* and *Reading-Order Agent (A_ro)*.

Every draft also carries a baked-in title reading the literal unrendered LaTeX
`\textsc{REPLICA}: Agentic Framework for High-Fidelity Document-to-Web Conversion`.
**This does not reach the published figure** — the PDF cropbox clips it, and I confirmed it is
absent from the paper's own p6 raster. No action needed; noted so nobody rediscovers it later.

---

# Addendum 2 — Fig. 4 rebuilt as vector

All four stages are rebuilt and composed. Files in `poster/assets/figures/`:

| File | What it is |
|---|---|
| `fig4-stage1.svg` … `fig4-stage4.svg` | One panel each. viewBoxes are 1517/1176/691/1120 × 1350 — the exact pixel boxes of the panels in the original, so each can be overlaid 1:1 for checking. |
| `fig4-full.svg` | The complete figure, viewBox 4682 × 1478, matching the original's pixel box. **55 KB**, versus 5.6 MB for the source PDF and 7.5 MB for the PNG. |
| `fig4-full-nochev.svg` | Same without the inter-stage chevrons, for a poster layout that draws its own continuous stage-to-stage connector (your §5). |
| `fig4-full-9272px.png` | Convenience raster at 300 dpi for a 785 mm placement, in case anything downstream can't take SVG. |

Generated by `poster/tools/fig4_lib.py` + `make_fig4_stage1.py` + `make_fig4_stages234.py`
+ `make_fig4_full.py`. Re-runnable; all geometry is in source, nothing hand-edited.

## Colour coding — sampled, not chosen

Every value below was read off `replica-agents-maindiag-final.png` at full resolution:
panel fills and header bands as the modal colour of a clean interior region, borders as the
darkest row of a clean bottom-edge strip, badges as the modal colour inside the disc, chevrons
read off magnified crops of the three inter-panel gaps.

| Stage | Panel fill | Header band | Border | Badge | Card | Chevron fill / stroke |
|---|---|---|---|---|---|---|
| 1 Segment | `#DBE7EF` | `#B9CCDE` | `#46617C` | `#4A6BA5` | `#E7F0F8` | `#C3D2E2` / `#6C8AAC` |
| 2 Localise | `#D9E7CB` | `#BED7A1` | `#6D9468` | `#689558` | `#E4EFD8` | `#C9DEB9` / `#7BA76B` |
| 3 Assemble | `#F5E8B2` | `#F0DC84` | `#C9A83F` | `#E9C136` | `#F7EDBE` | `#F0D97A` / `#CDA53E` |
| 4 Refine | `#F3E3CF` | `#EAC19F` | `#B4753F` | `#C67736` | `#F6E9DA` | `#F0CBA6` / `#C08A5C` |

Two badges break the stage scheme **in the original**, and I reproduced them rather than
"correcting" them: **1A is red `#B01F1E`** while every other Segment badge is blue, and
**1B is a darker navy `#37507F`** than 1C/1D/1E. Badge rings are the badge colour at 45 % luminance.

## Text — reproduced exactly, then four errors corrected on request

Every string is copied from the original. Four typographic errors it contained were then
**corrected at the author's request (2026-08-21)** and are no longer present in the rebuild:

| Original | Corrected | Where |
|---|---|---|
| `Sementic` | `Semantic` | Stage 1, Grouping Agent |
| `(Tags. CSS,` | `(Tags, CSS,` | Stage 2, all five fragment boxes |
| `(A .list)` | `(A_list)` — now matches `A_text` / `A_table` / `A_img` / `A_form` | Stage 2, List-Agent |
| `Evaluates Textual Continuity <` | trailing `<` dropped | Stage 3, 3B |

The trailing `<` was a truncated string in the original, not content. All four remain uncorrected
in the published paper — worth knowing for any camera-ready revision.

One ambiguity I resolved rather than guessed: the sub-HTML subscripts are unreadable in the
upscale. Zooming the paper's own cleaner raster resolves them as **H_v** and **C_v**, which
matches the paper's notation (`{H_v}` for `v ∈ T_layout`). The rebuild uses H_v / C_v consistently;
the original renders them inconsistently across the five columns, but that is blur, not intent.

## What is not identical

The **icons**. The wrench-and-gear Tool glyph, the Agent robot, the brain-headed Reading-Order
robot, the HTML page and the browser thumbnail are clipart in the original, available nowhere
above ~67 × 65 px. These are redrawn vector equivalents: same silhouette, proportion and palette,
recognisably the same characters, not pixel-identical. Everything else — geometry, colour, type,
connectors, badges — is reproduced.

Verified by overlaying the rebuild on the original at matched scale: panels, cards, badges,
buses and label positions line up element for element. At the real poster size (785 mm, 300 dpi)
the original is illegible and the rebuild is sharp.
