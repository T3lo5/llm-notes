# llm-notes

Notas de estudo sobre LLMs, publicadas como site estático. O conteúdo vem de um
vault do Obsidian; o vault é a fonte da verdade, o site é uma projeção limitada ao
que é publicável.

Gerado com [Quartz 5](https://quartz.jzhao.xyz). Deploy via GitHub Pages, sem custo.

## Como funciona

```
vault Obsidian
   │  scripts/exportar.py
   ├─► content/conceitos/      24 fichas de conceito
   ├─► content/pesquisas/       6 pesquisas
   ├─► content/labs/            4 labs com código
   ├─► content/papers/          8 fichas de paper
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

O vault fica em `~/Documentos/coders-pos/coders-pos` por padrão. Para usar outro
caminho, exporta a variável antes do sync:

```bash
CODERS_VAULT=/caminho/do/vault npm run sync
```

## O que entra no site

Definido no topo de `scripts/exportar.py`, em `PUBLIC_DIRS` e `PUBLIC_FILES`.

## O que não entra

- `01 - Diário/`
- Trabalhos e micro-capstones
- Notas que reproduzem conteúdo da pós-graduação
- O plano de leitura por módulo do curso
- Qualquer arquivo com credencial ou dado pessoal

Wikilinks para notas fora do site são convertidos em texto simples
automaticamente, então não há link quebrado e o site não revela a estrutura do
curso. Referências a aulas escritas em prosa ("ver aula 22") viram link para o
conceito equivalente, que é o que o leitor do site precisa. O exportador reporta
quantos fez isso a cada execução.

Para incluir uma pasta nova no site, acrescente a `PUBLIC_DIRS` e confira a
contagem de links convertidos no output. Se subir de repente, provavelmente
alguma nota do curso entrou por engano.

## Onde a exclusão é decidida

O `NEVER` no topo do exportador é o filtro mais forte: bloqueia por nome, mesmo
que a pasta esteja na lista. `Índice de papers.md` está lá porque é o plano de
leitura do curso — traz a trilha dos 12 módulos e o que cada um exige. É
organização do curso, não conteúdo técnico.

## Banco de questões

`quartz/static/dados/questions.json` é gerado a partir de dois bancos no vault,
que usam formatos diferentes:

- **M00** — lista numerada, com gabarito em tabela `| N | resposta |`.
- **M01** — headings `### Qn · \`D\` · [[Aula ...]]`, com nível de dificuldade.

O exportador detecta o formato pelo heading e normaliza para o mesmo JSON. Campos
por questão: `id`, `modulo`, `numero`, `nivel`, `aula`, `enunciado`, `detalhes`,
`resposta`, `origem`.

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
