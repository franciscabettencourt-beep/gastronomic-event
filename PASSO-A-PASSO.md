# Publicar no WordPress, passo a passo

Escrito para quem nunca fez isto. Segue pela ordem. Se alguma coisa não bater
certo com o que vês no ecrã, para e diz, não avances por adivinhação.

**Tempo:** cerca de 20 minutos para a primeira língua, 10 para cada uma das
outras.

**Antes de começares, precisas de:**

1. Utilizador **administrador** no WordPress de vilalara.com
2. Acesso ao **painel do alojamento** (cPanel, Plesk ou parecido) ou a um FTP

Se não tiveres o número 2, salta para a secção *"E se eu não tiver acesso ao
alojamento"* no fim.

---

# PARTE 1. Carregar as imagens e o CSS

Isto faz-se **uma vez só**. Serve as 25 páginas.

### 1.1

No teu Ambiente de Trabalho tens o ficheiro **`1-CARREGAR-NO-TEMA.zip`**.
Não o abras nem o descompactes. Vai assim mesmo.

### 1.2

Entra no painel do alojamento e abre o **Gestor de Ficheiros**
(*File Manager*). É um explorador de pastas dentro do browser.

### 1.3

Navega até à pasta do site. O caminho é quase sempre:

```
public_html  →  wp-content  →  themes  →  vilalara
```

Vais ver ficheiros como `style.css`, `functions.php`, `index.php`. Estás no
sítio certo.

### 1.4

Clica em **Upload** (ou *Carregar*), escolhe o `1-CARREGAR-NO-TEMA.zip`, e
espera. São 7,5 MB, demora menos de um minuto.

### 1.5

Volta à pasta `vilalara`. Clica com o **botão direito** no zip que acabaste de
carregar e escolhe **Extract** (ou *Extrair*). Confirma.

### 1.6

Deve ter aparecido uma pasta nova chamada **`gastronomic`**. Abre-a e confirma
que lá dentro está `assets`, e dentro dessa: `css`, `js`, `img`, `fonts`.

Se estiver assim, **apaga o zip**, já não é preciso.

### 1.7 Confirma que funcionou

Abre isto no browser:

```
https://vilalara.com/wp-content/themes/vilalara/gastronomic/assets/css/gastronomy-september.css
```

- Aparece texto a começar por `@charset "UTF-8"` → **certo**, avança
- Dá erro 404 → a pasta não ficou no sítio. Volta ao 1.3

---

# PARTE 2. Dizer ao WordPress para usar esse CSS

O WordPress não sabe que o ficheiro existe. Isto diz-lhe.

**Não vamos mexer no `functions.php`.** Um erro nesse ficheiro deita o site
abaixo. Usamos um plugin que faz o mesmo com rede de segurança.

### 2.1

No WordPress: **Plugins → Adicionar novo**. Procura por **Code Snippets**
(o autor é *Code Snippets Pro*). Instala e ativa.

### 2.2

Aparece **Snippets** no menu da esquerda. Clica em **Add New**.

### 2.3

Título: `Gastronomic September - CSS e JS`

Na caixa grande de código, cola isto:

```php
add_action( 'wp_enqueue_scripts', function () {
    $slugs = array( 'gastronomic', 'gastronomico', 'gastronomisch', 'gastronomique',
                    'atlantico', 'fogo', 'mediterraneo', 'algarve' );
    if ( ! is_page( $slugs ) ) {
        return;
    }
    $dir = get_stylesheet_directory() . '/gastronomic/assets';
    $uri = get_stylesheet_directory_uri() . '/gastronomic/assets';

    wp_enqueue_style( 'gastronomy-september', $uri . '/css/gastronomy-september.css',
        array(), filemtime( $dir . '/css/gastronomy-september.css' ) );

    wp_enqueue_script( 'gastronomy-carousel', $uri . '/js/carousel.js',
        array(), filemtime( $dir . '/js/carousel.js' ), true );
}, 20 );
```

### 2.4

Em baixo, escolhe **Run snippet everywhere**. Depois **Save Changes and
Activate**.

Se der erro vermelho, não guardou nada e o site continua bem. Manda-me o erro.

---

# PARTE 3. Criar a primeira página

Vamos fazer **só o inglês** primeiro. Confirmas que está bem, e só depois
repetes para as outras.

### 3.1

**Páginas → Adicionar nova**

### 3.2

Título: `Gastronomic`

### 3.3

Agora o passo que mais confunde. Precisas de colar HTML em bruto, não texto
normal.

**Se o editor for o moderno (blocos):**

1. Clica no **+** para adicionar um bloco
2. Procura por **HTML personalizado** (*Custom HTML*)
3. Cola lá dentro

**Se o editor for o clássico:**

1. Em cima à direita da caixa de texto há dois separadores: *Visual* e *Texto*
2. Clica em **Texto**
3. Cola

### 3.4

O que colar: abre o ficheiro **`wordpress/en/index.html`** do projeto num
editor de texto (Bloco de Notas serve), seleciona tudo com `Ctrl+A`, copia com
`Ctrl+C`, e cola na caixa.

É o ficheiro inteiro. Não tens de procurar nada lá dentro nem apagar nada.

### 3.5

No painel da direita, secção **Ligação permanente** (*Permalink*), confirma que
o slug é **`gastronomic`**. Se aparecer outra coisa, corrige.

### 3.6

**Publicar**. Depois **Ver página**.

### 3.7 O que deves ver

Fundo em areia no topo, **GASTRONOMY** grande com *Setembro* por baixo em
manuscrito, uma linha fina, o texto de introdução, e o menu com as quatro noites
e as datas. A seguir, quatro faixas alternadas com fotografia de um lado e texto
do outro.

**Se aparecer tudo desalinhado e sem cores**, o CSS não está a carregar. Volta à
Parte 2 e confirma que o snippet está ativo, e que o slug da página é mesmo um
dos que estão na lista do código.

---

# PARTE 4. As quatro noites

Cada noite é uma página **filha** da que acabaste de criar. É isso que faz o
endereço ficar `/en/gastronomic/fogo/`.

Para cada uma das quatro, repete:

1. **Páginas → Adicionar nova**
2. Título: `Atlântico` (depois `Fogo`, `Mediterrâneo`, `Algarve`)
3. Bloco **HTML personalizado**, e cola o ficheiro correspondente:
   `wordpress/en/atlantico.html`, `fogo.html`, `mediterraneo.html`,
   `algarve.html`
4. **No painel da direita**, procura **Atributos da página** (*Page
   Attributes*). No campo **Superior** (*Parent*), escolhe **Gastronomic**
5. Confirma que o slug é `atlantico`, `fogo`, `mediterraneo` ou `algarve`
6. **Publicar**

### 4.1 Confirma

Abre `https://vilalara.com/en/gastronomic/` e clica em **More information** numa
das noites. Deve levar-te à página certa. Lá em baixo, o **Back to events** deve
trazer-te de volta.

---

# PARTE 5. As outras quatro línguas

Repete a Parte 3 e a Parte 4, trocando a pasta e o slug da hub:

| Língua | Pasta | Slug da hub |
|---|---|---|
| Português | `wordpress/pt/` | `gastronomico` |
| Espanhol | `wordpress/es/` | `gastronomico` |
| Alemão | `wordpress/de/` | `gastronomisch` |
| Francês | `wordpress/fr/` | `gastronomique` |

Os slugs das quatro noites são sempre os mesmos: `atlantico`, `fogo`,
`mediterraneo`, `algarve`.

**Atenção:** ao criar uma página em espanhol, o WordPress tem de estar com o
idioma espanhol selecionado. No editor, do lado direito, há uma caixa do WPML
onde escolhes a língua da página. Se não a vires, cria a página normalmente e
depois usa o passo seguinte para a associar.

---

# PARTE 6. Ligar as traduções

Sem isto, o seletor de línguas do cabeçalho manda as pessoas para a homepage em
vez da versão traduzida.

1. **WPML → Gestão de traduções**
2. Encontra a página `Gastronomic`
3. Liga-lhe as versões `Gastronómico`, `Gastronomisch` e `Gastronomique` como
   traduções da mesma página
4. Repete para cada uma das quatro noites

---

# E se eu não tiver acesso ao alojamento

A Parte 1 precisa mesmo de alguém que consiga pôr ficheiros no servidor. Sem
isso, as imagens e o CSS não têm onde viver.

Duas saídas:

- **Pede a quem gere o site.** Manda-lhe o `1-CARREGAR-NO-TEMA.zip` e diz:
  *"extrair dentro de `/wp-content/themes/vilalara/`, fica uma pasta
  `gastronomic`"*. São dois minutos de trabalho para quem tem o acesso.
- **Ou diz-me**, e faço uma versão diferente das páginas em que o CSS vai
  dentro da própria página e as imagens ficam na Biblioteca de Media do
  WordPress. Fazes tudo sozinha sem tocar no servidor, mas fica menos limpo e
  cada alteração de estilo obriga a mexer nas 25 páginas.

---

# Quando alguma coisa correr mal

| O que vês | O que é |
|---|---|
| Página sem cores nem alinhamento, texto encostado à esquerda | O CSS não carrega. Parte 2, ou o slug da página não está na lista do snippet |
| Texto certo mas sem fotografias | A pasta `gastronomic` não ficou no sítio certo. Parte 1.7 |
| Dois cabeçalhos Vilalara na mesma página | Colaste um ficheiro da pasta errada. Usa sempre os de `wordpress/`, nunca os de `en/` ou `pt/` |
| O endereço fica `/gastronomic/fogo` sem o `/en/` | Falta o WPML associar a página à língua |
| Mudei o CSS e não vejo diferença | `Ctrl+Shift+R` no browser. O snippet já usa `filemtime`, que resolve isto sozinho |

---

# Ainda por preencher

Nada disto impede publicar. Podes fazer tudo agora e completar depois.

- **Botão Menu** aponta para `#`. Falta o link do menu de cada noite
- **Hora e número de lugares** nos fechos, onde está `[HORA]` e `[N]`
- **Uma linha sobre cada chef**, onde cozinha hoje
- **Revisão nativa** do espanhol, alemão e francês
- **Book your table** aponta para o motor de reservas de quartos. Se estes
  jantares se reservam por outra via, é preciso mudar
