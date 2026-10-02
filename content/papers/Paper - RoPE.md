---
title: "Paper - RoPE"
tags:
  - "paper"
  - "transformers"
tipo: "paper"
date: "2026-10-14"
---

# Paper — RoFormer: Enhanced Transformer with Rotary Position Embedding

> **Por que estou lendo isso:** porque RoPE é o padrão de codificação posicional de quase todo LLM moderno, e o paper original de 2017 usava uma abordagem diferente.

## Ficha

| Campo | Valor |
| --- | --- |
| Título | RoFormer: Enhanced Transformer with Rotary Position Embedding |
| Autores | Jianlin Su, Yu Lu, Shengfeng Pan, Ahmed Murtadha, Bo Wen, Yunfeng Liu |
| Ano / Venue | 2021 (arXiv) |
| Link | https://arxiv.org/abs/2104.09864 |
| Tópicos | Positional encoding · Attention · Comprimento de sequência |

## Resumo em 5 linhas

1. **Problema:** codificações posicionais **aditivas** codificam posição **absoluta**, o que é desligado do que a atenção de fato usa (distância entre pares) e dificulta extrapolação.
2. **Método:** em vez de adicionar um vetor de posição, **rotacionar** $Q$ e $K$ por matrizes de rotação que dependem da posição.
3. **Resultado:** o produto $QK^\top$ passa a codificar **posição relativa** de forma natural, com decaimento suave em distâncias longas.
4. **Custo:** nenhum parâmetro extra — é uma reparametrização, sem pesos novos.
5. **Conclusão:** compatível com atenção linear e com interpolação de comprimento; virou padrão em LLaMA, GPT-NeoX, PaLM, Mistral, Qwen, Gemma.

## O que eu levo embora

- **Posição relativa é a posição que importa** — e ela sai de graça da rotação.
- Extrapolação de contexto é um problema de **escala da base de rotação**, não de arquitetura.

## Detalhes que merecem atenção

### A ideia

Posicional **aditivo** (2017, BERT, GPT-2):

$$h = x + p_i \qquad \text{com } p_i \text{ um vetor por índice absoluto}$$

Posicional **rotacional** (RoPE):

$$q_i' = R(\theta i) \, q_i, \qquad k_j' = R(\theta j) \, k_j$$

e, como a rotação é um produto ortogonal,

$$q_i' \cdot k_j' = q_i^\top R(\theta (i - j)) \, k_j$$

O termo que aparece é $R(\theta(i-j))$ — **depende só da diferença**. Isso é o argumento inteiro do paper.

### Propriedades alegadas

| Propriedade | Aditivo | RoPE |
| --- | --- | --- |
| posição relativa | precisa ser aprendida | **emergente** |
| extrapolação | ruim | melhor (com ajuste de base) |
| parâmetros extras | $n_{\max} \times d$ | **nenhum** |
| compatível com atenção linear | não | **sim** |

### Limitações e a pergunta que ficou aberta

Extrapolação além do comprimento de treino **não é perfeita**. A comunidade resolve na prática com ajustes de **base de rotação** (NTK-aware scaling, YaRN), que não estavam no paper original — evolve na prática antes de evoluir na teoria.

### Perguntas que o paper deixa abertas

- [ ] Qual o ajuste correto da base de rotação para 4× o contexto? (→ YaRN, NTK)
- [ ] RoPE sobrevive à quantização do KV cache?

## Onde isso conecta

- Pesquisa: [[Pesquisa - Transformer e self-attention]]

## Rethinking

> A[[Transformer]] diz "atenção é permutacional, precisa de posição". Este paper mostra a **segunda metade**: posição absoluta é a representação errada. Uma boa intuição aqui já salva metade da leitura de papers de posição.

## Notas de leitura

| Passada | Data | Conclusão |
| --- | --- | --- |
| 1 — 15 min | | |
| 2 — método | | |
| 3 — crítica | | |

---
*Lido em 2026-09-30*
