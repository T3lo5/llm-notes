---
title: "Riscos e falhas em projetos de IA"
tags:
  - "riscos"
  - "falhas"
tipo: "guia"
date: "2026-10-26"
---

# Riscos e falhas em projetos de IA

> **Meta:** abrir a disciplina de riscos e falhas com o enquadramento que falta nas
> três anteriores: em IA, **falha não é exceção — é taxa**. A seção define o
> vocabulário de risco e mostra por que a resposta à pergunta "como evitar que a IA
> erre?" não é "testar mais", e sim **camadas empilhadas**.


## Resumo em 3 frases

1. Um sistema de IA erra **por construção**: ele estima a continuação mais provável do
   texto, não a resposta verdadeira — o erro é uma taxa esperada (ver [[Alucinação]]).
2. Por isso o risco não se resolve com teste: exige **camadas** — ancoragem no dado
   real, validação de saída, guardrails, humano nos casos críticos e medição contínua.
3. O trabalho da disciplina é transformar erro inevitável em **risco gerenciado**:
   documentado, medido, com alguém decide o que pode passar.

## O que muda quando o sistema erra por probabilidade

| | Software determinístico | Sistema de IA |
| --- | --- | --- |
| Origem da saída | regra escrita | distribuição de probabilidade |
| Erro | exceção (bug) | taxa esperada (amostragem) |
| Teste | entrada → saída fixa | entrada parecida → saída variável |
| Cobertura | conjunto de casos | distribuição, com cauda |
| Correção | conserta o código | conserta o **contexto**, o **guardrail** ou a **decisão de projeto** |

> A frase que resume a disciplina: **em software determinístico o erro é defeito; em
> IA probabilística o erro é parâmetro do sistema.** Muda o que se mede, quem assina e
> como se protege.

## A anatomia de uma falha

Quatro perguntas — as mesmas que um post-mortem precisa responder:

1. **O que** o sistema fez de errado? (resposta alucinada, dado vazado, saída fora do formato)
2. **Por quê?** (contexto faltando, recuperação errada, prompt ambíguo, [[Prompt Injection]], modelo trocado)
3. **Qual o impacto?** (gravidade × frequência — o gate de criticidade da [[Estratégia híbrida de modelos]])
4. **O que impede de repetir?** (guardrail novo, eval novo, mudança de processo)

Sem a 4, a falha vira história. Com ela, vira controle.

## O mapa do risco na disciplina

| Risco | Como se manifesta | Onde é tratado |
| --- | --- | --- |
| **Alucinação** | resposta plausível e falsa | Alucinação e Comportamentos · [[Alucinação]] |
| **Erro de arquitetura** | limitação estrutural do modelo (atenção, janela, memória) | Erros Inerentes à Arquitetura |
| **Falha em cascata** | um ponto único derruba o fluxo inteiro | Design de Sistemas Resilientes |
| **Fato sem lastro** | resposta sem fonte verificável | Grounding e Verificação de Fatos · [[Grounding]] |
| **Saída fora da política** | conteúdo impróprio, PII, prompt injection | Guardrails e Segurança na IA · [[Guardrails]] |
| **Erro humano caro** | decisão crítica sem revisão | Human-in-the-loop · [[Human-in-the-loop]] |
| **Qualidade não medida** | otimização no escuro | Evals · [[Evals]] |

## A régua de priorização: gravidade × probabilidade

Nem todo erro merece o mesmo controle. O critério que ordena as prioridades:

```mermaid
flowchart TB
    F[Falha observada] --> G{"Impacto no negócio"}
    G -->|baixo| L1[Registrar e medir<br/>não escalar]
    G -->|alto| P{"Frequência"}
    P -->|alta| L2[Corrigir na origem<br/>guardrail + prompt + dados]
    P -->|baixa e grave| L3[Gate de criticidade<br/>humano no circuito]
    L2 --> E["Evals: a correção vira caso de teste"]
    L3 --> E
```

- **Erro frequente e de baixo impacto**: irrita, não quebra. Vira métrica, não prioridade.
- **Erro frequente e de alto impacto**: bug de verdade. Correção na origem.
- **Erro raro e grave**: o caso que assusta o jurídico e o conselho. Vai para revisão humana — porque nenhuma regra pegaria um caso que você nem imaginou.

> A nota de moderação (Moderação de Conteúdo com IA) abre exatamente esse intervalo:
> como moderar o conteúdo para que a falha vire **ruído controlado** e não **incidente**.

## A postura: gerenciar, não eliminar

- Nenhum sistema de IA é infalível. A pergunta não é "como eliminar o erro?", e sim
  **"quanto erro, de que tipo, com que impacto e quem absorve?"**
- Cada camada de defesa tem custo — tokens, latência, atrito humano, complexidade. A
  escolha é um trade-off, como em [[Trade-offs na escolha do modelo]].
- **O que não é medido não é gerenciado**: sem [[Evals]], cada defesa é achismo com
  aparência de engenharia.
- Falha é dado de treino: cada incidente vira caso de teste, guardrail ou mudança de
  política. É assim que o erro deixa de ser surpresa.

## Checklist de partida (antes de colocar em produção)

- [ ] **Mapa do risco da tarefa** — o que o modelo faz e qual é o pior erro possível
- [ ] **Gate de criticidade** — definido o que vai para humano e o que não vai
- [ ] **Fonte de verdade** — existe dado real para ancorar? (sem isso, é otimismo)
- [ ] **Validação de saída** — schema e regras de domínio implementadas em código
- [ ] **Guardrails** — de entrada e de saída, com teste de falso positivo
- [ ] **Evals** — dataset versionado com casos ruins, rodando a cada mudança
- [ ] **Observabilidade** — log de entrada, saída, versão de prompt, versão de modelo

## O mapa da disciplina

| Item | Nota | O que responde |
| --- | --- | --- |
| Abertura: riscos e falhas | [[Riscos e falhas em projetos de IA]] | Como pensar risco em IA; por que teste sozinho não basta |
| Moderação de conteúdo | [[Moderação de conteúdo com IA]] | Quais controles reduzem o dano de uma resposta errada |
| Alucinação e Comportamentos | — | Como o modelo erra e com que frequência |
| Erros Inerentes à Arquitetura | — | Quais limitações são estruturais (não se corrigem com prompt) |
| Design de Sistemas Resilientes | — | Como o sistema sobrevive à falha de uma peça |
| Grounding e Verificação de Fatos | — | Como ancorar a resposta no dado real |
| Guardrails e Segurança na IA | — | Como barrar o que não deve entrar nem sair |
| Human-in-the-loop: Revisão Humana | — | Onde o humano entra sem virar gargalo |
| Evals: Medindo a Qualidade da IA | — | Como medir se as defesas seguram |
| Entrega final — IA no Setor Jurídico | — | Aplicação da disciplina num caso de alto risco |

> Cada item da disciplina, na ordem oficial; as seções restantes ainda não têm nota.

## Perguntas para validar

1. Por que "testar e corrigir" não funciona como estratégia de segurança em IA, e o
   que substitui isso?
2. Um erro raro e de impacto alto e um erro frequente de impacto baixo: por que o
   primeiro exige humano e o segundo não?
3. Em que ponto de um projeto de IA o risco deixa de ser uma issue e vira um
   **critério de arquitetura**?
4. Se cada camada de defesa custa tokens, latência ou tempo humano, como se decide
   quais camadas existem em um sistema pequeno?

## Ver também

- [[Moderação de conteúdo com IA]] · [[Alucinação]] · [[Prompt Injection]] · [[Lost in the Middle]]
- [[Ambiguidade e riscos na IA]] · [[Quando não usar inteligência artificial]] · [[Quando nao usar IA]]
- [[Guardrails]] · [[Human-in-the-loop]] · [[Evals]] · [[Grounding]]

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
