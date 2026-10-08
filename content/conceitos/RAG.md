---
title: "RAG"
tags:
  - "conceito"
  - "rag"
tipo: "conceito"
date: "2026-10-01"
---

# RAG

> **Definição em uma frase:** técnica que recupera documentos relevantes e os coloca na janela de contexto, para que o modelo responda com base na fonte em vez de na memória paramétrica.

## Mecanismo

```mermaid
flowchart LR
 A[Corpus] --> B[Chunking]
 B --> C[Embeddings]
 C --> D[Índice vetorial]
 Q[Query] --> E[Embedding]
 E --> F[Busca híbrida<br/>BM25 + vetorial]
 D --> F
 F --> G[Reranking<br/>cross-encoder]
 G --> H[Contexto no prompt]
 H --> I[LLM]
```

## Por que funciona

Porque separa **onde o conhecimento mora** de **como ele é usado**:

| | Conhecimento nos parâmetros | Conhecimento no contexto |
| --- | --- | --- |
| Atualizar | re-treinar | **trocar o índice** |
| Citar fonte | não | **sim** |
| Frescor | meses/anos | imediato |
| Verificar | impossível | possível |

## Decisões que importam mais que o modelo

1. **Chunking** — tamanho e sobreposição. Chunk grande demais: ruído e custo. Pequeno demais: perde contexto. Ver [[Chunking]].
2. **Busca** — híbrida (BM25 + vetorial) cobre os dois pontos cegos estruturais.
3. **Reranking** — embeddings são bons em *recall*, imprecisos no ranking fino. Cross-encoder reordena os 50–100 candidatos.
4. **Ordenação no prompt** — evidência relevante nas pontas, nunca no meio. Ver [[Lost in the Middle]].
5. **k (quantos chunks)** — cada um é token cobrado. Ver [[Janela de Contexto]].

## Quando RAG **não** é a resposta

| Necessidade | Melhor ferramenta |
| --- | --- |
| conhecimento factual atualizado | **RAG** |
| tom/formato/estrutura fixos | [[Fine-tuning]] |
| tarefa nova com muitas exemplos rotulados | [[Fine-tuning]] |
| capacidade nova (cálculo, acesso a rede) | **ferramentas** |
| conhecimento mutável e pessoal | memória externa / RAG |

Usar fine-tuning para ensinar fato é caro e desatualiza. Usar RAG para ensinar formato é desperdício de tokens.

## Autoavaliação
1. **P:** Por que RAG não altera os pesos? **R:** o mecanismo de atenção trata os tokens do contexto como parte da sequência, lendo-os na inferência. Nenhum gradiente é calculado.
2. **P:** RAG pode piorar a resposta? **R:** sim — contexto irrelevante e posição ruim podem piorar (lost in the middle). Retrieval é uma etapa com métrica própria, não um detalhe.

## Onde vi isso

- Visto em: [[O que é um LLM]], [[Embeddings e vetorização]]

## Ver também

- [[Embedding]] · [[Busca Semântica]] · [[Chunking]] · [[Fine-tuning]]

---
*Atualizado em 2026-09-30*

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
