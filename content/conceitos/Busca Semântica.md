---
title: "Busca Semântica"
tags:
  - "conceito"
  - "rag"
tipo: "conceito"
date: "2026-10-01"
---

# Busca Semântica

> **Definição em uma frase:** recuperar documentos por significado, usando similaridade entre embeddings, em vez de por sobreposição de termos.

## Por que BM25 sozinho não basta

BM25 pontua por **sobreposição exata** com peso IDF. Isso é poderoso — e cego:

| Caso | BM25 | Embedding |
| --- | --- | --- |
| "contrato 8842-A" | ✅ exato, IDF máximo | ❌ ruído numérico |
| nome próprio "Fulano Ltda" | ✅ se indexado | ⚠️ falha silenciosa |
| "como encerrar o contrato" ↔ "termo de rescisão" | ❌ sem termo em comum | ✅ por construção |

## Busca híbrida

Combina os dois ranqueamentos e funde com **RRF** (Reciprocal Rank Fusion) ou ponderação aprendida. Não é ornamento: cada método tem um ponto cego **estrutural**, não ajustável.

## Pipeline de recuperação

| Etapa | Função | Custo |
| --- | --- | --- |
| Busca vetorial | alto *recall*, 50–100 candidatos | baixo |
| **Reranking** (cross-encoder) | ordenação fina | médio — mas **barato em latência**, caro em qualidade |

Reranking é o passo que mais melhora qualidade por custo: embeddings são ótimos em lembrar e imprecisos em ordenar. O cross-encoder vê query e documento **juntos**, o que o embedding não consegue fazer.

## Avaliação

- **MTEB** — 8 tarefas, 58 datasets, 112 idiomas. Distinção essencial: **STS** ("mesmo significado?") vs. **Retrieval** ("qual chunk responde?"). Um modelo pode ganhar em um e perder no outro.
- **Avalie na sua tarefa**, com seus casos, não na média do leaderboard.

## Autoavaliação
1. **P:** Por que embeddings e BM25 são complementares e não redundantes? **R:** porque os erros são estruturalmente opostos: o embedding não tem representação de arbitrário/literal, o BM25 não tem paráfrase.
2. **P:** Quando reranking não compensa? **R:** quando o recall da busca vetorial já é alto e o corpus é pequeno; a etapa extra vira latência sem ganho.

## Onde vi isso

- Visto em: [[Embeddings: transformando texto em vetores]]

## Ver também

- [[Embedding]] · [[Similaridade de Cosseno]] · [[RAG]] · [[Chunking]]

---
*Atualizado em 2026-09-30*
