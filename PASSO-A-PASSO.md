# Publicar no WordPress, passo a passo

Escrito para quem nunca fez isto. Segue pela ordem. Se alguma coisa não bater
certo com o que vês no ecrã, para e diz, não avances por adivinhação.

**Só precisas de:** utilizador **administrador** no WordPress de vilalara.com.
Não é preciso acesso ao servidor nem ao alojamento.

**Tempo:** cerca de 20 minutos para a primeira língua, 10 para cada uma das
outras.

---

## O endereço final

Landing page própria, separada da página *Gastronomy* que já existe. É um
evento, com princípio e fim, não uma secção do site.

| Língua | Endereço do evento |
|---|---|
| EN | `/en/gastronomic-september/` |
| PT | `/pt/setembro-gastronomico/` |
| ES | `/es/septiembre-gastronomico/` |
| DE | `/de/gastronomischer-september/` |
| FR | `/fr/septembre-gastronomique/` |

São duas palavras para não se confundir com a página *Gastronomy*. Um
`gastronomic` sozinho, ao lado de um `gastronomy`, lê-se como gralha dele.

Cada uma das quatro noites fica por baixo, por exemplo
`/en/gastronomic-september/fogo/`. Os slugs das noites são sempre `atlantico`,
`fogo`, `mediterraneo`, `algarve`, em todas as línguas, porque são nomes
próprios.

São 5 páginas por língua, 25 no total.

---

# PARTE 1. As imagens

**Já está feito.** As 90 fotografias estão na Biblioteca de Media, e os blocos já
apontam para lá. Não tens de mexer em nada.

> **Porque é que cada foto aparece três vezes?**
> Cada fotografia existe em três larguras, por exemplo `-400`, `-760` e `-1130`.
> O browser escolhe sozinho: o telemóvel puxa a pequena, o ecrã grande puxa a
> maior. É isto que faz a página abrir depressa no telemóvel sem ficar
> desfocada no portátil. **Não apagues as pequenas.**

---

# PARTE 2. O CSS e o JavaScript

Isto faz-se **uma vez só** e serve as 25 páginas.

### 2.1 O CSS

**WPCode → Add Snippet → Add Your Custom Code**

- Tipo de código: **CSS Snippet**
- Título: `Gastronomy September - CSS`
- Cola o conteúdo do ficheiro `wordpress/snippet-1-css.txt`, inteiro
- Insert Method: **Auto Insert**
- Location: **Site Wide Header**
- **Save Changes**, e liga o interruptor para **Active**

### 2.2 O JavaScript

Outro snippet, da mesma maneira:

- Tipo de código: **JavaScript Snippet**
- Título: `Gastronomy September - JS`
- Cola o `wordpress/snippet-2-js.txt`
- Auto Insert, **Site Wide Footer**
- Save e Active

### Não te assustes com o "Site Wide"

O WPCode Lite não deixa escolher páginas, só site inteiro. Isto quer dizer que o
CSS carrega em todas as páginas do site, mas **todas as regras estão presas à
classe `.gs`**, que só existe nestas 25 páginas. O resto do site não é tocado.
O build tem um teste que rebenta se alguma regra escapar dessa classe.

São 21 KB. Não se nota.

---

# PARTE 3. Criar a primeira página

Vamos fazer **só o inglês** primeiro. Confirmas que está bem, e só depois
repetes para as outras quatro.

### 3.1

**Páginas → Adicionar nova**

### 3.2

Título: `Gastronomic September`

### 3.3 Colar o conteúdo

Precisas de colar HTML em bruto, não texto normal.

**Se o editor for o moderno (blocos):**

1. Clica no **+** para adicionar um bloco
2. Procura por **HTML personalizado** (*Custom HTML*)
3. Cola lá dentro

**Se o editor for o clássico:**

1. Em cima à direita da caixa de texto há dois separadores: *Visual* e *Texto*
2. Clica em **Texto**
3. Cola

### 3.4

O que colar: abre o ficheiro **`wordpress/en/index.html`** num editor de texto
(o Bloco de Notas serve), `Ctrl+A` para selecionar tudo, `Ctrl+C`, e cola na
caixa.

É o ficheiro inteiro. Não tens de procurar nada lá dentro nem apagar nada.

### 3.5 O slug

No painel da direita, secção **Ligação permanente** (*Permalink*), confirma que
o slug é **`gastronomic-september`**.

Deixa o campo **Superior** (*Parent*), em Atributos da página, **vazio**. Esta é
uma página independente, não uma filha da *Gastronomy*.

O endereço mostrado por baixo do título deve ficar
`vilalara.com/en/gastronomic-september/`.

### 3.6

**Publicar**. Depois **Ver página**.

### 3.7 O que deves ver

Fundo em areia no topo, **GASTRONOMY** grande com *Setembro* por baixo em
manuscrito, uma linha fina, o texto de introdução, e o menu com as quatro noites
e as datas. A seguir, quatro faixas alternadas com fotografia de um lado e texto
do outro.

Se aparecer tudo desalinhado e sem cores, o CSS não está a carregar. Volta à
Parte 2 e confirma que o snippet está mesmo **Active**.

---

# PARTE 4. As quatro noites

Cada noite é uma página **filha da Gastronomic September** que acabaste de
criar. É isso que faz o endereço ficar `/en/gastronomic-september/fogo/`.

Para cada uma das quatro, repete:

1. **Páginas → Adicionar nova**
2. Título: `Atlântico`, depois `Fogo`, `Mediterrâneo`, `Algarve`
3. Bloco **HTML personalizado**, e cola o ficheiro correspondente:
   `wordpress/en/atlantico.html`, `fogo.html`, `mediterraneo.html`,
   `algarve.html`
4. **Atributos da página → Superior**: escolhe **Gastronomic September**
5. Slug: `atlantico`, `fogo`, `mediterraneo` ou `algarve`. Sem acentos
6. **Publicar**

### 4.1 Confirma

Abre `https://vilalara.com/en/gastronomic-september/` e clica em **More
information** numa das noites. Deve levar-te à página certa. Lá em baixo, o
**Back to events** deve trazer-te de volta.

---

# PARTE 5. As outras quatro línguas

Repete a Parte 3 e a Parte 4, trocando a pasta, o título e o slug:

| Língua | Pasta dos ficheiros | Título | Slug |
|---|---|---|---|
| Português | `wordpress/pt/` | Setembro Gastronómico | `setembro-gastronomico` |
| Espanhol | `wordpress/es/` | Septiembre Gastronómico | `septiembre-gastronomico` |
| Alemão | `wordpress/de/` | Gastronomischer September | `gastronomischer-september` |
| Francês | `wordpress/fr/` | Septembre Gastronomique | `septembre-gastronomique` |

O campo **Superior** fica vazio nas cinco hubs. Só as noites é que têm superior.

Os slugs das quatro noites são sempre os mesmos em todas as línguas.

**Atenção:** ao criar uma página em espanhol, o WPML tem de estar com o espanhol
selecionado. No editor, do lado direito, há uma caixa do WPML onde escolhes a
língua da página.

---

# PARTE 6. Ligar as traduções

Sem isto, o seletor de línguas do cabeçalho manda as pessoas para a homepage em
vez da versão traduzida.

1. **WPML → Gestão de traduções**
2. Encontra a página `Gastronomic September`
3. Liga-lhe as versões `Setembro Gastronómico`, `Septiembre Gastronómico`,
   `Gastronomischer September` e `Septembre Gastronomique` como traduções da
   mesma página
4. Repete para cada uma das quatro noites

---

# Quando alguma coisa correr mal

| O que vês | O que é |
|---|---|
| Página sem cores nem alinhamento, texto encostado à esquerda | O snippet do CSS não está Active, ou não ficou em Site Wide Header |
| Texto certo mas sem fotografias | Alguma imagem foi apagada da Biblioteca de Media |
| Os pontos do carrossel não fazem nada | Falta o snippet do JavaScript, Parte 2.2 |
| O endereço fica `/en/gastronomic-september-2/` | Já existe uma página com esse slug. Apaga a antiga do lixo, ou muda o `SLUG` no `content.py` e diz-me |
| *More information* dá 404 | O slug da noite não é `atlantico`, `fogo`, `mediterraneo` ou `algarve`, ou falta pôr a hub no campo **Superior** |
| Dois cabeçalhos Vilalara na mesma página | Colaste um ficheiro da pasta errada. Usa sempre os de `wordpress/`, nunca os de `en/` ou `pt/` |
| Mudei o CSS e não vejo diferença | `Ctrl+Shift+R` no browser |

---

# Ainda por preencher

Nada disto impede publicar. Podes fazer tudo agora e completar depois.

- **Botão Menu** aponta para `#`. Falta o link do menu de cada noite
- **Hora e número de lugares** nos fechos, onde está `[HORA]` e `[N]`
- **Uma linha sobre cada chef**
- **Revisão nativa** do espanhol, alemão e francês
- **Book your table** aponta para o motor de reservas de quartos. Se estes
  jantares se reservam por outra via, é preciso mudar
