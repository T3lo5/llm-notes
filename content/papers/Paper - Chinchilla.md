---
title: "Paper - Chinchilla"
tags:
  - "paper"
  - "escala"
tipo: "paper"
date: "2026-10-14"
---

# Paper — Training Compute-Optimal Large Language Models (Chinchilla)

> **Por que estou lendo isso:** porque todo argumento sobre "qual modelo é melhor" depende de entender que qualidade é função de **parâmetros × dados**, e não só de parâmetros.

## Ficha

| Campo | Valor |
| --- | --- |
| Título | Training Compute-Optimal Large Language Models |
| Autores | Jordan Hoffmann, Sebastian Borgeaud, Arthur Mensch, Elena Buchatskaya, Trevor Cai, Eliza Rutherford, Diego de las Casas, Will_constant Buchanan, et al. (DeepMind) |
| Ano / Venue | 2022 (arXiv) · NeurIPS 2022 |
| Link | https://arxiv.org/abs/2203.15556 |
| Tópicos | Scaling · Compute · Dados |

## Resumo em 5 linhas

1. **Problema:** a lei de escala de Kaplan et al. (2020) sugeria que, para compute fixo, era melhor treinar modelos **grandes** com dados relativamente poucos.
2. **Método:** treinar centenas de modelos (de 70M a ~16B parâmetros) e ajustar a forma da lei de escala com o método correto.
3. **Resultado:** para compute **ótimo**, o número de tokens de treino deve escalar **na mesma proporção** que o número de parâmetros. Modelos grandes estavam sendo *undertrained*.
4. **Custo:** Chinchilla (70B, 1.4T tokens) supera Gopher (280B, 300B tokens) com muito menos compute de inferência.
5. **Conclusão:** aScaling da indústria foi reorientada — a partir daí, o padrão passou a ser "dados primeiro".

## O que eu levo embora

- **Dados importam tanto quanto parâmetros.** *Undertraining* é o erro padrão.
- O que se chama de "modelo pequeno" na prática é quase sempre um modelo com **dados suficientes** para o seu tamanho.

## Detalhes que merecem atenção

### O método (importa mais que o resultado)

O erro de Kaplan não foi o resultado — foi o **método de ajuste**. Eles usaram regressão de Holden–Stevenson sobre a qual se maximiza a perda mínima, o que é sensível à forma do modelo. Hoffmann et al. corrigiram com um método que:

- **exclui os menores modelos** (que não estão na região de lei de potência);
- aplica um **termo de correção** para o ajuste;
- parametriza a alocação de compute explicitamente.

**Lição de método:** quando um resultado contradiz o consenso, o primeiro suspeito é o ajuste, não o mundo.

### Resultados

| Modelo | Params | Tokens de treino | Corpus | Observação |
| --- | --- | --- | --- | --- |
| Gopher | 280B | 300B | MassiveText | compute subótimo — overtrained em dados, subdimensionado em capacidade |
| Chinchilla | 70B | 1.4T | MassiveText | **4× menos compute de inferência**, melhor em quase tudo |

O número "4×" vem do fato de que Chinchilla tem 4× menos parâmetros — o custo de inferência escala com parâmetros, não com tokens de treino.

### Limitações declaradas

- A análise é para **compute fixo de treino**, não para inferência. A pergunta "¿qual modelo é melhor para deploy?" tem resposta diferente.
- Os modelos vão até ~16B no ajuste; a extrapolação para centenas de bilhões **não é garantida**.
- Valores numéricos (28 tokens/param, etc.) são propriedades do corpus e da tokenização usados — não universais.

### Perguntas que o paper deixa abertas

- [ ] E quando o corpus é limitado? (→ Alexandria, DataComp)
- [ ] E com o advento de dados sintéticos e de distillação? A proporção 1:1 ainda vale?

## Onde isso conecta

- Conceito: [[Modelo Base]]
- Pesquisa: [[Pesquisa - O que é um LLM]]
- Anterior: *Scaling Laws for Neural Language Models* — Kaplan et al., arXiv:2001.08361

## Rethinking

- Quando alguém me disser "o modelo X tem 70B, o Y tem 400B", a primeira pergunta deveria ser: **quantos tokens de treino cada um viu?** Sem isso, a comparação de qualidade é vazia.

## Notas de leitura

| Passada | Data | Conclusão |
| --- | --- | --- |
| 1 — 15 min | | |
| 2 — método | | |
| 3 — crítica | | |

---
*Lido em 2026-09-30*
