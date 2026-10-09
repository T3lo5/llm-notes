---
title: "Micro Capstone: IA para SaaS"
tags:
  - "selecao-de-modelos"
  - "benchmark"
tipo: "guia"
date: "2026-10-25"
---

# Micro Capstone: IA para SaaS

> **Meta:** executar o **MC3** — um benchmark aplicado de ≥3 modelos que resulta numa recomendação de modelo para um produto SaaS, com evidência técnica e viabilidade econômica.


## Resumo em 3 frases

1. O MC3 pede um **benchmark aplicado**: escolher uma tarefa empresarial representativa, comparar **no mínimo 3 modelos** em condições equivalentes e **recomendar qual adotar** — qualidade, custo e velocidade na mesma balança.
2. A orientação da plataforma **recomenda usar um problema real seu** (profissional ou pessoal), adaptando escopo, critérios e alternativas — mas mantendo os princípios de análise, comparação e decisão; **não é preciso implementar em produção** (análise, experimentação, prototipação e recomendação valem).
3. As **6 métricas mínimas** e os **5 critérios de aceitação** definem o que torna a decisão aceitável: comparação justa, métricas claras e decisão baseada em evidência.

## Contexto empresarial (cenário proposto)

Uma startup **B2B SaaS** quer adicionar IA a um módulo de **análise textual** dentro do produto. A equipe está em dúvida entre:

| Alternativa | Rótulo |
| --- | --- |
| Modelo premium (mais caro) | [[Modelo Frontier]] |
| Modelo intermediário | [[Modelo Intermediário]] |
| Modelo open-source (mais barato) | [[Modelo Open-Weight]] |

A escolha errada compromete **margem, UX e escalabilidade** — exatamente os três eixos das Critérios de seleção de IA e dos Trade-offs na escolha do modelo.

## O que será entregue

| # | Entregável | Puxa de onde |
| --- | --- | --- |
| 1 | **Descrição da tarefa de negócio** |[[Seleção de modelos: por onde começar]]: tarefa, volume, tolerância a erro |
| 2 | **Plano de benchmark** |[[Benchmarks: como medir o desempenho]]: dados, repetição, métricas |
| 3 | **Tabela comparativa de métricas** |[[Critérios de seleção de IA]] medidos em números |
| 4 | **Relatório final com decisão recomendada** |[[Trade-offs na escolha do modelo]] com evidência |
| 5 | **Resumo executivo para liderança** | Trade-off traduzido para negócio: custo × qualidade × risco |

## Escopo (5 passos)

1. **Escolher uma tarefa empresarial representativa** — análise textual no módulo do produto (resumo, classificação, extração, resposta a perguntas sobre documentos...). Se for problema real seu, adapte a tarefa e documente a troca.
2. **Selecionar no mínimo 3 modelos** — um frontier, um intermediário, um open-weights: as três categorias da [[Categorias de modelos de IA]].
3. **Definir critérios de benchmark** — as métricas abaixo, com o peso de cada uma na decisão escrito **antes** de rodar.
4. **Testar em condições equivalentes** — mesmo dataset, mesma versão de prompt, mesma data: comparação justa é critério de aceitação.
5. **Gerar recomendação orientada a negócio** — qual modelo adotar, por quê, com que risco e sob quais gatilhos de revisão (ver [[Vendor lock-in]]).

## Métricas mínimas

| Métrica | Como medir | Liga com |
| --- | --- | --- |
| **Custo estimado por requisição** | preço in/out × tokens médios reais da tarefa × volume | [[Token]],[[Trade-offs na escolha do modelo]] |
| **Latência média** | tempo de resposta em p50/p95, repetido | [[Latência]] |
| **Qualidade da saída** | eval no domínio: acurácia/fidelidade no caso real | [[Benchmark]] |
| **Consistência** | repetição do mesmo caso: variação da resposta |[[Temperatura e previsibilidade]] |
| **Adequação ao tom/formato** | schema válido + aderência ao tom do produto | saída estruturada |
| **Risco percebido de erro** | gravidade × frequência de falha nas ações críticas | gate de risco da[[Estratégia híbrida de modelos]] |

## Critérios de aceitação

- [ ] A tarefa escolhida representa um **caso de uso empresarial plausível**
- [ ] Os modelos são comparados de forma **justa e documentada**
- [ ] As métricas estão **claramente definidas**
- [ ] A decisão final está **baseada em evidência**
- [ ] O relatório mostra **equilíbrio entre técnica e viabilidade econômica**

## Orientação de aplicabilidade

A plataforma **recomenda** — quando existir necessidade real (profissional ou pessoal) — usar o MC3 sobre **esse problema real**, em vez do cenário proposto:

- **Adapte** escopo, critérios de avaliação e alternativas tecnológicas à sua realidade
- **Mantenha** os princípios: análise → comparação → tomada de decisão
- **Não é preciso implementar em produção** — análise, experimentação, prototipação e recomendação bastam, conforme acesso a dados, sistemas e recursos
- O objetivo é duplo: entregar o capstone **e** desenvolver a capacidade de identificar problemas reais e propor soluções tecnicamente viáveis e relevantes

## Plano de execução até 25/10

| Dia | Passo |
| --- | --- |
| D+0 | Fixar tarefa (real ou cenário) e os 3 candidatos; escrever entregável 1 |
| D+1 | Dataset real/anonimizado + prompts versionados; escrever plano de benchmark (entregável 2) |
| D+2–3 | Rodar os 3 modelos em condições equivalentes, com repetição; preencher tabela (entregável 3) |
| D+4 | Calcular conta no volume + latência + risco; definir linha de decisão |
| D+5 | Relatório final (entregável 4) + resumo executivo (entregável 5); revisar contra os 5 critérios de aceitação; **entregar** |

> Dica da disciplina: a decisão não precisa ser "modelo único" — se o gate de criticidade indicar, a recomendação pode ser a **estratégia híbrida** (ver [[Roteamento de modelos]]), o que inclusive satisfaz melhor o critério de "equilíbrio entre técnica e viabilidade econômica".

## Perguntas para validar

1. Quais são as **entregáveis** do MC3 e o que cada uma responde para a liderança?
2. Quais as **6 métricas mínimas** — e por que custo por requisição é calculado com preço in/out × tokens reais, e não só com o preço por token?
3. O que os **critérios de aceitação** exigem de uma comparação "justa e documentada" — e o que a plataforma permite adaptar quando o problema é real?

## Ver também

- [[Seleção de modelos: por onde começar]] · [[Benchmarks: como medir o desempenho]] · [[Estratégia híbrida de modelos]] · [[Escolha final e conclusão]]
- [[Benchmark]] · [[Roteamento de modelos]] · [[Vendor lock-in]] · [[Pesquisa - Custo e qualidade na seleção de modelos]]
