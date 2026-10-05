---
title: "Embedding"
tags:
  - "conceito"
  - "embeddings"
tipo: "conceito"
date: "2026-10-01"
---

# Embedding

> **Definição em uma frase:** um vetor denso treinado para que a distância entre vetores represente similaridade de significado.

## Explicação curta

Um embedding mapeia texto (ou imagem, ou áudio) para um ponto de um espaço contínuo. O que faz ele funcionar é a **hipótese distribucional**: palavras que aparecem em contextos parecidos têm significados parecidos. O significado vira geometria.

## Como funciona (mecanismo)

**word2vec** (2013) — duas arquiteturas:

- *Skip-gram*: da palavra central, prever as vizinhas (bom para termos raros).
- *CBOW*: das vizinhas, prever a central (mais rápido).
- *Negative sampling*: troca softmax sobre 100 mil classes por um classificador binário "esse par apareceu / esse par foi sorteado". Foi esse truque que tornou o viável.

**SBERT** (Reimers & Gurevych, 2019) — rede **siamesa** (dois encoders com pesos compartilhados) que produz **um vetor fixo por frase**, permitindo comparar com um único cosseno em vez de rodar o modelo em cada par. Treinado com **contrastive learning** e **hard negatives**.

```python
from sentence_transformers import SentenceTransformer
m = SentenceTransformer("all-MiniLM-L6-v2")
v = m.encode("o dog está latindo")
v.shape # (384,)
```

## Comparações

| Abordagem | Bom em | Cego para |
| --- | --- | --- |
| Embedding denso | paráfrase, sinônimo, tradução | números, siglas, OOV |
| BM25 (esparso) | match literal, nomes, códigos | paráfrase sem sobreposição |

Por isso **busca híbrida** é o padrão real: ver [[Busca Semântica]].

## Confusões e aparências

- ❌ **Não é** compressão nem PCA. PCA preserva **variância**, não semântica. Reduzir embeddings com PCA pode colapsar a recuperação.
- ❌ **Não é** propriedade do texto. É propriedade do par *(modelo, corpus de treino)*.
- ✅ **É** um índice: trocar de modelo exige **reindexar tudo**.

## Limitações

1. Viés dos corpora replicado no espaço vetorial.
2. Ordem e negação se perdem (o chunk vira conjunto).
3. Domínio técnico degrada sem retreino.

## Autoavaliação
1. **P:** Por que `vetor("rei") - vetor("homem") + vetor("mulher") ≈ vetor("rainha")` funciona? **R:** porque a geometria do espaço foi otimizada para que relações semânticas apareçam como operações lineares.
2. **P:** Um sistema precisa achar o contrato "8842-A". Embedding resolve? **R:** não de forma confiável — identificadores arbitrários são ruído semântico. BM25 resolve.

## Onde vi isso

- Visto em: [[Embeddings: transformando texto em vetores]]
- Aprofundamento: [[Pesquisa - Embeddings e busca semântica]]

## Ver também

- [[Similaridade de Cosseno]] · [[RAG]] · [[Busca Semântica]] · [[Chunking]]

---
*Atualizado em 2026-09-30*
