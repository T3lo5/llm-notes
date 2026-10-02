---
title: "Positional Encoding"
tags:
  - "conceito"
  - "transformers"
tipo: "conceito"
date: "2026-10-01"
---

# Positional Encoding

> **Definição em uma frase:** mecanismo que injeta a noção de **ordem** em uma atenção que, sozinha, é permutacional.

## O problema

Atenção é **permutacional**: reordenar as entradas apenas reordena as saídas. O modelo não distingue "o gato mordeu o homem" de "o homem mordeu o gato" sem informação de posição.

## Métodos

| Método | Como funciona | Usado em |
| --- | --- | --- |
| **Sinusoidal** (Vaswani, 2017) | somas de senos com frequências decrescentes, por fórmula fechada (não aprendida) | paper original |
| **Absoluto aprendido** | um vetor de posição por índice | BERT, GPT-2 |
| **RoPE** (Su et al., 2021) | **rotaciona** Q e K por ângulos que dependem da posição | LLaMA, Mistral, Gemma, Qwen |

## Por que RoPE venceu

Com RoPE, o produto $QK^\top$ passa a codificar **distância relativa** de forma natural — não posição absoluta. Benefícios:

1. posição relativa é o que atenção de fato usa;
2. extrapolação para sequências mais longas é mais bem comportada;
3. compatível com atenção linear.

O custo: extrapolação ainda não é perfeita — por isso existem ajustes de **base de rotação** para contexto longo.

## Autoavaliação
1. **P:** O que aconteceria sem codificação posicional? **R:** o modelo não distinguiria ordem; "A matou B" e "B matou A" teriam a mesma representação.
2. **P:** Qual a diferença entre posição absoluta e relativa, e por que a relativa combina melhor com atenção? **R:** atenção pondera pares; o que importa no par é a distância entre eles, não o índice absoluto de cada um.

## Onde vi isso

- Visto em:[[Transformer]]

## Ver também

- [[Self-Attention]] · [[Transformer]] · [[Paper - RoPE]]

---
*Atualizado em 2026-09-30*
