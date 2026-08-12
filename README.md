# Gastronomy - September
## Landing pages for vilalara.com - build notes

**Event:** four gastronomic evenings, 4 / 5 / 7 / 8 September, Vilalara Grand Hotel Algarve
**Page type:** dedicated pages *inside* the existing website, not a microsite
**Source of truth:** the five approved mockups (`Landing Page - Geral / Atlântico / Fogo / Mediterrâneo / Algarve`)
**Date:** 12 August 2026 - copy applied, five languages, two calls to action

---

## What is here

| File | |
|---|---|
| `en/ pt/ es/ de/ fr/` | 5 pages each: the hub and the four evenings, 25 in total |
| `content.py` | **all copy, in five languages.** The only file that holds text |
| `build_pages.py` | rebuilds the 25 pages from `content.py` |
| `build_assets.py` | re-extracts and re-crops the photography from the mockup PDFs |
| `assets/css/gastronomy-september.css` | the only stylesheet written for this page |
| `assets/js/carousel.js` | dots for the Culinary fusion carousel |
| `assets/fonts/` | Optima Nova Light, Millionaire Script, Gill Sans Light |
| `assets/img/` | 31 photographs, 3 widths each, WebP |
| `WORDPRESS.md` | **how to publish it**, slugs, WPML, enqueue, what to paste |

Preview: `python -m http.server 8753 --directory vilalara-gastronomy-september`,
then `http://localhost:8753/en/`.

---

## How closely it matches

The mockups are single 1920 px-wide artboards. Every element was measured out of
the PDFs - glyph bounding boxes, image placement rectangles, rule coordinates,
fill colours - and the built pages were then measured back in the browser at
1920 px and compared against those numbers.

| Page | Largest deviation across the whole page |
|---|---|
| Geral (hub) | **1.1 px** |
| Atlântico | **1.5 px** |
| Fogo | **1.1 px** |
| Mediterrâneo | **1.1 px** |
| Algarve | **2.1 px** |

Measured against 16 anchor points per page - eyebrow, title, lead, both hairlines,
both section titles, chef row, chef name, chef note, carousel, dots, closing
paragraph, the Back to events button, and both edges of the arena band.

Exact, not approximate:

- **Chef portraits** 368 x 491 on every evening, with the 178 px gutter on the two-chef pages and 66 px on Algarve.
- **Carousel** four slides of 378 px on a 60 px gutter inside the 112 px page margins, at 2:3 on three evenings and Mediterrâneo's landscape 378 x 266.
- **Hairlines** 150 px, and the index row 1,431 x 72.
- **Header** 124 px (88 + 36), the same bar the live site renders.
- **Hero band** 1920 x 589.
- **Type** 72 / 50 / 40 / 22 / 20 / 18 / 16 / 14 px exactly as set, with tracking derived from the glyph advances rather than guessed.

The residual 1-2 px is the mockup drawing the header at 126.6 px where the live
site renders 124 px, plus the preview's scrollbar narrowing the page by 15 px.

### Changes requested after the second round

Five adjustments on top of the mockups:

1. **`GASTRONOMY` now reads larger than `Setembro`.** It had been rendering at 27 px, not 50 - the theme's `.vl-card.slider-card-info .vl-card-title` (0,3,0) was outranking the page's own rule, and stripping the script line's tracking with it. The selector now carries the full chain.
2. **Each index entry carries its date** underneath, in the same script a size down at 12 px.
3. **`Invite chef`** moved up under the chef's name - 24 px of air down to 8.
4. **`More information`** labels are optically centred. The theme adds `padding-top: 4px` to every `.vl-btn`, which sat the text low in the pill.
5. **`Chefs` and `Culinary fusion` sit closer to their photographs** - the drop is down about 35 %, from 250 to 115 px and from 216 to 103 px. This is a deliberate departure from the mockups, which set both looser.

The arena band was re-derived after (5) so it still crosses the portraits and the
first dish exactly where the mockups put it.

### Where the artboards disagree with themselves

Reproduced as drawn, per page, but flagged because you may prefer one rhythm:

1. **Algarve** sets the chef's name 8 px and the note 17 px tighter under its four-up row than the two-chef evenings do. In `.gs-field[data-chefs="4"]`.
2. **The drop from the carousel to its dots** differs by up to 26 px between the four artboards, though the gap from the dots to the closing paragraph is identical on all four. In the four `[data-evening]` blocks, alongside the band crossings.

Both blocks are commented in the CSS. Giving all four the same values puts the
evenings on one rhythm - a one-minute change if that is what you want.

### What changed in this round

| | First mockups | Second mockups |
|---|---|---|
| Hairlines | 582 px | **150 px** |
| Section titles | 50 px | **40 px** |
| Intro eyebrow / lead | 20 / 22 px | **18 / 20 px** |
| Chef portraits | 600 x 800, two-up | **368 x 491 everywhere**, four-up on Algarve unchanged |
| Under each chef | name only | **name + a short note** |
| Culinary fusion | four bespoke collages | **one four-slide carousel with dots** |
| End of page | closing paragraph | closing paragraph + **Back to events** |
| Hub index | 26 px, 1,541 px rule | **16 px, 1,431 px rule**, evenly distributed |
| Hub, Atlântico row | previous photograph | **new photograph** |
| Page heights | 3,850 - 4,900 px | 3,850 - 4,040 px |

Also caught on the way through: the hub's row eyebrow and row title had been
inheriting the evening pages' sizes. They now carry the 14 px and 50 px the
mockups draw, which the first round had at 20 px and 50 px.

---

## How it stays part of the website

The pages load the live theme's own stylesheet:

```html
<link rel="stylesheet" href="…/bootstrap@5.3.3/dist/css/bootstrap.min.css">
<link rel="stylesheet" href="…/themes/vilalara/assets/css/initFonts.min.css">
<link rel="stylesheet" href="…/themes/vilalara/assets/css/main.min.css">
<link rel="stylesheet" href="assets/css/gastronomy-september.css">
```

So the colour tokens, the header, the footer, `.vl-btn`, `.vl-card-title`, the
hairline and the `[data-anim]` reveals are not copies - they are the same rules
the rest of vilalara.com uses. `gastronomy-september.css` is purely additive and
redeclares nothing.

Reused rather than rebuilt:

- `--color-marron` `--color-arena` `--color-arena-light`, and the three brand faces
- `.vl-card` + `.vl-card-title` for the hub lockup - the same capitals-over-script pattern as *Savor / the Abundance* on the Gastronomy page
- `.vl-btn light` for **More information** (169 x 33) and `.vl-btn dark` for **Back to events** (236 x 46)
- `hr` at the theme's weight and colour
- `[data-anim="fade"]` and `[data-anim="zoom-image"]` with the theme's own `anim.js` - the reveals are the site's, not new ones
- 112 px page gutters, matching `.container.p-lg-medium`

### Putting it into WordPress

See **`WORDPRESS.md`**: slugs per language, WPML, enqueue, and exactly what to
paste. The `<header>` and `<footer>` in these files are a stand-in so the pages
can be reviewed in context; in the theme you paste only what sits between
`<main>` and `</main>`.


---

## Copy and content

All copy lives in **`content.py`**, in five languages. It is the only file that
holds text; edit there and run `python build_pages.py`.

**PT and EN are the approved copy.** ES, DE and FR are translations of it and
need a native pass before they go live. The build prints that warning every run.

Every string was measured against the box it sits in, so nothing reflows the
layout: 75 strings, all inside their budget.

What is real, taken from the mockups:

| Evening | Venue | Date | Guest chef | Kitchen |
|---|---|---|---|---|
| Atlântico | Coral | 4 September | João Viegas | Diogo Pereira, João Viegas |
| Fogo | Raízes | 5 September | Alexandre Silva | Telmo Pires, Alexandre Silva |
| Mediterrâneo | Trattoria | 7 September | Stefano Bula | Ricardo Lucas, Stefano Bula |
| Algarve | Praça das Rosas | 8 September | Louis Anjos | Diogo Pereira, Telmo Pires, Ricardo Lucas, Louis Anjos |

House style: commas and full stops only. No hyphen or dash standing in for an
aside. The framing is the sixtieth anniversary, never a founding date.

### Still missing

1. **Menu links.** The *Menu* button renders on all 20 event pages but points at `#`. Fill `MENUS` in `build_pages.py`.
2. **Time and covers.** The closing paragraphs carry `[HORA]` and `[N]`, in `content.py`.
3. **One line of fact per chef.** Eight notes are on a placeholder that is true of everyone and asserts nothing.
4. **Native review** of ES, DE and FR.


---

## Accessibility

- One `h1` per page, no heading level skipped, `main` landmark, skip link.
- Every photograph has descriptive alt text naming the chef or the dish.
- Contrast measured on every text style: lowest is **9.38:1**, well past AA.
- **Focus indicators restored.** The theme sets `* { outline: none }`, which leaves keyboard users with no indicator anywhere on vilalara.com. A `:focus-visible` ring is added, scoped to these pages, and nothing changes at rest. **Worth lifting into the theme** - it is a site-wide gap, not one this page introduced.
- Reveals respect `prefers-reduced-motion`, and content is never left stranded at opacity 0: without JavaScript, or if `anim.js` fails to load, everything shows.

---

## Performance

- **WebP at three widths per image** with `srcset` and `sizes`; 7.4 MB for all five pages together, and a page pulls roughly 1 - 1.5 MB at desktop.
- Photography is **pre-cropped to the exact window the designer used**, so `object-fit` has nothing to decide, the browser downloads no pixels it will crop away, and the framing cannot drift between breakpoints.
- Fonts subset to the three weights actually used, WOFF2, preloaded - 144 KB.
- Hero is `fetchpriority="high"`, everything below is lazy.
- JavaScript is the theme's own `anim.js`, Bootstrap's collapse for the mobile menu, and 1.4 KB for the carousel dots. No carousel library, no animation library.
- Every image carries intrinsic dimensions or a fixed aspect ratio, so there is no layout shift.

---

## Responsive

Desktop is the design; the rest adapts rather than stacks.

| | |
|---|---|
| **1920 - 1400** | the design, fluid via `clamp()` |
| **1400 - 1024** | gutters close, the four-up chef row becomes two-up, 2.2 slides in view |
| **1024 - 768** | chef row two-up at 248 x 331, event rows keep their 50/50 split |
| **below 768** | one column; 1.15 slides in view; the event photograph moves above its invitation |

The carousel is the one piece worth explaining. The track is a native
scroll-snap row, so it swipes on touch, scrolls with a trackpad and takes arrow
keys when focused **with no JavaScript at all**; `carousel.js` (1.4 KB) only
wires the dots to it and keeps the active one in step with the scroll. Four
slides show at the design width, 2.2 at tablet and 1.15 on a phone, so the next
one always peeks in and the row reads as swipeable. Dot clicks honour
`prefers-reduced-motion`.

---

## Rebuilding

```bash
python build_pages.py     # copy or structure changed
python build_assets.py    # the mockup photography changed (needs pymupdf + pillow)
```

`build_pages.py` reads the widths that actually exist in `assets/img/`, so if a
source photograph is too small for a given width the `srcset` follows rather than
pointing at a file that was never written.

---

## The honest limit

The smaller portraits stopped being a problem this round: now that every chef is
shown at 368 x 491 rather than 600 x 800, even the tightest source - **João
Viegas** at 890 x 1187 and **Alexandre Silva** at 879 x 1174 after cropping -
clears 2x on a retina screen.

One asset is worth a second look. The **new photograph on the hub's Atlântico
row** crops to 927 x 966 where the other three rows give 1,000 to 3,500 px. It
fills its 960 x 1000 slot at 1x, so it will be visibly softer than the rows above
and below it on a retina screen. A larger export of that same frame would fix it
outright.
