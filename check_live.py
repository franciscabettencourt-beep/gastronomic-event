#!/usr/bin/env python3
"""What the site actually has, against what the blocks expect.

    python check_live.py

Written for the rollout across languages. WordPress answers 200 for a child
page reached through the wrong parent path, because it resolves the page by its
own slug and ignores the rest, so a plain status check says everything is fine
while Back to events leads nowhere. The canonical it prints is the real address,
and that is what this compares.

Checks, per language:

  the hub exists at the address the blocks link to
  each evening sits under that hub
  Book your table points at the evening's own table service
  the page is in the language it claims

Nothing here writes anything. Safe to run at any time.
"""
import re
import sys
import time
import urllib.request

import content as C
from build_pages import EVENTS, TABLES, booking

SITE = 'https://vilalara.com'


def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    for _ in range(3):
        try:
            with urllib.request.urlopen(req, timeout=25) as r:
                return r.status, r.read().decode('utf-8', 'replace')
        except Exception as e:
            code = getattr(e, 'code', None)
            if code:
                return code, ''
            time.sleep(1)
    return None, ''


def canonical(html):
    m = re.search(r'rel="canonical" href="([^"]+)"', html)
    return m.group(1) if m else ''


def served_language(html):
    """Which language the visitor is actually being shown.

    The one thing a status code cannot tell you. Slugs are unique per parent,
    so while the German evenings do not exist, WordPress resolves `fogo` to
    whichever page owns that slug and serves it happily at 200 under the German
    path. Read from the language switcher, which is what the visitor sees, and
    fall back to the canonical's own prefix."""
    m = re.search(r'wpml-ls-current-language.*?<span[^>]*>\s*([A-Za-z]{2})', html, re.S)
    if m:
        return m.group(1).lower()
    m = re.search(r'rel="canonical" href="https://[^/]+/([a-z]{2})/', html)
    return m.group(1) if m else '?'


def main():
    problems = []
    for lang in C.LANGS:
        hub = f'{SITE}/{lang}/{C.SLUG[lang]}/'
        print(f'\n[{lang}]  {hub}')

        status, html = fetch(hub)
        real = canonical(html)
        if status != 200:
            print(f'   hub            HTTP {status}   por criar, ou noutro endereco')
            problems.append(f'{lang}: hub responde {status}')
        elif real and real.rstrip('/') != hub.rstrip('/'):
            print(f'   hub            esta em {real}')
            problems.append(f'{lang}: hub em {real}, os blocos apontam para {hub}')
        elif 'post-password-form' in html:
            print('   hub            ok, protegida por palavra-passe')
        else:
            print('   hub            ok')

        for ev in EVENTS:
            url = hub + ev['slug'] + '/'
            status, html = fetch(url)
            real = canonical(html)
            if status != 200:
                print(f"   {ev['slug']:<14} HTTP {status}")
                problems.append(f"{lang}/{ev['slug']}: responde {status}")
                continue
            served = served_language(html)
            if real and real.rstrip('/') != url.rstrip('/'):
                print(f"   {ev['slug']:<14} serve a pagina {served.upper()}, {real}")
                problems.append(f"{lang}/{ev['slug']}: por criar, cai na pagina {served.upper()}")
                continue
            if served != lang:
                print(f"   {ev['slug']:<14} responde, mas em {served.upper()}")
                problems.append(f"{lang}/{ev['slug']}: servida em {served.upper()}")
                continue

            want = booking(ev['slug'], lang)
            has_zenchef = 'zenchef.com' in html
            wants_zenchef = 'zenchef.com' in want
            if wants_zenchef and want not in html:
                what = 'motor de quartos' if not has_zenchef else 'outro endereco'
                print(f"   {ev['slug']:<14} ok, mas Reservar aponta para {what}")
                problems.append(f"{lang}/{ev['slug']}: bloco antigo, Reservar sem zenchef")
            else:
                print(f"   {ev['slug']:<14} ok")

    print()
    if problems:
        print(f'{len(problems)} por resolver:')
        for p in problems:
            print('  ', p)
    else:
        print('tudo no sitio.')
    return 1 if problems else 0


if __name__ == '__main__':
    sys.exit(main())
