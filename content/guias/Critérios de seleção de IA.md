---
title: "Critérios de seleção de IA"
tags:
  - "selecao-de-modelos"
  - "criterios"
  - "latencia"
  - "risco"
tipo: "guia"
date: "2026-10-16"
---

# Critérios de seleção de IA

> **Meta:** fixar os 5 critérios fundamentais de seleção — qualidade, custo, latência, confiabilidade e risco — e como cada um se mede.


## Resumo em 3 frases

1. Cinco critérios decidem a seleção: **qualidade, custo, latência, confiabilidade e risco**.
2. Nenhum deles se mede em abstrato: cada um só significa algo **contra a tarefa e o contexto** da aplicação.
3. Os cinco competem entre si — melhora de um quase sempre cobra dos outros — e gerenciar essa cobrança é o trabalho de decidir.

## Os 5 critérios

| Critério | O que pergunta | Como medir | Armadilha |
| --- | --- | --- | --- |
| **Qualidade** | o modelo acerta a *minha* tarefa? | evals com casos seus, no seu domínio | seguir leaderboard alheio (ver [[Pesquisa - Custo e qualidade na seleção de modelos]]) |
| **Custo** | quanto custa por 1M de tokens e por mês no meu volume? | preço in/out × volume real de chamadas | olhar só o preço por token e esquecer o volume e as respostas longas (ver [[Token]]) |
| **Latência** | a resposta chega a tempo? | TTFT e p50/p99 medidos, não prometidos (ver [[Latência]]) | confundir velocidade do streaming com latência total |
| **Confiabilidade** | a resposta vem consistente, hoje e semana que vem? | taxa de falha de schema, variação entre execuções, SLA e versionamento do provedor | assumir que o modelo de ontem é o de hoje (ver [[Temperatura e previsibilidade]]) |
| **Risco** | o que acontece quando erra? | custo do erro por incidente: dado vazado, resposta errada publicada, decisão errada | tratar risco como "o modelo erra às vezes" sem calcular o impacto (ver [[Alucinação]]) |

## Como os critérios competem

- **Qualidade × custo:** a fronteira que a disciplina inteira negocia.
- **Qualidade × latência:** modelos maiores demoram mais — raciocínio longo é lento por construção (ver [[KV Cache]], [[Prefill]]).
- **Custo × risco:** baratear trocando de provedor pode tirar SLA, auditoria ou residência de dados.
- **Confiabilidade × custo:** redundância e fallback custam o dobro de chamadas na prática.

> Ponto central: **qualidade e custo não andam de mãos dadas**: um modelo pode ser mais caro e igualmente (ou mais) adequado ao seu caso. É o mito do "melhor modelo" virando critério.

## Exemplo: os 5 critérios numa escolha real

| Critério | Classificador de ticket (alto volume) | Parecer jurídico (crítico) |
| --- | --- | --- |
| Qualidade | suficiente com 85% de acerto + revisão | exige precisão alta e citação |
| Custo | **decide** — 100k chamadas/dia | irrelevante frente ao risco |
| Latência | < 2s no chat do suporte | horas são aceitáveis |
| Confiabilidade | schema JSON sempre válido | consistência de raciocínio |
| Risco | baixo (fila interna) | alto (decisão e responsabilidade) |

Mesmos 5 critérios, pesos opostos — e escolhas diferentes. É o próximo assunto.

## Perguntas para validar

1. Liste os 5 critérios e, para cada um, diga como você mediria numa aplicação real.
2. Por que um leaderboard não responde ao critério "qualidade"?
3. Dê um exemplo de trade-off entre latência e qualidade — e um entre custo e risco.

## Ver também

- [[Trade-offs na escolha do modelo]] · [[Latência]] · [[Alucinação]] · [[Pesquisa - Custo e qualidade na seleção de modelos]]
