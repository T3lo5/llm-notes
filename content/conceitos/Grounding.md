---
title: "Grounding"
tags:
  - "conceito"
  - "riscos"
  - "rag"
tipo: "conceito"
date: "2026-10-26"
---

# Grounding

> **Definição em uma frase:** ancorar a resposta em **dados verificáveis externos ao
> modelo**, para que ela venha da fonte e não da memória paramétrica.

## Por que funciona

Porque troca **onde o conhecimento mora**:

| | Sem grounding | Com grounding |
| --- | --- | --- |
| Origem do fato | parâmetros do modelo (possivelmente inventado) | documento recuperado agora |
| Atualização | re-treinar | trocar o índice |
| Citação | impossível | natural |
| Verificação | impossível | comparável com a fonte |

## O caminho

```mermaid
flowchart LR
    Q[Pergunta] --> B[Busca híbrida<br/>BM25 + vetorial]
    C[Corpus] --> B
    B --> R[Reranking]
    R --> CTX[Contexto com citação]
    CTX --> L[LLM]
    L --> RES[Resposta ancorada<br/>ou recusa]
```

Os quatro passos que importam:

1. **Recuperar** o trecho relevante (busca híbrida — ver [[Busca Semântica]]).
2. **Reranking** — embeddings são bons em *recall*, imprecisos no ranking fino.
3. **Citar** — cada claim da resposta aponta para o trecho que a sustenta.
4. **Recusar** — sem evidência no contexto, a saída é "não consta", não invenção.

## O teste do grounding

> **Apague o contexto recuperado. A resposta muda?**
> Se não muda, a resposta não estava ancorada — saiu do modelo.

É o teste mais barato que existe e pega o erro mais comum: **grounding parcial**, em que
a resposta tem cara de ancorada (fala em "o documento diz") mas os números e nomes
saíram da memória do modelo.

## Falhas de grounding

| Falha | Como aparece | Mitigação |
| --- | --- | --- |
| Recuperação errada | resposta ancorada no trecho errado | reranking, mais candidatos, query melhor |
| Contexto no meio | evidência existe mas é ignorada | posição nas pontas (ver [[Lost in the Middle]]) |
| Contexto irrelevante | ruído distorce a resposta | filtrar por relevância e por chunking (ver [[Chunking]]) |
| Sem recusa | inventa quando não há evidência | instrução de "não consta" + checagem de cobertura |
| Fonte desatualizada | ancorado em documento velho | frescor do corpus |

## Relação com alucinação

Grounding **reduz** alucinação, não elimina: ele transfere a fonte da verdade do modelo
para o corpus. Se o corpus não tem o fato, o grounding nada faz — e ainda pode dar
segurança falsa ao usuário (resposta com citação errada é pior que resposta sem
citação). Ver [[Alucinação]] e [[RAG]].

## Autoavaliação
1. **P:** Como se prova que uma resposta está grounded? **R:** apagando o contexto e
   vendo se a resposta muda, ou conferindo cada claim contra o trecho citado.
2. **P:** Por que RAG não elimina a alucinação? **R:** o grounding transfere a fonte
   para o corpus; se o corpus não cobre o fato, o modelo continua respondendo do
   nada — e a citação cria confiança falsa.

## Onde vi isso

- Visto em: [[Riscos e falhas em projetos de IA]], [[Moderação de conteúdo com IA]]

## Ver também

- [[RAG]] · [[Busca Semântica]] · [[Chunking]] · [[Lost in the Middle]] · [[Alucinação]] · [[Evals]]

<script>
// Correcao do Mermaid no Quartz 5.0.0.
(() => {
  const CDN =
    "https://cdnjs.cloudflare.com/ajax/libs/mermaid/11.4.0/mermaid.esm.min.mjs";
  let proximo = 0;
  let tentativas = 0;

  const vazios = () =>
    [...document.querySelectorAll("code.mermaid")].filter((n) => {
      const svg = n.querySelector("svg");
      return svg && svg.querySelectorAll("path,rect,polygon,circle").length === 0;
    });

  const fonte = (n) =>
    (n.getAttribute("data-clipboard") || "")
      .replace(/^"|"$/g, "")
      .replace(/\\"/g, '"')
      .replace(/\\n/g, "\n")
      .replace(/&lt;/g, "<")
      .replace(/&gt;/g, ">")
      .replace(/\\\\/g, "\\");

  // As cores do tema vao em CSS vars; o plugin do Mermaid usa exatamente
  // estas. O padrao cobre o caso de a cor nao estar no quartz.config.yaml —
  // `--highlight: undefined` e o que derrubava o render original.
  const cor = (nome, padrao) => {
    const v = getComputedStyle(document.documentElement)
      .getPropertyValue(nome)
      .trim();
    return v && v !== "undefined" ? v : padrao;
  };

  const configuracao = () => {
    const escuro =
      document.documentElement.getAttribute("saved-theme") === "dark";
    return {
      startOnLoad: false,
      securityLevel: "loose",
      theme: escuro ? "dark" : "base",
      themeVariables: {
        fontFamily: cor("--codeFont", "monospace"),
        primaryColor: cor("--light", escuro ? "#1b1b19" : "#fdfdfc"),
        primaryTextColor: cor("--darkgray", escuro ? "#b0aca3" : "#4c4a45"),
        primaryBorderColor: cor("--tertiary", escuro ? "#c8b073" : "#8a7a4f"),
        lineColor: cor("--gray", escuro ? "#6e6b64" : "#b4b0a8"),
        secondaryColor: cor("--secondary", escuro ? "#7fc4a5" : "#1f5f4e"),
        tertiaryColor: cor("--tertiary", escuro ? "#c8b073" : "#8a7a4f"),
        clusterBkg: cor("--light", escuro ? "#1b1b19" : "#fdfdfc"),
        edgeLabelBackground: cor("--highlight", escuro ? "#3a3a36" : "#e8e6e1"),
      },
    };
  };

  const corrigir = (alvo) => {
    import(CDN)
      .then((m) => {
        m.default.initialize(configuracao());
        return Promise.all(
          alvo.map(async (n) => {
            try {
              const { svg } = await m.default.render(
                "corrige-" + proximo++,
                fonte(n),
              );
              n.innerHTML = svg;
            } catch (e) {
              console.warn("mermaid: falhou um diagrama", fonte(n).slice(0, 40), e);
            }
          })
        );
      })
      .then(ajustar)
      .catch((e) => console.warn("mermaid: CDN indisponivel", e));
  };

  // --------------------------------------------------------- contraste
  const rgb = (v) => {
    const m = (v || "").match(/[\d.]+/g);
    if (!m || m.length < 3) return null;
    const a = m.length > 3 ? Number(m[3]) : 1;
    return a === 0 ? null : [Number(m[0]), Number(m[1]), Number(m[2])];
  };

  const luminancia = (c) => {
    const f = (x) => {
      x /= 255;
      return x <= 0.03928 ? x / 12.92 : Math.pow((x + 0.055) / 1.055, 2.4);
    };
    return 0.2126 * f(c[0]) + 0.7152 * f(c[1]) + 0.0722 * f(c[2]);
  };

  const contraste = (a, b) => {
    const la = luminancia(a);
    const lb = luminancia(b);
    return (Math.max(la, lb) + 0.05) / (Math.min(la, lb) + 0.05);
  };

  // O Mermaid monta as cores das secoes do mindmap a partir de
  // --secondary/--tertiary escurecidas 25% — em tema claro vira fundo preto
  // (ou marrom escuro) com texto escuro por cima: 1.4:1 de contraste. O texto
  // ja vem na cor certa do tema; entao o fundo do no e que cede: clareia
  // (tema claro) ou escurece (tema escuro) ate bater 4.5:1.
  const ajustar = () => {
    const alvo =
      document.documentElement.getAttribute("saved-theme") === "dark"
        ? [0, 0, 0]
        : [255, 255, 255];
    document
      .querySelectorAll("code.mermaid svg .mindmap-node")
      .forEach((g) => {
        const texto = g.querySelector("text");
        // a caixa visivel e path.node-bkg; rect.background existe tambem mas
        // vem com 0x0 (serve so de ancora do rotulo) — tem que achar a forma
        // com area de verdade, senao o ajuste cai no elemento errado.
        const formas = [
          ...g.querySelectorAll(
            "path.node-bkg, path.node-circle, rect.background, ellipse, circle, polygon",
          ),
        ];
        let forma = null;
        let melhor = -1;
        for (const f of formas) {
          const b = f.getBoundingClientRect();
          const area = b.width * b.height;
          if (area > melhor) {
            melhor = area;
            forma = f;
          }
        }
        if (!texto || !forma || melhor <= 0) return;
        const t = rgb(getComputedStyle(texto).fill);
        let f = rgb(getComputedStyle(forma).fill);
        if (!t || !f || contraste(t, f) >= 4.5) return;
        for (let i = 0; i < 12 && contraste(t, f) < 4.5; i++) {
          f = f.map((v, k) => v + (alvo[k] - v) * 0.4);
        }
        f = f.map((v) => Math.round(v));
        forma.style.fill = "rgb(" + f.join(", ") + ")";
        // o sublinhado do no vinha na cor de contraste do fundo antigo
        const linha = g.querySelector("line");
        if (linha) {
          const l = rgb(getComputedStyle(linha).stroke);
          if (!l || contraste(l, f) < 3) {
            linha.style.stroke = "rgb(" + t.join(", ") + ")";
          }
        }
      });
  };

  // Tenta varias vezes: o SVG do Quartz pode aparecer depois do DOMContentLoaded.
  // O reset fica em observar(), senao a recursao re zerava a contagem.
  const agendar = (atraso) => {
    setTimeout(() => {
      ajustar();
      const alvo = vazios();
      if (alvo.length > 0) {
        tentativas = 0;
        return corrigir(alvo);
      }
      if (tentativas++ < 40) agendar(500);
    }, atraso);
  };

  const observar = (atraso) => {
    tentativas = 0;
    agendar(atraso);
  };

  if (document.readyState === "complete") observar(1500);
  else window.addEventListener("load", () => observar(1500));

  // No troque de tema o Quartz re-renderiza os diagramas com as cores novas;
  // se o render dele falhar de novo, aqui entra. O atraso deixa o do Quartz
  // terminar antes, para nao ser sobrescrito em seguida.
  document.addEventListener("themechange", () => observar(2000));
})();
</script>
