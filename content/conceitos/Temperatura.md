---
title: "Temperatura"
tags:
  - "conceito"
  - "decodificacao"
tipo: "conceito"
date: "2026-10-01"
---

# Temperatura

> **Definição em uma frase:** escalar que divide os logits antes do softmax, controlando quão concentrada (fina) ou difusa (chapada) é a distribuição de amostragem.

## Fórmula

$$p_i = \frac{e^{z_i/T}}{\sum_j e^{z_j/T}}$$

| Valor | Efeito |
| --- | --- |
| $T \to 0$ | converge para **argmax** — greedy decoding, sem sorteio |
| $T < 1$ | **afina** a distribuição; improváveis perdem massa |
| $T = 1$ | distribuição como saiu do modelo |
| $T > 1$ | **achata**; com amostragem pura, vira ruído |

## O detalhe que quase todo mundo erra

**Temperatura não muda o ranking dos tokens** — dividir por um escalar positivo é monotônico. Ela muda a **geometria** da distribuição: o quanto de massa fica nos poucos favoritos.

É por isso que provedores recomendam ajustar `temperature` **ou** `top_p`, nunca os dois: ajustar os dois é multiplicar efeitos e quase sempre piora.

## Escolha prática

| Caso | Valor típico |
| --- | --- |
| Extração de dados, código, classificação | `0` a `0.2` |
| Resposta factual com fonte (RAG) | `0` a `0.3` |
| Texto criativo, brainstorming | `0.8` a `1.2` |

⚠️ Parâmetros de sampling têm suporte desigual entre modelos e provedores, e alguns modelos recentes rejeitam valores fora do padrão. Consulte a referência do modelo antes de prescrever.

## Autoavaliação
1. **P:** Por que $T=0$ não é "temperatura zero" no sentido físico? **R:** porque a implementação não divide por zero — ela faz `argmax`. São duas rotas de código diferentes, mesmo que o efeito se pareça.
2. **P:** Por que aumentar a temperatura e o top-p juntos costuma degradar? **R:** os dois cortam a cauda em direções diferentes; combinados, deixam quase só o token de topo alto, com pouco espaço para recuperação.

## Onde vi isso

- Visto em:[[Temperatura]]

## Ver também

- [[Logits]] · [[Top-p Sampling]] · [[Top-k Sampling]] · [[KV Cache]]

---
*Atualizado em 2026-09-30*
