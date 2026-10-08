---
title: "Prefill"
tags:
  - "conceito"
  - "inferencia"
tipo: "conceito"
date: "2026-10-01"
---

# Prefill

> **Definição em uma frase:** a fase da inferência em que todo o prompt é processado de uma vez, em paralelo, antes do primeiro token ser emitido.

## As duas fases

| Fase | O que faz | Paralelismo | O que limita |
| --- | --- | --- | --- |
| **Prefill** | processa o prompt inteiro | **total** | **cálculo** — atenção $O(T^2)$ |
| **Decode** | gera um token por vez | **nenhum** | **banda de memória** — ler pesos + KV cache |

Duas métricas:

- **TTFT** (time to first token) — dominada pelo prefill. É o que o usuário percebe como "demora pra começar".
- **Tokens/s** (após o primeiro token) — dominada pelo decode, limitado por memória.

## Consequências práticas

- **Resposta curta + contexto longo** → prefill domina. Otimizar com FlashAttention e reduzir contexto.
- **Resposta longa + contexto curto** → decode domina. Otimizar com GQA, quantização, speculative decoding.
- **Aumentar o batch** → TTFT sobe (mais sequências competem, mais padding), throughput agregado sobe bastante (custo de memória por passo é compartilhado).

É o compromisso clássico **latência × vazão**, e é a razão de existir serving dedicado por workload.

## Autoavaliação
1. **P:** Por que o prefill é limitado por FLOPs e o decode por memória? **R:** no prefill há $T$ tokens simultâneos e operações de matrizes grandes (aritmética intensiva); no decode há 1 token por vez contra um peso de bilhões de parâmetros — quase todo o tempo é espera de memória.
2. **P:** Se o usuário reclama de lentidão, por que medir TTFT e tokens/s separadamente? **R:** porque a solução é completamente diferente em cada um.

## Onde vi isso

- Visto em: [[Nota Técnica - Geração token a token]]

## Ver também

- [[KV Cache]] · [[Janela de Contexto]] · [[Transformer]]

---
*Atualizado em 2026-09-30*
