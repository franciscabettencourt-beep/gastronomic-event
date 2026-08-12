#!/usr/bin/env python3
"""Route for when there is no server access.

    python build_no_ftp.py                       (prepares the two snippets)
    python build_no_ftp.py <url-de-uma-imagem>   (regenerates the blocks)

Nothing is uploaded to the theme. Instead:

  CSS      -> WPCode, a CSS Snippet
  JS       -> WPCode, a JavaScript Snippet
  imagens  -> WordPress Media Library

The @font-face block is stripped from the CSS: inside vilalara.com the theme
already serves Optima, Millionaire and Gill Sans from the same origin, so the
families resolve on their own and pointing at files that are not there would
only produce failed requests.

The Media Library base cannot be guessed reliably, so pass the URL of any one
uploaded image and the blocks are rebuilt against it.
"""
import os
import re
import shutil
import sys

import content as C

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'wordpress')
PAGES = ['index', 'atlantico', 'fogo', 'mediterraneo', 'algarve']


def write_snippets():
    css = open(os.path.join(HERE, 'assets', 'css', 'gastronomy-september.css'),
               encoding='utf-8').read()
    # drop section 0, the @font-face block
    css = re.sub(r'/\* =+ 0\. BRAND FONTS =+ \*/.*?(?=/\* =+ 1\. PAGE TOKENS)', '', css, flags=re.S)
    css = css.replace('@charset "UTF-8";\n', '')
    assert '@font-face' not in css, 'font-face still present'

    # WPCode Lite only auto-inserts site wide, so this stylesheet loads on every
    # page. Two rules were written for a page that carries its own <head> and
    # would otherwise reach the rest of the site: the no-JS fallback, whose `js`
    # class is set by an inline script that does not travel with the pasted
    # block, and the reduced-motion override. The first is dropped because the
    # theme always loads anim.js here; the second is scoped to .gs.
    css = css.replace(
        "html:not(.js) [data-anim] { opacity: 1 !important; "
        "visibility: visible !important; transform: none !important; }\n", "")
    css = css.replace(
        "  [data-anim] { opacity: 1 !important; ",
        "  .gs [data-anim] { opacity: 1 !important; ")

    # Anything able to paint outside .gs is a leak, since this loads site wide.
    # Rules that only declare custom properties are fine: they set variables on
    # attributes that exist nowhere else on the site.
    def only_vars(line):
        if "}" not in line:
            return False
        body = line[line.index("{") + 1:line.rindex("}")]
        decls = [d.strip() for d in body.split(";") if d.strip()]
        return bool(decls) and all(d.startswith("--") for d in decls)

    loose = [l for l in css.split("\n")
             if l[:1] not in ("", " ", "/", "*", "}", "@")
             and "{" in l and ".gs" not in l and ":root" not in l
             and not only_vars(l)]
    assert not loose, "regras fora de .gs: %s" % loose[:3]

    banner = ('/* Gastronomic September.\n'
              '   Cola isto num CSS Snippet do WPCode: Auto Insert, Site Wide Header.\n'
              '   Carrega em todas as paginas, mas tudo esta preso a .gs e nao toca\n'
              '   no resto do site.\n'
              '   As fontes vem do tema, por isso o bloco @font-face foi retirado. */\n\n')
    with open(os.path.join(OUT, 'snippet-1-css.txt'), 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(banner + css)

    js = open(os.path.join(HERE, 'assets', 'js', 'carousel.js'), encoding='utf-8').read()
    banner = ('/* Gastronomic September, pontos do carrossel.\n'
              '   Cola isto num JavaScript Snippet do WPCode, com Auto Insert,\n'
              '   Frontend Only, e Site Wide Footer. */\n\n')
    with open(os.path.join(OUT, 'snippet-2-js.txt'), 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(banner + js)

    print('  wordpress/snippet-1-css.txt   %5.1f KB   -> WPCode, CSS Snippet'
          % (os.path.getsize(os.path.join(OUT, 'snippet-1-css.txt')) / 1024))
    print('  wordpress/snippet-2-js.txt    %5.1f KB   -> WPCode, JavaScript Snippet'
          % (os.path.getsize(os.path.join(OUT, 'snippet-2-js.txt')) / 1024))


def rebuild_blocks(base):
    """Point every image at the Media Library instead of the theme."""
    base = base.rstrip('/') + '/'
    theme = '/wp-content/themes/vilalara/gastronomic/assets/img/'
    n = 0
    for lang in C.LANGS:
        for page in PAGES:
            p = os.path.join(OUT, lang, f'{page}.html')
            s = open(p, encoding='utf-8').read()
            s = s.replace(theme, base)
            open(p, 'w', encoding='utf-8', newline='\n').write(s)
            n += 1
    print(f'  {n} blocos apontam agora para {base}')


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    write_snippets()
    if len(sys.argv) > 1:
        url = sys.argv[1]
        base = url.rsplit('/', 1)[0]
        print()
        rebuild_blocks(base)
    else:
        print('\n  Falta a base da Media Library. Carrega uma imagem qualquer no')
        print('  WordPress, copia o endereco dela, e corre:')
        print('     python build_no_ftp.py <endereco>')
