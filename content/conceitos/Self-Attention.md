---
title: "Self-Attention"
tags:
  - "conceito"
  - "transformers"
tipo: "conceito"
date: "2026-10-01"
---

# Self-Attention

> **Definição em uma frase:** mecanismo em que cada token calcula, para todos os demais, o quanto é relevante, e mistura os valores com esses pesos.

## Fórmula

$$\text{Attention}(Q,K,V)=\text{softmax}\!\left(\frac{QK^\top}{\sqrt{d_k}}\right)V$$

Cada token produz três vetores por matrizes treináveis:

- **Q** (*query*) — o que estou procurando
- **K** (*key*) — o que eu ofereço
- **V** (*value*) — o que entrego se houver interesse

Passo a passo:

1. $QK^\top$ → matriz $n\times n$ de compatibilidades.
2. **Divisão por $\sqrt{d_k}$** → *scaling*. Sem ela, com $d_k$ grande, o softmax satura e o gradiente morre.
3. `softmax` → linha vira distribuição (soma 1). São os *attention weights*.
4. $\times V$ → cada posição vira **média ponderada** dos valores.

O passo 4 é o coração: cada token renova o próprio significado usando o contexto inteiro, em uma operação.

## Variações

| Variação | Efeito |
| --- | --- |
| **Máscara causal** | $z \to -\infty$ no triângulo superior — o token $t$ só vê $\le t$. Obrigatória em decoder-only. |
| **Multi-head** | $h$ cabeças em paralelo, cada uma livre para capturar outra relação |

## Confusões e aparências

- ❌ **Não é** "importância" interpretável. Attention weights de uma camada não são explicações.
- ❌ **Não é** um mecanismo de roteamento. As cabeças não são selecionadas; a especialização é emergente e frágil.

## Autoavaliação
1. **P:** O que acontece se remover $\sqrt{d_k}$? **R:** logits de atenção grandes → softmax satura → gradientes quase nulos → o modelo não treina.
2. **P:** Sem máscara causal, o que a loss faz num decoder-only? **R:** cai para quase zero: o modelo enxerga o token alvo ao prever, e nunca precisa aprender nada.
3. **P:** Por que atenção é $O(n^2)$ e isso importa? **R:** a matriz de scores é $n\times n$; com 32k de contexto isso domina custo e memória do prefill.

## Onde vi isso

- Visto em:[[Transformer]]

## Ver também

- [[Transformer]] · [[Positional Encoding]] · [[KV Cache]]

---
*Atualizado em 2026-09-30*
