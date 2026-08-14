#!/usr/bin/env python3
"""The upcoming half of the 60th anniversary page, as a block to paste.

    python build_anniversary.py

Writes wordpress/anniversary/<lang>.html, one block per language.

Why this exists
---------------
That page carries twelve events. On 13 August 2026 six of them have already
happened and three have not, and the page gives all of them the same weight:
the same large photograph, the same paragraph, the same Reserve your table
button, including for dinners that were served in May. The countdown at the
top still points at the eclipse of 12 August and shows negative numbers.

This turns the upcoming three into full rows, in the alternating photograph and
text pattern the site already uses on its restaurant pages, and condenses the
six that are done into a single quiet strip. The season is still all there; it
just stops competing with what can still be booked.

Nothing new is installed. The rows are .gs-event, the same component the
gastronomy hub uses, and the stylesheet that draws it already loads on every
page of the site. The photographs are the ones the page uses today, read from
the Media Library where they already live.

The copy is the hotel's own, in each of the five languages, taken from the page
as it stands rather than translated afresh. Where it carries a typo it is
corrected here, and the corrections are listed in FIXES so they can be checked.
"""
import io
import os

import content as C
from build_pages import BOOKING

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'wordpress', 'anniversary')
UPLOADS = 'https://vilalara.com/wp-content/uploads/'

# Corrections made to the live copy, so they can be checked rather than trusted.
FIXES = [
    'Athlantic Encounters -> Atlantic Encounters',
    'Coral Eden do Mar -> Coral Éden do Mar',
    'A week dedicate to -> A week dedicated to',
    'thallassotherapy -> thalassotherapy',
    'siz decades -> six decades',
    'An elegant an contemporary -> an elegant and contemporary',
]

# The hero photograph the page already uses, and the moment the clock counts to.
#
# All four widths WordPress generated, not just the largest and the smallest.
# The page as it stands offers only 1024 and 2560, so a laptop downloads a
# megabyte to show it; with the middle sizes listed it takes 385KB instead.
_HERO_DIR = 'https://vilalara.com/wp-content/uploads/2025/03/'
HERO_SIZES = [
    ('13_VL_PanoramicArial_LYCLAND-1024x683.jpg', 1024),
    ('13_VL_PanoramicArial_LYCLAND-1536x1024.jpg', 1536),
    ('13_VL_PanoramicArial_LYCLAND-2048x1365.jpg', 2048),
    ('13_VL_PanoramicArial_LYCLAND-scaled.jpg', 2560),
]
HERO_SRCSET = ', '.join(f'{_HERO_DIR}{f} {w}w' for f, w in HERO_SIZES)
HERO_SRC = _HERO_DIR + HERO_SIZES[1][0]

# The first evening of the gastronomy month, which is the next thing to happen.
# Written in the hotel's own time; carousel.js reads it and removes the block
# once it is past, rather than counting upwards as the old one did.
COUNTDOWN_UNTIL = '2026-09-04 19:00:00'

UI = {
    'en': {'next': 'Still to come', 'past': 'The season so far',
           'more': 'More information', 'invitation': 'By invitation',
           'kicker': 'Vilalara Grand Hotel Algarve, est. 1966',
           'title': '60 years of Vilalara',
           'lead': 'A season marked by gastronomy, wellness, culture and legacy.',
           'events': 'Discover the events', 'stay': 'Reserve your stay',
           'next_event': 'Next event',
           'days': 'Days', 'hours': 'Hours', 'minutes': 'Minutes', 'seconds': 'Seconds',
           'hero_alt': 'Vilalara from the air, the gardens between the cliffs and the sea'},
    'pt': {'next': 'Ainda por vir', 'past': 'A temporada até aqui',
           'more': 'Saber mais', 'invitation': 'Por convite',
           'kicker': 'Vilalara Grand Hotel Algarve, fundado em 1966',
           'title': '60 anos de Vilalara',
           'lead': 'Uma época marcada pela gastronomia, bem-estar, cultura e património.',
           'events': 'Descubra os eventos', 'stay': 'Reserve a sua estadia',
           'next_event': 'Próximo evento',
           'days': 'Dias', 'hours': 'Horas', 'minutes': 'Minutos', 'seconds': 'Segundos',
           'hero_alt': 'O Vilalara visto do ar, os jardins entre a falésia e o mar'},
    'es': {'next': 'Aún por venir', 'past': 'La temporada hasta ahora',
           'more': 'Saber más', 'invitation': 'Por invitación',
           'kicker': 'Vilalara Grand Hotel Algarve, fundado en 1966',
           'title': '60 años de Vilalara',
           'lead': 'Una temporada marcada por la gastronomía, el bienestar, la cultura y el legado.',
           'events': 'Descubra los eventos', 'stay': 'Reserve su estancia',
           'next_event': 'Próximo evento',
           'days': 'Días', 'hours': 'Horas', 'minutes': 'Minutos', 'seconds': 'Segundos',
           'hero_alt': 'Vilalara desde el aire, los jardines entre el acantilado y el mar'},
    'de': {'next': 'Noch bevorstehend', 'past': 'Die Saison bisher',
           'more': 'Mehr erfahren', 'invitation': 'Auf Einladung',
           'kicker': 'Vilalara Grand Hotel Algarve, gegründet 1966',
           'title': '60 Jahre Vilalara',
           'lead': 'Eine Saison im Zeichen von Gastronomie, Wellness, Kultur und Erbe.',
           'events': 'Die Veranstaltungen', 'stay': 'Aufenthalt buchen',
           'next_event': 'Nächste Veranstaltung',
           'days': 'Tage', 'hours': 'Stunden', 'minutes': 'Minuten', 'seconds': 'Sekunden',
           'hero_alt': 'Vilalara aus der Luft, die Gärten zwischen Klippe und Meer'},
    'fr': {'next': 'À venir', 'past': 'La saison jusqu\'ici',
           'more': 'En savoir plus', 'invitation': 'Sur invitation',
           'kicker': 'Vilalara Grand Hotel Algarve, fondé en 1966',
           'title': '60 ans de Vilalara',
           'lead': 'Une saison placée sous le signe de la gastronomie, du bien-être, '
                   'de la culture et du patrimoine.',
           'events': 'Découvrir les événements', 'stay': 'Réserver votre séjour',
           'next_event': 'Prochain événement',
           'days': 'Jours', 'hours': 'Heures', 'minutes': 'Minutes', 'seconds': 'Secondes',
           'hero_alt': 'Vilalara vu du ciel, les jardins entre la falaise et la mer'},
}

CLOSE = {'en': ('The season runs to the eighth of October. Rooms, tables and treatments are booked separately, and the concierge will put an evening together around your stay.', 'Reserve your stay'), 'pt': ('A temporada vai até 8 de outubro. Quartos, mesas e tratamentos reservam-se à parte, e o concierge monta a noite à volta da sua estadia.', 'Reserve a sua estadia'), 'es': ('La temporada se extiende hasta el 8 de octubre. Habitaciones, mesas y tratamientos se reservan por separado, y el concierge compone la velada en torno a su estancia.', 'Reserve su estancia'), 'de': ('Die Saison läuft bis zum 8. Oktober. Zimmer, Tische und Behandlungen werden getrennt gebucht, und der Concierge stellt den Abend um Ihren Aufenthalt herum zusammen.', 'Aufenthalt buchen'), 'fr': ("La saison court jusqu'au 8 octobre. Chambres, tables et soins se réservent séparément, et le concierge compose la soirée autour de votre séjour.", 'Réserver votre séjour')}

# The three that have not happened yet, in date order.
#
# `link` is where More information goes. Gastronomy has its landing page; the
# other two have none yet, so they are left empty and the button is not drawn
# rather than drawn pointing nowhere. Fill one in and the button appears.
UPCOMING = [
    {
        'key': 'gastronomy',
        'img': 'hub-fogo', 'widths': [1000, 960, 640],
        'link': lambda lang: f'/{lang}/{C.SLUG[lang]}/',
        'alt': {
            'en': 'Chef Alexandre Silva with an axe against a stacked woodpile',
            'pt': 'O chef Alexandre Silva com um machado, diante da lenha empilhada',
            'es': 'El chef Alexandre Silva con un hacha, ante la leña apilada',
            'de': 'Küchenchef Alexandre Silva mit einer Axt vor dem Holzstapel',
            'fr': 'Le chef Alexandre Silva, une hache à la main, devant le bois empilé',
        },
        'eyebrow': {
            'en': '4 to 8 September', 'pt': '4 a 8 de setembro',
            'es': 'Del 4 al 8 de septiembre', 'de': '4. bis 8. September',
            'fr': 'Du 4 au 8 septembre',
        },
        'title': {
            'en': 'A Week of Flavours', 'pt': 'Uma semana de sabores',
            'es': 'Una semana llena de sabores', 'de': 'Eine Woche voller Genüsse',
            'fr': 'Une semaine de saveurs',
        },
        'text': {
            'en': 'Four evenings, four restaurants, four guest chefs cooking four hands '
                  'with our own. The gastronomic season closes with a collective '
                  'celebration at Praça das Rosas.',
            'pt': 'Quatro noites, quatro restaurantes, quatro chefs convidados a cozinhar '
                  'a quatro mãos com os nossos. A temporada gastronómica fecha com uma '
                  'celebração colectiva na Praça das Rosas.',
            'es': 'Cuatro noches, cuatro restaurantes, cuatro chefs invitados cocinando a '
                  'cuatro manos con los nuestros. La temporada gastronómica cierra con una '
                  'celebración colectiva en Praça das Rosas.',
            'de': 'Vier Abende, vier Restaurants, vier Gastköche, die vierhändig mit '
                  'unseren eigenen kochen. Die gastronomische Saison schließt mit einer '
                  'gemeinsamen Feier auf der Praça das Rosas.',
            'fr': 'Quatre soirées, quatre restaurants, quatre chefs invités cuisinant à '
                  'quatre mains avec les nôtres. La saison gastronomique se referme sur '
                  'une célébration collective Praça das Rosas.',
        },
    },
    {
        'key': 'thalasso',
        'img': '2024/03/VLR_pool_sun_salutation_vertical.jpg', 'widths': None,
        'srcset': ['2024/03/VLR_pool_sun_salutation_vertical-768x939.jpg 768w',
                   '2024/03/VLR_pool_sun_salutation_vertical-838x1024.jpg 838w',
                   '2024/03/VLR_pool_sun_salutation_vertical.jpg 850w'],
        'link': lambda lang: '',
        'alt': {
            'en': 'A sun salutation by the pool at Vilalara',
            'pt': 'Uma saudação ao sol junto à piscina do Vilalara',
            'es': 'Un saludo al sol junto a la piscina de Vilalara',
            'de': 'Ein Sonnengruß am Pool von Vilalara',
            'fr': 'Une salutation au soleil au bord de la piscine de Vilalara',
        },
        'eyebrow': {
            'en': '21 to 28 September', 'pt': 'De 21 a 28 de setembro',
            'es': 'Del 21 al 28 de septiembre', 'de': '21. bis 28. September',
            'fr': 'Du 21 au 28 septembre',
        },
        'title': {
            'en': 'Thalassotherapy Legacy Week', 'pt': 'Talassoterapia, Semana do Legado',
            'es': 'Talasoterapia, Semana del legado', 'de': 'Thalasso-Therapie Legacy-Woche',
            'fr': 'Thalassothérapie, Semaine du patrimoine',
        },
        'text': {
            'en': 'A week dedicated to Vilalara\'s wellness legacy and its historic '
                  'connection to thalassotherapy. Special residencies, exclusive '
                  'treatments and wellbeing.',
            'pt': 'Uma semana dedicada ao legado de bem-estar de Vilalara e à sua ligação '
                  'histórica à talassoterapia. Estadias especiais, tratamentos exclusivos '
                  'e bem-estar.',
            'es': 'Una semana dedicada al legado de bienestar de Vilalara y a su vínculo '
                  'histórico con la talasoterapia. Estancias especiales, tratamientos '
                  'exclusivos y bienestar.',
            'de': 'Eine Woche, die ganz dem Wellness-Erbe von Vilalara und seiner '
                  'historischen Verbindung zur Thalassotherapie gewidmet ist. Besondere '
                  'Aufenthalte, exklusive Behandlungen und Wohlbefinden.',
            'fr': 'Une semaine consacrée à l\'héritage de Vilalara en matière de bien-être '
                  'et à son lien historique avec la thalassothérapie. Des séjours '
                  'spéciaux, des soins exclusifs et du bien-être.',
        },
    },
    {
        'key': 'legacy',
        'img': '2026/06/Vilalara_terrazapool__6-1024x769.webp', 'widths': None,
        'link': lambda lang: '',
        'badge': 'invitation',
        'alt': {
            'en': 'The pool terrace at Vilalara at dusk',
            'pt': 'A esplanada da piscina de Vilalara ao entardecer',
            'es': 'La terraza de la piscina de Vilalara al atardecer',
            'de': 'Die Poolterrasse von Vilalara in der Dämmerung',
            'fr': 'La terrasse de la piscine de Vilalara au crépuscule',
        },
        'eyebrow': {
            'en': '8 October, Vilalara Grand Hotel', 'pt': '8 de outubro, Vilalara Grand Hotel',
            'es': '8 de octubre, Vilalara Grand Hotel', 'de': '8. Oktober, Vilalara Grand Hotel',
            'fr': '8 octobre, Vilalara Grand Hotel',
        },
        'title': {
            'en': 'Legacy Celebration', 'pt': 'Celebração do Legado',
            'es': 'Celebración del Legado', 'de': 'Legacy-Feier',
            'fr': 'Célébration du patrimoine',
        },
        'text': {
            'en': 'An elegant evening dedicated to celebrating six decades of history, '
                  'hospitality and legacy.',
            'pt': 'Uma noite elegante dedicada a celebrar seis décadas de história, '
                  'hospitalidade e legado.',
            'es': 'Una velada elegante dedicada a celebrar seis décadas de historia, '
                  'hospitalidad y legado.',
            'de': 'Ein eleganter Abend, der sechs Jahrzehnte Geschichte, Gastfreundschaft '
                  'und Erbe feiert.',
            'fr': 'Une soirée élégante dédiée à six décennies d\'histoire, d\'hospitalité '
                  'et de patrimoine.',
        },
    },
]

# The six that are done, oldest first. Date and name only: they are a record of
# the year, not an invitation, and they no longer carry a Reserve button.
PAST = [
    {'date': {'en': '23 May', 'pt': '23 de maio', 'es': '23 de mayo', 'de': '23. Mai', 'fr': '23 mai'},
     'name': {'en': '60 Years on the Cliffs', 'pt': '60 anos nas falésias',
              'es': '60 años en los acantilados', 'de': '60 Jahre auf den Klippen',
              'fr': '60 ans sur les falaises'}},
    {'date': {'en': '17 June', 'pt': '17 de junho', 'es': '17 de junio', 'de': '17. Juni', 'fr': '17 juin'},
     'name': {'en': 'Vilalara x Vila Lisa Chronicle Dinners',
              'pt': 'Vilalara x Vila Lisa Jantares Crónica',
              'es': 'Vilalara x Vila Lisa Chronicle Dinners',
              'de': 'Vilalara x Vila Lisa Chronicle Dinners',
              'fr': 'Vilalara x Vila Lisa Chronicle Dinners'}},
    {'date': {'en': '27 June', 'pt': '27 de junho', 'es': '27 de junio', 'de': '27. Juni', 'fr': '27 juin'},
     'name': {'en': 'Santos Populares at Vilalara', 'pt': 'Santos Populares no Vilalara',
              'es': 'Santos Populares en Vilalara', 'de': 'Santos Populares in Vilalara',
              'fr': 'Santos Populares à Vilalara'}},
    {'date': {'en': '11 July', 'pt': '11 de julho', 'es': '11 de julio', 'de': '11. Juli', 'fr': '11 juillet'},
     'name': {'en': 'Atlantic meets Pacific', 'pt': 'O Atlântico encontra-se com o Pacífico',
              'es': 'El Atlántico se une con el Pacífico', 'de': 'Der Atlantik trifft auf den Pazifik',
              'fr': 'L\'Atlantique rencontre le Pacifique'}},
    {'date': {'en': '25 July', 'pt': '25 de julho', 'es': '25 de julio', 'de': '25. Juli', 'fr': '25 juillet'},
     'name': {'en': 'Blanc des Blancs', 'pt': 'Blanc des Blancs', 'es': 'Blanc des Blancs',
              'de': 'Blanc des Blancs', 'fr': 'Blanc des Blancs'}},
    {'date': {'en': '12 August', 'pt': '12 de agosto', 'es': '12 de agosto', 'de': '12. August', 'fr': '12 août'},
     'name': {'en': 'The Last Eclipse of your lifetime', 'pt': 'O último eclipse da tua vida',
              'es': 'El último eclipse de tu vida', 'de': 'Die letzte Sonnenfinsternis deines Lebens',
              'fr': 'La dernière éclipse de ta vie'}},
]


def esc(s):
    return (s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))


def media(ev, lang):
    """The photograph. The gastronomy row uses the hub images built for this
    component, which come in three widths; the other two reuse what the page
    already shows, one file each."""
    alt = esc(ev['alt'][lang])
    if ev['widths']:
        base = f"{UPLOADS}2026/08/{ev['img']}"
        srcset = ', '.join(f'{base}-{w}.webp {w}w' for w in ev['widths'])
        src = f"{base}-{ev['widths'][1]}.webp"
        return (f'<figure class="gs-event__media"><img src="{src}" srcset="{srcset}" '
                f'sizes="(max-width:767px) 100vw, 50vw" alt="{alt}" '
                f'loading="lazy" decoding="async"></figure>')
    extra = ''
    if ev.get('srcset'):
        extra = ' srcset="' + ', '.join(UPLOADS + x for x in ev['srcset']) + '"'
    return (f'<figure class="gs-event__media"><img src="{UPLOADS}{ev["img"]}"{extra} '
            f'sizes="(max-width:767px) 100vw, 50vw" alt="{alt}" '
            f'loading="lazy" decoding="async"></figure>')


def row(ev, lang, i):
    ui = UI[lang]
    reverse = ' gs-event--reverse' if i % 2 else ''
    href = ev['link'](lang)
    if href:
        cta = (f'<a class="vl-btn light gs-btn" href="{href}">{esc(ui["more"])}'
               f'<span class="visually-hidden"> {esc(ev["title"][lang])}</span></a>')
    elif ev.get('badge'):
        # No page to send anyone to, so the button would point nowhere. The line
        # says what the evening is instead.
        cta = f'<p class="gs-signature"><span>{esc(ui[ev["badge"]])}</span></p>'
    else:
        cta = ''
    return (f'<article class="gs-event{reverse}">'
            f'<div class="gs-event__body" data-anim="fade">'
            f'<p class="gs-eyebrow">{esc(ev["eyebrow"][lang])}</p>'
            f'<h2 class="gs-display gs-display--section">{esc(ev["title"][lang])}</h2>'
            f'<p class="gs-event__text">{esc(ev["text"][lang])}</p>'
            f'{cta}</div>'
            f'{media(ev, lang)}</article>')


def hero(lang):
    ui = UI[lang]
    return (
        f'<section class="gs-hero" data-anim="zoom-image">'
        f'<img src="{HERO_SRC}" srcset="{HERO_SRCSET}" '
        f'sizes="100vw" alt="{esc(ui["hero_alt"])}" fetchpriority="high" decoding="async">'
        f'</section>'
        f'<section class="gs-hub-head gs-anniv-head" aria-labelledby="anniv-title-{lang}">'
        f'<div class="gs-shell">'
        f'<article class="vl-card slider-card-info mx-auto" data-anim="fade">'
        f'<p class="vl-card-subtitle">{esc(ui["kicker"])}</p>'
        f'<h1 class="vl-card-title" id="anniv-title-{lang}">{esc(ui["title"])}</h1>'
        f'<hr class="gs-rule">'
        f'<p class="gs-lead">{esc(ui["lead"])}</p>'
        f'<div class="gs-cta">'
        f'<a class="vl-btn dark gs-btn-cta" href="#eventos">{esc(ui["events"])}</a>'
        f'<a class="vl-btn light gs-btn-cta" href="{BOOKING}" target="_blank" '
        f'rel="noopener">{esc(ui["stay"])}</a>'
        f'</div></article></div></section>'
    )


def countdown(lang):
    """Counts to the first evening of the gastronomy month.

    Hidden by the stylesheet until the script fills it in, and removed by the
    script once the date is past, so it can never show zeros or the negative
    figures the old one showed the morning after the eclipse."""
    ui = UI[lang]
    unit = ('<div class="gs-countdown__unit">'
            '<span class="gs-countdown__n" data-unit="{u}">--</span>'
            '<span class="gs-countdown__label">{l}</span></div>')
    sep = '<span class="gs-countdown__sep" aria-hidden="true">:</span>'
    clock = sep.join(unit.format(u=u, l=esc(ui[u])) for u in
                     ('days', 'hours', 'minutes', 'seconds'))
    return (
        f'<section class="gs-countdown" data-until="{COUNTDOWN_UNTIL}" '
        f'aria-label="{esc(ui["next_event"])}">'
        f'<hr class="gs-rule">'
        f'<p class="gs-countdown__kicker">{esc(ui["next_event"])}</p>'
        f'<p class="gs-countdown__title">{esc(UPCOMING[0]["title"][lang])}</p>'
        f'<div class="gs-countdown__clock">{clock}</div>'
        f'</section>'
    )


def block(lang):
    ui = UI[lang]
    rows = ''.join(row(ev, lang, i) for i, ev in enumerate(UPCOMING))
    past = ''.join(
        f'<li class="gs-past__item">'
        f'<span class="gs-past__date">{esc(p["date"][lang])}</span>'
        f'<span class="gs-past__name">{esc(p["name"][lang])}</span></li>' for p in PAST)
    return f'''<!-- 60 anos de Vilalara · {lang.upper()} · a pagina inteira.
     Pagina nova, com o Modelo (Template) `Privacy`, a mesma da gastronomica.
     Cola isto num bloco de HTML personalizado. Nao colar <header> nem
     <footer>: sao do tema. A <div class="gs"> de fora e obrigatoria. -->
<div class="gs">

{hero(lang)}

{countdown(lang)}

<section class="gs-anniv gs-shell" id="eventos" aria-labelledby="anniv-next-{lang}">
<hr class="gs-rule">
<h2 class="gs-display gs-display--section" id="anniv-next-{lang}" data-anim="fade">{esc(ui['next'])}</h2>
</section>

<div class="gs-anniv-rows">
{rows}
</div>

<section class="gs-past gs-shell" aria-labelledby="anniv-past-{lang}">
<hr class="gs-rule">
<h2 class="gs-display gs-display--section" id="anniv-past-{lang}" data-anim="fade">{esc(ui['past'])}</h2>
<ul class="gs-past__list" data-anim="fade">{past}</ul>
</section>

<section class="gs-close gs-shell" data-anim="fade">
<hr class="gs-rule">
<p class="gs-lead">{esc(CLOSE[lang][0])}</p>
<div class="gs-cta">
<a class="vl-btn dark gs-btn-cta" href="{BOOKING}" target="_blank" rel="noopener">{esc(CLOSE[lang][1])}</a>
</div>
</section>

</div>
'''


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for lang in C.LANGS:
        path = os.path.join(OUT, f'{lang}.html')
        with io.open(path, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(block(lang))
        print(f'  wordpress/anniversary/{lang}.html   {os.path.getsize(path) / 1024:.1f} KB')

    sem_link = [e['key'] for e in UPCOMING if not e['link']('en')]
    if sem_link:
        print('\nAVISO  sem pagina para onde apontar: ' + ', '.join(sem_link))
        print('       o botao nao e desenhado; preencher `link` em UPCOMING')
    print('\ncorreccoes feitas a copy que esta no ar:')
    for f in FIXES:
        print('  ', f)
