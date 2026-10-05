---
title: "KV Cache"
tags:
  - "conceito"
  - "inferencia"
tipo: "conceito"
date: "2026-10-01"
---

# KV Cache

> **Definição em uma frase:** armazenamento das projeções de chave e valor dos tokens já processados, para que a decodificação não recalcule o contexto inteiro a cada passo.

## O problema

A cada token gerado, o modelo precisa attentionar contra **todos** os tokens anteriores. Sem cache, $K$ e $V$ do contexto inteiro seriam recalculados a cada passo:

- **tempo:** $O(T^2)$
- **memória:** recursão de computação em cada passo

## O mecanismo

Com cache, guarda-se $K$ e $V$ de cada camada. A cada passo só se computa $K, V$ do **token novo**, e attentiona contra o que já está guardado:

$$\text{tamanho} \propto 2 \cdot n_{\text{camadas}} \cdot n_{\text{cabeças KV}} \cdot d_{\text{cabeça}} \cdot T$$

O fator 2 vem de K e V. Repare: o custo é **linear em $T$**, mas o coeficiente depende de camadas, cabeças e dimensão de cabeça — daí o impacto de reduzir cabeças KV.

## Consequências de projeto

| Técnica | Efeito no KV cache |
| --- | --- |
| **GQA / MQA** (Ainslie et al., 2023) | reduz `n_cabeças KV` → cache encolhe → decode mais rápido |
| **PagedAttention / vLLM** (Kwon et al., 2023) | pagina o cache como memória virtual: sem fragmentação + compartilhamento de prefixo |
| **Quantização do KV cache** | comprime a maior fonte de memória em contexto longo |

## Relação com latência

O decode é limitado por **banda de memória** (ler pesos + KV cache), não por FLOPs. É exatamente por ler cache que reduzir cabeças KV acelera tanto. Ver [[Prefill]] para a outra metade do problema.

## Autoavaliação
1. **P:** Por que o cache não elimina o custo quadrático da atenção no treino? **R:** porque o cache existe na **inferência**. No treino todos os passos são paralelos e o custo quadrático é absorvido pela GPU.
2. **P:** Por que contexto longo estoura memória mesmo num modelo pequeno? **R:** porque em $T$ grande o KV cache, não os pesos, domina o consumo.

## Onde vi isso

- Visto em: [[Como o modelo gera respostas, token a token]]

## Ver também

- [[Prefill]] · [[Self-Attention]] · [[Janela de Contexto]]

---
*Atualizado em 2026-09-30*
