---
title: "Alucinação e comportamentos"
tags:
  - "riscos"
  - "falhas"
  - "alucinacao"
  - "contexto"
tipo: "guia"
date: "2026-10-29"
---

# Alucinação e comportamentos

> **Meta:** explicar por que a IA **inventa informação com aparência de verdade** e como
> essa falha vem acompanhada de inconsistência, ambiguidade e perda de contexto — e o
> que fazer para detectar e conter cada uma.


## Resumo em 3 frases

1. **Alucinação** é a IA **inventar informação** e entregá-la com aparência de resposta
   correta: o formato e o tom não distinguem verdade de invenção.
2. A seção agrupa o problema com outros três comportamentos — **inconsistência**,
   **ambiguidade** (geralmente causada por prompt ruim) e **perda de contexto** — falhas
   que aparecem juntas e derrubam a confiabilidade da saída.
3. Como a origem é a **natureza probabilística** do modelo, a resposta não é "pedir para
   não errar": é **validar a saída**, revisar planos propostos, usar **documentação real**
   como referência, bloquear comportamentos indesejados e **medir a qualidade com testes**.

## Os quatro comportamentos que a seção separa

| Comportamento | Definição (segundo os bullets) | Como reconhecer |
| --- | --- | --- |
| **Alucinação** | A IA inventa informação; a resposta *parece* correta, mas é imprecisa | O dado existe no mundo? A fonte citada existe? |
| **Inconsistência** | A mesma entrada passa a devolver algo diferente do que devolvia antes, ou a saída se contradiz | Repetir a mesma consulta muda o resultado? O texto bate com ele mesmo? |
| **Ambiguidade** | A pergunta ou a resposta admite mais de uma leitura — **geralmente causado por prompt ruim** | Dá para responder de mais de um jeito e todos "cabem" no pedido? |
| **Perda de contexto** | A informação estava no contexto, mas deixa de ser usada — por limite de janela ou por estar no meio de um contexto longo | Uma regra/dado dito antes desaparece da resposta? |

> Os sinais da coluna "como reconhecer" são **meus**, para transformar o bullet em
> pergunta de verificação. A definição de **inconsistência** também é minha interpretação:
> "busco algo que antes retornava de um jeito e agora retorna diferente". A seção define os
> quatro comportamentos; não detalha (nos meus bullets) como medi-los. Fichas:
> [[Alucinação]] · [[Inconsistência]] · [[Ambiguidade]] · [[Perda de Contexto]].

## O que a seção aborda (escopo declarado)

- Os **principais tipos de falha** que uma IA pode cometer.
- **Alucinação** como foco: como a IA gera respostas que **parecem corretas**, mas são
  **inventadas e imprecisas**.
- **Incoerência**, **ambiguidade** e **limites do contexto**, e como impactam a
  confiabilidade das saídas.
- **Por que** essas falhas ocorrem e como se relacionam com a **natureza probabilística**
  dos modelos.
- **Mecanismos de controle** para mitigar os riscos em aplicações práticas.
- **Validar saídas**, **revisar planos propostos**, usar **documentações reais** como
  referência, **bloquear comportamentos indesejados** e **medir a qualidade com testes**.

## Objetivos

- [ ] Identificar as falhas mais comuns em IAs
- [ ] Compreender o conceito de alucinação em modelos de IA
- [ ] Reconhecer a influência de ambiguidade e inconsistência
- [ ] Aprender sobre limites de contexto em IA
- [ ] Aplicar mecanismos de controle para mitigar erros
- [ ] Desenvolver estratégias de validação de saída

## Por que acontece: a base probabilística

> Ligação com o que já estudamos — **não** é um detalhe novo da[[Alucinação e comportamentos]].

O modelo estima a **continuação mais provável** do texto, não "a resposta verdadeira"
(ver [[Modelos de Linguagem: como funcionam]] e [[Alucinação]]). Por isso uma resposta falsa
pode ser tão fluente quanto uma verdadeira: o objetivo de treino premia
**plausibilidade**, não veracidade. [[Temperatura]] e amostragem mudam o quanto a saída
se arrisca fora do topo da distribuição (ver [[Temperatura e previsibilidade]]).

A consequência prática é a que a seção cobra: **não existe autoavaliação confiável**.
Quem diz se a saída está certa é uma verificação **externa** — fonte, documento real,
validação em código, revisão humana ou teste.

## Mecanismos de controle citados na seção

| Controle | O que a seção propõe | Como eu pretendo verificar |
| --- | --- | --- |
| **Validar saídas** | conferir a resposta antes de entregá-la ao usuário | schema/regra de domínio + conferência com a fonte (ver [[Grounding]]) |
| **Revisar planos propostos** | revisar **com o agente** o plano que ele propôs, antes de executar: o que ele entendeu, os passos, os dados que vai usar e o resultado esperado | o plano está coeso? cada passo corresponde ao pedido? o que pode sair diferente? |
| **Documentação real como referência** | usar doc oficial/real em vez da memória do modelo | citar a fonte de cada afirmação técnica; recusar quando não houver fonte |
| **Bloquear comportamentos indesejados** | impedir entradas/saídas fora da política | guardrails de entrada e saída, testados contra falso positivo (ver [[Guardrails]]) |
| **Medir a qualidade com testes** | medir o sistema, não confiar na impressão | conjunto de casos versionado, rodando a cada mudança (ver [[Evals]]) |

> **O que é "revisar planos propostos" (fechado):** é a revisão do **plano do agente com
> o agente**, antes da execução — conferir se o que ele planejou está **coeso** e se
> **corresponde** ao pedido. Não é revisar a resposta final; é pegar o desvio antes de ele
> virar ação. Critério prático: reler o plano elo por elo — entendeu o pedido? escolheu os
> dados certos? a sequência fecha? o resultado esperado é o que eu pedi?

## Síntese em um fluxo

```mermaid
flowchart LR
    A[Pergunta] --> B[Resposta do modelo]
    B --> C{Válida?}
    C -->|não| D[Corrigir / recusar / escalar]
    C -->|sim| E{Ainda ambígua ou sem fonte?}
    E -->|sim| D
    E -->|não| F[Entregar + registrar caso de teste]
    D --> G[Medir e realimentar evals]
    F --> G
```

## Exemplo concreto (ilustrativo, meu)

> Não é o exemplo. É um caso que eu consigo reproduzir para reconhecer cada falha
> no mesmo cenário.

**Pedido:** "escreva um script em Python que leia `vendas.csv`, calcule a média de vendas
por mês e gere um resumo executivo".

| Falha | O que apareceria | Por que é essa falha |
| --- | --- | --- |
| **Alucinação** | `df.sample_frac(0.1)` para tirar uma amostra | `sample_frac` existe no dplyr (R), não no pandas: o método **parece** plausível e só quebra quando roda (`AttributeError`). |
| **Inconsistência** | na segunda-feira o resumo diz "média mensal: R$ 42.300"; na terça, mesmo CSV, "R$ 38.900" | o critério mudou (média das vendas × média dos dias) sem aviso. Não é fato inventado: é resultado que não se repete. |
| **Ambiguidade** | o script calcula total do mês, mas eu queria média por venda | "média de vendas por mês" admite as duas leituras; o problema está no pedido, não no cálculo. |
| **Perda de contexto** | eu disse "valores em centavos" no início; 30 mensagens depois ele divide por 100 de novo | a regra estava no contexto, mas saiu do alcance efetivo (janela ou meio do contexto). |

**Como o exemplo vira controle:** rodar o script pega a alucinação de API; rodar duas
vezes e comparar pega a inconsistência; pedir o critério antes de calcular fecha a
ambiguidade; reancorar a regra dos centavos no ponto de uso segura a perda de contexto.

## Erros comuns / armadilhas

- ❌ Tratar **fluência como evidência de verdade** — o tom confiante é estilo, não
  calibração (ver [[Moderação de conteúdo com IA]]).
- ❌ Achar que **prompt melhor elimina alucinação**. Prompt melhor reduz ambiguidade;
  não cria fonte de verdade.
- ❌ Confundir **"respondeu o que eu quis"** com **"respondeu corretamente"**.
- ❌ Testar só o caso feliz e concluir que o sistema está pronto (ver [[Evals]]).
- ✅ Para cada afirmação factual, perguntar: **qual é a fonte?** Sem fonte, não entra na
  saída (ver [[Grounding]]).

## O que ficou fechado e o que ainda está aberto

- ✅ **Inconsistência** é falha separada da alucinação: a resposta pode estar correta e
  ainda assim mudar entre execuções. Ver [[Inconsistência]].
- ✅ **Perda de contexto** acontece pelos dois mecanismos: limite de [[Janela de Contexto]]
  e evidência no meio do contexto ([[Lost in the Middle]]). Ver [[Perda de Contexto]].
- ✅ **"Revisar planos propostos"** é revisar com o agente o plano dele antes de executar,
  checando coesão e correspondência com o pedido.
- ✅ **Ambiguidade** tem causa principal no prompt, mas também pode vir do domínio ou da
  própria resposta. Ver [[Ambiguidade]].
- [ ] **Como medir alucinação** de forma reproduzível — taxa por tipo de pergunta, com
  [[Evals]] ou revisão humana amostrada? Fica para a ficha [[Evals]].

## Referências


- Fichas: [[Alucinação]] · [[Inconsistência]] · [[Ambiguidade]] · [[Perda de Contexto]] · [[Janela de Contexto]] · [[Lost in the Middle]] · [[Temperatura]] · [[Grounding]] · [[Guardrails]] · [[Evals]] · [[Human-in-the-loop]]

- Ver também: [[Ambiguidade e riscos na IA]] · [[Engenharia de prompt e contexto]] · [[Moderação de conteúdo com IA]]

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
