---
title: "Perplexidade"
tags:
  - "conceito"
  - "metricas"
tipo: "conceito"
date: "2026-10-01"
---

# Perplexidade

> **Definição em uma frase:** o médio geométrico da probabilidade que o modelo atribui a cada token real de um texto — $\exp(\text{NLL})$.

## Fórmula

$$\mathcal{L} = -\frac{1}{T}\sum_{t=1}^{T}\log p_\theta(x_t \mid x_{1:t-1})$$

$$\text{PPL} = e^{\mathcal{L}}$$

Leitura: "das $V$ possibilidades do vocabulário, o modelo está efetivamente estreitando para cerca de PPL delas". PPL de 20 é melhor que PPL de 50 **no mesmo corpus e para o mesmo tokenizer**.

## Comparações e limites

- Só é comparável **entre modelos com o mesmo tokenizador**. PPL de um tokenizer de 200k não é comparável a um de 32k.
- É medida de **ajuste ao corpus**, não de qualidade, raciocínio ou utilidade.
- Holtzman et al. (ICLR 2020) argumentam que o problema da **cauda não confiável** nasce justamente do maximum likelihood: as distribuições ficam muito suavizadas, e maximizá-las (greedy, beam) gera degeneração.

## Quando usar

| ✅ Usar | ❌ Não usar |
| --- | --- |
| comparar checkpoints no mesmo treino | comparar modelos de tokenizers diferentes |
| acompanhar uma curva de treino | medir "qual modelo é melhor" |
| avaliar ajuste a um domínio | como critério de decodificação em texto aberto |

## Autoavaliação
1. **P:** Por que PPL de um modelo de 3B pode ser pior que um de 70B no mesmo corpus? **R:** quase sempre é **tokenizer diferente** (menor vocabulário = token mais informativo). A comparação é inválida.
2. **P:** O que uma PPL muito baixa indica? **R:** overfitting ao corpus de avaliação.

## Onde vi isso

- Visto em: [[Como o modelo gera respostas, token a token]]

## Ver também

- [[Logits]] · [[Teacher Forcing]] · [[Temperatura]]

---
*Atualizado em 2026-09-30*
