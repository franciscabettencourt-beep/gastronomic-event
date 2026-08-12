"""Extract the mockup photography and emit optimised responsive WebPs cropped to
exactly the window the designer used, so `object-fit:cover` has nothing left to decide.

Heroes are the one exception: their crop is widened to 16:9 so the band can grow
taller on small screens, and the desktop object-position that restores the
designer's band is printed for the stylesheet.
"""
import glob, io, os, unicodedata
import pymupdf
from PIL import Image

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'img')
os.makedirs(OUT, exist_ok=True)


def key(path):
    b = os.path.basename(path).replace('Landing Page - ', '').replace('.pdf', '')
    return unicodedata.normalize('NFKD', b).encode('ascii', 'ignore').decode()


# point this at wherever the approved mockup PDFs live
MOCKUPS = os.environ.get('VL_MOCKUPS', 'C:/Users/francisca/Downloads')
DOCS = {key(p): p for p in glob.glob(os.path.join(MOCKUPS, 'Landing Page - *.pdf'))}

# visible (clipped) boxes measured from the rendered mockups: x0, y0, x1, y1
VISIBLE = {
    'Geral': {1: (960, 841.6, 1920, 1841.6), 2: (0, 1841.6, 960, 2841.6),
              3: (960, 2841.6, 1920, 3841.6), 4: (0, 3841.6, 960, 4841.6)},
    'Atlantico': {0: (0, 126.6, 1920, 716),
                  2: (503, 1643, 871, 2134), 3: (1049, 1643, 1417, 2134),
                  4: (112, 2856, 490, 3422), 5: (549, 2856, 927, 3422),
                  6: (990, 2856, 1368, 3422), 7: (1430, 2856, 1808, 3422)},
    'Fogo': {0: (0, 126.6, 1920, 716),
             2: (504, 1643, 872, 2134), 3: (1051, 1643, 1419, 2134),
             4: (990, 2857, 1368, 3423), 5: (1430, 2857, 1808, 3423),
             6: (113, 2857, 491, 3423), 7: (550, 2857, 928, 3423)},
    'Mediterraneo': {0: (0, 126.6, 1920, 716),
                     2: (503, 1643, 871, 2134), 3: (1049, 1643, 1417, 2134),
                     4: (957, 2856, 1356, 3122), 5: (1409, 2856, 1808, 3122),
                     6: (138, 2856, 493, 3122), 7: (540, 2856, 895, 3122)},
    'Algarve': {0: (0, 126.6, 1920, 716),
                2: (115, 1643, 483, 2134), 3: (549, 1643, 917, 2134),
                4: (984, 1643, 1352, 2134), 5: (1418, 1643, 1786, 2134),
                6: (112, 2860, 490, 3426), 7: (549, 2860, 927, 3426),
                8: (986, 2860, 1364, 3426), 9: (1430, 2860, 1808, 3426)},
}

NAMES = {
    'Geral': {1: ('hub-atlantico', 'hubrow'), 2: ('hub-fogo', 'hubrow'),
              3: ('hub-mediterraneo', 'hubrow'), 4: ('hub-algarve', 'hubrow')},
    'Atlantico': {0: ('atlantico-hero', 'hero'), 2: ('chef-diogo-pereira', 'chef'),
                  3: ('chef-joao-viegas', 'chef'), 4: ('atlantico-dish-1', 'slide'),
                  5: ('atlantico-dish-2', 'slide'), 6: ('atlantico-dish-3', 'slide'),
                  7: ('atlantico-dish-4', 'slide')},
    'Fogo': {0: ('fogo-hero', 'hero'), 2: ('chef-telmo-pires', 'chef'),
             3: ('chef-alexandre-silva', 'chef'), 4: ('fogo-dish-3', 'slide'),
             5: ('fogo-dish-4', 'slide'), 6: ('fogo-dish-1', 'slide'),
             7: ('fogo-dish-2', 'slide')},
    'Mediterraneo': {0: ('mediterraneo-hero', 'hero'), 2: ('chef-ricardo-lucas', 'chef'),
                     3: ('chef-stefano-bula', 'chef'), 4: ('mediterraneo-dish-3', 'slide'),
                     5: ('mediterraneo-dish-4', 'slide'), 6: ('mediterraneo-dish-1', 'slide'),
                     7: ('mediterraneo-dish-2', 'slide')},
    'Algarve': {0: ('algarve-hero', 'hero'), 2: ('chef-diogo-pereira', 'chef'),
                3: ('chef-telmo-pires', 'chef'), 4: ('chef-ricardo-lucas', 'chef'),
                5: ('chef-louis-anjos', 'chef'), 6: ('algarve-dish-1', 'slide'),
                7: ('algarve-dish-2', 'slide'), 8: ('algarve-dish-3', 'slide'),
                9: ('algarve-dish-4', 'slide')},
}

# every evening now shows its chefs at 368 x 491 and its dishes at 378 wide,
# so one crop per photograph serves every page it appears on.
WIDTHS = {'hero': [1920, 1280, 800], 'hubrow': [1440, 960, 640],
          'chef': [1200, 800, 480], 'slide': [1130, 760, 400]}
HERO_ASPECT = 16 / 9

built, rows = {}, []
for page, doc_path in DOCS.items():
    doc = pymupdf.open(doc_path)
    infos = sorted(doc[0].get_image_info(xrefs=True), key=lambda i: (i['bbox'][1], i['bbox'][0]))
    for idx, info in enumerate(infos):
        if idx not in NAMES.get(page, {}):
            continue
        slug, role = NAMES[page][idx]
        if slug in built:
            rows.append((page, slug, role, 'reused', built[slug]))
            continue

        im = Image.open(io.BytesIO(doc.extract_image(info['xref'])['image'])).convert('RGB')
        bx0, by0, bx1, by1 = VISIBLE[page][idx]
        px0, py0, px1, py1 = info['bbox']
        sx, sy = im.width / (px1 - px0), im.height / (py1 - py0)   # page px -> image px

        # the designer's window, in source-image pixels
        cx0, cy0 = (bx0 - px0) * sx, (by0 - py0) * sy
        cx1, cy1 = (bx1 - px0) * sx, (by1 - py0) * sy
        note = 'exact crop'

        if role == 'hero':
            want_h = (cx1 - cx0) / HERO_ASPECT                    # widen to 16:9 for small screens
            mid = (cy0 + cy1) / 2
            ny0, ny1 = mid - want_h / 2, mid + want_h / 2
            if ny0 < 0:
                ny0, ny1 = 0, min(im.height, want_h)
            if ny1 > im.height:
                ny1, ny0 = im.height, max(0, im.height - want_h)
            band = cy1 - cy0
            free = (ny1 - ny0) - band                             # vertical travel under cover
            pos = 50 if free <= 0.5 else round((cy0 - ny0) / free * 100)
            note = f'desktop object-position: 50% {pos}%'
            cy0, cy1 = ny0, ny1

        crop = im.crop((max(0, round(cx0)), max(0, round(cy0)),
                        min(im.width, round(cx1)), min(im.height, round(cy1))))
        files = []
        for w in WIDTHS[role]:
            w = min(w, crop.width)
            h = max(1, round(crop.height * w / crop.width))
            path = f'{OUT}/{slug}-{w}.webp'
            crop.resize((w, h), Image.LANCZOS).save(path, 'WEBP', quality=80, method=6)
            files.append((w, h, os.path.getsize(path)))
        built[slug] = note
        rows.append((page, slug, role, f'{crop.width}x{crop.height} '
                     f'({crop.width/crop.height:.3f})', note))

print(f'{"page":<13}{"slug":<22}{"role":<9}{"crop":<22}note')
for r in rows:
    print(f'{r[0]:<13}{r[1]:<22}{r[2]:<9}{r[3]:<22}{r[4]}')
total = sum(os.path.getsize(f'{OUT}/{f}') for f in os.listdir(OUT))
print(f'\n{len(built)} images -> {len(os.listdir(OUT))} files, {total/1024/1024:.2f} MB')
