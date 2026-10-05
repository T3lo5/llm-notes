---
title: "Lab 03 - Inspecionando a atenção"
tags:
  - "lab"
  - "transformers"
tipo: "lab"
date: "2026-10-07"
---

# Lab 03 — Inspecionando a atenção

> **O que este lab prova:** que a atenção é uma média ponderada cuja distribuição é construída por `softmax(QKᵀ/√d_k)`, e que a máscara causal é o que impede o modelo de "ver o futuro".

## Pergunta

O que os pesos de atenção realmente medem, e o que acontece numericamente quando removemos o scaling ou a máscara causal?

## Hipótese

> (1) Cada linha de attention weights soma 1. (2) Sem o scaling por `√d_k`, os logits saturam e os pesos ficam degenerados (um-hot). (3) Sem máscara causal, a posição final consegue "enxergar" o último token.

## Setup

```bash
pip install numpy matplotlib
```

## Código

```python
import numpy as np

np.set_printoptions(precision=3, suppress=True, linewidth=120)

def softmax(x, axis=-1):
 x = x - x.max(axis=axis, keepdims=True) # estabilidade numérica
 e = np.exp(x)
 return e / e.sum(axis=axis, keepdims=True)

def attention(Q, K, V, causal=False, scale=True):
 """
 Q, K, V: (n, d_k) — n tokens, d_k dimensão por cabeça
 """
 s = Q @ K.T
 if scale:
 s = s / np.sqrt(Q.shape[-1]) # SCALING: sem isso, softmax satura
 if causal:
 n = len(Q)
 s = np.triu(s, k=1) # mascara causal: proibe o futuro
 s = np.where(np.triu(np.ones((n, n), dtype=bool), k=1), -np.inf, s)
 W = softmax(s)
 return W @ V, W

rng = np.random.default_rng(0)
n, dk = 6, 64 # 6 tokens, d_k = 64 (grande de propósito)
Q, K, V = rng.normal(size=(n, dk)), rng.normal(size=(n, dk)), rng.normal(size=(n, dk))

# --- 1) Com scaling + máscara causal ---
_, W_causal = attention(Q, K, V, causal=True, scale=True)
print("1) COM scaling, COM máscara causal:")
print(W_causal)
assert np.allclose(W_causal.sum(axis=1), 1.0), "cada linha deve somar 1"
assert np.allclose(np.triu(W_causal, k=1), 0.0), "triângulo superior deve ser 0"
print(" ✓ linhas somam 1; ✓ nenhum token 'enxerga' o futuro\n")

# --- 2) SEM máscara causal ---
_, W_full = attention(Q, K, V, causal=False, scale=True)
print("2) SEM máscara causal (o token 0 'enxerga' todos):")
print(W_full)
print(f" peso do token 0 na posição do token 0 (diagonal): {W_full[0,0]:.4f}")
print(" → agora o modelo pode copiar a resposta\n")

# --- 3) SEM scaling ---
_, W_noscale = attention(Q, K, V, causal=False, scale=False)
print("3) SEM scaling (d_k grande):")
print(W_noscale)
ent = -(W_noscale * np.log(W_noscale + 1e-12)).sum(axis=1)
print(f" entropia média por linha: {ent.mean():.4f} (baixa = degenerate, quase one-hot)")
print(" → gradientes morrem: o softmax saturou\n")

# --- 4) Efeito de dimensionar d_k ---
print("4) Entropia da atenção vs. d_k (sem scaling):")
for dk_test in [4, 16, 64, 256, 1024]:
 Qt = rng.normal(size=(n, dk_test)); Kt = rng.normal(size=(n, dk_test))
 s = Qt @ Kt.T / np.sqrt(dk_test)
 ent_s = -(softmax(s) * np.log(softmax(s) + 1e-12)).sum(axis=1).mean()
 s_raw = Qt @ Kt.T
 ent_r = -(softmax(s_raw) * np.log(softmax(s_raw) + 1e-12)).sum(axis=1).mean()
 print(f" d_k={dk_test:>5} com scaling: {ent_s:.4f} sem scaling: {ent_r:.4f}")

print("\n → quanto maior d_k, pior fica SEM scaling. É por isso que /sqrt(d_k) existe.")

# --- 5) Interpretação: atenção é média ponderada ---
out, W = attention(Q, K, V, causal=True)
manual = np.zeros(dk)
for i in range(n):
 manual += W[i] * V[i]
print(f"\n5) Saída pela matriz de pesos == soma manual: {np.allclose(out[0], manual, atol=1e-10)}")
print(" → atenção não é 'mágica': é uma média ponderada simples.")
```

## Como rodar

```bash
python lab03_atencao.py
```

## O que observei

| Teste | Esperado | Observado |
| --- | --- | --- |
| Linhas somam 1 | sim | |
| Triângulo superior zero (causal) | sim | |
| Entropia SEM scaling | baixa (degenerada) | |
| Entropia cresce com $d_k$ sem scaling | sim | |
| Saída == soma manual | true | |

## Análise

- [ ] A entropia sem scaling realmente colapsa? Em que ponto de $d_k$?
- [ ] O que os pesos da diagonal sugerem sobre a posição $t$ prever a posição $t+1$?
- [ ] Por que atenção como "média ponderada" não é uma explicação?

## Extensão

- [ ] Carregar um Transformer real (`transformers`) e plotar os mapas de atenção.
- [ ] Verificar empiricamente que **não** há roteamento entre cabeças.
- [ ] Comparar mapas de atenção com a remoção de uma camada — as explicações sobrevivem?
- [ ] Demonstrar o custo do KV cache: tempo de atenção com e sem cache.

## Conceitos tocados


## Erros que cometi

- 

---
*Atualizado em 2026-09-30*
