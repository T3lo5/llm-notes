---
title: "Benchmark"
tags:
  - "conceito"
  - "selecao-de-modelos"
  - "benchmarks"
  - "evaluacao"
tipo: "conceito"
date: "2026-10-16"
---

# Benchmark

> **Definição em uma frase:** conjunto padronizado de testes que compara modelos sob condições controladas — e que só decide quando os dados refletem o uso real.

## Explicação curta

Um benchmark transforma "parece melhor" em número comparável: mesmo dataset para todos os modelos, métrica definida antes, execução controlada. Existem três fontes, com pesos diferentes: **leaderboard público** (triagem — mede média alheia, sofre contaminação e saturação), **benchmark do provedor** (comparação no cenário que favorece o próprio produto) e **benchmark do seu domínio** (a decisão). O que separa um benchmark bom de um ruim não é o tamanho — é a ligação com a função real que o modelo vai exercer no produto.

## Como funciona (o pipeline)

1. **Dataset real** — casos do uso de produção, anonimizados; nunca frases escritas para o teste.
2. **Execução repetida** — a decodificação é estocástica (ver [[Temperatura]]), então o mesmo caso roda mais de uma vez.
3. **Scoring** — automático no formato/fidelidade + revisão humana amostral no conteúdo.
4. **Relatório com três números juntos** — acurácia no caso real, custo por caso, latência.

Um teste estatisticamente sério exige **amostra suficiente**, **margem de erro explícita** e métrica ligada ao uso — 10 casos não separam 90% de 80%.

## Exemplos

| Benchmark ruim | Benchmark bom |
| --- | --- |
| 10 frases escritas por mim, 1 execução | 200 casos reais anonimizados, 3 execuções cada |
| "Responda qualquer coisa sobre este texto" | a função real do produto: prompt + contexto + formato + validação |
| Métrica: "pareceu bom" | métrica: formato válido, fidelidade ao caso, taxa de falha |
| Comparar modelos em datasets diferentes | mesmo dataset, mesma versão do prompt, mesma data |

## Confusões e aparências

- ❌ **Não é** leaderboard — o ranking responde "melhor em média no benchmark deles", não "melhor no meu caso".
- ❌ **Não é** garantia contra falsos positivos — dado contaminado (vazou no treino) ou caso escolhido depois da resposta infla o resultado.
- ✅ **É** um artefato de decisão: **benchmark ruim leva a escolha ruim**, porque a escolha herda os defeitos do teste — é por isso que o custo de montar um benchmark do domínio é menor que o custo da escolha errada.

## Autoavaliação
1. **P:** Qual a diferença entre leaderboard público e benchmark do domínio? **R:** O público faz triagem com média alheia; o do domínio decide, com dados reais do uso e métrica da função real.
2. **P:** Por que repetir a execução do mesmo caso? **R:** Porque a decodificação é estocástica; uma execução mede sorte, repetição mede desempenho.

## Onde vi isso

- Visto em: [[Benchmarks: como medir o desempenho]]
- Aprofundamento: [[Pesquisa - Custo e qualidade na seleção de modelos]] (Chatbot Arena e HELM sobre os riscos do benchmark estático)

## Ver também

- [[Roteamento de modelos]] · [[Vendor lock-in]] · [[Latência]] · [[Token]]

---
*Atualizado em 2026-10-09*
