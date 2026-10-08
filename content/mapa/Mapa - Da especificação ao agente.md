---
title: "Mapa - Da especificação ao agente"
tags:
  - "mapa"
tipo: "mapa"
date: "2026-10-15"
---

# Mapa — Da especificação ao agente

> **Síntese do módulo.** Este mapa é o entregável final: se você conseguir
> redesenhar de memória e explicar cada aresta, o módulo está consolidado.

## O pipeline completo

```mermaid
flowchart TD
 subgraph P["1 · Processo"]
 AMB["Ambiente<br/>git · credencial · verificação"]
 SPEC["Spec<br/>requisitos · critérios · fora de escopo"]
 AMB --> SPEC
 end

 subgraph I["2 · Instrução"]
 PR["Prompt<br/>papel · tarefa · contexto · formato"]
 SK["Skills<br/>description gatilho · corpo sob demanda"]
 end

 subgraph E["3 · Execução"]
 OC["OpenCode<br/>loop: ler → agir → observar"]
 REV["Revisão humana do diff"]:::humano
 end

 subgraph G["4 · Projeto guiado"]
 N8N["N8N<br/>grafo · payload · caminho de erro"]
 MAS["Mastra<br/>agent · tools tipadas (zod)"]
 UI["Plataforma de avaliação"]
 end

 SPEC --> PR
 SPEC --> OC
 PR --> OC
 SK --> OC
 OC --> REV
 REV -->|"bate com a spec"| UI
 REV -->|"divergiu"| SPEC
 N8N -->|"precisa decidir"| MAS
 MAS -->|"ação chamada"| N8N
 N8N --> UI

 classDef humano fill:#fde68a,stroke:#b45309,color:#111
```

## Onde cada conceito entra

| Conceito | Papel no pipeline | Falha típica se ele faltar |
| --- | --- | --- |
| [[Ambiente de Desenvolvimento com IA]] | base: retorno e verificação | sem saber de onde veio o vermelho |
| [[Spec-Driven Development]] | direção antes da geração | agente supõe, humano conserta depois |
| [[Prompt Engineering - fundamentos]] | contrato da instrução pontual | resposta genérica, formato errado |
| [[Agent Skills]] | conhecimento reutilizável sob demanda | preferências repetidas toda sessão |
| [[OpenCode]] | executor do loop no terminal | — (é a ferramenta, não o método) |
| [[Desenvolvimento de Software com IA]] | o ciclo completo, humano no portão | *vibe coding* incansável |
| [[N8N]] | orquestração determinística do projeto | lógica de negócio escondida em código |
| [[Mastra]] | cérebro do agente: decisões e tools | alucinação de argumento, efeito sem contrato |

## Para redesenhar de memória

1. Desenhe o fluxo **Processo → Instrução → Execução** com as arestas de
 retroalimentação (o que volta para a spec quando a revisão diverge).
2. Onde entra o **custo de contexto** nesse desenho? (dica: níveis 1–3 das
 skills, histórico do agente)
3. Ligue **N8N ↔ Mastra** explicando o contrato de cada lado (chamada e retorno).
4. Marque os **3 pontos de verificação humana** do pipeline inteiro.
5. Sem olhar: qual falha cada conceito previne? (tabela acima é o gabarito)

## Ver também

- [[Desenvolvimento de Software com IA]] · [[Spec-Driven Development]]
- [[N8N]] · [[Mastra]] · [[Agent Skills]]

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
