---
title: "Transformer"
tags:
  - "conceito"
  - "transformers"
tipo: "conceito"
date: "2026-10-01"
---

# Transformer

> **Definição em uma frase:** arquitetura de rede neural que processa todos os tokens de uma sequência em paralelo, usando [[Self-Attention]] em vez de recorrência.

## Explicação curta

Antes de 2017 o padrão eram RNN/LSTM, lidos um passo por vez. Isso impedia treino paralelo e degradava dependências longas. Vaswani et al. (2017) removeram recorrência e convolução: sobrou atenção.

## Anatomia de um bloco

```
x
├─→ RMSNorm → Self-Attention ─┐ (+x) ─┐
└─→ RMSNorm → MLP (SwiGLU) ───┘ (+) ─┴─→ x'
```

Cada subcamada: **normalização → subcamada → conexão residual**.

| Peça | Papel | Parâmetros |
| --- | --- | --- |
| Self-attention | mistura informação entre tokens | ~4d² |
| MLP | transforma cada posição **independentemente** | ~8d²/3 (com SwiGLU) |

O MLP concentra a maior parte dos parâmetros — é onde o conhecimento fica.

## Famílias

| Família | Atenção | Exemplos |
| --- | --- | --- |
| Encoder-only | bidirecional, sem máscara | BERT, RoBERTa |
| **Decoder-only** | **causal** | **GPT, LLaMA, Mistral, Gemma** |
| Encoder-decoder | encoder + decoder cross-atendendo | T5, BART |

Os LLMs de chat são **decoder-only**.

## O que mudou desde 2018

| Original | Moderno |
| --- | --- |
| post-LayerNorm | pre-RMSNorm |
| posicional sinusoidal / absoluto | Positional Encoding |
| ReLU 4d | SwiGLU 8d/3 |
| multi-head denso | GQA/MQA |
| atenção materializada | FlashAttention (tiling, ainda exata) |

**Distinção que importa:** GQA e FlashAttention otimizam **constantes**, não complexidade. A atenção continua $O(T^2)$. Só janela esparsa, atenção linear ou [[Paper - Mamba]] mudam o regime.

## Autoavaliação
1. **P:** Por que remover a recorrência mudou o que era possível treinar? **R:** porque eliminou a dependência sequencial entre estados, permitindo paralelizar todos os passos do treino na GPU.
2. **P:** Onde estão a maior parte dos parâmetros? **R:** no MLP, não na atenção. A atenção é a parte que "razona"; o MLP é o que guarda.
3. **P:** Por que attention weights não servem como explicação? **R:** são uma fração dos parâmetros e produto de muitas camadas; explicabilidade exige accounting do caminho causal completo.

## Onde vi isso

- Visto em: [[Transformers, de um jeito simples]]

## Ver também

- [[Self-Attention]] · [[Positional Encoding]] · [[KV Cache]] · [[Logits]]

---
*Atualizado em 2026-09-30*
