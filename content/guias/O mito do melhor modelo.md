---
title: "O mito do melhor modelo"
tags:
  - "selecao-de-modelos"
  - "tradeoff"
  - "custo"
tipo: "guia"
date: "2026-10-16"
---

# O mito do melhor modelo

> **Meta:** desmontar a ideia de que existe "o melhor modelo" — e entender por que a escolha é sempre contextual e passa por trade-offs.


## Resumo em 3 frases

1. **"O melhor modelo" não existe como resposta absoluta:** para cada contexto existe a melhor escolha, e ela depende da tarefa, do volume e do orçamento.
2. Esperar que exista, **inevitavelmente**, uma IA boa e barata ao mesmo tempo é parte do mito: melhor treinamento, maior qualidade e mais desenvolvimento custam caro — o preço de um [[Modelo Frontier]] reflete esse investimento.
3. **Precisão e qualidade não estão necessariamente atreladas ao custo:** caro não garante adequação ao seu caso, e barato não condena a solução — por isso sempre sobra levantamento e decisão de trade-offs.

## O mito enunciado

O mito tem duas faces:

- **"Existe um modelo melhor que todos."** — falso como absoluto: melhor **para quê**? Um frontier é melhor em raciocínio longo; um intermediário é melhor em custo para tarefa direta; um [[Modelo Open-Weight]] é melhor quando o dado não pode sair da sua infra.
- **"Se pago mais, recebo mais."** — falso como lei: preço e adequação são eixos independentes. O modelo caro pode ser pior no *seu* caso (excesso de capacidade, formato errado, latência alta), e o barato pode resolver a tarefa inteira.

## Por que o mito persiste

| Fonte do mito | O que esconde |
| --- | --- |
| Um número só no leaderboard | a adequação é multi-métrica (ver [[Pesquisa - Custo e qualidade na seleção de modelos]]) |
| Marketing do provedor | comparação no cenário que favorece o produto |
| Anedota ("funcionou pra mim") | sem controle de tarefa, volume nem critérios |

## A consequência prática

A aula fecha com o método: **levantamento antes, decisão depois**. Sem levantamento, a escolha vira opinião; com ele, vira trade-off documentado — que é o assunto das aulas Critérios de seleção de IA e Trade-offs na escolha do modelo.

| Situação | Mito diz | A análise diz |
| --- | --- | --- |
| Resumir PDFs internos em volume | "usa o mais forte" | tarefa direta: intermediário resolve, e o volume paga a diferença |
| Parecer jurídico único, com risco | "usa o mais barato" | erro custa mais que o modelo: frontier, com revisão humana |
| Dado sensível que não sai da empresa | "só existe API" | open-weight auto-hospedado muda a conta |

## Exemplo concreto

Duas aplicações, mesmo dia, mesmo time:

- **Classificador de urgência de tickets** (100k/dia, 4 campos): um modelo intermediário com saída estruturada resolve; o frontier resolveria 2 pontos percentuais melhor a 20× o custo.
- **Análise de cláusula de risco em contrato** (50/mês): o frontier paga-se sozinho — uma cláusula perdida custa mais que um ano de diferença de preço.

> O "melhor modelo" das duas aplicações são modelos diferentes. É esse o ponto.

## Perguntas para validar

1. Por que "quanto mais caro, melhor" é um mito, e não apenas uma simplificação?
2. Cite duas tarefas em que o melhor modelo é, cada uma, um modelo diferente — e o que decide cada escolha.
3. O que transforma uma opinião de preferência ("eu gosto do X") em decisão de engenharia?

## Ver também

- [[Seleção de modelos: por onde começar]] · [[Categorias de modelos de IA]] · [[Trade-offs na escolha do modelo]] · [[Modelo Frontier]]
