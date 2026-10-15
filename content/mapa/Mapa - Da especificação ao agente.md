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
