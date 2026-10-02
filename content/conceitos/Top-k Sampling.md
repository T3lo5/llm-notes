---
title: "Top-k Sampling"
tags:
  - "conceito"
  - "decodificacao"
tipo: "conceito"
date: "2026-10-01"
---

# Top-k Sampling

> **Definição em uma frase:** mantém apenas os $k$ tokens de maior probabilidade e sorteia dentro deles.

## Mecanismo

```python
import numpy as np

def top_k_filter(p, k):
    keep = np.argsort(-p)[:k]
    m = np.zeros(len(p), dtype=bool); m[keep] = True
    return p * m / (p * m).sum()
```

## Quando ainda faz sentido

- Custo computacional previsível: você sabe exatamente quantos candidatos serão avaliados.
- Top-k é uma **restrição rígida de qualidade**: nunca sai nada abaixo do rank $k$. Em sistemas onde "não pode sair besteira" importa mais do que criatividade, é uma rede de segurança útil.
- Em muitos modelos atuais via API, `top_k` nem está exposto — o padrão é top-p.

## Erro comum

Usar $k$ fixo sem considerar a distribuição. Com $k=50$ e o modelo muito confiante, você mantém 50 candidatos quando 1 bastava, introduzindo ruído. Com $k=2$ e o modelo perdido, você corta a resposta certa. **Confiança e $k$ precisam andar juntos** — é o que o top-p faz automaticamente.

## Autoavaliação
1. **P:** Top-k com $k=1$ é o que? **R:** greedy decoding (argmax) — exatamente equivalente a $T=0$.
2. **P:** Por que top-k puro é mais frágil que top-p? **R:** $k$ é escolhido às cegas, sem considerar se a distribuição está plana ou concentrada.

## Onde vi isso

- Visto em:[[Temperatura]]

## Ver também

- [[Top-p Sampling]] · [[Temperatura]]

---
*Atualizado em 2026-09-30*
