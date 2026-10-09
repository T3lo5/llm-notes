---
title: "Mapa - Funcionamento de LLMs"
tags:
  - "mapa"
tipo: "mapa"
date: "2026-10-14"
---

# Mapa — Funcionamento de LLMs


## O pipeline completo

```mermaid
flowchart TD
    A["Texto do usuário"] --> B["Tokenizador<br/>BPE / Unigram"]
    B --> C["IDs + posições"]
    C --> D["Embeddings<br/>ID -> vetor denso"]
    D --> E["N blocos Transformer"]
    E --> E1["Self-Attention causal<br/>softmax(QK^T/sqrt(d_k))V"]
    E --> E2["MLP / SwiGLU"]
    E1 --> F["Residual + RMSNorm"]
    E2 --> F
    F -->|"repite N vezes"| E
    F --> G["Projeção final<br/>-> logits sobre V tokens"]
    G --> H["Temperatura"]
    H --> I["Top-k / Top-p / min-p"]
    I --> J["Penalidades"]
    J --> K["Softmax"]
    K --> L{"Amostrar token"}
    L --> M["EOS ou max_tokens?"]
    M -->|nao| C
    M -->|sim| N["Detokenizador"]
    N --> A
```

## Áreas temáticas

```mermaid
mindmap
  root((Funcionamento<br/>de LLMs))
    Representacao
      Token
      Subpalavra / BPE
      Embedding
      Cosseno
      Positional Encoding / RoPE
    Arquitetura
      Transformer
      Self-Attention
      Multi-head
      Mascara causal
      RMSNorm
      SwiGLU
      MLP
    Inferencia
      Prefill
      Decode
      KV Cache
      TTFT vs tokens/s
      Quantizacao
      Speculative decoding
    Amostragem
      Logits
      Temperatura
      Top-k
      Top-p
      Min-p
      Greedy vs beam
      Penalidades
    Engenharia
      Janela de contexto
      Prompt engineering
      Lost in the middle
      Prompt injection
      RAG
      Alucinacao
      Avaliacao
```

## Relações que valem memorizar

```mermaid
graph LR
    T["Tokenização"] -->|"mais tokens = mais caro<br/>e mais lento"| J["Janela de Contexto"]
    J -->|"cabe tudo aqui"| R["RAG"]
    J --> L["Lost in the Middle"]
    E["Embeddings"] --> R
    E -->|"cosseno"| B["Busca Semântica"]
    B -->|"candidatos"| RR["Reranking"]
    RR --> R
    R --> A["Alucinação"]
    K["KV Cache"] -->|"memória no decode"| P["Prefill vs Decode"]
    LG["Logits"] --> TEM["Temperatura"]
    TEM --> TP["Top-p"]
    TP -->|"amostra"| OUT["Saída não determinística"]
    NF["Não-associatividade FP"] -->|"batch muda tudo"| OUT
```

## As perguntas que este site tenta responder

| # | Pergunta | Onde está |
| --- | --- | --- |
| 1 | Como o texto vira tokens, e por isso custa dinheiro? | [[Tokens: o significado dos números]] |
| 2 | Como o significado vira geometria? | [[Embeddings e vetorização]] |
| 3 | Como cada token "lê" o contexto inteiro? | [[Arquitetura Transformers e Attention]] |
| 4 | Por que a mesma pergunta dá respostas diferentes? | [[Temperatura e previsibilidade]] |
| 5 | Como um token vira o próximo token? | [[Nota Técnica - Geração token a token]] |
| 6 | Por que a ordem no prompt importa? | [[Engenharia de prompt e contexto]] |

## Conceitos-chave (20 neste mapa)

**Representação** — [[Token]] · [[Embedding]] · [[Similaridade de Cosseno]] · [[Positional Encoding]]
**Arquitetura** — [[Transformer]] · [[Self-Attention]]
**Inferência** — [[KV Cache]] · [[Prefill]] · [[Janela de Contexto]]
**Decodificação** — [[Logits]] · [[Temperatura]] · [[Top-p Sampling]] · [[Top-k Sampling]] · [[Perplexidade]]
**Engenharia** — [[Alucinação]] · [[RAG]] · [[Busca Semântica]] · [[Modelo Base]] · [[Lost in the Middle]] · [[Prompt Injection]]

## Labs disponíveis

```mermaid
flowchart LR
    L1["Lab 01<br/>tokens e custo"] --> L2["Lab 02<br/>embeddings"]
    L2 --> L3["Lab 03<br/>atenção"]
    L3 --> L4["Lab 04<br/>sampling"]
    L4 --> Q["Banco de questões"]
```

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
