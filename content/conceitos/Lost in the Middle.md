---
title: "Lost in the Middle"
tags:
  - "conceito"
  - "prompt"
tipo: "conceito"
date: "2026-10-01"
---

# Lost in the Middle

> **Definição em uma frase:** queda de desempenho de LLMs quando a informação relevante cai no meio de um contexto longo, seguindo uma curva em U.

## O gráfico

```
desempenho
 │ ╱‾‾‾╲ ╱‾‾‾
 │ ╱ ╲ ╱
 │╱ ╲________________╱
 └──────────────────────────────────► posição da informação
 início fim
 (primacy) (recency)
```

- **Primacy bias** — o início do contexto é mais respeitado.
- **Recency bias** — o fim é mais respeitado, por estar mais próximo da posição de geração.

Fonte: Liu et al., *Lost in the Middle*, TACL 2024.

## O detalhe que muda decisões de projeto

**Com a informação no meio, o desempenho pode ficar abaixo do desempenho sem documento nenhum** (closed-book).

Isto é contraintuitivo e importante: Retrieved contexto não é neutro. Contexto mal posicionado é **ativamente prejudicial** — você está pagando tokens para piorar a resposta.

## Implicação de engenharia

1. Evidence mais relevante **no início ou no fim**, nunca no meio de uma lista de 20.
2. Se recuperar só um trecho, coloque-o explicitamente na ponta.
3. Ordene por relevância decrescente — as extremidades ficam com as melhores.
4. Meça: a curva muda com o modelo e com o tamanho do contexto.

## Autoavaliação
1. **P:** Por que recency bias existe? **R:** porque a geração começa a partir do fim do contexto; tokens próximos dessa posição tem influência mais forte no primeiro token gerado.
2. **P:** "Se eu duplico a informação no início e no fim, garanto o resultado?" **R:** melhora a chance, mas dobra o custo dos tokens dessa informação. Avalie se vale.

## Onde vi isso

- Visto em: [[Sensibilidade de prompt: ordem importa]]

## Ver também

- [[Janela de Contexto]] · [[RAG]] · [[Alucinação]] · [[Pesquisa - Sensibilidade de prompt e posição]]

---
*Atualizado em 2026-09-30*
