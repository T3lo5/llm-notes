---
title: "Logits"
tags:
  - "conceito"
  - "decodificacao"
tipo: "conceito"
date: "2026-10-01"
---

# Logits

> **Definição em uma frase:** pontuação bruta (escala real, sem normalização) que o modelo atribui a cada token do vocabulário antes do softmax.

## Explicação curta

O último passo do transformer é uma projeção linear que leva o vetor do último token a um vetor de dimensão $V$ (tamanho do vocabulário). Esse vetor são os logits.

Dois fatos que resolvem metade das confusões:

1. **Logits não são probabilidades.** Podem ser negativos e não somam 1. O softmax converte.
2. **O softmax preserva a ordem.** Dividir os logits por uma temperatura não muda o ranking — muda a concentração.

## Onde a temperatura entra

$$p_i = \frac{e^{z_i/T}}{\sum_j e^{z_j/T}}$$

A divisão acontece **nos logits, antes do softmax**. Toda truncagem (top-k, top-p), penalidade e `logit_bias` também é aplicada nesse ponto — é por isso que structured output é possível.

```python
import numpy as np

def softmax(z, T=1.0):
    if T <= 0:                       # caso degenerado: argmax
        m = np.zeros_like(z); m[np.argmax(z)] = 1.0; return m
    z = z / T                        # temperatura ANTES do softmax
    z = z - z.max()                  # estabilidade numérica
    e = np.exp(z)
    return e / e.sum()
```

## Autoavaliação
1. **P:** Logits somam 1? **R:** não. São reais sem normalização; o softmax é quem normaliza.
2. **P:** Temperatura muda o ranking dos tokens? **R:** não, porque dividir por um escalar positivo é monotônico. Muda a geometria da distribuição.

## Onde vi isso

- Visto em:[[Temperatura]],[[Self-Attention]]

## Ver também

- [[Temperatura]] · [[Top-p Sampling]] · [[Perplexidade]] · [[Token]]

---
*Atualizado em 2026-09-30*
