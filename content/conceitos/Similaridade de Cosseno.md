---
title: "Similaridade de Cosseno"
tags:
  - "conceito"
  - "embeddings"
tipo: "conceito"
date: "2026-10-01"
---

# Similaridade de Cosseno

> **Definição em uma frase:** medida do ângulo entre dois vetores, invariante à magnitude.

## Fórmula

$$\text{cos}(a,b)=\frac{a \cdot b}{\|a\|\,\|b\|}$$

Resultado entre **-1 e 1**. Em embeddings de texto, valores altos são quase sempre próximos de 1.

## Por que é o padrão

Porque é **invariante à norma**: mede só direção. Um documento longo e um curto com o mesmo conteúdo têm cosseno ≈ 1, o que é o comportamento desejado em busca textual.

| Métrica | Comportamento | Quando preferir |
| --- | --- | --- |
| **Cosseno** | ângulo, invariante à norma | padrão para embeddings de texto |
| **Produto escalar** | ângulo × magnitude | quando a magnitude carrega informação (frequência) — comum em índices de produção |
| **Euclidiana** | distância, fora de [0,1] | quando o modelo foi treinado com distância euclidiana |

⚠️ Misturar métricas entre treino e inferência quebra o índice silenciosamente.

## Código

```python
import numpy as np

def cos(a, b):
    a, b = np.asarray(a), np.asarray(b)
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))

# atenção: divide por zero se algum vetor for nulo
```

## Autoavaliação
1. **P:** Por que cosseno e não produto escalar em geral? **R:** porque embeddings não têm magnitude semanticamente calibrada entre exemplos; o cosseno isola a direção, que é onde está o significado.
2. **P:** E se o modelo foi treinado com produto escalar? **R:** aí o produto escalar passa a ser melhor — métrica errada degrada ranqueamento de forma silenciosa.

## Onde vi isso

- Visto em:[[Embedding]]

## Ver também

- [[Embedding]] · [[Busca Semântica]] · [[RAG]]
