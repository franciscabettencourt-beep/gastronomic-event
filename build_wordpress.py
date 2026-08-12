#!/usr/bin/env python3
"""Turn the built pages into blocks ready to paste into WordPress.

    python build_wordpress.py

Writes wordpress/<lang>/<page>.html, each holding only what goes inside the
page editor: everything between <main> and </main>, with

  ../assets/...   ->  /wp-content/themes/vilalara/gastronomic/assets/...
  fogo.html       ->  /<lang>/<slug>/fogo/
  index.html      ->  /<lang>/<slug>/

The theme renders the header and the footer, so neither travels with the block.
Also writes wordpress/enqueue.php, the snippet that loads the CSS and the JS.
"""
import os
import re

import content as C

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'wordpress')

# Where assets/ will live once uploaded to the theme.
ASSET_BASE = '/wp-content/themes/vilalara/gastronomic/assets'

PAGES = ['index', 'atlantico', 'fogo', 'mediterraneo', 'algarve']


def page_url(lang, page):
    base = f'/{lang}/{C.SLUG[lang]}/'
    return base if page == 'index' else f'{base}{page}/'


def to_wordpress(markup, lang):
    main = re.search(r'<main[^>]*>(.*?)</main>', markup, re.S)
    if not main:
        raise SystemExit('no <main> found')
    body = main.group(1)

    body = body.replace('../assets/', ASSET_BASE + '/')
    for page in PAGES:
        body = body.replace(f'href="{page}.html"', f'href="{page_url(lang, page)}"')

    # Every rule in the stylesheet is scoped to .gs, which on the standalone
    # pages sits on <body>. That element does not travel with the block, so the
    # wrapper carries the class instead. Without it nothing matches, and the
    # page does not merely lose its styling: the theme hides [data-anim=fade]
    # above 1200px until its script adds .animated, and every section here
    # carries that attribute, so the page renders blank.
    body = f'<div class="gs">\n{body.strip()}\n</div>'

    header = (f'<!-- Gastronomy - September · {lang.upper()} · '
              f'cola isto no editor da página em modo HTML.\n'
              f'     A página é {page_url(lang, "index")} e as noites são páginas filhas.\n'
              f'     Não colar <header> nem <footer>: são do tema.\n'
              f'     A <div class="gs"> de fora é obrigatória, é o que liga o CSS. -->\n')
    return header + body + '\n'


ENQUEUE = '''<?php
/**
 * Gastronomy - September: carrega o CSS e o JS só nestas páginas.
 *
 * SÓ SERVE SE A PASTA gastronomic/ ESTIVER MESMO NO TEMA.
 *
 * Sem esse upload não há nada para carregar, e este ficheiro é o errado:
 * usa antes os dois snippets, wordpress/snippet-1-css.txt em CSS Snippet e
 * wordpress/snippet-2-js.txt em JavaScript Snippet. Ter os dois caminhos
 * ligados ao mesmo tempo carrega o estilo duas vezes.
 *
 * Cola no functions.php do tema, ou num plugin de snippets.
 * Ajusta a lista de slugs se mudares os endereços.
 */
add_action( 'wp_enqueue_scripts', function () {

    $slugs = array( %SLUGS% );

    if ( ! is_page( $slugs ) ) {
        return;
    }

    $dir = get_stylesheet_directory() . '/gastronomic/assets';
    $uri = get_stylesheet_directory_uri() . '/gastronomic/assets';

    // Sem os ficheiros no sítio, filemtime() falha e o aviso do PHP sai
    // impresso no topo da página, à vista de quem visita. Já aconteceu.
    if ( ! file_exists( $dir . '/css/gastronomy-september.css' ) ) {
        return;
    }

    wp_enqueue_style(
        'gastronomy-september',
        $uri . '/css/gastronomy-september.css',
        array(),                                  // depois do main.min.css do tema
        filemtime( $dir . '/css/gastronomy-september.css' )
    );

    $js = $dir . '/js/carousel.js';
    if ( ! file_exists( $js ) ) {
        return;
    }

    wp_enqueue_script(
        'gastronomy-carousel',
        $uri . '/js/carousel.js',
        array(),
        filemtime( $js ),
        true
    );
}, 20 );
'''


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    n = 0
    for lang in C.LANGS:
        folder = os.path.join(OUT, lang)
        os.makedirs(folder, exist_ok=True)
        for page in PAGES:
            src = os.path.join(HERE, lang, f'{page}.html')
            with open(src, encoding='utf-8') as fh:
                markup = fh.read()
            with open(os.path.join(folder, f'{page}.html'), 'w',
                      encoding='utf-8', newline='\n') as fh:
                fh.write(to_wordpress(markup, lang))
            n += 1
        print(f'  wordpress/{lang}/   5 blocos   {page_url(lang, "index")}')

    # is_page() matches post_name, which is the last path segment, never the
    # full path. English and German both land on `september`, hence the dedupe.
    names = list(dict.fromkeys(C.PAGE_SLUG[l] for l in C.LANGS))
    names += ['atlantico', 'fogo', 'mediterraneo', 'algarve']
    slugs = ', '.join(f"'{n}'" for n in names)
    with open(os.path.join(OUT, 'enqueue.php'), 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(ENQUEUE.replace('%SLUGS%', slugs))

    print(f'\n{n} blocos + enqueue.php')
    print(f'assets esperados em  {ASSET_BASE}')
