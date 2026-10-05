---
title: "Por que a resposta do modelo muda"
tags:
  - "decodificacao"
tipo: "guia"
date: "2026-10-01"
---

# Por que a resposta do modelo muda

> **Meta:** explicar por que a mesma pergunta gera respostas diferentes, e distinguir a fonte **estatística** (sorteio) da fonte **numérica** (ponto flutuante em GPU).

## Resumo em 3 frases

1. A estocasticidade está na **decodificação**, não nos pesos: o modelo devolve logits, e escolher um token da distribuição é um sorteio.
2. `temperature` reescala os logits **antes** do softmax; `top-k` e `top-p` truncam a cauda. `temperature=0` (argmax) elimina o sorteio — mas não elimina a variância numérica.
3. Somar ponto flutuante **não é associativo**, e o particionamento das reduções numa GPU depende do batch. Mandar a mesma requisição com `temperature=0` em lotes diferentes já pode devolver saídas diferentes.

## Onde a variação nasce

Cadeia canônica entre o modelo e o texto:

$$
z \;\longrightarrow\; \text{temperatura} \;\longrightarrow\; \text{truncamento} \;\longrightarrow\; \text{penalidades} \;\longrightarrow\; \text{softmax} \;\longrightarrow\; \text{amostragem}
$$

O modelo em si, dado o contexto, é uma função determinística: produz o mesmo vetor de logits. **Toda a variação nasce depois.**

## Temperatura

$$p_i = \frac{e^{z_i/T}}{\sum_j e^{z_j/T}}$$

- $T \to 0$ → converge para o **argmax** (greedy decoding): sempre o token mais provável.
- $T < 1$ → **afina** a distribuição; improváveis perdem massa.
- $T = 1$ → distribuição como saiu do modelo.
- $T > 1$ → **achata**; combined com amostragem pura, vira ruído.

Detalhe que passa despercebido: **temperatura não muda o ranking**, muda a geometria da distribuição. Por isso provedores recomendam mexer em `temperature` **ou** `top_p`, nunca nos dois.

> Uso prático: `T ≈ 0` para extração, código, classificação e qualquer coisa que exija reprodutibilidade. `T ≈ 0.7–1.0` para texto criativo. Para tarefas de raciocínio com cadeia de passos, temperatura baixa e estável.

## Truncamento: top-k, top-p, min-p

| Método | Regra | Tamanho do conjunto |
| --- | --- | --- |
| **Top-k** | mantém os $k$ mais prováveis | fixo ($k$ candidatos) |
| **Top-p** (nucleus) | mantém o menor conjunto com massa acumulada $\ge p$ | **variável** |
| **min-p** | mantém tokens com $p_v \ge \tau \cdot p_{\max}$ | variável, relativo à confiança |

Top-k com $k$ fixo é ruim quando a distribuição é plana (o modelo não sabe nada e mantém 50 candidatos) e bom quando é concentrada. Top-p se adapta: mantém poucos candidatos quando o modelo está confiante, muitos quando está em dúvida. É por isso que top-p virou o padrão.

**Holtzman et al. (ICLR 2020)** formalizam o problema: a distribuição do modelo tem uma **cauda não confiável** — maximizá-la (greedy, beam) produz texto degenerado e repetitivo. Daí a regra prática: **amostre, mas trunque.**

## Penalidades de repetição

Aplicadas aos logits antes do softmax:

- `frequency_penalty` — proporcional à **frequência acumulada** de um token no texto já gerado.
- `presence_penalty` — proporcional à **presença** (binário: apareceu ou não).

Ambas costumam ficar em $[-2, 2]$. Repetição excessiva é quase sempre sintoma de distribuição muito concentrada (modelo super-confiante) — às vezes temperatura baixa demais resolve melhor do que penalidade alta.

## Seed

`seed` inicializa o gerador pseudoaleatório, tornando a **sequência de sorteios** reproduzível. Mas a documentação dos provedores é explícita: a API é **não determinística por padrão**, e com seed fixo as saídas são "majoritariamente" iguais — **sem garantia**. O campo `system_fingerprint` muda quando o backend muda, sinalizando que as saídas podem divergir.

## A segunda fonte: ponto flutuante

Aqui está o ponto que quase todo mundo ignora.

Em precisão finita, a adição **não é associativa**:

$$(a + b) + c \;\neq\; a + (b + c)$$

Num modelo transformer há dezenas de reduções e somas por token. Em GPU:

- o particionamento da redução depende do **tamanho do batch** e do número de threads;
- operações atômicas (`atomicAdd`) acumulam em **ordem arbitrária**;
- alguns kernels são não determinísticos entre execuções.

Consequência prática: **enviar a mesma requisição como parte de um batch maior muda os logits o suficiente para inverter o `argmax`** em posições onde o topo está muito próximo. `temperature=0` remove a fonte estatística, **não** a numérica.

> Isso vale inclusive para a API: `system_fingerprint` igual + saídas diferentes ⇒ causa numérica. `system_fingerprint` diferente ⇒ o provedor mudou o backend.

## Erro comum

> "Vou setar `temperature=0` e `seed=42`, então a resposta é idêntica toda vez."

Determinismo de decodificação é um objetivo de **infraestrutura**, não uma propriedade que se obtém ligando dois parâmetros. Se você precisa de reprodutibilidade bit a bit: fixe seed, `temperature=0`, desative o batching dinâmico onde possível, e registre `system_fingerprint` junto de cada resultado do experimento. Mesmo assim, registre como "reprodutibilidade best effort".

## Referências

- Holtzman et al., *The Curious Case of Neural Text Degeneration* — https://arxiv.org/abs/1904.09751
- OpenAI Cookbook, *Reproducible outputs with the seed parameter* — https://developers.openai.com/cookbook/examples/reproducible_outputs_with_the_seed_parameter
- PyTorch, *Reproducibility* — https://docs.pytorch.org/docs/stable/notes/randomness.html
- NVIDIA, *Floating Point and IEEE 754 Compliance for NVIDIA GPUs* — https://docs.nvidia.com/cuda/archive/12.5.0/pdf/Floating_Point_on_NVIDIA_GPU.pdf

## Ver também

- [[Pesquisa - Amostragem e reprodutibilidade]] · [[Lab 04 - Temperatura, top-p e reprodutibilidade]] · [[Como o modelo gera respostas, token a token]]
