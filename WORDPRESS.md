# Como pôr isto no WordPress

Guia prático para publicar as 25 páginas em vilalara.com, com WPML nas cinco
línguas. Pressupõe acesso de administrador e FTP ou o gestor de ficheiros do
alojamento.

---

## O endereço final

Pediste `vilalara.com/en/gastronomic`. Fica assim:

| Língua | Hub | Uma noite |
|---|---|---|
| EN | `/en/gastronomic/` | `/en/gastronomic/fogo/` |
| PT | `/pt/gastronomico/` | `/pt/gastronomico/fogo/` |
| ES | `/es/gastronomico/` | `/es/gastronomico/fogo/` |
| DE | `/de/gastronomisch/` | `/de/gastronomisch/fogo/` |
| FR | `/fr/gastronomique/` | `/fr/gastronomique/fogo/` |

São 5 páginas por língua, 25 no total: uma hub e quatro noites.

Os slugs das noites (`atlantico`, `fogo`, `mediterraneo`, `algarve`) ficam iguais
em todas as línguas, porque são nomes próprios. Só o slug da hub é traduzido. Se
preferires outra coisa, muda o dicionário `SLUG` no topo do `content.py` e corre
`python build_pages.py` outra vez.

---

## Passo 1. Carregar os ficheiros estáticos

O CSS, o JavaScript, as fontes e as fotografias não vão para a biblioteca de
media. Vão para o tema, para manterem os caminhos relativos.

Por FTP, copia a pasta `assets/` inteira para:

```
/wp-content/themes/vilalara/gastronomic/assets/
```

Deve ficar com esta forma:

```
themes/vilalara/gastronomic/assets/
├── css/gastronomy-september.css
├── js/carousel.js
├── fonts/          3 ficheiros .woff2
└── img/            90 ficheiros .webp
```

**As fontes podem ficar de fora.** O tema já carrega Optima, Millionaire e Gill
Sans na própria origem, por isso dentro de vilalara.com elas resolvem sozinhas.
Se as deixares de fora, apaga também o bloco `@font-face` do topo do
`gastronomy-september.css`, secção 0.

---

## Passo 2. Carregar o CSS e o JS

No `functions.php` do tema, ou num plugin de snippets:

```php
add_action( 'wp_enqueue_scripts', function () {
    if ( ! is_page_template( 'page-gastronomic.php' ) ) {
        return;                       // só nestas páginas
    }
    $base = get_stylesheet_directory_uri() . '/gastronomic/assets';
    $ver  = filemtime( get_stylesheet_directory() . '/gastronomic/assets/css/gastronomy-september.css' );

    wp_enqueue_style(
        'gastronomy-september',
        $base . '/css/gastronomy-september.css',
        array( 'main' ),              // depois do main.min.css do tema
        $ver                          // muda sozinho quando editares o ficheiro
    );
    wp_enqueue_script(
        'gastronomy-carousel',
        $base . '/js/carousel.js',
        array(),
        filemtime( get_stylesheet_directory() . '/gastronomic/assets/js/carousel.js' ),
        true
    );
} );
```

O `filemtime` como versão é o equivalente ao `?v=` que os ficheiros estáticos já
usam. É o que impede o browser de servir uma versão antiga, que foi exatamente o
que nos atrasou antes.

---

## Passo 3. Criar as páginas

Para cada língua, no WordPress:

1. **Páginas → Adicionar nova**
2. Título: `Gastronomic` (EN), `Gastronómico` (PT), e assim por diante
3. Slug: o da tabela acima
4. Editor em modo **HTML** ou um bloco **HTML personalizado**
5. Cola **apenas o que está entre `<main id="main">` e `</main>`** do ficheiro
   correspondente. O `<header>` e o `<footer>` são do tema e já existem: se
   colares o ficheiro inteiro ficas com dois cabeçalhos
6. As quatro noites são páginas filhas da hub, para o endereço ficar
   `/en/gastronomic/fogo/`. No painel lateral, **Atributos da página → Superior**,
   escolhe a hub

### Os caminhos das imagens

Nos ficheiros estáticos as imagens estão como `../assets/img/...`. Dentro do
WordPress passam a ser absolutas. Substitui em todo o HTML colado:

```
../assets/          ->   /wp-content/themes/vilalara/gastronomic/assets/
```

É um localizar e substituir por página. Se preferires, faço eu essa variante dos
ficheiros e ficam prontos a colar.

### As ligações entre páginas

Nos ficheiros estáticos apontam para `fogo.html`. No WordPress passam a
`/en/gastronomic/fogo/`. Mesma lógica de substituição.

---

## Passo 4. Ligar as traduções no WPML

Depois de criares as cinco versões da hub:

1. **WPML → Gestão de traduções**
2. Liga as cinco páginas entre si como traduções da mesma página
3. Repete para cada uma das quatro noites

Feito isto, o seletor de línguas do cabeçalho passa a saltar entre as versões
certas em vez de mandar toda a gente para a homepage.

O `hreflang` já vem escrito no `<head>` de cada ficheiro. Se o WPML gerar o dele,
apaga o meu para não haver duplicados.

---

## Passo 5. SEO

Cada página traz `<title>`, `meta description`, Open Graph e dados estruturados
`FoodEvent`. Se o site usa Yoast ou RankMath, o plugin escreve os dele e ganha.
Nesse caso:

- Copia o `<title>` e a `description` de cada ficheiro para os campos do plugin
- Mantém o JSON-LD, que o plugin não substitui

**Confirma a data no JSON-LD.** Está `2026-09-04T19:30` e seguintes. A hora é um
valor por confirmar.

---

## O que falta antes de publicar

| | |
|---|---|
| **Link do menu** | O botão *Menu* existe nas 20 páginas de evento mas aponta para `#`. Preenche `MENUS` no topo do `build_pages.py` e volta a correr |
| **Hora e lugares** | Os fechos têm `[HORA]` e `[N]`. Estão em `content.py`, secção `CLOSE` |
| **Notas dos chefs** | Falta uma linha de facto por chef. Secção `CHEF_NOTE_*` do `content.py` |
| **Revisão nativa** | ES, DE e FR são tradução minha e precisam de um nativo antes de irem para o ar |
| **Book your table** | Aponta para o motor de reservas do hotel, que reserva quartos. Se estes jantares se reservam por outra via, muda `BOOKING` |

O build avisa dos dois primeiros sempre que corre.

---

## Fluxo depois de publicado

Qualquer alteração de texto faz-se num sítio só:

```bash
# 1. editar content.py
python build_pages.py        # regenera as 25 páginas
```

Depois copias o `<main>` novo para a página correspondente no WordPress. Se as
alterações forem muitas, vale a pena passar a um template PHP em vez de HTML
colado, e aí a copy passa a viver em campos ACF. Digo como, se chegarmos lá.
