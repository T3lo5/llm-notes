---
title: "Transformers, de um jeito simples"
tags:
  - "transformers"
tipo: "guia"
date: "2026-10-01"
---

# Transformers, de um jeito simples

> **Meta:** explicar o mecanismo de self-attention, por que a posição precisa ser injetada, e o que mudou entre o paper de 2017 e os LLMs que você usa hoje.

## Resumo em 3 frases

1. Self-attention resolve cada token **olhando para todos os outros** e misturando os valores com pesos — sem recorrência e sem convolução, o que permite treino massivamente paralelo.
2. A equação é `softmax(QKᵀ/√d_k)V`; a divisão por `√d_k` existe só para o softmax não saturar, e a posição entra por fora porque atenção, sozinha, não sabe ordem.
3. Do paper original até hoje: a mesma receita, mas com RMSNorm, RoPE, SwiGLU, GQA e FlashAttention — quase todas otimizações de **constante**, não de complexidade.

## O problema que o Transformer resolveu

Antes de 2017, o estado da arte eram RNN/LSTM, lidos **um passo por vez**. Dois problemas:

1. **Não paralelizava no treino.** A posição *t* depende do estado em *t−1*, então a GPU ficava ociosa. Nenhum modelo grande era treinável.
2. **Dependência de longo alcance.** Levar informação da primeira palavra até a última atravessava um caminho longo e sujeta a desaparecimento de gradiente.

Vaswani et al. (2017) removem recorrência e convolução inteiramente. Daí o nome.

## Self-attention

Cada token é projetado em três vetores por matrizes treináveis:

- **Q (query)** — o que estou procurando
- **K (key)** — o que eu tenho a oferecer
- **V (value)** — o que eu entrego se houver interesse

$$\text{Attention}(Q,K,V) = \text{softmax}\!\left(\frac{QK^\top}{\sqrt{d_k}}\right) V$$

Leia passo a passo:

1. $QK^\top$ — matriz $n \times n$ de **scores** de compatibilidade entre cada par (token que pergunta, token que responde).
2. Divide por $\sqrt{d_k}$ — **scaling**. Com $d_k$ grande os produtos têm variância alta e o softmax satura (gradiente morre). A divisão normaliza.
3. `softmax` — cada linha vira distribuição; os pesos somam 1. Esses são os *attention weights*.
4. Multiplica por $V$ — a saída de cada posição é a **média ponderada** dos valores, com o peso dado por quanto cada token importa.

O ponto 4 é o coração da coisa: **cada token renova o próprio significado usando o contexto inteiro**, em uma única operação.

## Multi-head

Uma cabeça só é forçada a aprender uma única noção de relação. Com *h* cabeças em paralelo, cada uma com projeções próprias, o modelo pode capturar relações diferentes (dependência sintática em uma, coreferência em outra).

⚠️ **Armadilha:** não há roteamento, e a especialização é **emergente**, não projetada. Nenhum sistema pode assumir "a cabeça 3 faz coreferência" — isso não sobrevive a um fine-tune. E attention weights **não são explicações**.

## Máscara causal

Em modelos **decoder-only**, ao prever o token na posição *t* o modelo só pode ver posições ≤ *t*. Isso é a **máscara causal**: soma-se $-\infty$ ao triângulo superior dos scores antes do softmax, zerando qualquer dependência do futuro.

Sem ela, o modelo "veria a resposta enquanto aprende a prevê-la" e a loss cairia para quase zero sem nenhum aprendizado real.

Modelos **encoder-only** (BERT) não usam máscara: veem o texto inteiro dos dois lados.

## Positional encoding

Atenção é **permutacional**: reordenar as entradas apenas reordena as saídas. O modelo não tem ideia do que é "primeiro".

| Método | Como funciona | Onde é usado |
| --- | --- | --- |
| **Sinusoidal** (2017) | somas de senos com frequências decrescentes, por fórmula fechada | paper original |
| **Absoluto aprendido** | um vetor de posição por índice | BERT, GPT-2 |
| **RoPE** (Su et al., 2021) | rotaciona Q e K por ângulos dependentes da posição | LLaMA, Mistral, Gemma, Qwen |

**RoPE virou o padrão** porque o produto $QK^\top$ passa a codificar **distância relativa** de forma natural, e a extrapolação para sequências mais longas fica mais bem comportada.

## Bloco residual + normalização

Cada subcamada é embrulhada em `x + Sublayer(x)`. O residual dá um caminho direto para o gradiente e permite empilhar dezenas de camadas.

- **Pre-LayerNorm** (padrão dos LLMs atuais): normaliza antes da subcamada, com um segundo residual. Mais fácil de treinar que o post-LN do paper original.
- **RMSNorm** (Zhang & Sennrich, 2019): em vez de subtrair a média e dividir pelo desvio padrão, **apenas divide pela raiz da média dos quadrados**. A recentração foi removida por ser dispensável. Mais barato, qualidade equivalente — padrão em LLaMA e derivados.

## Feed-forward

Cada posição passa, independentemente das outras, por um MLP de duas camadas com expansão — tipicamente $d \rightarrow 4d \rightarrow d$ no paper original. **Aqui mora a maior parte dos parâmetros do modelo** e é onde a rede ajusta o conhecimento.

Variante atual: **SwiGLU** (Shazeer, 2020) — uma porta multiplicativa no lugar do ReLU/GELU simples. Para manter o número de parâmetros, a camada oculta encolhe de $4d$ para cerca de $\frac{8}{3}d$ (regra do LLaMA).

## Famílias de arquitetura

| Família | Atenção | Exemplos | Gera texto? |
| --- | --- | --- | --- |
| **Encoder-only** | bidirecional | BERT, RoBERTa | ❌ (representação) |
| **Decoder-only** | causal | GPT, LLaMA, Mistral | ✅ |
| **Encoder-decoder** | encoder bidirecional + decoder cross-atendendo | T5, BART, transformer original | ✅ |

Os LLMs de chat que você conhece são **decoder-only**.

## O que mudou desde 2018

| Componente | Original | Moderno |
| --- | --- | --- |
| Normalização | post-LayerNorm | **RMSNorm** (pre-norm) |
| Posição | sinusoidal / absoluto | **RoPE** |
| MLP | ReLU, 4d | **SwiGLU**, 8d/3 |
| Cabeças KV | multi-head denso | **GQA/MQA** (Ainslie et al., 2023) |
| Implementação | matriz de atenção materializada | **FlashAttention** (Dao et al., 2022) |
| Dropout | presente em tudo | removido em vários pontos |

Ressalva importante: **GQA e FlashAttention otimizam constantes, não complexidade.** GQA reduz o número de cabeças K/V (encolhe o [[KV Cache]], enorme ganho no decode); FlashAttention faz tiling e é IO-aware, mantendo a atenção **exata** (mesma matemática). As duas compram fatores — e fatores se esgotam. Só uma mudança de complexidade (atenção esparsa/sliding window, ou [[Paper - Mamba]]) altera o regime.

## O teto: O(n²)

A atenção é quadrática no comprimento da sequência. Dobrar o contexto dobra o custo. Reações conhecidas:

1. **Otimizar sem mudar a matemática** — FlashAttention.
2. **Atenção esparsa / sliding window** — cada token só olha `w` vizinhos: custo $O(n \cdot w)$.
3. **Atenção linear** — reordena operações para complexidade linear.
4. **Trocar de paradigma** — Mamba (Gu & Dao, 2023) usa state space models seletivos com complexidade linear.

## Perguntas para validar

1. Por que a divisão por $\sqrt{d_k}$ é necessária? O que acontece sem ela?
2. Se eu remover a máscara causal de um decoder-only, o que a loss faz? Por quê?
3. RoPE e codificação posicional absoluta: o que cada uma faz melhor?
4. Em um contexto de 1M de tokens, GQA e FlashAttention resolvem o problema? Justifique separando tempo de memória.

## Referências

- Vaswani et al., *Attention Is All You Need* — https://arxiv.org/abs/1706.03762
- Devlin et al., *BERT* — https://arxiv.org/abs/1810.04805
- Su et al., *RoFormer (RoPE)* — https://arxiv.org/abs/2104.09864
- Zhang & Sennrich, *RMSNorm* — https://arxiv.org/abs/1910.07467
- Shazeer, *GLU Variants Improve Transformer (SwiGLU)* — https://arxiv.org/abs/2002.05202
- Ainslie et al., *GQA* — https://arxiv.org/abs/2305.13245
- Dao et al., *FlashAttention* — https://arxiv.org/abs/2205.14135
- Gu & Dao, *Mamba* — https://arxiv.org/abs/2312.00752

## Ver também

- [[Pesquisa - Transformer e self-attention]] · [[Lab 03 - Inspecionando a atenção]] · [[Paper - Attention Is All You Need]]
