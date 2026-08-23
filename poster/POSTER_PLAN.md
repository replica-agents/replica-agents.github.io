# POSTER_PLAN.md — REPLICA, ICDAR 2026
### Pass 1. Nothing is built yet. Written before any HTML/CSS exists, per §0.

---

## 1. Decisions already locked by the author

| Question | Answer | Where it applies |
|---|---|---|
| Language / domain counts | **`15+ languages · 20+ document categories`** (the §5 benchmark description) | Band E only, once. Never restated. |
| ICDAR logo | Fetched from `icdar2026.org` with permission. 1600×604, real alpha, **369 dpi at 110 mm** | Band A |
| Institutional logos | Use what exists for now; hi-res coming from the other team | Footer — see §8 |
| Fig. 4 | Rebuilt as vector, colours sampled not chosen | See §6, Band D |
| Fig. 1B radar | Rebuilt as vector from author-supplied values | Band E |
| Fig. 4 typos | **All four corrected** (2026-08-21) | `fig4-full.svg` and Band D |
| QR codes | **Three**: Project page · Paper · Contact us | Band A |
| Overriding directive | **"very neat and clean"** — see §2.6 | Everywhere |

---

## 2. Token system

### 2.1 Palette — eight named values, all derived

Nothing here was picked off a colour wheel. The two grounds are sampled from the poster's own
subject matter; the four stage colours and the violet come off the paper's figures.

```css
--paper : #EDE4E1;  /* warm rag      — input / source document / the PDF world */
--screen: #EDF0F4;  /* cool screen   — output / Fid-HTML / the web world, and the poster ground */
--ink-p : #1E1815;  /* warm near-black, for type on --paper  */
--ink-s : #141A21;  /* blue-cast near-black, for type on --screen */
--seg   : #4A6BA5;  /* Stage 1 Segment  */
--loc   : #689558;  /* Stage 2 Localize */
--asm   : #C9A83F;  /* Stage 3 Assemble */
--ref   : #C67736;  /* Stage 4 Refine   */
--mark  : #6124BC;  /* SoM badges, the seam glow, "ours" highlight */

/* darkened "on-light" variants: used wherever a stage colour carries white
   type, or is itself set as type. The bright values above stay for rules and
   fills only. Derived by walking value down at constant hue/saturation until
   both contrast thresholds are met -- see the table below. */
--seg-d : #4A6AA5;
--loc-d : #527545;
--asm-d : #806B28;
--ref-d : #9C5E2A;
```

**`--paper #EDE4E1` — the justification §3 asks for.** The hero source document's own restored
paper stock samples as `#F2E5DC`: hue 25°, saturation 9.1 %. I pulled that down in chroma and
shifted it rosier, landing at hue 15°, saturation 5.1 %. That is **27° of hue away from the
`#F4F1EA` cream the anti-brief bans** (hue 42°, which reads yellow because its G−B gap is +7).
`--paper` inverts that relationship: R−G is +9 and G−B is only +3, so it reads as warm grey with
a rose cast rather than as cream. It is also darker, which keeps it from competing with the white
inside the document images that sit on it.

**`--screen #EDF0F4`.** The Segment panel fill from the paper's own Fig. 4 is `#DBE7EF`, hue 204°.
Lightened and calmed to hue 214°, saturation 2.9 %. So the poster's ground is literally the
paper's own "this is a detected region" blue, bleached — which is the right joke for a ground
that is conceptually Fid-HTML output.

**Stage colours** are the sampled badge colours from Fig. 4, listed with their full family in
`ASSET_INVENTORY.md` addendum 2. Used **only** on stage-related content: the Band D top rules and
badges, and the four SoM numerals. A metric card does not get to be green.

**`--mark #6124BC` — a deliberate deviation, flagged.** The paper's SoM violet samples as
`#7F00FF`: fully saturated, hue 270°, exactly the neon §1 and §2 tell me to avoid. `#6124BC` is
the same hue family (268°) — recognisably the paper's violet, but it will not fluoresce on a
press. It is also the *shallowest* darkening of that hue that clears the 7 : 1 body floor on
`--screen`, so it stays as close to the paper as the contrast rule permits. If you want the
literal `#7F00FF` instead, it is one token change — but it would fail §1's contrast requirement.

**Contrast — computed, not estimated.** Every value below is a real WCAG ratio against the actual
token hexes. Two of these forced changes to the palette rather than the other way round:

| Pair | Ratio | Requirement | |
|---|---|---|---|
| `--ink-s` on `--screen` | **15.32** | body ≥ 7 | ✓ |
| `--ink-p` on `--paper` | **14.03** | body ≥ 7 | ✓ |
| `--mark` on `--screen` | **7.39** | body ≥ 7 | ✓ |
| white on `--mark` | **8.44** | numeral ≥ 4.5 | ✓ |
| white on `--seg-d` / `--loc-d` / `--asm-d` / `--ref-d` | **5.39 / 5.26 / 5.18 / 5.19** | numeral ≥ 4.5 | ✓ |
| `--seg-d` / `--loc-d` / `--asm-d` / `--ref-d` on `--screen` | **4.72 / 4.61 / 4.53 / 4.54** | caption ≥ 4.5 | ✓ |
| `--asm` on `--screen` | **2.01** | — | **rules and fills only, never type** |
| `--loc` / `--ref` on `--screen` | **3.05 / 3.02** | — | **rules and fills only, never type** |

**Two findings that changed the palette.** My first draft used the bright sampled stage colours
everywhere, including as badge fills with white numerals. Computing the ratios killed that: white
on `--loc` is **3.48 : 1** and on `--ref` is **3.45 : 1**, both below even the 4.5 caption floor.
A reader at three metres would lose the ② and ④ numerals. Hence the `-d` variants — the bright
values keep the stage identity on rules and fills, the dark ones carry type. My first `--mark`
(`#6E2ED0`) measured **6.20 : 1**, which fails the body floor the thesis line has to meet; hence
the darkening to `#6124BC`.

`--asm` remains the trap in this palette. Amber on a light ground cannot carry text at any weight.
It is restricted to the Stage 3 top rule, the badge fill (with a dark ring, as in the original)
and the ablation bars — with `--asm-d` for any Stage 3 label that is set *in* the stage colour.

### 2.2 Typography — three faces, each with a job

The mapping is the poster's own argument, stated in a two-line footer legend:

| Role | Family | Why |
|---|---|---|
| **Serif = the document world (input)** | **Source Serif 4** | Transitional, real text authority at display size, open licence. Explicitly not Playfair. Title, source-document callouts, anything on `--paper`. |
| **Sans = the web world (output)** | **IBM Plex Sans** | Engineered, slightly technical, genuine 400/600 weight contrast rather than size alone. All body, heads, tables, anything on `--screen`. |
| **Mono = the representation itself** | **IBM Plex Mono** | HTML snippets, tag names, metric abbreviations, all table numerals. `font-variant-numeric: tabular-nums` on every table, no exceptions. |

Plex Sans and Plex Mono are a designed pair, which keeps the two "output" voices related while
the serif stays clearly foreign. All three are SIL OFL and ship as `.woff2`.

**Fetched and verified.** 16 `.woff2` files (latin, latin-ext, greek), 729 KB total, in
`poster/fonts/` with a generated `fonts.css`. No CDN reference remains. A render probe confirms
all three families load and none falls back to Times.

**One finding from that probe, and it is a trap.** Four characters the poster wants are *outside*
the downloaded subsets: **`→` `≤` `✓` `✗`** (and the circled numerals `①`…). On this Mac they
still render — because Chrome silently substituted a **system font**. That looks fine here and
would break on any other machine or in the embedded PDF. So: those four are **drawn as inline
SVG, never typed as characters.** The circled SoM numerals were always going to be CSS circles
with a white numeral, so they were never at risk. `↑ ↓ × π δ · —` *are* genuinely in the files
and verified rendering from them.

### 2.3 Type scale (A0)

| Role | Size | Face | ≈ height |
|---|---|---|---|
| Poster title | 102 pt | Serif 600 | 36 mm |
| Thesis line | 44 pt | Sans 400 | 15.5 mm |
| Authors | 33 pt | Sans 400 | 11.6 mm |
| Affiliations / footer | 26 pt | Sans 400 | 9.2 mm |
| Band eyebrow (caps, +0.12em tracking) | 24 pt | Mono 500 | 8.5 mm |
| Section heading | 54 pt | Sans 600 | 19 mm |
| Sub-heading | 37 pt | Sans 600 | 13 mm |
| Body | 30 pt | Sans 400 | 10.6 mm |
| Table body | 27 pt | Mono 400 tabular | 9.5 mm |
| Caption / label | 24 pt | Mono 400 | 8.5 mm |
| Hero stat numeral | 200 pt | Mono 500 tabular | 70 mm |

Body line-height 1.40. **Measure is enforced by column width, not by `max-width` guesses:** at
30 pt IBM Plex Sans the average advance is ≈ 0.50 em = 5.3 mm, so a 45-character line is 239 mm.
Four columns (253.7 mm) minus 14 mm of padding gives 239.7 mm — 45 characters, dead centre of the
35–55 band. **Every body column on this poster is 4 grid columns wide.** That is the rule, and it
is why Band E is three equal quarters rather than the brief's suggested split.

### 2.4 Grid

- Trim 841 × 1189 mm, safe margin 28 mm → **live area 785 × 1133 mm**
- 12 columns, 12 mm gutters → **column 54.42 mm**
- Spans: 4 col = 253.7 · 5 col = 320.1 · 7 col = 452.9 · 8 col = 519.3 · 12 col = 785.0
- Vertical rhythm: 8 mm base unit
- Band gap 16 mm, whitespace only, never a rule

### 2.6 "Very neat and clean" — what that actually constrains

Stated as a directive, so it needs to bind specific decisions rather than float as a mood:

- **One idea per band, one risk on the poster.** The seam is the risk. Nothing else competes.
- **Alignment is absolute.** Every element starts on a 12-column line and sits on the 8 mm
  rhythm. No optical nudges, no one-off offsets.
- **Whitespace does the separating.** 16 mm band gaps, corner brackets instead of boxes, and
  *zero* full rules on the poster except the seam and the four stage top-rules.
- **No effects.** No drop shadows, no gradients except the seam halo, no rounded "card" chrome,
  no tinted panels that are not carrying the two-substrate rule.
- **Three type sizes per band, maximum.** Heading, body, caption. If a band needs a fourth, the
  band is doing too much.
- **A hard cap of five colours visible in any one band** — the two grounds, ink, and at most two
  accents. Band D is the exception and is the reason the stage colours exist.

The practical test: at the squint stage (§10 item 14) the poster should read as six calm
horizontal blocks with one bright vertical seam. If it reads as busy, something above was broken.

### 2.5 The signature element

**One vertical reconstruction seam down Band B.** Left of it, the Telugu newspaper page sits on
`--paper` in its original state. Crossing it, the page decomposes into tinted detection regions, a
layout tree, and mono sub-HTML fragment chips. Right of it, it re-solidifies as the Fid-HTML
render on `--screen`, framed in minimal browser chrome. The seam is a 1 mm `--mark` rule with an
8 mm gradient halo either side; three fragments cross it, clipped so their left half is warm and
their right half is cool.

The assets for this are real and matched: `hero-source.png`, `hero-boxes.png` and
`hero-render.png` are the same page at 452 / 452 / 904 dpi, pixel-aligned, no baked chrome.

**Supporting motifs, used as structure and nothing else:** SoM badges as section numbering
(filled `--mark` circle, white numeral); corner brackets instead of boxes (four L-shaped crop
marks, never a 4-sided border); the layout-tree spine in the left gutter; a 0.03-alpha baseline
grid behind everything.

---

## 3. Band layout — heights re-derived, because the brief's do not fit

**The brief's band table sums to 1229 mm against a 1133 mm live area — a 96 mm overshoot.** §3
says to adjust and re-verify, so here is the corrected allocation. Every band is a multiple of the
8 mm rhythm; the footer takes the 13 mm remainder, which is exactly the brief's own footer figure.

```
┌─────────────────────────────────────────────────────────────────────┐ ← 28 mm margin
│ BAND A — TITLE                                              128 mm  │
│ [ICDAR]  REPLICA title, 2 lines serif        [QR] [QR] [QR]  45mm   │
│  110mm   thesis line · authors · affiliations proj paper contact    │
├─────────────────────────────────────── gap 16 ──────────────────────┤
│ BAND B — THE SEAM                                           248 mm  │
│  ╔═══════════╗   ░│░   ╔═══════════╗    ┌────┬────┬────┬────┐      │
│  ║  source   ║ → ░│░ → ║ Fid-HTML  ║    │0.93│0.86│ +39│ .86│      │
│  ║   page    ║   ░│░   ║  render   ║    │ VFS│ OS │ pts│ GPS│      │
│  ╚═══════════╝   ░│░   ╚═══════════╝    └────┴────┴────┴────┘      │
│   --paper       SEAM      --screen       each with a 24pt mono src  │
├─────────────────────────────────────── gap 16 ──────────────────────┤
│ BAND C — ① WHAT GETS LOST (7 col)  │ ② FID-HTML (5 col)     176 mm │
│ 4-panel strip + TE/LS/PS/VF chips  │ 2×3 dimension chips ①–⑥       │
│ 3 leader-line callouts             │ condensed Table 1, 4 rows      │
├─────────────────────────────────────── gap 16 ──────────────────────┤
│ BAND D — ③ REPLICA PIPELINE (12 col, full width)            208 mm  │
│ ▔▔▔seg▔▔▔  ▔▔▔loc▔▔▔  ▔▔▔asm▔▔▔  ▔▔▔ref▔▔▔   ← 3mm stage top rules │
│ ①Segment → ②Localize → ③Assemble → ④Refine   one continuous line   │
│ agent/tool chips by SHAPE + 3-item legend                           │
│ ── closed loop strip: R(H) → compare to I → inject CSS → ≤5 ──      │
├─────────────────────────────────────── gap 16 ──────────────────────┤
│ BAND E — ④ MEASURE (4col) │ ⑤ RESULTS (4col) │ ⑥ ABLATION  176 mm  │
│ VFDR-Bench stat chips     │ 6-row table      │ 9-step staircase    │
│ metric definitions        │ bar-in-table     │ 0.53 → 0.93         │
│ + radar plot              │                  │ + reliability strip │
├─────────────────────────────────────── gap 16 ──────────────────────┤
│ BAND F — ⑦ UNLOCKS (7 col) │ LIMITATIONS (5 col)            88 mm  │
│ six application tiles      │ 2 lines, then the TAKEAWAY on --paper  │
├─────────────────────────────────────── gap 16 ──────────────────────┤
│ FOOTER — type legend │ project URL │ funding │ logos         13 mm  │
└─────────────────────────────────────────────────────────────────────┘
```

**Arithmetic, verified:** 128 + 248 + 176 + 208 + 176 + 88 + 13 = **1037 mm** of bands.
Six gaps × 16 mm = **96 mm**. Total **1133 mm** = live height exactly. ✓

### Where the 96 mm came from, and why

| Band | Brief | Plan | Δ | Reason |
|---|---|---|---|---|
| A Title | 140 | **128** | −12 | Logo beside the title, not above. 2 title lines (72) + thesis (16) + authors (12) + affils (9) + padding (19) = 128. Three 45 mm QRs plus labels are 58 mm tall and 151 mm wide — they sit right, inside the band. |
| B Seam | 250 | **248** | −2 | Protected. This is the one risk; it does not get trimmed. |
| C Lost + Fid-HTML | 185 | **176** | −9 | Fig. 1A panels at 104 mm wide × 139 mm tall + chip row + framing line fits in 176. |
| D Pipeline | 235 | **208** | −27 | See below — the poster-native layout is shorter than the paper's proportions. |
| E Measure/Results/Ablation | 215 | **176** | −39 | Biggest cut. The ablation becomes a staircase, not a table, which is *taller* per row but far shorter overall than 9 table rows. |
| F Unlocks | 95 | **88** | −7 | Tiles at 65 mm wide, 4:3 → 49 mm + label. |
| Footer | 13 | **13** | 0 | Unchanged. |

---

## 4. Band D — the decision the geometry forces

I asked twice whether Band D should reproduce Fig. 4 faithfully or follow §5's own spec. The
measurements now answer it, so I am proceeding on the answer rather than asking a third time.

**The faithful rebuild cannot go in Band D.** `fig4-full.svg` has an aspect ratio of 4682 : 1478 =
3.17 : 1. Placed at the full 785 mm live width it needs **248 mm of height**. Band D is 208 mm,
and there is nowhere to find another 40 mm without eating the seam.

Placing the four stage SVGs as separate columns does not work either — their natural widths are
1517 / 1176 / 691 / 1120, so equal 190 mm columns would distort every one of them, stage 3 worst
of all (its natural aspect is 0.51 : 1, which in a 190 mm column wants 371 mm of height).

**So Band D is laid out natively in HTML/CSS, per §5.** Four equal panels, stage colour as a 3 mm
top rule and badge only, every label re-set in poster type, agents and tools distinguished by
**shape** — rounded chip + filled dot for agents, square chip + hollow square for tools — with the
3-item legend at the band's right edge. One continuous connector line runs through all four panels
with arrowheads at the boundaries. Beneath it, the closed-loop strip.

The vector rebuild is not wasted: it supplies the exact sampled colours, the icon vocabulary, and
a checkable reference for every label string. And `fig4-full.svg` at 55 KB is now the right asset
for the project page and the slide deck, where the aspect ratio is not fighting anything.

---

## 5. Copy

### Thesis line — three candidates

1. **"Rebuild any page as HTML that still looks like the page."** — 10 words
2. "Four agents take a document apart and put it back as web." — 12 words
3. "Turn a document into HTML that keeps its layout, styling and look." — 12 words

**Pick: candidate 1.** Verb-first, ten words, no hedging, and it states the entire claim including
the part that is hard — *still looks like*. Candidate 2 leads with the method rather than the
result. Candidate 3 lists dimensions, which the reader has not been given a reason to care about
yet; that job belongs to Band C.

### Word budget

| Band | Cap | What it buys |
|---|---|---|
| A Title block | 60 | Title, thesis line, 7 authors, 2 affiliations, 2 QR labels |
| B Hero | 45 | Nothing but the four stat captions and their sources |
| C Lost + Fid-HTML | 200 | 1 framing line, 3 callouts, 6 dimension chips, table caption |
| D Pipeline | 220 | 4 questions in italic serif, 4 one-sentence blurbs, sub-step chips, legend, loop strip |
| E Bench + results + ablation | 220 | Stat chips, metric definitions, 2 captions, 2 annotated jumps |
| F Unlocks + limitations + takeaway | 105 | 6 three-word labels, 2 limitation lines, 1 takeaway sentence |
| **Total** | **850** | |

Rules I am holding myself to: no sentence over 22 words; verb-first phrasing; no restating the
abstract; no bulleted list longer than 4 items.

---

## 6. Asset placement, with the resolution already verified

| Band | Asset | Placed | Effective dpi | Verdict |
|---|---|---|---|---|
| A | `logos/icdar26.png` | 110 mm w | 369 | PRINT-OK |
| A | `qr/project.svg`, `qr/paper.svg`, `qr/contact.svg` | 45 mm sq each | vector | ECC-H, generated locally |
| B | `hero-source` / `hero-boxes` / `hero-render` | 120 mm w | 452 / 452 / 904 | PRINT-OK |
| C | `fig1a-{source,replica,gpt5,qwen,marker}` | 104 mm w | 383–939 | PRINT-OK |
| D | native HTML/CSS, tokens from `fig4_lib.py` | — | vector | — |
| E | `fig1b-radar-plot.svg` + poster-set labels | ~150 mm w | vector | see note |
| E | tables, staircase | — | vector | — |
| F | `fig2-app-{a..f}.png` | 65 mm w | 485–1409 | PRINT-OK |
| Footer | `logos/{bharatgen,iiith,cvit}` | 35–60 mm w | 90–193 | **REJECT — placeholder** |

**Radar note:** the labelled `fig1b-radar.svg` needs ≥ 170 mm to keep its legend above 24 pt, and
Band E's column is 253.7 mm wide but only 176 mm tall. So Band E uses **`fig1b-radar-plot.svg`**,
the geometry-only variant, and sets TE/LS/PS/VF and the legend in poster type at whatever size the
column allows. That is the same treatment §6 mandates for Fig. 2 and Fig. 4, applied consistently.

**Logo note:** BharatGen (193 dpi), IIIT-H (177 dpi, and a JPEG with a baked white box) and CVIT
(90 dpi) all fail the 300 dpi floor. Per your instruction I am placing them anyway, at the
smallest size the footer allows to maximise effective dpi, and `REPORT.md` will list all three as
knowingly sub-spec pending the hi-res files. The IIIT-H white box will be keyed out so it does not
show as a slab on `--screen`.

---

## 7. Self-critique against §2 and §3

I wrote the plan above, then read it back against the anti-brief. Four things were wrong.

**1. Band E was a generic three-column dashboard.** My first draft had "Benchmark | Results |
Ablation" as three equal cards with headings — which is exactly the SaaS-panel template §2 bans,
just without the rounded corners. **Fixed:** the three columns are no longer peers. ④ and ⑥ are
supporting evidence set at body scale; ⑤ carries the bar-in-table so the REPLICA row reads
pre-attentively from three metres. The ablation becomes a staircase because a nine-row table is
the single least persuasive way to present the most persuasive number in the paper.

**2. I had drifted into decorative numbering.** My draft used ①–⑦ across all bands including the
title and footer. §2 bans numbering things that are not a real sequence. **Fixed:** SoM badges are
used only where the paper itself numbers things — the six Fid-HTML dimensions ①–⑥, and the four
pipeline stages. Band headings get eyebrows in mono caps, not badges.

**3. The two-substrate rule was decorative, not structural.** I had `--paper` appearing as a
background tint behind the Band C callouts purely for visual variety. That breaks the code the
hero teaches. **Fixed:** `--paper` appears in exactly three places on the whole poster — the left
half of the seam, the source-document thumbnails inside the Fig. 1A strip, and the takeaway block
in Band F. Nothing else. The takeaway sitting on warm stock is the poster returning to the
substrate it opened on, which is the one place the rule earns an emotional beat rather than just
encoding information.

**4. The hero stats were unmoored.** §3's reading-order note is right and I had ignored it: Band B
shows 0.93 and 0.86 before Band E defines VFS or OS. **Fixed:** every stat carries a 24 pt mono
caption naming its source — `VFS ↑ · VLM-as-judge · VFDR-Bench`, `OS_all ↑ · vs 0.58 GPT-5`,
`at 3.75× fewer parameters`, `GPS ↑ · physical structure`. A reader who only reads the hero still
knows what each number measures.

**One risk I am taking knowingly.** §2 says take exactly one risk. It is the seam. Everything
else — the grid, the corner brackets, the tree spine, the baseline grid — is quiet by design. If
the seam fails in the proof render, the fix is to make the seam better, not to add a second idea.

**One thing I already know I will have to cut.** Band E's reliability micro-strip (`RA 0.97 · SVR
0.96 · ROA 0.98 · TCSR 0.995`) is optional in §5 and is the first thing that will fight for space
against the radar. If Band E overflows, the strip goes.

---

## 8. Open items before the build pass

1. **Contact-us email addresses.** The QR generator is built and the sizing is proven (see below);
   `CONTACT_EMAILS` in `poster/tools/make_qr.py` is empty and must stay that way until you supply
   the real addresses. Guessing an academic's email and printing it on a conference poster is not
   a risk worth taking.
2. **Paper QR target.** Currently a placeholder pointing at the project page. arXiv, a PDF on the
   project page, or the ICDAR proceedings entry?
3. **Hi-res institutional logos.** Proceeding with placeholders per your instruction; all three
   will be listed as knowingly sub-spec in `REPORT.md`.

### Contact QR — sizing, measured

Yes, one QR can carry every author. `mailto:` with comma-separated recipients is valid per
RFC 6068 and opens a composer addressed to all of them. Measured at ECC-H and 45 mm:

| Recipients | Version | Modules | mm per module | |
|---|---|---|---|---|
| 1 | v8 | 57 | 0.79 | comfortable |
| 3 | v11 | 69 | 0.65 | comfortable |
| 5 | v14 | 81 | 0.56 | fine |
| **7 (all authors)** | **v16** | **89** | **0.51** | **works, but it is the floor** |

Below about 0.50 mm per module a phone starts to struggle at poster distance. All seven fit, but
with no margin — so **the contact QR is planned at 50 mm rather than 45 mm** (0.56 mm/module),
which costs nothing in Band A and buys back the headroom. If you would rather keep all three codes
at a uniform 45 mm, use Ravi's address alone at v8 and it is comfortable.

`make_qr.py` verifies every emitted SVG by parsing its path data back into a module matrix and
comparing against a freshly encoded one — so §10 item 12 is satisfied without a decoder
dependency. Confirmed working, with a negative control that correctly fails.
