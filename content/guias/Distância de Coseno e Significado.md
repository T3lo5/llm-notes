---
title: "Distância de Coseno e Significado"
tags:
  - "embeddings"
  - "similaridade"
tipo: "guia"
date: "2026-10-15"
---

# Distância de Coseno e Significado

> **Meta:** explicar por que a *distância* entre dois vetores de embedding mede o
> *significado* — e por que o cosseno, e não a distância euclidiana, é o padrão.
> Escreva no fim: se passar de 40 palavras explicando por que cosseno,
> ainda está abstrato demais.

## Resumo em 3 frases

1. Embeddings põem o significado na **direção** do vetor, não no seu tamanho — por
   isso comparar vetores é comparar significado.
2. A **distância de cosseno** mede o ângulo entre dois vetores e ignora a magnitude,
   o que a torna invariante ao tamanho do documento.
3. O cosseno retorna valores entre **-1 e 1**; em embeddings de texto, textos com o
   mesmo tema ficam quase sempre acima de 0,7.

## O mapa

A[[Embeddings e vetorização]] mostrou *como* texto vira vetor. Esta aula mostra *o que fazer* com esses
vetores: medir o quanto dois textos significam a mesma coisa. É a ponte entre
"ter embeddings" e "buscar por similaridade" (o coração de qualquer RAG).

```mermaid
flowchart TD
    A["texto vira vetor"] --> B["vetores põem sentido<br/>na DIREÇÃO"]
    B --> C["medir ângulo entre<br/>dois vetores"]
    C --> D["distância de cosseno<br/>→ escala -1 a 1"]
    D --> E["limiar de corte<br/>(o que é 'parecido'?)"]
    E --> F["busca semântica<br/>e RAG"]
```

## Conceitos-chave

- [x] [[Similaridade de Cosseno]] — o ângulo entre dois vetores; padrão para embeddings.
- [x] [[Embedding]] — a representação vetorial do texto (visto na[[Embeddings e vetorização]].
- [x] [[Busca Semântica]] — recuperar pelo *significado*, não pela palavra-chave.
- [x] [[RAG]] — usa cosseno para achar trechos relevantes antes de responder.
- [x] [[Chunking]] — o cosseno só funciona bem se os pedaços forem coerentes.

## Distância de cosseno vs. as outras métricas

| Métrica | O que mede | Quando preferir |
| --- | --- | --- |
| **Cosseno** | ângulo, invariante à magnitude | **padrão** para embeddings de texto |
| **Produto escalar** | ângulo × magnitude | quando a magnitude carrega informação (ex.: frequência) — comum em índices de produção |
| **Euclidiana** | distância direta, fora de [0,1] | quando o modelo foi treinado com distância euclidiana |

⚠️ **Misturar métricas entre treino e inferência quebra o índice silenciosamente.**
Se o modelo foi treinado com produto escalar, usar cosseno na hora de buscar degrada
o ranqueamento sem lançar erro nenhum.

## Erros comuns

| Erro | Correção |
| --- | --- |
| "Distância de cosseno vai de 0 a 1" | Vai de **-1 a 1**. Embeddings de texto costumam ficar todos no positivo, mas o domínio completo é [-1, 1]. |
| "Quanto maior o cosseno, mais longe" | Ao contrário: **maior cosseno = mais parecido** (ângulo menor). |
| "Euclidiana e cosseno dão o mesmo ranqueamento" | Só se todos os vetores tiverem a mesma norma. Com normas diferentes, o ranqueamento muda. |
| "Embeddings mais longos têm cosseno menor" | Não — o cosseno **ignora o tamanho**. É exatamente por isso que ele é o padrão. |

## O limiar de corte é o pulo do gato

O cosseno te dá um número; a *decisão* é sua. Onde você corta para dizer "isto
contém"? Corta baixo (0,3) e o RAG puxa lixo; corta alto (0,9) e ele deixa de fora
trechos úteis. Esse limiar é empirico, por domínio, e é a parte do RAG que ninguém
ajusta — e que mais afeta a qualidade da resposta.

## Exercício

Rode o [[Lab 02 - Embeddings e similaridade]] e, antes de olhar o resultado, escreva
o que você espera para três pares: (mesmo texto), (texto parecido), (texto
relacionado mas de outro tema). Depois compare com o cosseno calculado. Se seu chute
e o número discordarem no terceiro caso, o limiar de corte é onde olhar.

## Onde isso conecta

- Anterior: [[Embeddings e vetorização]] — de onde vem o vetor.
- Próxima: [[Arquitetura Transformers e Attention]] — como o contexto é
  processado antes de virar embedding.
- Prática: [[Lab 02 - Embeddings e similaridade]]
- Pesquisa: [[Pesquisa - Embeddings e busca semântica]]

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
