---
title: "Top-p Sampling"
tags:
  - "conceito"
  - "decodificacao"
tipo: "conceito"
date: "2026-10-01"
---

# Top-p Sampling

> **Definição em uma frase:** mantém apenas o menor conjunto de tokens cuja probabilidade acumulada atinge `p`, e sorteia dentro dele.

## Comparação com top-k

| | Top-k | Top-p (nucleus) |
| --- | --- | --- |
| Regra | mantém os $k$ mais prováveis | mantém massa acumulada $\ge p$ |
| Tamanho do conjunto | **fixo** ($k$) | **variável** |
| Distribuição concentrada | mantém $k$ candidatos a mais do que o necessário | mantém poucos |
| Distribuição plana | corta demais (modelo não sabe, mantém 50) | mantém muitos (o modelo está em dúvida) |

Top-k com $k$ fixo é arbitrário: o mesmo $k$ é errado para uma distribuição afiada e para uma plana. Top-p se adapta ao **grau de confiança do modelo** — por isso virou o padrão.

```python
import numpy as np

def top_p_filter(p, top_p=0.9):
    order = np.argsort(-p)
    cum = np.cumsum(p[order])
    k = int(np.searchsorted(cum, top_p) + 1)
    mask = np.zeros(len(p), dtype=bool)
    mask[order[:k]] = True
    return p * mask / (p * mask).sum()   # renormaliza
```

## Parentes

- **min-p** (Nguyen et al., ICLR 2025) — mantém tokens com $p_v \ge \tau \cdot p_{\max}$: limiar **relativo à confiança**, mais estável que top-p quando a distribuição é muito achatada.
- **Typical decoding** (Meister et al., 2022) — mantém tokens cuja informação $-\log p$ está próxima da entropia condicional.

## Autoavaliação
1. **P:** Por que top-p substituiu top-k na prática? **R:** porque adapta o número de candidatos à confiança real do modelo, em vez de usar um $k$ arbitrário.
2. **P:** Top-p com $p=0.99$ é "sem truncagem"? **R:** quase. Depende da distribuição; se nem 99% da massa couber em 10 tokens, ainda trunca.

## Onde vi isso

- Visto em: [[Temperatura e previsibilidade]]

## Ver também

- [[Temperatura]] · [[Logits]] · [[Top-k Sampling]]

---
*Atualizado em 2026-09-30*
