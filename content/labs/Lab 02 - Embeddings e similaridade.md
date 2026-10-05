---
title: "Lab 02 - Embeddings e similaridade"
tags:
  - "lab"
  - "embeddings"
tipo: "lab"
date: "2026-10-07"
---

# Lab 02 — Embeddings e similaridade

> **O que este lab prova:** que a similaridade de cosseno recupera paráfrases que BM25 não recupera, e que falha exatamente nos casos que você esperaria (códigos e números).

## Pergunta

Em que tipos de consulta o embedding ganha, em que tipos perde, e o que isso implica para escolher a estratégia de recuperação?

## Hipótese

> Embedding vence em paráfrase e perde em match literal (códigos, números, siglas). BM25 é o oposto. Um sistema que usa só um dos dois falha em casos previsíveis.

## Setup

```bash
pip install sentence-transformers numpy
```

## Código

```python
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2") # 384 dims, rápido, CPU

CORPUS = {
 "d1": "O contrato pode ser encerrado mediante aviso prévio de 30 dias.",
 "d2": "O servidor de produção caiu às 3h e ficou indisponível por duas horas.",
 "d3": "Contrato nº 8842-A, firmado em 12/03/2024 entre as partes.",
 "d4": "O termo de rescisão prevê aviso prévio de trinta dias.",
 "d5": "A política de backup exige retenção de 90 dias.",
 "d6": "Fulano Ltda registrou contrato 8842-A com a Alfa S.A.",
}
QUERIES = {
 "paráfrase sem termo comum": "como encerrar o contrato",
 "código exato": "contrato 8842-A",
 "nome próprio": "Fulano Ltda",
 "sinônimo técnico": "caiu o servidor",
}

ids = list(CORPUS)
texts = [CORPUS[i] for i in ids]
E = model.encode(texts, normalize_embeddings=True) # normalizado => cosseno = dot

def buscar(q, top=3):
 v = model.encode(q, normalize_embeddings=True)
 scores = E @ v
 order = np.argsort(-scores)
 return [(ids[i], float(scores[i])) for i in order[:top]]

def bm25_aproximado(q, top=3):
 """BM25 simplificado: sobreposição de termos (sem IDF real)."""
 qt = set(q.lower().split())
 scores = []
 for i in ids:
 dt = set(CORPUS[i].lower().split())
 overlap = len(qt & dt) / (len(qt) ** 0.5) # normalização simples
 scores.append((i, overlap))
 scores.sort(key=lambda x: -x[1])
 return scores[:top]

for nome, q in QUERIES.items():
 print(f"\n{'='*66}\nQUERY [{nome}]: {q!r}")
 print("-"*66)
 print(" embedding (cosseno):")
 for i, s in buscar(q):
 print(f" {s:.3f} {i}: {CORPUS[i][:60]}")
 print(" BM25 (sobreposição aproximada):")
 for i, s in bm25_aproximado(q):
 print(f" {s:.3f} {i}: {CORPUS[i][:60]}")

# --- Verificação: o mesmo texto tem cosseno 1 consigo mesmo ---
v = model.encode("teste de sanidade", normalize_embeddings=True)
print(f"\nautossimilaridade = {float(v @ v):.6f} (deve ser 1.0)")

# --- Verificação: PCA destrói semântica? ---
from sklearn.decomposition import PCA
import warnings; warnings.filterwarnings("ignore")

E_pca = PCA(n_components=2).fit_transform(E)
print("\nEmbeddings projetados em 2D com PCA (ruído, mas mostra a perda):")
for i, (a, b) in zip(ids, E_pca):
 print(f" {i}: ({a:+.3f}, {b:+.3f})")

# PCA preserva VARIÂNCIA, não SEMÂNTICA.
# Verifique: um PCA nas embeddings pode colapsar a recuperação.
```

## Como rodar

```bash
pip install scikit-learn
python lab02_embeddings.py
```

## O que observei

| Caso | Embedding | BM25 | Vencedor |
| --- | --- | --- | --- |
| paráfrase sem termo comum | | | embedding |
| código exato | | | BM25 |
| nome próprio | | | BM25 |
| sinônimo técnico | | | embedding |

## Análise

- [ ] A hipótese se confirmou?
- [ ] Em algum caso os dois erraram? Por quê?
- [ ] O PCA decomposto preservou a separação entre documentos parecidos?
- [ ] Qual modelo de embedding usaria para produção, e por quê?

## Extensão

- [ ] Implementar busca híbrida com RRF e comparar com cada método isolado.
- [ ] Avaliar os modelos no MTEB (subset de retrieval) e comparar com o resultado nas minhas queries.
- [ ] Testar um modelo multilíngue (BGE-M3, E5) com queries em português e documentos em inglês.
- [ ] Medir o ganho do reranking com um cross-encoder.

## Conceitos tocados


## Erros que cometi

- 

---
*Atualizado em 2026-09-30*
