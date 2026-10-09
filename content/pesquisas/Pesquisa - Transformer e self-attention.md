---
title: "Pesquisa - Transformer e self-attention"
tags:
  - "pesquisa"
  - "transformers"
tipo: "pesquisa"
date: "2026-10-07"
---

# Pesquisa — Transformer e self-attention

> **Pergunta que motivou esta pesquisa:** o que exatamente o Transformer resolveu, o que mudou desde 2018, e quais otimizações de hoje mudam **complexidade** e quais só mudam **constante**?

## Resposta curta (TL;DR)

O Transformer removeu recorrência e convolução, substituindo por atenção — o que destravou treino massivamente paralelo e dependências de longo alcance. A equação `softmax(QKᵀ/√d_k)V` é tudo que há; o resto (LayerNorm, MLP, codificação posicional) é estrutura de suporte. Desde 2018 as mudanças de arquitetura foram quase todas substituições (RMSNorm no lugar de LayerNorm, RoPE no lugar de posicional aditivo, SwiGLU no lugar de ReLU) e otimizações **de constante** — GQA e FlashAttention melhoram o gargalo sem mudar o $O(n^2)$ da atenção.

## Resposta completa

### O que foi abandonado, e por quê

RNN/LSTM liam a sequência um passo por vez. Dois problemas práticos:

1. **Sem paralelismo no treino.** O estado em $t$ depende do estado em $t-1$; a GPU fica ociosa. Nenhum modelo grande era treinável.
2. **Dependência de longo alcance.** Caminho longo entre a primeira e a última palavra, sujeito a desaparecimento de gradiente.

**Attention Is All You Need** (Vaswani et al., 2017) elimina ambos.

### A equação

$$\text{Attention}(Q,K,V)=\text{softmax}\!\left(\frac{QK^\top}{\sqrt{d_k}}\right)V$$

- $QK^\top$ — compatibilidade par a par, matriz $n\times n$.
- $\sqrt{d_k}$ — **scaling**: sem ele, com $d_k$ grande o softmax satura e o gradiente morre.
- `softmax` — linha vira distribuição (attention weights).
- $\times V$ — média ponderada dos valores.

**Multi-head**: $h$ cabeças em paralelo com projeções próprias. Não há roteamento — a especialização é emergente e frágil.

**Máscara causal** (decoder-only): $-\infty$ no triângulo superior antes do softmax. Sem ela o modelo veria a resposta ao prevê-la.

### O que mudou desde 2018

| Original (2017) | Moderno | Paper |
| --- | --- | --- |
| post-LayerNorm | pre-RMSNorm | Zhang & Sennrich, 2019 — arXiv:1910.07467 |
| posicional sinusoidal / absoluto | **RoPE** | Su et al., 2021 — arXiv:2104.09864 |
| ReLU $4d$ | **SwiGLU** $\frac{8}{3}d$ | Shazeer, 2020 — arXiv:2002.05202 |
| multi-head denso | **GQA/MQA** | Ainslie et al., 2023 — arXiv:2305.13245 |
| matriz de atenção materializada | **FlashAttention** | Dao et al., 2022 — arXiv:2205.14135 |
| dropout amplo | removido em vários pontos | — |

### A distinção que separa quem entende de quem decora

| Técnica | Muda complexidade? | Muda o quê |
| --- | --- | --- |
| **FlashAttention** | ❌ não (atenção continua **exata**) | tempo de parede e memória — tiling, IO-aware. Speedups reportados de 2–4× |
| **GQA** | ❌ não | número de cabeças K/V → encolhe o [[KV Cache]], acelera o decode |
| **Mamba** (Gu & Dao, 2023) | ✅ **sim** — linear em $T$ | substitui atenção por SSM seletivo |
| **Sliding window** | ✅ sim (parcial) | $O(n \cdot w)$ em vez de $O(n^2)$ |

> **Para um contexto de 1M de tokens, GQA e FlashAttention não resolvem.** Elas compram fatores — e fatores se esgotam. O termo quadrático continua mandando no orçamento de memória.

### RoPE em detalhe

Em vez de **adicionar** um vetor de posição, RoPE **rotaciona** $Q$ e $K$ por matrizes de rotação que dependem da posição. O produto $QK^\top$ passa a codificar **distância relativa** naturalmente, com decaimento suave em distâncias longas. É o padrão de LLaMA, Mistral, Gemma, Qwen.

### Limites práticos

1. atenção é $O(n^2)$ — dobrar o contexto dobra o custo;
2. extrapolação além do treino ainda exige ajuste (base de rotação, escala de RoPE);
3. atenção densa é cara em memória — daí quantização do KV cache e [[Paper - Mamba]].

## Detalhes técnicos

```python
import numpy as np

def softmax(x, axis=-1):
    x = x - x.max(axis=axis, keepdims=True)   # estabilidade numérica
    e = np.exp(x)
    return e / e.sum(axis=axis, keepdims=True)

def self_attention(Q, K, V, mask=None):
    """
    Q, K, V: (n, d_k) — n tokens, d_k dimensão por cabeça
    mask: (n, n) booleano, True = bloquear (ex.: causal)
    """
    scores = Q @ K.T / np.sqrt(Q.shape[-1])     # scaling por sqrt(d_k)
    if mask is not None:
        scores = np.where(mask, -np.inf, scores)
    W = softmax(scores)                          # (n, n) attention weights
    return W @ V, W                              # saída e pesos

# Máscara causal: token i só vê tokens <= i
causal = np.tril(np.ones((n, n), dtype=bool))

# Verificação crítica: W deve somar 1 em cada linha
out, W = self_attention(Q, K, V, mask=causal)
assert np.allclose(W.sum(axis=1), 1.0)
```

> 💡 Verificação rápida que vale memorizar: **cada linha de attention weights soma 1**. Se não soma, há bug.

## Comparações

| Arquitetura | Vantagem | Custo |
| --- | --- | --- |
| Transformer | paralelismo, dependências longas | $O(n^2)$ |
| RNN/LSTM | linear em $T$ | sem paralelismo, memória curta |
| SSM (Mamba) | linear e com *content awareness* | ecossistema imaturo |

## Limitações e riscos

- **Attention weights não são explicações.** São uma fração dos parâmetros e produto de muitas camadas.
- **Cabeças não são unidades nomeáveis.** Nenhum sistema pode assumir "a cabeça 3 faz coreferência" — não sobrevive a fine-tune.
- A literature de explicabilidade documenta extensivamente que mapas de calor de atenção são interpretáveis de forma enganosa.

## O que isso muda na minha prática

- [x] Sempre aplicar máscara causal em decoder-only (e verificar somatório das linhas = 1).
- [ ] Ao estimar custo de contexto longo, lembrar que o gargalo é quadrático.
- [ ] Ao escolher otimização, perguntar: muda complexidade ou só constante?

## Fontes

1. **Attention Is All You Need** — Vaswani et al., NeurIPS 2017. https://arxiv.org/abs/1706.03762
2. **BERT** — Devlin et al., NAACL 2019. https://arxiv.org/abs/1810.04805
3. **Root Mean Square Layer Normalization (RMSNorm)** — Zhang & Sennrich, 2019. https://arxiv.org/abs/1910.07467
4. **GLU Variants Improve Transformer (SwiGLU)** — Shazeer, 2020. https://arxiv.org/abs/2002.05202
5. **RoFormer (RoPE)** — Su et al., 2021. https://arxiv.org/abs/2104.09864
6. **FlashAttention** — Dao et al., NeurIPS 2022. https://arxiv.org/abs/2205.14135
7. **GQA** — Ainslie et al., EMNLP 2023. https://arxiv.org/abs/2305.13245
8. **Mamba** — Gu & Dao, 2023. https://arxiv.org/abs/2312.00752
9. **Exploring the Limits of Transfer Learning with T5** — Raffel et al., JMLR 2020. https://arxiv.org/abs/1910.10683

## Perguntas abertas

- [ ] Rodar a atenção numericamente e observar as heads em um modelo pequeno — lab 03
- [ ] Onde está o gargalo real do meu pipeline: prefill ou decode?

## Ver também

- [[Arquitetura Transformers e Attention]] · [[Transformer]] · [[Self-Attention]] · [[KV Cache]]

---
*Atualizado em 2026-09-30*
