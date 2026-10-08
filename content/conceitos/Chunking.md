---
title: "Chunking"
tags:
  - "conceito"
  - "rag"
tipo: "conceito"
date: "2026-10-07"
---

# Chunking

> **Definição em uma frase:** o processo de cortar um documento em pedaços menores que serão os itens unitários da indexação vetorial.

## Explicação curta

Embeddings são calculados por pedaço. Se o pedaço for o documento inteiro, o vetor fica dilatado e sem informação específica. Se for pequeno demais, a ideia se parte e a busca perde o contexto. Chunking é a decisão que arbitra esse trade-off.

## Como funciona (mecanismo)

Parâmetros que se mexe:

| Parâmetro | Efeito |
| --- | --- |
| **Tamanho** | pequeno demais → fragmenta; grande demais → dilui |
| **Sobreposição** | evita que uma ideia seja partida na fronteira |
| **Estrutura** | respeitar títulos, parágrafos e listas em vez de cortar no meio |
| **Metadados** | guardar título, seção e origem — isso vira **citação** na resposta |

## O erro caro

> Chunking por **número fixo de caracteres**, ignorando a estrutura do documento.

Resultado: metade dos chunks começa no meio de uma frase e termina cortando a ideia seguinte. O embedding fica ruim e o modelo recebe trechos incoerentes.

Alternativa melhor: **chunking semântico por seção** (agrupar por heading) ou por frases, com sobreposição.

## Autoavaliação
1. **P:** Chunk maior é sempre melhor, porque captura mais contexto? **R:** não. O embedding representa o centro do conteúdo; texto irrelevante no chunk dilui o vetor. Além disso, cada chunk é token cobrado.
2. **P:** Como você cita a fonte na resposta? **R:** guardando metadados no índice e instruindo o modelo a citar o identificador. Sem metadados, não há citação possível.

## Onde vi isso

- Visto em: [[Embeddings e vetorização]]
- Aprofundamento: [[Pesquisa - Embeddings e busca semântica]]

## Ver também

- [[RAG]] · [[Embedding]] · [[Busca Semântica]]

---
*Atualizado em 2026-09-30*
