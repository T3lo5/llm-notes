---
title: "Modelo Frontier"
tags:
  - "conceito"
  - "selecao-de-modelos"
  - "frontier"
tipo: "conceito"
date: "2026-10-16"
---

# Modelo Frontier

> **Definição em uma frase:** o modelo de ponta de uma geração — o mais capaz e o mais caro disponível de uma organização, usado em tarefas onde a capacidade de raciocínio e linguagem justifica o preço.

## Explicação curta

"Frontier" nomeia a fronteira do que existe: é o modelo que abre a geração atual em benchmarks e capacidades. Ele é vendido por API a um preço alto por token, e o preço reflete o que está atrás: treinamento em escala enorme, curadoria de dados, pós-treino com preferência humana e avaliação extensiva. O uso típico é tarefa **complexa e crítica com volume baixo**: parecer, arquitetura, prova de conceito, análise ambígua.

## Como funciona (o que o preço compra)

- Capacidade de raciocínio em cadeias longas (raciocinar sobre dezenas de passos sem desmoronar).
- Instrução e formato complexos com poucos exemplos.
- Cobertura ampla de domínios e idiomas, incluindo casos raros.
- Frequentemente multimodal (imagem/áudio) de fato, não só declarado (ver [[IA multimodal]]).

Nada disso é garantia de adequação: é **excesso de capacidade** que você paga mesmo quando a tarefa é simples.

## Exemplos

| Caso | Frontier | Alternativa |
| --- | --- | --- |
| Parecer jurídico com raciocínio longo | adequado | intermediário erraria mais barato — mas o erro custa caro |
| Classificar urgência de ticket | pagaria 20× por 2pp | intermediário com saída estruturada resolve |
| Prova de conceito de produto | acelera o ciclo | — |

## Confusões e aparências

- ❌ **Não é** "o melhor modelo" em absoluto — é o de maior capacidade geral; para a sua tarefa específica pode ser desnecessário (ver [[O mito do melhor modelo]]).
- ❌ **Não é** caro por ganância — o custo reflete treinamento, qualidade e desenvolvimento.
- ✅ **É** a escolha certa quando o **custo do erro domina** a diferença de preço.

## Autoavaliação
1. **P:** Por que o preço de um frontier reflete treinamento e desenvolvimento? **R:** Porque a capacidade vem de escala de dados, compute e pós-treino — cada ponto de capacidade tem custo marginal alto.
2. **P:** Cite um caso em que o frontier é a escolha errada. **R:** Tarefa direta e alto volume (ex.: classificação simples), onde o intermediário resolve com diferença pequena a 10× menos.

## Onde vi isso

- Visto em: [[Categorias de modelos de IA]]
- Aprofundamento: [[Pesquisa - Custo e qualidade na seleção de modelos]]

## Ver também

- [[Modelo Intermediário]] · [[Modelo Open-Weight]] · [[Trade-offs na escolha do modelo]]

---
*Atualizado em 2026-10-09*
