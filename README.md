# llm-notes

Notas de estudo sobre LLMs, publicadas como site estático. O conteúdo vem de um
vault do Obsidian; o vault é a fonte da verdade, o site é uma projeção limitada ao
que é publicável.

Gerado com [Quartz 5](https://quartz.jzhao.xyz). Deploy via GitHub Pages, sem custo.

## Como funciona

```
vault Obsidian
   │  scripts/exportar.py  +  scripts/origem.py (não versionado)
   ├─► content/conceitos/      24 fichas de conceito
   ├─► content/guias/          18 guias em prosa
   ├─► content/pesquisas/       6 pesquisas
   ├─► content/labs/            5 labs com código
   ├─► content/papers/          7 fichas de paper
   ├─► content/mapa/            mapa conceitual
   ├─► content/{index,questoes,sobre}.md
   └─► quartz/static/dados/questions.json   45 questões
        │  npx quartz build
        ▼
      public/                    site estático
```

O exportador **apaga e reescreve** `content/` a cada execução. `content/` é
gerado, não editado. Para mudar conteúdo, muda-se o vault.

Para mudar a página de questões, a home ou a página "sobre", edita-se
`templates/`, que também é copiado para `content/`.

## Uso

```bash
npm install
npm run serve      # build + preview em http://localhost:8080
npm run sync       # exportar do vault + build (use antes de commitar)
npm run check      # typecheck + prettier
```

O exportador precisa de duas coisas que são só da sua máquina: o caminho do
vault, que é privado, e `scripts/origem.py`, que **não é versionado**.

```bash
LLM_NOTES_VAULT=/caminho/do/vault npm run sync
```

Sem a variável o exportador aborta com erro, em vez de gerar um `content/`
quase vazio sem avisar. Sem `scripts/origem.py` ele avisa o que está faltando.

### Por que `origem.py` não está no git

O repositório é público e o material de origem é privado. `origem.py` concentra
tudo que descreve essa origem: os caminhos das pastas no vault, o que entra e o
que sai, e o vocabulário que precisa ser removido do texto antes de publicar.

Um filtro que remove um termo precisa conter o termo — se a regra ficasse em
`exportar.py`, o próprio filtro publicaria o vocabulary que existe para apagar.
Então `exportar.py` guarda só a parte limpa (layout do site, frontmatter, links,
slugs) e importa o resto de `origem.py`.

O arquivo está no seu `.gitignore`.

## O que entra no site

Definido em `scripts/origem.py`: `PUBLICA` e `PUBLICA_ARQUIVOS` para as pastas
comuns, `NOTAS_PUBLICAS` para a seção `guias/`.

## O que não entra

- `01 - Diário/`
- Trabalhos e entregáveis
- Notas que reproduzem material de terceiros
- Planejamentos de leitura
- Qualquer arquivo com credencial ou dado pessoal

Wikilinks para notas fora do site são convertidos em texto simples
automaticamente, então não há link quebrado e o site não expõe a estrutura de
origem do material. Referências escritas em prosa viram link para a nota
equivalente, que é o que o leitor do site precisa. O exportador reporta quantos
fez isso a cada execução.

Para incluir uma pasta nova no site, acrescente a `PUBLICA` e confira a contagem
de links convertidos no output. Se subir de repente, provavelmente alguma nota
que não era pública entrou por engano.

## Onde a exclusão é decidida

O `NUNCA` em `origem.py` é o filtro mais forte: bloqueia por nome, mesmo que a
pasta esteja na lista. `Índice de papers.md` está lá porque é um plano de
leitura, não conteúdo técnico: diz o que ler em cada etapa e o que cada uma exige.

As notas numeradas entram por uma allowlist explícita, `NOTAS_PUBLICAS`, e é a
fronteira de publicação mais sensível do site: ela lista **números**, não
pastas, para que uma nota nova na pasta não entre sozinha. O que ficou de fora
está comentado no arquivo, com o motivo.

## Banco de questões

`quartz/static/dados/questions.json` é gerado a partir de dois bancos no vault,
que usam formatos diferentes:

- **lista numerada**, com gabarito em tabela `| N | resposta |`.
- **headings** `### Qn · \`D\` · [[...]]`, com nível de dificuldade.

O exportador detecta o formato pelo heading e normaliza para o mesmo JSON. Campos
por questão: `id`, `tema`, `numero`, `nivel`, `enunciado`, `detalhes`,
`resposta`, `seq`. `fonte` e `origem` são lidos do vault e descartados na
exportação: os dois identificam de onde o material veio, e o site não precisa
mostrar isso. O campo `tema` guarda um rótulo neutro, suficiente para filtrar.

A página `/questoes` faz `fetch()` desse arquivo. Como é estático, o gabarito
está no próprio JSON e visível no devtools — isso é deliberado num site de
revisão pessoal, não é um banco de prova.

## `content/` vai para o git

`content/` é gerado, mas **é versionado de propósito**. O exportador depende do
vault, que é privado e não vive neste repositório — se `content/` fosse gerado
no CI, o build quebraria. Então o fluxo é: você roda `npm run sync` localmente
e commita o resultado. O CI só executa `npx quartz build`.

O custo disso é que `content/` pode divergir do vault se alguém esquecer o sync.
Por isso o README e a nota do vault mandam rodar o sync antes de `git add`.

## Deploy

`.github/workflows/deploy.yml` faz build e deploy no GitHub Pages a cada push na
`main`. Nas settings do repositório, configure Pages com source **GitHub
Actions** — o workflow não faz essa configuração sozinho.

O site sai em `https://<usuario>.github.io/llm-notes/`, o que confere com o
`baseUrl: "llm-notes"` em `quartz.config.yaml`. Sem build no servidor, sem custo.
