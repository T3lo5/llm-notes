---
title: "Vendor lock-in: como evitar?"
tags:
  - "selecao-de-modelos"
  - "vendor-lock-in"
  - "arquitetura"
tipo: "guia"
date: "2026-10-16"
---

# Vendor lock-in: como evitar?

> **Meta:** tratar o vendor lock-in como decisão arquitetural do início do projeto — e conhecer as alavancas concretas que mantêm a troca de modelo sempre possível.


## Resumo em 3 frases

1. **Vendor lock-in em IA** é a dependência de um fornecedor cujo custo de troca ficou proibitivo — e ela nasce de escolhas arquiteturais tomadas **no início do projeto**, não do preço da API.
2. A mitigação é **projetar processos que trocam de modelo**: interface estável de acesso, prompts e dados em formatos portáveis, e evals que validam o substituto antes da troca.
3. Manter a opção de trocar é barato no início e caríssimo depois — por isso lock-in é **decisão de arquitetura de software**, com padrões de projeto conhecidos.

## De onde vem o lock-in

| Forma de lock-in | O que prende |
| --- | --- |
| API proprietária | endpoint, SDK, autenticação e limites próprios de cada provedor |
| Formato de prompt | instruções calibradas para o comportamento de um modelo específico |
| Embeddings presos | vetor gerado por um modelo não serve para busca de outro (ver [[Embedding]]) |
| Fine-tuning preso | pesos ajustados num provedor não migram para outro |
| Ferramentas e saída estruturada | recursos (tools, structured output) com semântica própria |

## Por que decidir no início

O custo de troca **cresce com o tempo**: dados acumulados no formato do provedor, prompts reescritos em volta do comportamento de um modelo, produto inteiro montado em torno de respostas de um único modelo. Cada mês de uso aumenta o trabalho da troca; a arquitetura que permite trocar, uma vez feita, custa quase nada.

```mermaid
flowchart LR
    A[Produto] --> B[Camada de acesso<br/>interface estável]
    B --> C{Gateway / router}
    C --> D[Modelo A]
    C --> E[Modelo B]
    C --> F[Modelo C]
```

## Alavancas de mitigação

| Alavanca | O que faz |
| --- | --- |
| **Interface única (adaptador)** | o produto fala com uma interface; quem conhece os provedores é a camada de acesso — padrão **Adapter/Port** |
| **Camada anticorrupção** | traduz semântica do provedor para o seu modelo de domínio — padrão **Anti-corruption layer** |
| **Prompts genéricos e versionados** | instrução escrita para a *tarefa*, não para os modismos de um modelo; versionamento permite comparar versões |
| **Dados portáveis** | histórico, cache e vetores exportáveis; evitar que a base de conhecimento só exista dentro do provedor |
| **Evals de troca** | uma suite de testes que o substituto precisa passar — é o que transforma "trocar é possível" em "trocar é comprovado" |
| **Multi-provider opcional** | gateway que fala com mais de um provedor, mantendo o segundo caminho vivo por pequeno tráfego |

## Armadilhas

- ❌ **Abstração que finge igualdade:** os modelos **não** se comportam igual — a camada de acesso esconde o acoplamento, não a diferença. Por isso a alavanca nº 5 (evals de troca) é obrigatória junto com a nº 1.
- ❌ **Fine-tuning não é portável:** peso ajustado fica no provedor; se depender dele, o lock-in é total.
- ❌ **Over-engineering:** nem todo projeto precisa de dois provedores vivos; a interface única já compra a maior parte da liberdade.

## Perguntas para validar

1. Por que vendor lock-in é decisão de **arquitetura** e não de compra — e por que ela precisa ser tomada no início do projeto?
2. Cite quatro alavancas de mitigação e explique por que a abstração sozinha não basta.
3. Se o seu produto usasse só um modelo hoje, o que teria que existir para trocar amanhã sem reescrever o produto?

## Ver também

- [[Vendor lock-in]] · [[Roteamento de modelos]] · [[Benchmark]] · [[Benchmarks: como medir o desempenho]] · [[Modelo Open-Weight]]

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
