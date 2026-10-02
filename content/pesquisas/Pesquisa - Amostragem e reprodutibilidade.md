---
title: "Pesquisa - Amostragem e reprodutibilidade"
tags:
  - "pesquisa"
  - "decodificacao"
tipo: "pesquisa"
date: "2026-10-07"
---

# Pesquisa — Amostragem e reprodutibilidade

> **Pergunta que motivou esta pesquisa:** por que a mesma requisição, com os mesmos parâmetros, devolve respostas diferentes? É o sorteio, o modelo, ou a infraestrutura?

## Resposta curta (TL;DR)

São **duas fontes distintas**. A **estatística**: a decodificação amostra de uma distribuição, e `temperature=0` (argmax) a elimina. A **numérica**: somar ponto flutuante não é associativo, e o particionamento das reduções em GPU depende do batch — logo `temperature=0` **não** a elimina. Diagnosticar qual das duas está agindo é simples: `system_fingerprint` igual com saídas diferentes aponta para a causa numérica; `system_fingerprint` diferente aponta para mudança do provedor.

## Resposta completa

### O pipeline de decodificação

```
logits → temperatura → truncamento → penalidades → softmax → amostragem
```

Toda a estocasticidade nasce **depois** do modelo. Dado o contexto, o transformer é uma função determinística: devolve o mesmo vetor de logits.

### Temperatura

$$p_i = \frac{e^{z_i/T}}{\sum_j e^{z_j/T}}$$

$T \to 0$ → argmax. $T < 1$ → afina. $T > 1$ → achata.

**Detalhe crucial:** temperatura não muda o **ranking** (dividir por escalar positivo é monotônico), muda a **concentração**. Daí a recomendação de mexer em `temperature` **ou** `top_p`, nunca nos dois.

### A cauda não confiável

**Holtzman et al. (ICLR 2020)**, *The Curious Case of Neural Text Degeneration*, é o paper que fundamenta a amostragem em vez de maximização:

- distribuições de maximum likelihood ficam muito suavizadas;
- a cauda de baixa probabilidade é **não confiável**;
- maximizá-la (greedy, beam) produz texto repetitivo e degenerado;
- a solução é **amostrar, mas truncar** → top-k, top-p, min-p, typical.

Daí a regra prática: *sampling* sozinho é ruído; maximização é degeneração; **amostrar da cauda truncada** é o ponto estável.

### A segunda fonte: ponto flutuante

Em precisão finita:

$$(a + b) + c \neq a + (b + c)$$

Num transformer há dezenas de reduções por token. Em GPU:

- o particionamento da redução depende do **tamanho do batch** e do número de threads;
- operações atômicas (`atomicAdd`) acumulam em **ordem arbitrária**;
- alguns kernels são não determinísticos entre execuções.

**Consequência:** mandar a mesma requisição como parte de um batch maior muda os logits o suficiente para **inverter o `argmax`** onde o topo está próximo.

Documentação de reprodutibilidade do PyTorch descreve exatamente isso e oferece `torch.use_deterministic_algorithms(True)`.

### Seed

`seed` inicializa o gerador pseudoaleatório, tornando a **sequência de sorteios** reproduzível. A documentação dos provedores é explícita: a API é não determinística por padrão, e com seed fixo as saídas são "majoritariamente iguais" — **sem garantia**.

O campo `system_fingerprint` muda quando o backend muda.

### Diagnóstico prático

| Observação | Diagnóstico |
| --- | --- |
| `system_fingerprint` **igual**, saídas diferentes | causa **numérica** (batch, kernel, backend não reprodutível) |
| `system_fingerprint` **diferente** | o **provedor** mudou o backend |
| Saídas diferentes só com `temperature > 0` | causa **estatística**, o que é esperado |
| Saídas diferentes só com batch maior | causa **numérica**, isolada |

## Detalhes técnicos

Implementação mínima e executável do pipeline completo:

```python
import numpy as np

V = 6   # vocabulário fictício

def softmax(z, T=1.0):
    if T <= 0:                       # T=0 não divide: faz argmax
        p = np.zeros_like(z); p[np.argmax(z)] = 1.0
        return p
    z = z / T                        # TEMPERATURA NOS LOGITS, antes do softmax
    z = z - z.max()                  # estabilidade numérica
    e = np.exp(z)
    return e / e.sum()

def fake_model(prefix):
    """'Modelo' fictício: logits condicionados ao último token."""
    last = prefix[-1] if prefix else 0
    z = np.array([3.0, 2.2, 1.4, 0.6, -0.4, -1.0]) * (0.5 + 0.1 * last)
    return z

def mask_top_k(p, k):
    keep = np.argsort(-p)[:k]
    m = np.zeros(V, dtype=bool); m[keep] = True
    return m

def mask_top_p(p, top_p):
    order = np.argsort(-p)
    cum = np.cumsum(p[order])
    k = int(np.searchsorted(cum, top_p) + 1)
    m = np.zeros(V, dtype=bool); m[order[:k]] = True
    return m

def generate(steps=8, seed=7, T=1.0, k=None, top_p=None):
    rng = np.random.default_rng(seed)
    out = []
    for _ in range(steps):
        z = fake_model(out)
        if T <= 0:
            out.append(int(np.argmax(z)))     # greedy: sem sorteio
            continue
        p = softmax(z, T)
        m = np.ones(V, dtype=bool)
        if k is not None:     m &= mask_top_k(p, k)
        if top_p is not None: m &= mask_top_p(p, top_p)
        p = np.where(m, p, 0.0)
        p = p / p.sum()                            # renormaliza
        u = rng.random()
        idx = int(np.searchsorted(np.cumsum(p), u, side="right"))
        out.append(min(idx, V - 1))
    return out

print("T=0  (greedy) :", generate(T=0))
print("T=0.7         :", generate(T=0.7))
print("T=0.7 top_p=.9:", generate(T=0.7, top_p=0.9))
print("seeds 1 e 2   :", generate(seed=1), generate(seed=2))

# T=0 deve ser SEMPRE igual, independentemente do seed:
assert generate(seed=1, T=0) == generate(seed=999, T=0)
```

## Comparações

| Estratégia | Ideia | Risco |
| --- | --- | --- |
| Greedy | argmax | repetição, degeneração |
| Top-k | $k$ candidatos | $k$ arbitrário; ruim se a distribuição é plana |
| Top-p | massa acumulada | mais estável; padrão da indústria |
| Min-p | limiar relativo a $p_{\max}$ | muito estável em distribuições achatadas |
| Typical | $-\log p$ próxima da entropia | evita o "previsível demais" e o "surpreendente demais" |
| Beam | $k$ sequências de maior score | máx. likelihood → degeneração; evite para chat |

## Limitações e riscos

- **Reprodutibilidade bit a bit é objetivo de infraestrutura**, não propriedade que se obtenha ligando parâmetros.
- Parâmetros de sampling têm **suporte desigual entre modelos**; modelos recentes às vezes rejeitam valores fora do padrão. Confira a referência do modelo.
- **Puxar a temperatura para 0 como default de produção** é erro: extração de dados e texto criativo quer exatamente o oposto.

## O que isso muda na minha prática

- [x] Todo experimento registra: modelo, temperatura, top-p, seed, `system_fingerprint`.
- [x] Extração/classificação com `temperature=0`; criativo com `0.8–1.2`.
- [ ] Rodar o código acima (lab 04) e confirmar que `T=0` é seed-independente.
- [ ] Verificar se a infraestrutura usa batching dinâmico (e como isso afeta reprodutibilidade).

## Fontes

1. **The Curious Case of Neural Text Degeneration** — Holtzman et al., ICLR 2020. https://arxiv.org/abs/1904.09751 — *cauda não confiável; origem do nucleus sampling*
2. **Reproducible outputs with the seed parameter** — OpenAI Cookbook. https://developers.openai.com/cookbook/examples/reproducible_outputs_with_the_seed_parameter
3. **Reproducibility (PyTorch)** — https://docs.pytorch.org/docs/stable/notes/randomness.html — *CUDA, cuDNN, `atomicAdd`, `use_deterministic_algorithms`*
4. **Floating Point and IEEE 754 Compliance for NVIDIA GPUs** — NVIDIA, CUDA 12.5. https://docs.nvidia.com/cuda/archive/12.5.0/pdf/Floating_Point_on_NVIDIA_GPU.pdf
5. **Typical Decoding for Natural Language Generation** — Meister et al., 2022. https://arxiv.org/abs/2202.00666
6. **Truncation Sampling as Language Model Desmoothing** — Hewitt, Manning & Liang, EMNLP Findings 2022. https://aclanthology.org/2022.findings-emnlp.249/

## Perguntas abertas

- [ ] Qual a temperatura padrão do meu sistema hoje, e ela está justificada por medição?
- [ ] Meus resultados de experimento são reprodutíveis ou só "parecidos"?

## Ver também

-[[Temperatura]] · [[Temperatura]] · [[Top-p Sampling]] · [[Lab 04 - Temperatura, top-p e reprodutibilidade]]

---
*Atualizado em 2026-09-30*
