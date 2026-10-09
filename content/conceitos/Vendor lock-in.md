---
title: "Vendor lock-in"
tags:
  - "conceito"
  - "selecao-de-modelos"
  - "vendor-lock-in"
  - "arquitetura"
tipo: "conceito"
date: "2026-10-16"
---

# Vendor lock-in

> **Definição em uma frase:** dependência de um fornecedor cujo custo de troca ficou proibitivo — em IA, nasce das escolhas arquiteturais do início do projeto, não do preço da API.

## Explicação curta

O lock-in não é o fato de usar um fornecedor (todo projeto usa alguém); é a situação em que **trocar de fornecedor viraria um projeto de reescrita**. Em LLMs ele se acumula em camadas: a API e o SDK do provedor, prompts calibrados no comportamento de um modelo, embeddings gerados por um modelo (que não servem para busca de outro), fine-tuning preso nos pesos do provedor, histórico no formato dele. Cada camada soma trabalho de troca — e o produto, construído em volta das respostas de um único modelo, soma o maior custo de todos.

## Como funciona (as alavancas)

- **Interface única (Adapter/Port):** o produto fala com uma interface estável; quem conhece os provedores é a camada de acesso. Padrão de projeto que compra a maior parte da liberdade.
- **Anti-corruption layer:** traduz a semântica do provedor para o modelo de domínio do produto, sem vazar jargão proprietário para dentro.
- **Formatos portáveis:** prompts escritos para a tarefa (não para os modismos de um modelo), vetores e histórico exportáveis.
- **Evals de troca:** a suite de testes que o substituto precisa passar — é o que transforma "é possível trocar" em "é comprovado que troca".
- **Multi-provider:** gateway com mais de um provedor vivo (mesmo com pouco tráfego no secundário, para manter o caminho exercitado).

A decisão é **arquitetural e do início**: o custo de troca cresce com o uso, então a janela de barateza fecha rápido.

## Exemplos

| Situação | Lock-in instalado | Mitigação possível |
| --- | --- | --- |
| Base de conhecimento só no índice do provedor | alto — dados no formato dele | exportar chunks e vetores; índice reconstruível |
| Prompts escritos com os "truques" de um modelo | médio — reescrita do zero na troca | prompts genéricos por tarefa, comparáveis entre modelos |
| Fine-tuning ajustando pesos no provedor | total — pesos não migram | LoRA local, ou assumir o custo com os olhos abertos |

## Confusões e aparências

- ❌ **Não é** usar só um provedor — usar um com interface própria e evals de troca não é lock-in; é foco.
- ❌ **Não é** resolvido pela abstração sozinha — a camada de acesso esconde o acoplamento, **não** a diferença de comportamento entre modelos; sem evals de troca, a "portabilidade" é suposição.
- ✅ **É** uma decisão arquitetural: padrões de projeto (Adapter, Anti-corruption layer) e arquitetura de software decidem o assunto antes do contrato de compra.

## Autoavaliação
1. **P:** Por que lock-in é decisão de início de projeto? **R:** Porque o custo de troca cresce com o acúmulo de dados, prompts e produto em volta do fornecedor — mitigar depois custa mais do que projetar antes.
2. **P:** Cite três formas de lock-in em IA e a alavanca correspondente. **R:** API proprietária → interface única; prompts calibrados → prompts genéricos por tarefa; embeddings/fine-tuning presos → dados exportáveis + evals de troca.

## Onde vi isso

- Visto em: [[Vendor lock-in: como evitar?]]
- Aprofundamento: [[Pesquisa - Custo e qualidade na seleção de modelos]]

## Ver também

- [[Roteamento de modelos]] · [[Benchmark]] · [[Modelo Open-Weight]] · [[Escolha final e conclusão]]

---
*Atualizado em 2026-10-09*
