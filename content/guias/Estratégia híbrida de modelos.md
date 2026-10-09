---
title: "Estratégia híbrida de modelos"
tags:
  - "selecao-de-modelos"
  - "estrategia-hibrida"
  - "custo"
tipo: "guia"
date: "2026-10-16"
---

# Estratégia híbrida de modelos

> **Meta:** aplicar a disciplina num caso real de SaaS com usuários: modelo barato por padrão, modelo caro só no que é estritamente necessário.


## Resumo em 3 frases

1. Num **SaaS com usuários**, o modelo simples é impreciso demais para as ações críticas, e o modelo caro é eficiente — mas **muito caro** para o volume inteiro; nenhum dos dois sozinho fecha a conta.
2. A **estratégia híbrida** usa o modelo caro **só quando é estritamente necessário** (ações críticas) e modelos baratos para o que é simples.
3. A porta de entrada é o **gate**: definir "estritamente necessário" com regras, confiança e custo do erro — e escalar para o caro quando o barato não passa.

## O problema do SaaS

| Força | Empurra para |
| --- | --- |
| Usuários pagam por qualidade percebida | modelo forte |
| Volume cresce com o sucesso | modelo barato |
| Erro em ação crítica vira reclamação, chargeback, processo | modelo forte + humano |
| Margem do SaaS some com 10× o custo por token | modelo barato |

Os dois erros extremos — só barato e só caro — são simétricos: um quebra a qualidade, outro quebra a margem.

## A lógica híbrida

| Tipo de ação | Exemplo | Modelo | Por quê |
| --- | --- | --- | --- |
| **Simples e de alto volume** | resumo, classificação, resposta a FAQ, formatação | barato ([[Modelo Intermediário]]) | erro recuperável, custo unitário multiplica pelo volume |
| **Crítica e de baixo volume** | cobrança, compromisso jurídico, decisão sobre dinheiro do usuário | caro ([[Modelo Frontier]]) ou humano | o custo do erro supera a diferença de preço |

## Como definir "estritamente necessário"

O gate não é opinião — é critério escrito:

1. **Critério de domínio:** quais ações são críticas por definição (lista explícita, não "o modelo decide").
2. **Critério de confiança:** se o barato responde com baixa confiança ou falha no validador (schema, checker), escala.
3. **Custo do erro:** ação cujo erro custa mais que N chamadas do modelo caro escala — N é número, não sentimento.

```mermaid
flowchart LR
    A[Requisição do usuário] --> B{Gate de criticidade}
    B -->|simples + confiável| C[Modelo barato]
    B -->|crítica ou baixa confiança| D[Modelo caro]
    C --> E{Validador}
    E -->|passa| F[Resposta]
    E -->|falha| D
    D --> G[Revisão humana<br/>quando a ação exigir]
```

## Os mecanismos que sustentam

- **Cascata com verificador:** barato primeiro, verificador no fim, caro como fallback — até 98% de economia sem perder qualidade (FrugalGPT, ver [[Pesquisa - Custo e qualidade na seleção de modelos]]).
- **Roteamento aprendido:** um router decide por consulta se manda para forte ou fraco — >2× de economia (RouteLLM, ver [[Roteamento de modelos]]).
- **Revisão humana** no caminho das ações críticas: o modelo caro reduz o volume que o humano vê, não o substitui.

## Exemplo concreto

SaaS de suporte, 50k interações/dia: ~90% são FAQ (barato resolve, ~R$ 1,5k/mês), ~9% precisam de raciocínio sobre o caso (meio: barato com contexto ampliado), ~1% envolvem cobrança ou pedido formal — o 1% vai para o caro + revisão (≈R$ 600/mês). "Só caro" custaria ~R$ 40k/mês pela mesma receita. A híbrida entrega a qualidade onde ela é paga e protege a margem onde ela não é notada.

## Perguntas para validar

1. Por que "só modelo barato" e "só modelo caro" são dois erros simétricos num SaaS?
2. Quais os três critérios de um gate de criticidade — e qual deles precisa virar número?
3. Como a cascata com verificador e o roteamento aprendido se diferem na prática?

## Ver também

- [[Roteamento de modelos]] · [[Pesquisa - Custo e qualidade na seleção de modelos]] · [[Modelo Frontier]] · [[Modelo Intermediário]] · [[Escolha final e conclusão]]

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
