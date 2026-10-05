---
title: "Paper - GQA"
tags:
  - "paper"
  - "inferencia"
tipo: "paper"
date: "2026-10-21"
---

# Paper — GQA: Training Generalized Multi-Query Transformer Models

> **Por que estou lendo isso:** porque responde uma pergunta prática que a[[Transformers, de um jeito simples]] deixa em aberto — por que reduzir cabeças de chave/valor acelera tanto o decode.

## Ficha

| Campo | Valor |
| --- | --- |
| Título | GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints |
| Autores | Joshua Ainslie, James Lee-Thorp, Michiel de Jong, Yury Zemlyanskiy, Federico Lebrón, Sumit Sanghai (Google) |
| Ano / Venue | EMNLP 2023 |
| Link | https://arxiv.org/abs/2305.13245 |
| Tópicos | KV cache · Eficiência · Inferência |

## Resumo em 5 linhas

1. **Problema:** MQA (1 cabeça K/V) é rápido mas perde qualidade; MHA (H cabeças) é caro no decode por causa do [[KV Cache]].
2. **Método:** generalizar para **G** grupos de cabeças de query compartilhando uma cabeça K/V, com $1 < G < H$.
3. **Resultado:** qualidade próxima de MHA com velocidade próxima de MQA. E o ponto prático: converte um checkpoint MHA existente com **~5% do compute original**.
4. **Custo:** qualidade ligeiramente abaixo de MHA em model sizes pequenos.
5. **Conclusão:** adopted como padrão (LLaMA 2/3, Mistral, Gemma, Qwen).

## O que eu levo embora

- **O gargalo do decode é memória, e o KV cache é a maior fatia.** Reduzir cabeças K/V é a alavanca mais direta.
- É otimização de **constante**, não de complexidade: a atenção continua O(n²).

## Detalhes que merecem atenção

### A progressão

| Variante | Cabeças K/V | Cache | Qualidade |
| --- | --- | --- | --- |
| **MHA** | H | máximo | melhor |
| **GQA** | G (intermediário) | intermediário | quase MHA |
| **MQA** | 1 | mínimo | pior |

### O truque de uptraining

Conversão de MHA → GQA:

1. agrupar as $H$ cabeças em $G$ grupos;
2. **médiaponderada** (mean-pooling) das matrizes de projeção de cada grupo;
3. continuar o pré-treino por um curto período.

É por isso que é barato: não é retreinar, é uma conversão + refino.

### Limitações

- Ganho depende do tamanho do modelo; em modelos pequenos o ganho é modesto.
- Não muda a complexidade assintótica da atenção.

### Perguntas abertas

- [ ] E se combinarmos GQA com quantização do KV cache — qual o ganho composto?
- [ ] Existe limite para quantas cabeças K/V se pode remover sem dano?

## Onde isso conecta

- Pesquisa: [[Pesquisa - Transformer e self-attention]]

## Rethinking

> Ao otimizar inferência, a pergunta correta não é "qual kernel usar" mas **"qual é o gargalo agora: FLOPs ou bytes lidos?"**. GQA só faz sentido porque o gargalo do decode são bytes.

## Notas de leitura

| Passada | Data | Conclusão |
| --- | --- | --- |
| 1 — 15 min | | |
| 2 — método | | |
| 3 — crítica | | |

---
*Lido em 2026-09-30*
