---
title: "Pesquisa - Embeddings e busca semântica"
tags:
  - "pesquisa"
  - "embeddings"
tipo: "pesquisa"
date: "2026-10-07"
---

# Pesquisa — Embeddings e busca semântica

> **Pergunta que motivou esta pesquisa:** por que busca vetorial e BM25 são usados juntos, e o que exatamente um modelo de embedding aprende a considerar "parecido"?

## Resposta curta (TL;DR)

Embeddings aprendem a **geometria do significado** a partir da hipótese distribucional: itens em contextos parecidos ficam próximos no espaço. Essa similaridade é **uma escolha do modelo**, não um fato do texto — por isso trocar de modelo exige reindexar tudo. BM25 captura o oposto (correspondência literal, códigos, nomes) e por isso os dois são estruturalmente complementares. E embeddings são Bons em *recall*, ruins em ranqueamento fino — daí a etapa obrigatória de reranking.

## Resposta completa

### word2vec e a hipótese distribucional

> *"Palavras que aparecem em contextos parecidos têm significados parecidos."* — Harris (1954); Firth (1957).

**Mikolov et al. (2013)** formalizam em duas arquiteturas:

- **Skip-gram** — da palavra central, prever as vizinhas. Cada ocorrência gera vários exemplos, então funciona bem para termos raros.
- **CBOW** — das vizinhas, prever a palavra central. Mais rápido, mas enviesado contra termos raros.

**Negative sampling** (Mikolov et al., 2013b) é o truque que tornou a abordagem viável: em vez de softmax sobre 100 mil classes, o modelo distingue binariamente "esse par apareceu" de "esse par foi sorteado". Converge muito mais rápido.

**GloVe** (Pennington et al., 2014) parte de uma matriz explícita de coocorrência e a fatora — mesma intuição, formalismo diferente.

Efeito colateral: aritmética vetorial vira semântica.

```python
# rei - homem + mulher ≈ rainha (ilustrativo, não exato)
v_rei = model.encode("rei"); v_homem = model.encode("homem")
v_mulher = model.encode("mulher"); v_rainha = model.encode("rainha")

analogy = v_rei - v_homem + v_mulher
score = cosine(analogy, v_rainha)
```

### De palavra para frase: SBERT

**O problema:** embeddings de palavra são estáticos — "banana" é o mesmo vetor em qualquer frase. Média de embeddings perde **ordem** e **negação** ("não é bom" não é a média de "não" e "bom").

**Reimers & Gurevych (2019)** treinam uma **rede siamesa**: duas instâncias do encoder com pesos compartilhados produzem **um vetor fixo por entrada**. A comparação passa a ser um único cosseno.

O resultado reportado: achar o par mais similar entre 10 mil sentenças cai de horas para segundos, mantendo a acurácia. É o que viabilizou busca semântica em escala de produção.

**Hard negatives** (DPR, Karpukhin et al. 2020) são o detalhe que separa recuperação robusta de embedding decorativo: negativos que **já são altamente similares** por busca lexical, forçando o modelo a discriminar diferença de sentido real.

### A tabela que resolve decisões de projeto

| Caso | BM25 | Embedding |
| --- | --- | --- |
| "contrato 8842-A" | ✅ | ❌ (ruído numérico) |
| nome próprio indexado | ✅ | ⚠️ falha silenciosa |
| paráfrase sem termo em comum | ❌ (estrutural) | ✅ (por construção) |

Conclusão: **busca híbrida**, com fusão por ranqueamento (RRF).

### Pipeline

- **Chunking** — ver [[Chunking]].
- **Índice** — kNN exato (força bruta, milhares), IVF (k-means), **HNSW** (grafo hierárquico, padrão atual).
- **Reranking** — cross-encoder reordena os 50–100 candidatos. Embeddings têm alto *recall* e ordenação imprecisa; o cross-encoder vê query e documento juntos.

### Métrica

[[Similaridade de Cosseno]] é o padrão por ser invariante à norma. Produto escalar em alguns modelos carrega informação de frequência e é preferível em índices de produção.

### Avaliação

**MTEB** (Muennighoff et al., 2022): 8 tarefas, 58 datasets, 112 idiomas.

A distinção que importa para projeto:

- **STS** — "esses dois textos significam a mesma coisa?"
- **Retrieval** — "qual chunk responde a esta pergunta?"

**Nenhum método domina todas as tarefas.** Avalie na sua tarefa, com seus casos.

## Detalhes técnicos

```python
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2") # 384 dims, rápido
corpus = ["o cachorro latiu", "o cachorro dormiu",
 "o servidor caiu", "o contrato foi encerrado"]

E = model.encode(corpus, normalize_embeddings=True) # normaliza -> cosseno = dot
q = model.encode("o cachorro fez barulho", normalize_embeddings=True)

scores = E @ q
rank = np.argsort(-scores)
for i in rank:
 print(f"{scores[i]:.3f} {corpus[i]}")
```

## Limitações e riscos

1. **Viés herdado** — os corpora moldam o espaço; estereótipos vazam para o resultado da busca.
2. **Ordem se perde** — o chunk é tratado como conjunto.
3. **Similaridade é escolha** — trocar o modelo exige **reindexar tudo**. Embeddings de modelos diferentes não convivem.
4. **Domínio** — embedding genérico degrada em jargão técnico sem retreino.

## O que isso muda na minha prática

- [x] Nunca reduzir embeddings com PCA (preserva variância, não semântica).
- [ ] Avaliar embeddings na **minha** tarefa, com cases reais, não no leaderboard.
- [ ] Indexar com busca híbrida desde o começo.
- [ ] Incluir reranking no pipeline do RAG e medir o ganho.

## Fontes

1. **Efficient Estimation of Word Representations in Vector Space** — Mikolov et al., 2013. https://arxiv.org/abs/1301.3781
2. **Distributed Representations of Words and Phrases and their Compositionality** — Mikolov et al., 2013. https://arxiv.org/abs/1310.4546
3. **GloVe: Global Vectors for Word Representation** — Pennington, Socher & Manning, EMNLP 2014. https://aclanthology.org/D14-1162/
4. **Sentence-BERT** — Reimers & Gurevych, EMNLP 2019. https://arxiv.org/abs/1908.10084
5. **Dense Passage Retrieval (DPR)** — Karpukhin et al., EMNLP 2020. https://arxiv.org/abs/2004.04906
6. **MTEB** — Muennighoff et al., EACL 2023. https://arxiv.org/abs/2210.07316
7. **HNSW** — Malkov & Yashunin, 2016. https://arxiv.org/abs/1603.09320
8. Leaderboard MTEB (vivo) — https://huggingface.co/spaces/mteb/leaderboard

## Perguntas abertas

- [ ] Qual modelo de embedding performo melhor no **meu** domínio?
- [ ] HNSW vs. IVF para o meu volume de corpus?

## Ver também

- [[Embeddings e vetorização]] · [[Embedding]] · [[Busca Semântica]] · [[Lab 02 - Embeddings e similaridade]]

---
*Atualizado em 2026-09-30*
