---
title: "Seleção de modelos: por onde começar"
tags:
  - "selecao-de-modelos"
  - "custo"
  - "performance"
tipo: "guia"
date: "2026-10-16"
---

# Seleção de modelos: por onde começar

> **Meta:** enxergar a seleção de modelo como decisão de engenharia guiada por requisitos (performance × custo) — não como compra do "melhor modelo".


## Resumo em 3 frases

1. A disciplina inteira cabe numa pergunta: **dado o meu caso, qual modelo entrega a performance que eu preciso pelo custo que eu posso pagar?**
2. **Performance, custo e escolha de modelos** são os três eixos: performance sozinha leva ao modelo mais caro, custo sozinho leva ao mais barato, e a escolha é o ponto de equilíbrio entre os dois.
3. Por onde começar: **não pelo catálogo de modelos**, e sim pelo levantamento do que a aplicação exige — os 5 critérios formais vêm a seguir.

## O que esta disciplina cobre

| Aula | Tema | O que fecha |
| --- | --- | --- |
| 21 | Seleção de modelos: por onde começar | o enquadramento (esta nota) |
| 22 | [[O mito do melhor modelo]] | por que "melhor" é relativo |
| 23 | [[Categorias de modelos de IA]] | frontier, intermediário, open-weight |
| 24 | [[Critérios de seleção de IA]] | os 5 critérios: qualidade, custo, latência, confiabilidade, risco |
| 25 | [[Trade-offs na escolha do modelo]] | a tabela caro × barato e a decisão sem achismo |

Depois vêm vendor lock-in, benchmarks, estratégia híbrida, escolha final e o **MC3 — IA para SaaS (25/10)**.

## O ponto de partida: o levantamento

Antes de comparar modelos, levanta-se o que a aplicação exige:

| Pergunta | Exemplo | Por que pesa |
| --- | --- | --- |
| Qual é a tarefa? | resumir contrato · classificar ticket · gerar parecer | tarefa simples não precisa de frontier |
| Qual o volume? | 10 chamadas/dia · 1M/mês | em volume, o custo por token decide tudo |
| Qual o orçamento? | R$ por chamada · R$ por mês | é o teto, não o objetivo |
| Qual o prazo de resposta? | chat < 2s · relatório offline | puxa para modelos menores |
| Qual a tolerância a erro? | rascunho interno · decisão jurídica | puxa para modelos maiores |

> **Regra prática:** a escolha começa na linha "tolerância a erro" e "volume". São as duas que derrubam a maioria das respostas prontas ("usa o X, é o melhor").

## Perguntas para validar

1. Por que começar pela tarefa e não pelo modelo?
2. Em um produto de alto volume, qual linha do levantamento domina a decisão — e por quê?
3. Se a tolerância a erro é alta, o que isso faz com o orçamento previsto?

## Ver também

- [[O mito do melhor modelo]] · [[Critérios de seleção de IA]] · [[Modelo Frontier]] · [[Pesquisa - Custo e qualidade na seleção de modelos]]
