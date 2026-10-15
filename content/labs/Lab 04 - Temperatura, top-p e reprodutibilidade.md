---
title: "Lab 04 - Temperatura, top-p e reprodutibilidade"
tags:
  - "lab"
  - "decodificacao"
tipo: "lab"
date: "2026-10-07"
---

# Lab 04 — Temperatura, top-p e reprodutibilidade

> **O que este lab prova:** que temperatura e top-p alteram o **conjunto de candidatos**, que `T=0` é determinístico e independente de seed, e que temperatura **não muda o ranking** dos tokens.

## Pergunta

Qual é o efeito quantitativo de cada parâmetro de sampling sobre a distribuição e sobre a variedade de saída?

## Hipótese

> (1) Temperatura não altera a ordem dos tokens, só a concentração. (2) Top-k fixa o número de candidatos; top-p varia com a confiança. (3) `T=0` produz sempre a mesma saída, qualquer que seja a seed.

## Setup

```bash
pip install numpy
```

## Código

```python
import numpy as np

V = 12

def fake_model(prefix, rng):
    """'Modelo' fictício: logits que dependem do último token."""
    last = prefix[-1] if prefix else 0
    z = rng.normal(0, 1, size=V) * 1.5
    z[last] += 2.0                      # viés para repetir o último token
    z[(last + 1) % V] += 0.7            # e para o próximo
    return z

def softmax(z, T=1.0):
    if T <= 0:
        p = np.zeros_like(z); p[np.argmax(z)] = 1.0
        return p
    z = z / T                            # temperatura ANTES do softmax
    z = z - z.max()
    e = np.exp(z)
    return e / e.sum()

def top_k_mask(p, k):
    m = np.zeros(len(p), dtype=bool)
    m[np.argsort(-p)[:k]] = True
    return m

def top_p_mask(p, top_p):
    order = np.argsort(-p)
    k = int(np.searchsorted(np.cumsum(p[order]), top_p) + 1)
    m = np.zeros(len(p), dtype=bool); m[order[:k]] = True
    return m

def generate(steps=12, seed=0, T=1.0, k=None, top_p=None, logprobs=False):
    rng = np.random.default_rng(seed)
    out, lps = [], []
    for _ in range(steps):
        z = fake_model(out, rng)
        p = softmax(z, T)
        if logprobs: lps.append(p.copy())
        if T <= 0:
            out.append(int(np.argmax(z))); continue
        m = np.ones(V, dtype=bool)
        if k is not None:     m &= top_k_mask(p, k)
        if top_p is not None: m &= top_p_mask(p, top_p)
        p = np.where(m, p, 0.0); p = p / p.sum()
        out.append(int(np.searchsorted(np.cumsum(p), rng.random(), side="right")))
    return (out, lps) if logprobs else out

def entropia(p):
    p = p[p > 0]
    return float(-(p * np.log(p)).sum())

def n_candidatos(p, k=None, top_p=None):
    m = np.ones(len(p), dtype=bool)
    if k is not None:     m &= top_k_mask(p, k)
    if top_p is not None: m &= top_p_mask(p, top_p)
    return int(m.sum())

# ================= 1) Temperatura: entropia e número de candidatos =================
print("1) Efeito da temperatura (mesmos logits)")
rng = np.random.default_rng(42)
z = rng.normal(0, 1.5, size=V)
print(f"   {'T':>6}{'entropia':>12}{'T':>6}{'entropia':>12}")
for T in [0.1, 0.3, 0.5, 0.7, 1.0, 1.5, 2.0]:
    p = softmax(z, T)
    print(f"   {T:>6}{entropia(p):>12.4f}", end="")
    if T in [0.3, 1.5]: print()
print()

# ================= 2) Ranking NÃO muda com temperatura =================
print("\n2) O ranking dos tokens muda com a temperatura?")
for T in [0.3, 1.0, 2.0]:
    order = np.argsort(-softmax(z, T))
    print(f"   T={T}: top-5 ids = {list(order[:5])}")
print("   → o MESMO ranking. A temperatura muda a GEOMETRIA, não a ordem.\n")

# ================= 3) top-k (fixo) vs top-p (variável) =================
print("3) Nº de candidatos: top-k é fixo; top-p varia com a confiança")
rng = np.random.default_rng(7)
for nome, z in [("confiante", np.array([6.,4.,2.,1.,0.,-1.,-2.,-3.,-4.,-5.,-6.,-7.])),
                ("diferente", rng.normal(0,1,V))]:
    p1 = softmax(z, 1.0)
    print(f"   {nome:<11} top_k=3 -> {n_candidatos(p1, k=3)} | "
          f"top_p=0.9 -> {n_candidatos(p1, top_p=0.9)}")
print("   → top-k sempre 3; top-p adapta. Em distribuição difusa, top_p mantém mais.\n")

# ================= 4) Variety de saída =================
print("4) Variety de saída em 20 execuções")
for label, kw in [("T=0",        dict(T=0)),
                  ("T=0.7",      dict(T=0.7)),
                  ("T=1.0",      dict(T=1.0)),
                  ("T=0.7 k=1",  dict(T=0.7, k=1)),
                  ("T=0.7 p=0.8",dict(T=0.7, top_p=0.8))]:
    outs = {tuple(generate(seed=s, **kw)) for s in range(20)}
    print(f"   {label:<12} saídas distintas: {len(outs):>2}/20")

# ================= 5) Reprodutibilidade =================
print("\n5) Reprodutibilidade")
assert generate(seed=1, T=0) == generate(seed=999, T=0), "T=0 deveria ser idêntico"
print("   T=0 independente de seed ✓")
assert generate(seed=1, T=0.7) == generate(seed=1, T=0.7), "mesma seed deve reproduzir"
print("   mesma seed + mesmos parâmetros reproduz ✓")
assert generate(seed=1, T=0.7) != generate(seed=2, T=0.7), "seeds diferentes devem divergir"
print("   seeds diferentes divergem (esperado) ✓")

# ================= 6) Repetição =================
print("\n6) Efeito de k=1 (greedy) em texto com viés de repetição")
out = generate(seed=3, T=0.7, k=1)
print(f"   {out}")
print("   → observe tokens repetidos: o modelo está preso num loop.")
```

## Como rodar

```bash
python lab04_sampling.py
```

## O que observei

| Teste | Esperado | Observado |
| --- | --- | --- |
| Entropia cresce com $T$ | sim | |
| Ranking invariante a $T$ | sim | |
| top-k: sempre $k$ candidatos | sim | |
| top-p: varia com confiança | sim | |
| $T=0$ independente de seed | sim | |
| $k=1$ produz repetição | sim | |

## Análise

- [ ] A entropia dobra quando a temperatura dobra?
- [ ] Em $T=0.7$, top-p mantém mais ou menos candidatos que top-k=3? Por quê?
- [ ] Se eu precisar de saída idêntica em produção, o que ainda pode quebrar? (resposta: **fonte numérica** —[[Temperatura e previsibilidade]]

## Extensão

- [ ] Chamar uma API real 10× com `temperature=0` e `seed` fixo, e comparar.
- [ ] Verificar `system_fingerprint` em cada resposta.
- [ ] Medir a taxa de acerto de extração de JSON com `T=0` vs. `T=0.7`.
- [ ] Implementar `min_p` e comparar com `top_p`.

## Conceitos tocados


## Erros que cometi

- 

---
*Atualizado em 2026-09-30*
