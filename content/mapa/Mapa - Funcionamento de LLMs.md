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
| 1 | Como o texto vira tokens, e por isso custa dinheiro? |[[Token]] |
| 2 | Como o significado vira geometria? |[[Embedding]] |
| 3 | Como cada token "lê" o contexto inteiro? |[[Transformer]] |
| 4 | Por que a mesma pergunta dá respostas diferentes? |[[Temperatura]] |
| 5 | Como um token vira o próximo token? |[[Self-Attention]] |
| 6 | Por que a ordem no prompt importa? |[[Janela de Contexto]] |

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
    L4 --> Q["Banco de perguntas"]
```

<script>
// Correcao do Mermaid no Quartz 5.0.0.
//
// O Quartz le `innerText` do <code class="mermaid"> para alimentar o Mermaid.
// Em parte dos diagramas esse innerText chega vazio e o render sai como
// <svg><g></g></svg>, sem erro no console. Reproduzido nos 4 blocos do mapa,
// dos quais so o mindmap renderizava.
//
// A correcao espera o SVG existir antes de medir: rodar antes faz o script
// ver zero diagramas e sair cedo. O timeout cobre o caso em que o Mermaid
// nem carregou (CDN bloqueado), para nao esperar para sempre.
(() => {
  const CDN =
    "https://cdnjs.cloudflare.com/ajax/libs/mermaid/11.4.0/mermaid.esm.min.mjs";

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

  const corrigir = (alvo) => {
    import(CDN)
      .then((m) => {
        m.default.initialize({ startOnLoad: false, securityLevel: "loose" });
        return Promise.all(
          alvo.map(async (n, i) => {
            try {
              const { svg } = await m.default.render("corrige-" + i, fonte(n));
              n.innerHTML = svg;
            } catch (e) {
              console.warn("mermaid: falhou um diagrama", fonte(n).slice(0, 40), e);
            }
          })
        );
      })
      .catch((e) => console.warn("mermaid: CDN indisponivel", e));
  };

  // Tenta varias vezes: o SVG do Quartz pode aparecer depois do DOMContentLoaded.
  let tentativas = 0;
  const tentar = () => {
    const alvo = vazios();
    if (alvo.length > 0) return corrigir(alvo);
    if (tentativas++ < 20) setTimeout(tentar, 500);
  };

  if (document.readyState === "complete") setTimeout(tentar, 1500);
  else window.addEventListener("load", () => setTimeout(tentar, 1500));
})();
</script>
