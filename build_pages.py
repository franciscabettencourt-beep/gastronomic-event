#!/usr/bin/env python3
"""Build Gastronomy - September in every language the site runs.

    python build_pages.py

Output: one folder per language, each holding the hub and the four evenings.
All copy lives in content.py. Header, footer and every shared component live
here, once.
"""
import hashlib
import html
import os

import content as C

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = 'https://vilalara.com'
THEME = f'{SITE}/wp-content/themes/vilalara/assets'
BOOKING = 'https://reservations.vilalara.com/en/hotel/vilalara'

# One menu link per evening. Leave empty and the button still renders, pointing
# nowhere, and the build prints a warning so it cannot ship unnoticed.
MENUS = {'atlantico': '', 'fogo': '', 'mediterraneo': '', 'algarve': ''}

CHEFS = {
    'diogo-pereira':   ('Diogo Pereira',   'Chef Diogo Pereira seated in the Coral dining room'),
    'joao-viegas':     ('João Viegas',     'Chef João Viegas in his dining room'),
    'telmo-pires':     ('Telmo Pires',     'Chef Telmo Pires in front of the wood-fired oven'),
    'alexandre-silva': ('Alexandre Silva', 'Chef Alexandre Silva with an axe against a stacked woodpile'),
    'ricardo-lucas':   ('Ricardo Lucas',   'Chef Ricardo Lucas picking lemons in the kitchen garden'),
    'stefano-bula':    ('Stefano Bula',    'Chef Stefano Bula in the Gusto by Heinz Beck kitchen'),
    'louis-anjos':     ('Louis Anjos',     'Chef Louis Anjos under the pass lamps of his kitchen'),
}

# The three chefs who hold Vilalara's own kitchens; everyone else is a guest.
RESIDENTS = {'diogo-pereira', 'telmo-pires', 'ricardo-lucas'}

# Chefs still on the generic line, collected while building so the run can say so.
_GENERIC = set()

EVENTS = [
    {'slug': 'atlantico', 'title': 'Atlântico', 'venue': 'Coral', 'day': 4,
     'hero_y': '66%', 'guest': 'joao-viegas',
     'hero_alt': 'The Coral restaurant terrace at Vilalara',
     'chefs': ['diogo-pereira', 'joao-viegas'],
     'dishes': [('atlantico-dish-1', 'Whole red mullet served on a stone table'),
                ('atlantico-dish-2', 'Slow-cooked rice with pork and baby carrots'),
                ('atlantico-dish-3', 'Clams, oysters and coriander in a red casserole'),
                ('atlantico-dish-4', 'Seared scallops in a shellfish broth on black marble')],
     'hub_alt': 'Chef João Viegas in the dining room'},
    {'slug': 'fogo', 'title': 'Fogo', 'venue': 'Raízes', 'day': 5,
     'hero_y': '50%', 'guest': 'alexandre-silva',
     'hero_alt': 'A table laid in the kitchen garden at Raízes, tomatoes still on the vine behind it',
     'chefs': ['telmo-pires', 'alexandre-silva'],
     'dishes': [('fogo-dish-1', 'Heirloom tomatoes and just-picked lettuce on a sunlit table'),
                ('fogo-dish-2', 'The open fire and grill at Raízes'),
                ('fogo-dish-3', 'A tiled table set with Douro wines under the vines'),
                ('fogo-dish-4', 'Oysters grilled over embers in a cast-iron dish')],
     'hub_alt': 'Chef Alexandre Silva with an axe against a stacked woodpile'},
    {'slug': 'mediterraneo', 'title': 'Mediterrâneo', 'venue': 'Trattoria', 'day': 7,
     'hero_y': '50%', 'guest': 'stefano-bula',
     'hero_alt': 'The Trattoria Pantaleone dining room',
     'chefs': ['ricardo-lucas', 'stefano-bula'],
     'dishes': [('mediterraneo-dish-1', 'Burrata with heirloom tomatoes, basil and pine nuts'),
                ('mediterraneo-dish-2', 'The Trattoria Pantaleone dining room in chequered marble'),
                ('mediterraneo-dish-3', 'Caviar, radish and cauliflower on a white plate'),
                ('mediterraneo-dish-4', 'A white-chocolate and berry dessert with sorbet')],
     'hub_alt': 'Chef Stefano Bula in the Gusto by Heinz Beck kitchen'},
    {'slug': 'algarve', 'title': 'Algarve', 'venue': 'Praça das Rosas', 'day': 8,
     'hero_y': '84%', 'guest': 'louis-anjos',
     'hero_alt': 'Praça das Rosas with the fire pit and the sea beyond',
     'chefs': ['diogo-pereira', 'telmo-pires', 'ricardo-lucas', 'louis-anjos'],
     'dishes': [('algarve-dish-1', 'Chilled tomato soup with prawns on a green tiled table'),
                ('algarve-dish-2', 'Poached fish with carrots and samphire'),
                ('algarve-dish-3', 'Grilled fish with salad and a bowl of rice'),
                ('algarve-dish-4', 'Oysters and prawns on ice with a glass of white wine')],
     'hub_alt': 'Chef Louis Anjos under the pass lamps of his kitchen'},
]

NAV = [('Our Heritage', '/en/our-heritage/'), ('Suites &amp; Residences', '/en/suites-residences/'),
       ('Gastronomy', '/en/gastronomy/'), ('Wellness', '/en/wellness/'), ('Clubs', '/en/clubs/'),
       ('Experiences', '/en/clubsandexperiences/'), ('Occasions', '/en/occasions/'),
       ('Season Highlights', '/en/exclusive-benefits/'), ('60&#8242; Anniversary', '/en/60-anniversary/')]

FOOTER_COLS = [
    [('Contact Us', '/en/contacts/'), ('Sustainability', '/en/sustainability/'),
     ('Be Our Guest', '/en/be-our-guest/'), ('Careers', '/en/careers/'),
     ('Lost &amp; Found', 'https://lost.faundit.com/vilalara-grand-hotel-algarve')],
    [('Terms and Conditions', '/en/terms-and-conditions/'), ('Privacy Policy', '/en/privacy-policy/'),
     ('Cookie Policy', '/en/cookie-policy/'), ('Complaints Book', 'https://www.livroreclamacoes.pt/Inicio/')],
]
SOCIAL = [
    ('instagram.svg', 'Vilalara on Instagram', 'https://www.instagram.com/vilalaragrandhotel', 16, 16),
    ('facebook.svg', 'Vilalara on Facebook', 'https://www.facebook.com/VilalaraThalassaResort', 16, 16),
    ('tripadvisor.svg', 'Vilalara on Tripadvisor',
     'https://www.tripadvisor.com/Hotel_Review-g652080-d231460-Reviews-Vilalara_Thalassa_Resort-Porches_Faro_District_Algarve.html', 24, 16),
]

_BUILT = {}
for _f in sorted(os.listdir(os.path.join(HERE, 'assets', 'img'))):
    if _f.endswith('.webp'):
        _slug, _, _w = _f[:-5].rpartition('-')
        _BUILT.setdefault(_slug, []).append(int(_w))


# ------------------------------------------------------------------ helpers --

def widths(slug):
    built = sorted(_BUILT.get(slug, []), reverse=True)
    if not built:
        raise SystemExit(f'no images built for "{slug}" - run build_assets.py first')
    return built


def srcset(slug):
    return ', '.join(f'../assets/img/{slug}-{w}.webp {w}w' for w in widths(slug))


def fallback(slug):
    w = widths(slug)
    return w[len(w) // 2]


def asset_version(rel):
    """Content hash on the CSS and JS links, so a stale copy cannot be served."""
    with open(os.path.join(HERE, rel), 'rb') as fh:
        return hashlib.sha1(fh.read()).hexdigest()[:8]


def esc(s):
    return html.escape(s, quote=False)


def canonical(lang, page=''):
    base = f'{SITE}/{lang}/{C.SLUG[lang]}'
    return f'{base}/{page}/' if page else f'{base}/'


def eyebrow(ev, lang):
    """`Coral - 4 Setembro`, as the mockups set it. The hyphen separates a place
    from a date; it is not standing in for an aside."""
    return f"{ev['venue']} - {ev['day']} {C.MONTH[lang]}"


# ------------------------------------------------------------------- chrome --

def head(lang, title, description, og_image, page='', extra=''):
    alts = '\n'.join(
        f'<link rel="alternate" hreflang="{l}" href="{canonical(l, page)}">' for l in C.LANGS)
    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script>document.documentElement.className+=" js"</script>
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{canonical(lang, page)}">
{alts}
<link rel="alternate" hreflang="x-default" href="{canonical('en', page)}">

<meta property="og:type" content="website">
<meta property="og:site_name" content="Vilalara Grand Hotel Algarve">
<meta property="og:locale" content="{lang}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:image" content="{SITE}/{lang}/{C.SLUG[lang]}/assets/img/{og_image}-{max(_BUILT[og_image])}.webp">
<meta name="twitter:card" content="summary_large_image">

<link rel="preconnect" href="{SITE}" crossorigin>
<link rel="preload" as="font" type="font/woff2" href="../assets/fonts/OptimaNovaLTProLight.woff2" crossorigin>
<link rel="preload" as="font" type="font/woff2" href="../assets/fonts/Millionaire-Script.woff2" crossorigin>
<link rel="preload" as="font" type="font/woff2" href="../assets/fonts/GillSansLight.woff2" crossorigin>
<!-- No Bootstrap. vilalara.com does not ship it, and loading it here made these
     pages a friendlier place than the one they have to live in: mx-auto and
     visually-hidden worked in the preview and were missing on the site. Both
     are declared in the page stylesheet now. -->
<link rel="stylesheet" href="{THEME}/css/initFonts.min.css">
<link rel="stylesheet" href="{THEME}/css/main.min.css">
<link rel="stylesheet" href="../assets/css/gastronomy-september.css?v={asset_version("assets/css/gastronomy-september.css")}">
{extra}</head>
<body class="gs">
<a class="visually-hidden-focusable" href="#main">{esc(C.UI[lang]['skip'])}</a>
'''


def lang_toggler(lang, page, variant):
    others = ''.join(
        f'<li class="wpml-ls-item"><a class="wpml-ls-link" href="{canonical(l, page)}">'
        f'<span class="wpml-ls-display">{l.upper()}</span></a></li>'
        for l in C.LANGS if l != lang)
    return f'''<div class="lang-toggler {variant}">
<div class="wpml-ls wpml-ls-legacy-dropdown js-wpml-ls-legacy-dropdown">
<ul><li tabindex="0" class="wpml-ls-item wpml-ls-current-language wpml-ls-item-legacy-dropdown">
<a href="#" class="js-wpml-ls-item-toggle wpml-ls-item-toggle" aria-haspopup="true" aria-expanded="false"><span class="wpml-ls-native">{lang.upper()}</span></a>
<ul class="wpml-ls-sub-menu">{others}</ul>
</li></ul></div></div>'''


def header(lang, page):
    desktop = ''.join(
        f'<li class="menu-item{" active" if u == "/en/gastronomy/" else ""}">'
        f'<a href="{SITE}{u}">{t}</a></li>' for t, u in NAV)
    mobile = ''.join(f'<li class="menu-item"><a href="{SITE}{u}">{t}</a></li>' for t, u in NAV)
    book = (f'<a class="vl-btn light white book-engine" href="{BOOKING}" '
            f'target="_blank" rel="noopener">{esc(C.UI[lang]["book_short"])}</a>')
    return f'''<header class="sticky-top">
<div id="site_menu">
<nav class="navbar" aria-label="Main">
<div class="container">
<div class="menu-options">
<button class="navbar-toggler collapsed mobile" type="button" data-bs-toggle="collapse"
  data-bs-target="#main_navbar" aria-controls="main_navbar" aria-expanded="false"
  aria-label="Toggle navigation"><span class="toggler-icon"></span></button>
{lang_toggler(lang, page, 'desktop')}
</div>
</div>
<a class="navbar-brand" href="{SITE}/{lang}/">
<img src="{SITE}/wp-content/uploads/2026/04/cropped-cropped-LOGO-DEFINTIVO-1-scaled-1.png"
  width="2293" height="610" alt="Vilalara Grand Hotel Algarve" fetchpriority="high" decoding="async">
</a>
{lang_toggler(lang, page, 'mobile')}
<div class="collapse navbar-collapse" id="main_navbar"><ul class="navbar-nav">{mobile}</ul></div>
</nav>
<nav class="desktop" aria-label="Sections">
<div class="navbar-nav"><ul>{desktop}</ul>{book}</div>
</nav>
</div>
{book.replace('vl-btn light white book-engine', 'vl-btn light white book-engine mobile')}
</header>
'''


def footer():
    cols = ''.join('<ul>' + ''.join(
        f'<li><a href="{u if u.startswith("http") else SITE + u}">{t}</a></li>'
        for t, u in col) + '</ul>' for col in FOOTER_COLS)
    social = ''.join(
        f'<li><a href="{u}" target="_blank" rel="noopener">'
        f'<img src="{THEME}/images/{f}" alt="{a}" width="{w}" height="{h}" loading="lazy"></a></li>'
        for f, a, u, w, h in SOCIAL)
    return f'''<footer class="vl-bg-dark">
<div class="container">
<div class="logo mx-auto"><figure class="text-center">
<img src="{THEME}/images/vilalara_address.svg" width="100" height="30" alt="" loading="lazy">
<img src="{THEME}/images/Group 27831.svg" width="57" height="60" alt="" loading="lazy">
</figure></div>
<hr class="separator mb-min">
<aside class="links d-flex">
<ul><li><span>Vilalara - <i>Grand Hotel Algarve</i></span></li></ul>
<ul>
<li class="d-flex flex-column mb-3"><a href="tel:+351282320000">(+351) 282 320 000</a></li>
<li><a href="mailto:reservas@vilalara.com">RESERVAS@VILALARA.COM</a></li>
</ul>
{cols}
<ul class="social-links d-flex">{social}</ul>
</aside>
<hr class="mt-0">
<div class="d-flex copyright">
<div class="col-lg-6"></div>
<div class="col-lg-6 d-flex">
<div class="rnet"><h2>RNET REGISTRATION NUMBER FOR HOTEL-APARTMENT: 3423</h2></div>
<p>2026 &copy; VILALARA GRAND HOTEL ALGARVE. ALL RIGHTS RESERVED.</p>
</div>
</div>
</div>
</footer>
<script src="{THEME}/js/anim.js" defer></script>
<script src="../assets/js/carousel.js?v={asset_version("assets/js/carousel.js")}" defer></script>
<script>addEventListener("load",function(){{setTimeout(function(){{
if(typeof loadImages!=="function"){{document.querySelectorAll("[data-anim]").forEach(function(e){{e.classList.add("animated")}})}}
}},1200)}})</script>
</body>
</html>
'''


# --------------------------------------------------------------- components --

def media(slug, alt, sizes, lazy=True, delay=0):
    load = 'loading="lazy" ' if lazy else ''
    d = f' style="--gs-delay:{delay}ms"' if delay else ''
    return (f'<figure class="gs-media" data-anim="zoom-image"{d}>'
            f'<img src="../assets/img/{slug}-{fallback(slug)}.webp" srcset="{srcset(slug)}" '
            f'sizes="{sizes}" alt="{esc(alt)}" {load}decoding="async"></figure>')


def chef_grid(keys, lang):
    sizes = '(max-width:767px) 84vw, (max-width:1024px) 40vw, 20vw'
    items = ''
    for i, k in enumerate(keys):
        note = C.CHEF_NOTE.get(k, {}).get(lang, '').strip()
        if not note:
            note = C.CHEF_NOTE_RESIDENT[lang] if k in RESIDENTS else C.CHEF_NOTE_GUEST[lang]
            _GENERIC.add(k)
        items += (f'<li class="gs-chef" data-anim="fade" data-anim-delay="{i * 110}">'
                  f'{media(f"chef-{k}", CHEFS[k][1], sizes)}'
                  f'<h3 class="gs-chef__name">{esc(CHEFS[k][0])}</h3>'
                  f'<p class="gs-chef__bio">{esc(note)}</p></li>')
    return f'<ul class="gs-chef-grid" data-count="{len(keys)}">{items}</ul>'


def carousel(dishes, label, lang):
    sizes = '(max-width:767px) 78vw, (max-width:1024px) 44vw, 20vw'
    slides = ''.join(
        f'<li class="gs-slide" id="slide-{i + 1}">{media(s, a, sizes, delay=i * 110)}</li>'
        for i, (s, a) in enumerate(dishes))
    dots = ''
    for i in range(len(dishes)):
        current = ' aria-current="true"' if i == 0 else ''
        label_i = esc(C.UI[lang]['dish_of'] % (i + 1, len(dishes)))
        dots += (f'<button type="button" class="gs-dot" aria-controls="slide-{i + 1}"{current}>'
                 f'<span class="visually-hidden">{label_i}</span></button>')
    return (f'<div class="gs-carousel" data-carousel>'
            f'<ul class="gs-carousel__track" tabindex="0" aria-label="{esc(label)}">{slides}</ul>'
            f'<div class="gs-carousel__dots">{dots}</div></div>')


def event_schema(ev, lang):
    performers = ', '.join(f'{{"@type":"Person","name":"{CHEFS[k][0]}"}}' for k in ev['chefs'])
    hero = f"{ev['slug']}-hero"
    return f'''<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"FoodEvent","name":"{ev['title']} - {ev['venue']}",
"startDate":"2026-09-{ev['day']:02d}T19:30","inLanguage":"{lang}",
"eventStatus":"https://schema.org/EventScheduled",
"eventAttendanceMode":"https://schema.org/OfflineEventAttendanceMode",
"url":"{canonical(lang, ev['slug'])}",
"image":"{SITE}/{lang}/{C.SLUG[lang]}/assets/img/{hero}-{max(_BUILT[hero])}.webp",
"location":{{"@type":"Place","name":"Vilalara Grand Hotel Algarve","address":{{"@type":"PostalAddress",
"streetAddress":"Praia das Gaivotas, Alporchinhos","postalCode":"8400-450","addressLocality":"Porches",
"addressCountry":"PT"}}}},
"organizer":{{"@type":"Organization","name":"Vilalara Grand Hotel Algarve","url":"{SITE}/{lang}/"}},
"performer":[{performers}]}}
</script>'''


# -------------------------------------------------------------------- pages --

def build_event(ev, lang):
    ui = C.UI[lang]
    title = f"{ev['title']} · {ev['venue']} | Vilalara Grand Hotel Algarve"
    desc = C.ROW[ev['slug']][lang]

    out = [head(lang, title, desc, f"{ev['slug']}-hero", ev['slug'], event_schema(ev, lang) + '\n'),
           header(lang, ev['slug']),
           f'<main id="main" data-evening="{ev["slug"]}">']
    out.append(f'''
<section class="gs-hero" style="--gs-hero-y:{ev['hero_y']}">
<img src="../assets/img/{ev['slug']}-hero-{fallback(ev['slug'] + '-hero')}.webp" srcset="{srcset(ev['slug'] + '-hero')}"
  sizes="100vw" alt="{esc(ev['hero_alt'])}" fetchpriority="high" decoding="async" width="1920" height="590">
</section>

<section class="gs-intro gs-shell" data-anim="fade">
<p class="gs-eyebrow">{esc(eyebrow(ev, lang))}</p>
<h1 class="gs-display">{esc(ev['title'])}</h1>
<p class="gs-lead">{esc(C.INTRO[ev['slug']][lang])}</p>
</section>

<div class="gs-field" data-chefs="{len(ev['chefs'])}">

<section class="gs-chefs gs-shell" aria-labelledby="chefs-{ev['slug']}">
<hr class="gs-rule">
<h2 class="gs-display gs-display--section" id="chefs-{ev['slug']}" data-anim="fade">{esc(ui['chefs'])}</h2>
{chef_grid(ev['chefs'], lang)}
</section>

<section class="gs-fusion gs-shell" aria-labelledby="fusion-{ev['slug']}">
<hr class="gs-rule">
<h2 class="gs-display gs-display--section" id="fusion-{ev['slug']}" data-anim="fade">{esc(ui['fusion'])}</h2>
{carousel(ev['dishes'], ev['title'] + ', ' + ui['dishes'], lang)}
</section>

</div>

<section class="gs-outro gs-shell" data-anim="fade">
<p class="gs-lead">{esc(C.CLOSE[ev['slug']][lang])}</p>
<div class="gs-cta">
<a class="vl-btn dark gs-btn-cta" href="{BOOKING}" target="_blank" rel="noopener">{esc(ui['book'])}</a>
<a class="vl-btn light gs-btn-cta" href="{MENUS[ev['slug']] or '#'}">{esc(ui['menu'])}</a>
</div>
<a class="gs-back" href="index.html">{esc(ui['back'])}</a>
</section>
</main>
''')
    out.append(footer())
    return ''.join(out)


def build_hub(lang):
    ui = C.UI[lang]
    title = f"{ui['kicker']} {C.MONTH[lang]} | Vilalara Grand Hotel Algarve"
    desc = C.HUB_LEAD[lang]
    schema = ('<script type="application/ld+json">\n{"@context":"https://schema.org",'
              f'"@type":"ItemList","name":"{ui["kicker"]} {C.MONTH[lang]}","itemListElement":['
              + ','.join(f'{{"@type":"ListItem","position":{i + 1},"name":"{e["title"]}",'
                         f'"url":"{canonical(lang, e["slug"])}"}}'
                         for i, e in enumerate(EVENTS)) + ']}\n</script>')

    tabs = ''.join(
        f'<li><a class="gs-tab" href="{e["slug"]}.html">{esc(e["title"])}'
        f'<span class="gs-tab__date">{e["day"]} {esc(C.MONTH[lang])}</span></a></li>'
        for e in EVENTS)

    rows = []
    for i, e in enumerate(EVENTS):
        rows.append(f'''
<article class="gs-event{' gs-event--reverse' if i % 2 else ''}">
<div class="gs-event__body" data-anim="fade">
<p class="gs-eyebrow">{esc(eyebrow(e, lang))}</p>
<h2 class="gs-display gs-display--section">{esc(e['title'])}</h2>
<p class="gs-event__text">{esc(C.ROW[e['slug']][lang])}</p>
<p class="gs-signature"><b>{esc(CHEFS[e['guest']][0])}</b><span>{esc(ui['invite'])}</span></p>
<a class="vl-btn light gs-btn" href="{e['slug']}.html">{esc(ui['more'])}<span class="visually-hidden"> {esc(e['title'])}</span></a>
</div>
<figure class="gs-event__media">
<img src="../assets/img/hub-{e['slug']}-{fallback('hub-' + e['slug'])}.webp" srcset="{srcset('hub-' + e['slug'])}"
  sizes="(max-width:767px) 100vw, 50vw" alt="{esc(e['hub_alt'])}" loading="lazy" decoding="async">
</figure>
</article>''')

    return (head(lang, title, desc, 'hub-algarve', '', schema + '\n') + header(lang, '')
            + f'''<main id="main">

<section class="gs-hub-head" aria-labelledby="hub-title">
<div class="gs-shell">
<article class="vl-card slider-card-info mx-auto" data-anim="fade">
<p class="vl-card-subtitle">{esc(C.HUB_KICKER[lang])}</p>
<h1 class="vl-card-title" id="hub-title">{esc(ui['kicker'])} <i>{esc(C.MONTH[lang])}</i></h1>
<hr class="gs-rule">
<p class="gs-lead">{esc(C.HUB_LEAD[lang])}</p>
</article>
<nav class="gs-index" aria-label="{esc(ui['index_label'])}"><ul>{tabs}</ul></nav>
</div>
</section>

{''.join(rows)}

</main>
''' + footer())


def build_root_redirect():
    """Root index, for static previews such as GitHub Pages.

    On the real site nothing lives at this address: each language sits under its
    own folder. This sends the visitor to their own language, falls back to
    English, and still works with JavaScript off through the meta refresh. It is
    marked noindex so it never competes with the real pages in search.
    """
    options = ''.join("'%s'," % l for l in C.LANGS)
    return (
        '<!DOCTYPE html>\n<html lang="en">\n<head>\n'
        '<meta charset="utf-8">\n'
        '<meta name="robots" content="noindex">\n'
        '<meta http-equiv="refresh" content="0; url=en/">\n'
        '<title>Gastronomy - September | Vilalara Grand Hotel Algarve</title>\n'
        '<link rel="canonical" href="' + canonical('en') + '">\n'
        '<script>\n(function () {\n'
        "  var want = (navigator.language || 'en').slice(0, 2).toLowerCase();\n"
        '  var have = [' + options + '];\n'
        "  location.replace((have.indexOf(want) > -1 ? want : 'en') + '/');\n"
        '})();\n</script>\n</head>\n<body>\n'
        '<p>Redirecting to <a href="en/">Gastronomy - September</a>.</p>\n'
        '</body>\n</html>\n')


if __name__ == '__main__':
    missing = [k for k, v in MENUS.items() if not v]
    if missing:
        print('AVISO  sem link de menu: ' + ', '.join(missing)
              + '   (preencher MENUS no topo deste ficheiro)')
    if C.NEEDS_NATIVE_REVIEW:
        print('AVISO  copy por rever por nativo: ' + ', '.join(C.NEEDS_NATIVE_REVIEW))
    print()

    total = 0
    for lang in C.LANGS:
        folder = os.path.join(HERE, lang)
        os.makedirs(folder, exist_ok=True)
        pages = [('index.html', build_hub(lang))]
        pages += [(f'{e["slug"]}.html', build_event(e, lang)) for e in EVENTS]
        for name, markup in pages:
            with open(os.path.join(folder, name), 'w', encoding='utf-8', newline='\n') as fh:
                fh.write(markup)
            total += len(markup)
        print(f'  {lang}/   {len(pages)} paginas   /{lang}/{C.SLUG[lang]}/')
    with open(os.path.join(HERE, 'index.html'), 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(build_root_redirect())
    # keeps GitHub Pages from rendering README.md as the home page
    open(os.path.join(HERE, '.nojekyll'), 'w').close()
    print('  index.html    redireciona para a lingua do visitante')
    print(f'\n{len(C.LANGS) * 5} paginas, {total / 1024:.0f} KB')

    if _GENERIC:
        print('\nAVISO  chefs ainda com a frase generica: '
              + ', '.join(sorted(_GENERIC)))
        print('       preencher CHEF_NOTE no content.py, 150 a 200 caracteres cada')
