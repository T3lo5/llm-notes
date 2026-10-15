---
title: "Modelos de Linguagem: como funcionam"
tags:
  - "llm"
tipo: "guia"
date: "2026-10-01"
---

# Modelos de Linguagem: como funcionam

> **Meta:** descrever o pipeline completo de um LLM em uma frase, do texto à resposta, sem consultar nada.
> Escreva a versão final no fim e meça: se passar de 40 palavras, ainda está abstrato demais.

## Resumo em 3 frases

1. Um LLM é uma função que recebe uma sequência de tokens e devolve uma **distribuição de probabilidade sobre o próximo token**; repetir isso passo a passo é o que "escreve" a resposta.
2. Todo o trabalho pesado está em uma única peça — o **Transformer** — que processa todos os tokens do contexto **em paralelo** e produz um vetor por token que carrega o significado no contexto atual.
3. Nada disso é conhecimento: o modelo aprendeu **estatística de texto**. Por isso ele acerta tanto e por isso ele inventa com a mesma fluência.

## O mapa

Esta aula é o índice do módulo. Ela não pede que você saiba nada ainda — pede que você saiba o que *vai* saber.

```mermaid
flowchart TD
    A["LLM é um<br/>modelo de linguagem"] --> B["O que é"]
    A --> C["Como representamos<br/>texto: tokens e embeddings"]
    A --> D["Como processa:<br/>Transformer"]
    A --> E["Como gera:<br/>amostragem token a token"]
    A --> F["Como obedeca:<br/>prompt"]
```

## Conceitos-chave

- [x] [[Token]] — unidade de texto que o modelo realmente enxerga
- [x] [[Embedding]] — representação vetorial de um token no espaço
- [x] [[Transformer]] — arquitetura que processa o contexto em paralelo
- [x] [[Logits]] — pontuação de cada token possível para a próxima posição
- [x] [[Janela de Contexto]] — tudo que cabe numa chamada

## Por que "linguagem" e não "compreensão"

O modelo é treinado para responder à pergunta: **qual token vem a seguir?**. Essa tarefa, sozinha, é suficiente para produzir sistemas que parecem entender texto. É a mesma lógica de como uma criança aprende a falar: ninguém chega explicando gramática antes da primeira frase.

A consequência é profunda e vale internalizar: **o modelo não tem uma noção interna de "verdade"**. Ele otimiza plausibilidade estatística. Daí decorrem alucinação, deferência indevida de instrução, e o sucesso de contextos muito longos (veja [[Lost in the Middle]]).

## O que eu não devo acreditar

Mitos que aparecem desde o primeiro dia e custam caro depois:

| Mito | Realidade |
| --- | --- |
| "O modelo guarda o que eu falei" | Só se estiver dentro da [[Janela de Contexto]] desta chamada. Nada persiste. |
| "Ele tem acesso à internet / à data de hoje" | Não. Só tem o que está no contexto + o que foi visto no pré-treino. |
| "Ele tem memória entre conversas" | Não, sem um mecanismo explícito de memória externa. |
| "Se pedir duas vezes, dá a mesma resposta" | Quase nunca. Ver [[Temperatura]]. |
| "É uma base de dados que consulta" | Não. Não há consulta; há distribuição de probabilidade. |
| "Entender = compreender" | Não. Compreender a saída de um LLM não implica compreender o processo interno. |

## A intuição do pipeline

Quando você pede "explique o que é KV cache", acontece isto:

1. **Tokenização** — seu texto vira tokens. (~)
2. **Embeddings** — cada token vira um vetor; "cache" vira um vetor diferente de " Cachê". (~)
3. **Transformer** — cada token olha para todos os outros e ajusta seu próprio vetor conforme o contexto. É aqui que "cache" ganha o sentido de "guardar". (~)
4. **Logits** — o modelo sai um score para cada token do vocabulário. (ex:) não é o mais alto)
5. **Amostragem** — você sorteia. (Maior pontuação, mas não obrigatoriamente.)("")
6. **Loop** — repete até o modelo sinalizar fim.

Dois fatos que valem mais que todo o resto desta lista:

- **Os passos 2–4 são paralelos**; só o passo 5–6 é sequencial. Essa assimetria explica a latência (ver [[Prefill]] vs decode).
- **Nada na etapa 4 consulta "a resposta certa"**. Existe uma distribuição, e você escolhe um ponto dela.

## Perguntas para validar

Responda agora, sem olhar, e confira depois:

1. Em uma frase, o que um LLM faz?
2. Quais das etapas do pipeline são paralelas e qual é sequencial?
3. Por que "ele não tem acesso à internet" é uma consequência do treino, e não uma configuração?
4. Se um modelo é determinístico no papel, por que a mesma pergunta gera respostas diferentes? *(resposta na [[Temperatura e previsibilidade]])*

## Referências de entrada (depois: [[O que é um LLM]])

- Karpathy, A. — *Let's build GPT: from scratch, in code, spelled out* (YouTube). Base mais clara para o resto do módulo.
- Karpathy, A. — *The spelled-out intro to transformers* (YouTube). É praticamente a[[Arquitetura Transformers e Attention]] animada.
- Alammar, J. — *The Illustrated Transformer* — https://jalammar.github.io/illustrated-transformer/
- Jurafsky & Martin — *Speech and Language Processing*, cap. 3 (rascunho gratuito) — https://web.stanford.edu/~jurafsky/slp3/

## Checklist de conclusão

- [ ] Escrevi a frase-resumo do topo sem consultar
- [ ] Sei explicar por que a etapa de amostragem torna o sistema estocástico
- [ ] Consigo citar 3 mitos e responder por que são falsos

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
