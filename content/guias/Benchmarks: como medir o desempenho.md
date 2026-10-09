---
title: "Benchmarks: como medir o desempenho"
tags:
  - "selecao-de-modelos"
  - "benchmarks"
  - "evaluacao"
tipo: "guia"
date: "2026-10-16"
---

# Benchmarks: como medir o desempenho

> **Meta:** saber montar um benchmark que **decide** — comparação estatisticamente séria, funções reais do modelo, dados o mais próximos possível do uso real.


## Resumo em 3 frases

1. Medir desempenho de modelos é comparar sob condições controladas: **testes estatisticamente válidos**, das **funções reais** do modelo, com **dados o mais próximos possível do uso real**.
2. Benchmark público faz triagem; o que decide é o **benchmark do seu caso de uso** — porque teste irreal gera **falsos positivos**.
3. **Benchmark ruim leva a escolha ruim:** se a comparação não cobre as variações nem reflete o uso real, a escolha herdou o defeito do teste.

## As três fontes de medição

| Fonte | Para que serve | Limite |
| --- | --- | --- |
| **Leaderboard público** | triagem — descartar modelos fracos no que importa | mede média alheia; sofre contaminação e saturação (ver [[Pesquisa - Custo e qualidade na seleção de modelos]]) |
| **Benchmark do provedor** | entender o que ele se dispõe a comparar | comparação no cenário que favorece o próprio produto |
| **Benchmark do seu domínio** | **a decisão** | exige dados e esforço seus |

## O que torna um teste estatisticamente sério

- **Amostra suficiente** para a decisão que se vai tomar — 10 casos não separam 90% de 80%.
- **Repetição:** o mesmo caso roda mais de uma vez, porque a decodificação é estocástica (ver [[Temperatura e previsibilidade]]) — sem repetição, mede-se sorte.
- **Margem de erro explícita:** a comparação só vale se os intervalos não se sobrepõem.
- **Métrica ligada ao uso:** acurácia só se a tarefa for classificação; para geração, scoring de formato, fidelidade e taxa de falha de schema.

## Testar funções reais do modelo

O objeto do teste não é a micro-tarefa isolada — é a **função que o produto exige**: prompt completo (instrução + contexto + exemplos), saída no formato do produto, validação no fim. Um modelo que acerta "traduza esta frase" pode falhar no pipeline inteiro de resumo de contrato com saída estruturada. O benchmark ruim testa a tarefa fácil; o bom testa o trabalho.

## Gerar dados comparáveis para o seu caso

- **Mesmo dataset para todos os modelos** — nunca uma amostra diferente por modelo.
- **Casos reais** (anonimizados) do uso de produção — não frases escritas para o teste.
- **Cobrir as variações:** tamanhos de entrada, casos-limite, ruído (abreviação, erro de digitação), formatos de saída, variações de prompt.
- **Evitar falsos positivos:** dado contaminado (que apareceu no treino), caso escolhido depois de ver a resposta, avaliação só por modelo (sem revisão humana amostral).

## Pipeline mínimo

```mermaid
flowchart LR
    A[Dataset real<br/>anônimo] --> B[Execução repetida<br/>por modelo]
    B --> C[Scoring automático<br/>+ amostra humana]
    C --> D[Relatório: acurácia,<br/>custo, latência]
    D --> E[Decisão]
```

Cada modelo passa pelo **mesmo** pipeline, e o relatório junta os 3 critérios medidos: qualidade, custo por caso real e latência. É o benchmark virando a linha de decisão da [[Trade-offs na escolha do modelo]].

## Perguntas para validar

1. Por que benchmark público não decide — e o que decide? Qual é o papel de cada um?
2. Seu teste de 10 casos deu 90% (modelo A) e 80% (modelo B). Por que isso ainda não é comparação?
3. Dê um exemplo de falsos positivo num benchmark do seu domínio — e como evitá-lo.

## Ver também

- [[Benchmark]] · [[Estratégia híbrida de modelos]] · [[Pesquisa - Custo e qualidade na seleção de modelos]] · [[Latência]]

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
