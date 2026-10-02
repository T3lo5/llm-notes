---
title: "Teacher Forcing"
tags:
  - "conceito"
  - "treinamento"
tipo: "conceito"
date: "2026-10-07"
---

# Teacher Forcing

> **Definição em uma frase:** treinar alimentando sempre o token **real** da sequência como entrada do passo seguinte, em vez de um token sorteado pelo próprio modelo.

## Por que isso importa

Sem teacher forcing, cada passo de treino dependeria do token sorteado no passo anterior — uma cadeia que **não paraleliza** e não tem gradiente limpo (é RL puro).

Com teacher forcing:

- todos os passos da sequência são **conhecidos de antemão**;
- o gradiente flui por todos eles **em paralelo**;
- o treino vira uma única operação de batch, como em qualquer rede profunda.

É o que torna treinar um transformer viável em GPU.

## Função de perda

$$\mathcal{L} = -\frac{1}{T}\sum_{t=1}^{T}\log p_\theta(x_t \mid x_{1:t-1})$$

Cross-entropy média por token. E a [[Perplexidade]] é $e^{\mathcal{L}}$.

Note a simetria com a inferência:

| | Treino | Inferência |
| --- | --- | --- |
| alvo | token **real** (teacher forcing) | token **sorteado** |
| paralelismo | total | um por vez |
| entrada do passo $t$ | $x_{<t}$ real | prefixo **já gerado** |

Esse dessincronia é a razão pela qual o modelo pode gerar **um token por vez** mas ser treinado **todo de uma vez**.

## Autoavaliação
1. **P:** Qual o problema se você treinar com tokens sorteados pelo próprio modelo? **R:** os passos ficam encadeados e não paralelizáveis; além disso, erros próprios se propagam. É o caminho do RL puro, muito mais caro.
2. **P:** Por que não dá para fazer inferência exatamente como o treino? **R:** na inferência o token seguinte **não existe** ainda — é justamente o que precisa ser previsto.

## Onde vi isso

- Visto em:[[Self-Attention]]

## Ver também

- [[Perplexidade]] · [[Logits]] · [[Modelo Base]]

---
*Atualizado em 2026-09-30*
