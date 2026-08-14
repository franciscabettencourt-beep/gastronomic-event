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

# Headings for the two halves.
UI = {
    'en': {'next': 'Still to come', 'past': 'The season so far',
           'more': 'More information', 'invitation': 'By invitation'},
    'pt': {'next': 'Ainda por vir', 'past': 'A temporada até aqui',
           'more': 'Saber mais', 'invitation': 'Por convite'},
    'es': {'next': 'Aún por venir', 'past': 'La temporada hasta ahora',
           'more': 'Saber más', 'invitation': 'Por invitación'},
    'de': {'next': 'Noch bevorstehend', 'past': 'Die Saison bisher',
           'more': 'Mehr erfahren', 'invitation': 'Auf Einladung'},
    'fr': {'next': 'À venir', 'past': 'La saison jusqu\'ici',
           'more': 'En savoir plus', 'invitation': 'Sur invitation'},
}

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
        'img': '2024/07/VLR_yoga_cliff_homepage.jpg', 'widths': None,
        'link': lambda lang: '',
        'alt': {
            'en': 'Yoga on the cliff at Vilalara, the Atlantic below',
            'pt': 'Yoga na falésia de Vilalara, o Atlântico em baixo',
            'es': 'Yoga en el acantilado de Vilalara, el Atlántico abajo',
            'de': 'Yoga auf der Klippe von Vilalara, der Atlantik darunter',
            'fr': 'Yoga sur la falaise de Vilalara, l\'Atlantique en contrebas',
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
    return (f'<figure class="gs-event__media"><img src="{UPLOADS}{ev["img"]}" '
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


def block(lang):
    ui = UI[lang]
    rows = ''.join(row(ev, lang, i) for i, ev in enumerate(UPCOMING))
    past = ''.join(
        f'<li class="gs-tab"><span class="gs-tab__date">{esc(p["date"][lang])}</span>'
        f'{esc(p["name"][lang])}</li>' for p in PAST)
    return f'''<!-- 60 anos, a metade que ainda vem · {lang.upper()}
     Cola no editor da pagina do aniversario, em modo HTML, no lugar das
     seccoes dos eventos. O herei e a contagem ficam onde estao.
     A <div class="gs"> de fora e obrigatoria, e o que liga o CSS. -->
<div class="gs">

<section class="gs-anniv gs-shell" aria-labelledby="anniv-next-{lang}">
<hr class="gs-rule">
<h2 class="gs-display gs-display--section" id="anniv-next-{lang}" data-anim="fade">{esc(ui['next'])}</h2>
</section>

{rows}

<section class="gs-anniv gs-shell" aria-labelledby="anniv-past-{lang}">
<hr class="gs-rule">
<h2 class="gs-display gs-display--section" id="anniv-past-{lang}" data-anim="fade">{esc(ui['past'])}</h2>
<nav class="gs-index" aria-label="{esc(ui['past'])}"><ul>{past}</ul></nav>
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
