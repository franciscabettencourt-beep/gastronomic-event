# -*- coding: utf-8 -*-
"""All copy for Gastronomy - September, in the five languages the site runs.

Edit here and run `python build_pages.py`. Nothing else holds text.

House style: commas and full stops only. No hyphen, en dash or em dash standing
in for an aside. The framing is the sixtieth anniversary, never a founding date.

PT and EN are the approved copy. ES, DE and FR are translations of it and are
marked `REVIEW` below: they need a native pass before they go live.
"""

LANGS = ['en', 'pt', 'es', 'de', 'fr']
NEEDS_NATIVE_REVIEW = ['es', 'de', 'fr']

# The hub's slug per language. The four evenings sit underneath it.
#
# Top level, deliberately: this is an event with a start and an end, not a
# section of the site, so it does not belong under the permanent Gastronomy
# page (/en/gastronomy/, /pt/gastronomia/, and so on).
#
# Two words rather than one, for the same reason `gastronomic` was dropped: a
# lone `gastronomic` next to an existing `gastronomy` reads as a typo of it.
# The pair names the event, and matches the wording on the page itself.
SLUG = {
    'en': 'gastronomic-september',
    'pt': 'setembro-gastronomico',
    'es': 'septiembre-gastronomico',
    'de': 'gastronomischer-september',
    'fr': 'septembre-gastronomique',
}

# The last path segment, which is what goes in the WordPress slug field and
# what is_page() matches on. Identical to SLUG while the hub stays top level.
PAGE_SLUG = {lang: s.rsplit('/', 1)[-1] for lang, s in SLUG.items()}

# Month name used in the eyebrow and the index, in each language.
MONTH = {'en': 'September', 'pt': 'Setembro', 'es': 'Septiembre',
         'de': 'September', 'fr': 'Septembre'}

# ---------------------------------------------------------------- interface --

UI = {
    'en': {'kicker': 'Gastronomy', 'chefs': 'Chefs', 'fusion': 'Culinary fusion',
           'invite': 'Invite chef', 'more': 'More information',
           'book': 'Book your table', 'book_short': 'Book', 'menu': 'Menu', 'back': 'Back to events',
           'index_label': 'The four evenings', 'dishes': 'dishes',
           'skip': 'Skip to content', 'dish_of': 'Dish %d of %d'},
    'pt': {'kicker': 'Gastronomia', 'chefs': 'Chefs', 'fusion': 'Fusão de sabores',
           'invite': 'Chef convidado', 'more': 'Saber mais',
           'book': 'Reservar mesa', 'book_short': 'Reservar', 'menu': 'Menu', 'back': 'Voltar aos eventos',
           'index_label': 'As quatro noites', 'dishes': 'pratos',
           'skip': 'Saltar para o conteúdo', 'dish_of': 'Prato %d de %d'},
    'es': {'kicker': 'Gastronomía', 'chefs': 'Chefs', 'fusion': 'Fusión de sabores',
           'invite': 'Chef invitado', 'more': 'Saber más',
           'book': 'Reservar mesa', 'book_short': 'Reservar', 'menu': 'Menú', 'back': 'Volver a los eventos',
           'index_label': 'Las cuatro noches', 'dishes': 'platos',
           'skip': 'Saltar al contenido', 'dish_of': 'Plato %d de %d'},
    'de': {'kicker': 'Gastronomie', 'chefs': 'Chefs', 'fusion': 'Fusion der Aromen',
           'invite': 'Gastkoch', 'more': 'Mehr erfahren',
           'book': 'Tisch reservieren', 'book_short': 'Buchen', 'menu': 'Menü', 'back': 'Zurück zu den Abenden',
           'index_label': 'Die vier Abende', 'dishes': 'Gerichte',
           'skip': 'Zum Inhalt springen', 'dish_of': 'Gericht %d von %d'},
    'fr': {'kicker': 'Gastronomie', 'chefs': 'Chefs', 'fusion': 'Fusion des saveurs',
           'invite': 'Chef invité', 'more': 'En savoir plus',
           'book': 'Réserver une table', 'book_short': 'Réserver', 'menu': 'Menu', 'back': 'Retour aux soirées',
           'index_label': 'Les quatre soirées', 'dishes': 'plats',
           'skip': 'Aller au contenu', 'dish_of': 'Plat %d sur %d'},
}

# ------------------------------------------------------------- hub, opening --

# The small line above the title, which every page-head on the site carries:
# CLUBS over "A place for everyone", GASTRONOMY over "Savor the abundance".
# Taken verbatim from the site's own navigation in each language rather than
# translated afresh, so the page names the anniversary the way the rest of the
# site already names it. The theme uppercases it, so the casing here is only
# what shows in the markup.
HUB_KICKER = {
    'en': "60′ Anniversary",   # the prime is the site's, kept for consistency
    'pt': "60.º Aniversário",
    'es': "60º aniversario",
    'de': "60 Jahre",
    'fr': "60e anniversaire",
}

HUB_LEAD = {
    'en': "Sixty years of Vilalara, celebrated at the table. In September, four guest "
          "chefs cook in four of our kitchens, one evening each. Tables set at dusk, "
          "the Atlantic close by, and nothing to do but stay.",
    'pt': "Sessenta anos de Vilalara, celebrados à mesa. Em setembro, quatro chefs "
          "convidados cozinham em quatro das nossas cozinhas, uma noite cada. Mesas "
          "postas ao entardecer, o Atlântico por perto, e nada para fazer senão ficar.",
    'es': "Sesenta años de Vilalara, celebrados en la mesa. En septiembre, cuatro chefs "
          "invitados cocinan en cuatro de nuestras cocinas, una noche cada uno. Mesas "
          "puestas al atardecer, el Atlántico cerca, y nada que hacer salvo quedarse.",
    'de': "Sechzig Jahre Vilalara, gefeiert bei Tisch. Im September kochen vier Gastköche "
          "in vier unserer Küchen, je einen Abend. Gedeckte Tische in der Dämmerung, der "
          "Atlantik ganz nah, und nichts zu tun außer zu bleiben.",
    'fr': "Soixante ans de Vilalara, célébrés à table. En septembre, quatre chefs invités "
          "cuisinent dans quatre de nos cuisines, un soir chacun. Tables dressées au "
          "crépuscule, l'Atlantique tout près, et rien à faire que rester.",
}

# ------------------------------------------------------- hub, one per night --

ROW = {
    'atlantico': {
        'en': "The sea, served without artifice. At Coral, João Viegas reads the Atlantic "
              "his own way, with coastal fish, shellfish at their peak, salt and acidity.",
        'pt': "O mar, servido sem artifício. No Coral, João Viegas lê o Atlântico à sua "
              "maneira, com peixe da costa, marisco no ponto, sal e acidez em equilíbrio.",
        'es': "El mar, servido sin artificio. En Coral, João Viegas lee el Atlántico a su "
              "manera, con pescado de costa, marisco en su punto, sal y acidez.",
        'de': "Das Meer, ohne Umschweife serviert. Im Coral liest João Viegas den Atlantik "
              "auf seine Art, mit Küstenfisch, Meeresfrüchten, Salz und Säure.",
        'fr': "La mer, servie sans artifice. Au Coral, João Viegas lit l'Atlantique à sa "
              "manière, avec poisson de côte, coquillages à point, sel et acidité.",
    },
    'fogo': {
        'en': "Embers, smoke and patience. At Raízes, Alexandre Silva cooks over live fire, "
              "the oldest gesture in the kitchen. Contained intensity, depth of flavour.",
        'pt': "Brasa, fumo e paciência. No Raízes, Alexandre Silva cozinha sobre fogo vivo, "
              "o gesto mais antigo da cozinha. Intensidade contida, sabor profundo.",
        'es': "Brasa, humo y paciencia. En Raízes, Alexandre Silva cocina sobre fuego vivo, "
              "el gesto más antiguo de la cocina. Intensidad contenida, sabor profundo.",
        'de': "Glut, Rauch und Geduld. Im Raízes kocht Alexandre Silva über offenem Feuer, "
              "der ältesten Geste der Küche. Verhaltene Intensität, tiefer Geschmack.",
        'fr': "Braise, fumée et patience. Au Raízes, Alexandre Silva cuisine sur feu vif, "
              "le geste le plus ancien de la cuisine. Intensité contenue, saveur profonde.",
    },
    'mediterraneo': {
        'en': "Simplicity as a destination. Stefano Bula brings the Mediterranean to "
              "Trattoria, with pasta by hand, olive oil and ripe tomato. Few ingredients, "
              "the right ones.",
        'pt': "A simplicidade como ponto de chegada. Stefano Bula traz o Mediterrâneo à "
              "Trattoria, com massa à mão, azeite e tomate maduro. Poucos ingredientes, os "
              "certos.",
        'es': "La simplicidad como punto de llegada. Stefano Bula trae el Mediterráneo a "
              "Trattoria, con pasta a mano, aceite y tomate maduro. Pocos ingredientes, "
              "los justos.",
        'de': "Einfachheit als Ziel. Stefano Bula bringt das Mittelmeer in die Trattoria, "
              "mit Pasta von Hand, Olivenöl und reifer Tomate. Wenige Zutaten, die "
              "richtigen.",
        'fr': "La simplicité, point d'arrivée. Stefano Bula amène la "
              "Méditerranée à la Trattoria, avec pâtes à la main, huile d'olive et "
              "tomate mûre. Peu d'ingrédients, les bons.",
    },
    'algarve': {
        'en': "A return to origin. At Praça das Rosas, Louis Anjos celebrates the Algarve, "
              "between hills and sea. The night that closes the circle, where it all began.",
        'pt': "Um regresso à origem. Na Praça das Rosas, Louis Anjos celebra o Algarve "
              "entre a serra e o mar. A noite que fecha o ciclo, onde tudo começou.",
        'es': "Un regreso al origen. En Praça das Rosas, Louis Anjos celebra el Algarve, "
              "entre la sierra y el mar. La noche que cierra el ciclo, donde todo empezó.",
        'de': "Eine Rückkehr zum Ursprung. Auf der Praça das Rosas feiert Louis Anjos die "
              "Algarve, zwischen Bergen und Meer. Der Abend, der den Kreis schließt.",
        'fr': "Un retour à l'origine. Sur la Praça das Rosas, Louis Anjos célèbre "
              "l'Algarve, entre montagne et mer. La soirée qui referme le cercle.",
    },
}

# ------------------------------------------------------ event page, opening --

INTRO = {
    'atlantico': {
        'en': "The sea arrives before the wine. For one evening Coral hands its pass to "
              "João Viegas, cooking beside our own team. Shellfish opened to order, rice "
              "that will not be hurried, salt and acidity in balance. A table guided by "
              "what the tide left that morning.",
        'pt': "O mar chega antes do vinho. Por uma noite, o Coral entrega o passe a João "
              "Viegas, que cozinha ao lado da nossa equipa. Marisco aberto na hora, arroz "
              "que não se apressa, sal e acidez em equilíbrio. Uma mesa guiada pelo que a "
              "maré deixou nessa manhã.",
        'es': "El mar llega antes que el vino. Por una noche, Coral entrega el pase a João "
              "Viegas, que cocina junto a nuestro equipo. Marisco abierto al momento, arroz "
              "que no se apura, sal y acidez en equilibrio. Una mesa guiada por lo que dejó "
              "la marea esa mañana.",
        'de': "Das Meer kommt vor dem Wein. Für einen Abend übergibt das Coral den Pass an "
              "João Viegas, der neben unserem Team kocht. Meeresfrüchte à la minute "
              "geöffnet, Reis, der sich Zeit nimmt, Salz und Säure im Gleichgewicht. Ein "
              "Tisch nach dem, was die Flut am Morgen zurückließ.",
        'fr': "La mer arrive avant le vin. Le temps d'une soirée, Coral confie son passe à "
              "João Viegas, qui cuisine aux côtés de notre équipe. Coquillages ouverts à la "
              "minute, riz qui ne se presse pas, sel et acidité en équilibre. Une table "
              "guidée par ce que la marée a laissé.",
    },
    'fogo': {
        'en': "There is no gas at Raízes. There is wood, and there is patience. On 5 "
              "September Alexandre Silva takes the embers beside our kitchen and returns to "
              "the oldest gesture of all. Contained intensity, depth of flavour, and the "
              "time that smoke asks for.",
        'pt': "No Raízes não há gás. Há lenha, e há paciência. A 5 de setembro Alexandre "
              "Silva assume a brasa ao lado da nossa cozinha e devolve ao produto o gesto "
              "mais antigo de todos. Intensidade contida, sabor profundo, e o tempo que o "
              "fumo exige.",
        'es': "En Raízes no hay gas. Hay leña, y hay paciencia. El 5 de septiembre Alexandre "
              "Silva toma la brasa junto a nuestra cocina y devuelve al producto el gesto "
              "más antiguo de todos. Intensidad contenida, sabor profundo, y el tiempo que "
              "el humo exige.",
        'de': "Im Raízes gibt es kein Gas. Es gibt Holz, und es gibt Geduld. Am 5. September "
              "übernimmt Alexandre Silva die Glut neben unserer Küche und kehrt zur "
              "ältesten Geste zurück. Verhaltene Intensität, tiefer Geschmack, und die "
              "Zeit, die Rauch verlangt.",
        'fr': "Au Raízes, il n'y a pas de gaz. Il y a du bois, et de la patience. Le 5 "
              "septembre, Alexandre Silva prend la braise aux côtés de notre cuisine et "
              "revient au geste le plus ancien. Intensité contenue, saveur profonde, et le "
              "temps qu'exige la fumée.",
    },
    'mediterraneo': {
        'en': "Simplicity as a destination, not a starting point. Stefano Bula joins our "
              "kitchen at the Trattoria, with pasta made by hand, olive oil and ripe "
              "tomato. Few ingredients, when they are the right ones. You stay at the table "
              "longer than you planned.",
        'pt': "A simplicidade como ponto de chegada, não de partida. Stefano Bula junta-se "
              "à nossa cozinha na Trattoria, com massa feita à mão, azeite e tomate maduro. "
              "Poucos ingredientes, quando são os certos. Fica-se à mesa mais tempo do que "
              "se previa.",
        'es': "La simplicidad como punto de llegada, no de partida. Stefano Bula se suma a "
              "nuestra cocina en Trattoria, con pasta hecha a mano, aceite y tomate maduro. "
              "Pocos ingredientes, cuando son los justos. Uno se queda en la mesa más de lo "
              "previsto.",
        'de': "Einfachheit als Ziel, nicht als Anfang. Stefano Bula kocht mit unserem Team "
              "in der Trattoria, mit Pasta von Hand, Olivenöl und reifer Tomate. Wenige "
              "Zutaten, wenn es die richtigen sind. Man bleibt länger am Tisch als geplant.",
        'fr': "La simplicité comme point d'arrivée, non de départ. Stefano Bula rejoint "
              "notre cuisine à la Trattoria, avec des pâtes à la main, de l'huile d'olive "
              "et de la tomate mûre. Peu d'ingrédients, quand ce sont les bons. On reste à "
              "table plus longtemps que prévu.",
    },
    'algarve': {
        'en': "The last evening happens in the open air, at Praça das Rosas, with the sea "
              "darkening below. Louis Anjos cooks with the three chefs who hold Vilalara's "
              "kitchens all year. Between them, a whole region at the table, from the "
              "garden to the salt to the day's catch.",
        'pt': "A última noite acontece ao ar livre, na Praça das Rosas, com o mar a "
              "escurecer em baixo. Louis Anjos cozinha com os três chefs que sustentam as "
              "cozinhas do Vilalara todo o ano. Entre eles, uma região inteira à mesa, da "
              "horta ao sal ao que o dia trouxe.",
        'es': "La última noche sucede al aire libre, en Praça das Rosas, con el mar "
              "oscureciendo abajo. Louis Anjos cocina con los tres chefs que sostienen las "
              "cocinas de Vilalara todo el año. Entre ellos, una región entera en la mesa, "
              "de la huerta a la sal a lo que trajo el día.",
        'de': "Der letzte Abend findet unter freiem Himmel statt, auf der Praça das Rosas, "
              "während unten das Meer dunkel wird. Louis Anjos kocht mit den drei Chefs, "
              "die Vilalaras Küchen das ganze Jahr tragen. Zusammen eine ganze Region bei "
              "Tisch, vom Garten bis zum Fang des Tages.",
        'fr': "La dernière soirée se passe en plein air, sur la Praça das Rosas, la mer "
              "s'assombrissant en contrebas. Louis Anjos cuisine avec les trois chefs qui "
              "tiennent les cuisines de Vilalara toute l'année. Entre eux, toute une région "
              "à table, du potager au sel à la pêche du jour.",
    },
}

# ---------------------------------------------------------- event, closing ---
# [HORA] and [N] are placeholders. Fill them in before publishing.

CLOSE = {
    'atlantico': {
        'en': "One service, one sitting. Dinner from [HORA] on 4 September at Coral, for "
              "[N] guests. Reserve through the concierge or on (+351) 282 320 000.",
        'pt': "Um só serviço, uma só mesa. Jantar a partir das [HORA] de 4 de setembro, no "
              "Coral, para [N] pessoas. Reserve pelo concierge ou por (+351) 282 320 000.",
        'es': "Un solo servicio, una sola mesa. Cena desde las [HORA] del 4 de septiembre, "
              "en Coral, para [N] personas. Reserve por el concierge o en (+351) 282 320 000.",
        'de': "Ein Service, eine Tafel. Abendessen ab [HORA] am 4. September im Coral, für "
              "[N] Gäste. Reservierung über den Concierge oder unter (+351) 282 320 000.",
        'fr': "Un seul service, une seule table. Dîner à partir de [HORA] le 4 septembre au "
              "Coral, pour [N] convives. Réservez auprès du concierge ou au "
              "(+351) 282 320 000.",
    },
    'fogo': {
        'en': "The fire is lit long before you arrive. Dinner from [HORA] on 5 September at "
              "Raízes, for [N] guests around the embers. Reserve through the concierge or "
              "on (+351) 282 320 000.",
        'pt': "O lume acende-se muito antes de chegar. Jantar a partir das [HORA] de 5 de "
              "setembro, no Raízes, para [N] pessoas à volta da brasa. Reserve pelo "
              "concierge ou por (+351) 282 320 000.",
        'es': "El fuego se enciende mucho antes de llegar. Cena desde las [HORA] del 5 de "
              "septiembre, en Raízes, para [N] personas alrededor de la brasa. Reserve por "
              "el concierge o en (+351) 282 320 000.",
        'de': "Das Feuer brennt lange bevor Sie kommen. Abendessen ab [HORA] am 5. September "
              "im Raízes, für [N] Gäste rund um die Glut. Reservierung über den Concierge "
              "oder unter (+351) 282 320 000.",
        'fr': "Le feu est allumé bien avant votre arrivée. Dîner à partir de [HORA] le 5 "
              "septembre au Raízes, pour [N] convives autour de la braise. Réservez auprès "
              "du concierge ou au (+351) 282 320 000.",
    },
    'mediterraneo': {
        'en': "Come hungry, and leave the evening open. Dinner from [HORA] on 7 September "
              "at the Trattoria, for [N] guests. Reserve through the concierge or on "
              "(+351) 282 320 000.",
        'pt': "Venha com fome, e deixe a noite em aberto. Jantar a partir das [HORA] de 7 "
              "de setembro, na Trattoria, para [N] pessoas. Reserve pelo concierge ou por "
              "(+351) 282 320 000.",
        'es': "Venga con hambre, y deje la noche abierta. Cena desde las [HORA] del 7 de "
              "septiembre, en Trattoria, para [N] personas. Reserve por el concierge o en "
              "(+351) 282 320 000.",
        'de': "Kommen Sie hungrig, und halten Sie den Abend frei. Abendessen ab [HORA] am 7. "
              "September in der Trattoria, für [N] Gäste. Reservierung über den Concierge "
              "oder unter (+351) 282 320 000.",
        'fr': "Venez avec appétit, et gardez la soirée libre. Dîner à partir de [HORA] le 7 "
              "septembre à la Trattoria, pour [N] convives. Réservez auprès du concierge ou "
              "au (+351) 282 320 000.",
    },
    'algarve': {
        'en': "Of four evenings, this is the one that closes them. From [HORA] on 8 "
              "September at Praça das Rosas, in the open air, for [N] guests. Reserve "
              "through the concierge or on (+351) 282 320 000.",
        'pt': "De quatro noites, esta é a que as fecha. A partir das [HORA] de 8 de "
              "setembro, na Praça das Rosas, ao ar livre, para [N] pessoas. Reserve pelo "
              "concierge ou por (+351) 282 320 000.",
        'es': "De cuatro noches, esta es la que las cierra. Desde las [HORA] del 8 de "
              "septiembre, en Praça das Rosas, al aire libre, para [N] personas. Reserve "
              "por el concierge o en (+351) 282 320 000.",
        'de': "Von vier Abenden ist dies der, der sie beschließt. Ab [HORA] am 8. September "
              "auf der Praça das Rosas, unter freiem Himmel, für [N] Gäste. Reservierung "
              "über den Concierge oder unter (+351) 282 320 000.",
        'fr': "De quatre soirées, voici celle qui les referme. À partir de [HORA] le 8 "
              "septembre sur la Praça das Rosas, en plein air, pour [N] convives. Réservez "
              "auprès du concierge ou au (+351) 282 320 000.",
    },
}

# ------------------------------------------------------------- chef notes ----
# PENDING. One line of fact per chef is still missing: where they cook today and
# one characteristic of their work. Until it arrives these two lines are used,
# which are true of every chef and assert nothing.

# One note per chef, in each language. Two to three short sentences: the box is
# 310px wide in Gill Sans at 16px, so roughly 150 to 200 characters before it
# runs past the portrait above it. Say where they cook and one thing that is
# theirs. Not a CV.
#
# A chef left out here, or left empty, falls back to the generic line below.
# Nothing breaks; the page just says less.
CHEF_NOTE = {
    'diogo-pereira': {
        'en': "At Vilalara every day of the year, Diogo Pereira brings the Atlantic "
              "to the table. His cuisine celebrates the Algarve through its finest "
              "produce, seasonality and a deep connection to the sea, a philosophy "
              "recognised by the MICHELIN Guide Portugal 2026.",
        'pt': "No Vilalara todos os dias do ano, Diogo Pereira traz o Atlântico à "
              "mesa. A sua cozinha celebra o Algarve pelo melhor produto, pela "
              "estação do ano e por uma ligação profunda ao mar, uma filosofia "
              "reconhecida pelo Guia MICHELIN Portugal 2026.",
        'es': "En Vilalara todos los días del año, Diogo Pereira lleva el Atlántico "
              "a la mesa. Su cocina celebra el Algarve a través del mejor producto, "
              "la temporada y un vínculo profundo con el mar, una filosofía "
              "reconocida por la Guía MICHELIN Portugal 2026.",
        'de': "Das ganze Jahr über bei Vilalara bringt Diogo Pereira den Atlantik "
              "auf den Tisch. Seine Küche feiert die Algarve mit bestem Produkt, mit "
              "der Jahreszeit und mit einer tiefen Verbindung zum Meer, eine Haltung, "
              "die der Guide MICHELIN Portugal 2026 auszeichnet.",
        'fr': "Chez Vilalara tous les jours de l'année, Diogo Pereira porte "
              "l'Atlantique à table. Sa cuisine célèbre l'Algarve par le meilleur "
              "produit, par la saison et par un lien profond à la mer, une démarche "
              "distinguée par le Guide MICHELIN Portugal 2026.",
    },
    'telmo-pires': {
        'en': "Rooted in the Algarve and guided by the fire, Telmo Pires celebrates "
              "the flavours of the land. At Raízes, local produce, tradition and the "
              "warmth of the flame come together in a cuisine made to be shared.",
        'pt': "Com raízes no Algarve e guiado pelo fogo, Telmo Pires celebra os "
              "sabores da terra. No Raízes, o produto local, a tradição e o calor da "
              "chama juntam-se numa cozinha feita para partilhar.",
        'es': "Con raíces en el Algarve y guiado por el fuego, Telmo Pires celebra "
              "los sabores de la tierra. En Raízes, el producto local, la tradición y "
              "el calor de la llama se unen en una cocina hecha para compartir.",
        'de': "In der Algarve verwurzelt und vom Feuer geführt, feiert Telmo Pires "
              "die Aromen des Landes. Im Raízes verbinden sich regionales Produkt, "
              "Tradition und die Wärme der Flamme zu einer Küche zum Teilen.",
        'fr': "Enraciné en Algarve et guidé par le feu, Telmo Pires célèbre les "
              "saveurs de la terre. Au Raízes, le produit local, la tradition et la "
              "chaleur de la flamme composent une cuisine faite pour être partagée.",
    },
    'ricardo-lucas': {
        'en': "From Italy to the Algarve, Ricardo Lucas brings the soul of the "
              "Italian table to Vilalara. At Trattoria Pantaleone, tradition, "
              "simplicity and generous flavours create an experience made for "
              "gathering.",
        'pt': "De Itália para o Algarve, Ricardo Lucas traz a alma da mesa italiana "
              "ao Vilalara. Na Trattoria Pantaleone, a tradição, a simplicidade e os "
              "sabores generosos criam uma experiência feita para reunir.",
        'es': "De Italia al Algarve, Ricardo Lucas trae el alma de la mesa italiana "
              "a Vilalara. En Trattoria Pantaleone, la tradición, la sencillez y los "
              "sabores generosos crean una experiencia hecha para reunirse.",
        'de': "Von Italien an die Algarve bringt Ricardo Lucas die Seele der "
              "italienischen Tafel nach Vilalara. In der Trattoria Pantaleone werden "
              "Tradition, Einfachheit und großzügige Aromen zu einem Abend, der "
              "Menschen zusammenführt.",
        'fr': "D'Italie à l'Algarve, Ricardo Lucas apporte l'âme de la table "
              "italienne à Vilalara. À la Trattoria Pantaleone, tradition, simplicité "
              "et saveurs généreuses composent une soirée faite pour se réunir.",
    },
    'joao-viegas': {
        'en': "For one evening, João Viegas brings his own interpretation of the "
              "Algarve to Vilalara. With an internationally shaped career and a "
              "MICHELIN Guide Portugal 2026 recommendation, his cuisine brings "
              "together local ingredients, contemporary technique and a deep sense "
              "of place.",
        'pt': "Por uma noite, João Viegas traz ao Vilalara a sua leitura do Algarve. "
              "Com um percurso construído lá fora e uma recomendação do Guia MICHELIN "
              "Portugal 2026, a sua cozinha junta produto local, técnica "
              "contemporânea e um sentido profundo do lugar.",
        'es': "Por una noche, João Viegas trae a Vilalara su propia lectura del "
              "Algarve. Con una carrera forjada fuera y una recomendación de la Guía "
              "MICHELIN Portugal 2026, su cocina reúne producto local, técnica "
              "contemporánea y un hondo sentido del lugar.",
        'de': "Für einen Abend bringt João Viegas seine eigene Lesart der Algarve "
              "nach Vilalara. Mit international geprägtem Werdegang und einer "
              "Empfehlung des Guide MICHELIN Portugal 2026 verbindet seine Küche "
              "regionales Produkt, zeitgenössische Technik und ein tiefes Gespür für "
              "den Ort.",
        'fr': "Le temps d'une soirée, João Viegas apporte à Vilalara sa lecture de "
              "l'Algarve. Fort d'un parcours international et d'une recommandation du "
              "Guide MICHELIN Portugal 2026, sa cuisine réunit produit local, "
              "technique contemporaine et sens profond du lieu.",
    },
    'alexandre-silva': {
        'en': "With fire at its heart, Alexandre Silva explores the depth and "
              "character of Portuguese cuisine. A MICHELIN-starred chef, he brings to "
              "Vilalara a cuisine shaped by fire, exceptional Portuguese produce and "
              "a deep connection to tradition.",
        'pt': "Com o fogo no centro, Alexandre Silva explora a profundidade e o "
              "carácter da cozinha portuguesa. Chef com estrela MICHELIN, traz ao "
              "Vilalara uma cozinha feita de fogo, de produto português de exceção e "
              "de uma ligação profunda à tradição.",
        'es': "Con el fuego en el centro, Alexandre Silva explora la hondura y el "
              "carácter de la cocina portuguesa. Chef con estrella MICHELIN, trae a "
              "Vilalara una cocina de fuego, de producto portugués excepcional y de "
              "profundo apego a la tradición.",
        'de': "Mit dem Feuer im Zentrum erkundet Alexandre Silva die Tiefe und den "
              "Charakter der portugiesischen Küche. Der mit einem MICHELIN Stern "
              "ausgezeichnete Koch bringt nach Vilalara eine Küche aus Feuer, "
              "herausragendem portugiesischem Produkt und tiefer Verbundenheit mit "
              "der Tradition.",
        'fr': "Le feu au cœur, Alexandre Silva explore la profondeur et le caractère "
              "de la cuisine portugaise. Chef étoilé au Guide MICHELIN, il apporte à "
              "Vilalara une cuisine de flamme, de produit portugais d'exception et "
              "d'attachement à la tradition.",
    },
    'louis-anjos': {
        'en': "For Louis Anjos, the Algarve is more than a place, it is a source of "
              "inspiration. A MICHELIN-starred chef, his cuisine reflects the sea, "
              "land and traditions of the region, reimagined through a contemporary "
              "and deeply personal lens.",
        'pt': "Para Louis Anjos, o Algarve é mais do que um lugar, é uma fonte de "
              "inspiração. Chef com estrela MICHELIN, a sua cozinha reflete o mar, a "
              "terra e as tradições da região, reinventados por um olhar "
              "contemporâneo e muito pessoal.",
        'es': "Para Louis Anjos, el Algarve es más que un lugar, es una fuente de "
              "inspiración. Chef con estrella MICHELIN, su cocina refleja el mar, la "
              "tierra y las tradiciones de la región, reinterpretados con una mirada "
              "contemporánea y muy personal.",
        'de': "Für Louis Anjos ist die Algarve mehr als ein Ort, sie ist eine Quelle "
              "der Inspiration. Der mit einem MICHELIN Stern ausgezeichnete Koch "
              "spiegelt Meer, Land und Traditionen der Region in einer "
              "zeitgenössischen, sehr persönlichen Handschrift.",
        'fr': "Pour Louis Anjos, l'Algarve est plus qu'un lieu, c'est une source "
              "d'inspiration. Chef étoilé au Guide MICHELIN, sa cuisine reflète la "
              "mer, la terre et les traditions de la région, réinventées par un "
              "regard contemporain et très personnel.",
    },
    'stefano-bula': {
        'en': "Stefano Bula brings the precision of Italian fine dining to the "
              "Mediterranean. Head Chef of Gusto by Heinz Beck, a MICHELIN-starred "
              "restaurant, his cuisine balances technique, lightness and exceptional "
              "seasonal produce.",
        'pt': "Stefano Bula traz ao Mediterrâneo a precisão da alta cozinha italiana. "
              "Chef executivo do Gusto by Heinz Beck, restaurante com estrela "
              "MICHELIN, equilibra técnica, leveza e produto de época de exceção.",
        'es': "Stefano Bula lleva al Mediterráneo la precisión de la alta cocina "
              "italiana. Chef ejecutivo de Gusto by Heinz Beck, restaurante con "
              "estrella MICHELIN, equilibra técnica, ligereza y producto de temporada "
              "excepcional.",
        'de': "Stefano Bula bringt die Präzision der italienischen Spitzenküche ans "
              "Mittelmeer. Als Küchenchef des Gusto by Heinz Beck, ausgezeichnet mit "
              "einem MICHELIN Stern, verbindet er Technik, Leichtigkeit und "
              "herausragendes Saisonprodukt.",
        'fr': "Stefano Bula apporte à la Méditerranée la précision de la haute "
              "cuisine italienne. Chef exécutif du Gusto by Heinz Beck, restaurant "
              "étoilé au Guide MICHELIN, il allie technique, légèreté et produit de "
              "saison d'exception.",
    },
}

# The fallback, and what every chef says until CHEF_NOTE is filled in.
CHEF_NOTE_RESIDENT = {
    'en': "At Vilalara every day of the year.",
    'pt': "No Vilalara todos os dias do ano.",
    'es': "En Vilalara todos los días del año.",
    'de': "Das ganze Jahr über bei Vilalara.",
    'fr': "Chez Vilalara tous les jours de l'année.",
}
CHEF_NOTE_GUEST = {
    'en': "With us for one evening, and one only.",
    'pt': "Connosco por uma noite, e uma só.",
    'es': "Con nosotros por una noche, y una sola.",
    'de': "Bei uns für einen Abend, und nur einen.",
    'fr': "Avec nous le temps d'une soirée, une seule.",
}
