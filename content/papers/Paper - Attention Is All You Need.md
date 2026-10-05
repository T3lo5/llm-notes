---
title: "Paper - Attention Is All You Need"
tags:
  - "paper"
  - "transformers"
tipo: "paper"
date: "2026-10-07"
---

# Paper — Attention Is All You Need

> **Por que estou lendo isso:** porque o Transformer é o objeto de tudo que o mapa descreve. Sem este paper, a[[Transformers, de um jeito simples]] é receita sem receita original.

## Ficha

| Campo | Valor |
| --- | --- |
| Título | Attention Is All You Need |
| Autores | Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Łukasz Kaiser, Illia Polosukhin |
| Ano / Venue | 2017 (arXiv) · NeurIPS 2017 |
| Link | https://arxiv.org/abs/1706.03762 |
| Tópicos | Transformer · Self-Attention · Eficiência · Paralelismo |

## Resumo em 5 linhas

1. **Problema:** sequência-a-sequência dependia de RNNs, que não paralelizam no treino e degradam dependências longas.
2. **Método:** uma arquitetura **apenas** de atenção, com projeções multi-cabeça, codificação posicional, conexões residuais e normalização — sem recorrência, sem convolução.
3. **Resultado:** qualidade no nível do estado da arte em tradução, com **treinamento ordens de grandeza mais rápido**.
4. **Custo:** mais memória por passo (a matriz de atenção é $O(n^2)$) — o que seria decidido muito depois, por FlashAttention e alternativas.
5. **Conclusão:** a remoção da recorrência é o que destrava escala; o resto do paper é a estrutura de suporte.

## O que eu levo embora

- **Self-attention + paralelismo = fundação de todos os LLMs modernos.**
- A equação `softmax(QKᵀ/√d_k)V` é o suficiente; o resto do paper é bookkeeping.
- O gargalo quadrático é a dívida que o campo pagou por 8 anos.

## Detalhes que merecem atenção

### Arquitetura

Seções 3.2–3.4 são o coração. Ler nesta ordem:

- **3.2 Attention** — a equação, o *scaling factor* $1/\sqrt{d_k}$, e por que masked attention é permitido.
- **3.2.1 Scaled Dot-Product Attention** — comparar com *dot product* e com *additive* (Bahdanau). Por que o dot escalado é mais barato computacionalmente.
- **3.2.2 Multi-Head Attention** — por que $h$ projeções paralelas em vez de uma só, e por que a saída é concatenada e projetada de volta ($W^O$).
- **3.2.3 Applications** — três usos: self-attention (encoder e decoder), attention entre encoder e decoder.
- **3.3 Positional Encoding** — a justificativa: atenção **não** é sensível à ordem. A solução sinusoidal com frequências decrescentes.
- **3.4 Encoder / Decoder** — 6 camadas, $d_{model}=512$, $h=8$, $d_{ff}=2048$.
- **3.5 Embeddings and Softmax** — o embedding de saída é compartilhado com a entrada (weight tying), e o softmax é calculado com tensores de mesma dimensão.

### Detalhes que o paper já aponta e ninguém lê

- **3.2.3.1 Einsum notation** — a notação de Einstein para os produtos matriciais. Se você não sabe, é 10 minutos bem investidos.
- **Apêndice B** — complexidades por camada: self-attention $O(n^2 d)$, feed-forward $O(n d^2)$. É aqui que está a justificativa quantitativa de que o MLP domina para $n \ll d$.
- **Apêndice D** — a posição no encoding é só adicionar, e que a sinusoidal "might be sufficient".

### Limitações declaradas pelos autores

> *"The Transformer does not inherently model sequential structure, so less effective than recurrent... in tasks requiring generating inference order."*

Eles **sabiam** que era um problema em 2017. Interessante ler isso e comparar com onde estamos.

### Perguntas que o paper deixa abertas

- [ ] Como escalar para sequências muito mais longas sem custo quadrático? (→ FlashAttention, sliding window, Mamba)
- [ ] Positional encoding learned em vez de fixed? (→ GPT-2, e depois RoPE)
- [ ] Quantas cabeças K/V são realmente necessárias? (→ GQA/MQA)

## Onde isso conecta

- Pesquisa: [[Pesquisa - Transformer e self-attention]]
- Lab: o lab 03

## Rethinking (o que eu faria diferente)

- Implementar self-attention em numpy **antes** de ler o paper. Lendo primeiro, a seção 3.2 vira fórmula; implementando depois, vira conferência.
- Ler a seção 3.2 com o o lab 03 ao lado, e verificar numericamente o que acontece sem `√d_k`.
- Comparar com Bahdanau (2014) para entender por que *dot product* escalado venceu *additive* — a resposta é custo computacional, e o paper não diz isso claramente.

## Notas de leitura

| Passada | Data | Conclusão |
| --- | --- | --- |
| 1 — 15 min | | |
| 2 — método | | |
| 3 — crítica | | |

---
*Lido em 2026-09-30*
