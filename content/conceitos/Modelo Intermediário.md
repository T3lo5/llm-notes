---
title: "Modelo Intermediário"
tags:
  - "conceito"
  - "selecao-de-modelos"
  - "intermediario"
  - "fine-tuning"
tipo: "conceito"
date: "2026-10-16"
---

# Modelo Intermediário

> **Definição em uma frase:** modelo de meio de linha: custo por token muito menor que o Modelo Frontier, com qualidade que cai em tarefas complexas — e que pode ser especializada com fine-tuning para chegar perto do nível frontier na tarefa alvo.

## Explicação curta

O intermediário é a categoria de maior uso real: resolve a maior parte das tarefas de produto (classificação, extração, resumo direto, resposta a FAQ) a uma fração do custo. Onde ele perde é na fronteira: raciocínio longo, tarefas ambíguas, instruções complexas com poucos exemplos. E é aí que entra o detalhe decisivo da categoria: **fine-tuning pode aproximá-lo do frontier na tarefa que você escolher** — porque o que falta não é capacidade geral, é especialização.

## Como funciona (a economia do custo por token)

Em volume, o custo por token é o multiplicador do orçamento:

```
custo/mês = tokens_in × preço_in + tokens_out × preço_out   (por 1M de tokens)
```

Ver [[Token]] e [[Lab 01 - Contando tokens e medindo custo]] para a conta completa. O fine-tuning que fecha a lacuna de qualidade usa técnicas baratas de adaptação — [[LoRA]] congela os pesos e treina só matrizes de baixo posto (ver [[Fine-tuning]]).

## Exemplos

| Caso | intermediário puro | intermediário + fine-tuning |
| --- | --- | --- |
| Classificar urgência de ticket | resolve | sobra qualidade |
| Extrair campos de contrato padrão | aceitável | perto do frontier no formato alvo |
| Parecer que exige raciocínio longo | cai | não resolve: tarefa geral, não especialização |

## Confusões e aparências

- ❌ **Não é** "modelo ruim" — é adequação: para tarefa direta ele é a escolha economicamente racional.
- ❌ **Não é** upgrade de categoria via fine-tuning — o modelo **na tarefa alvo** aproxima-se do frontier; a capacidade geral não muda.
- ✅ **É** a resposta para alto volume: custo unitário baixo multiplicado por escala.

## Autoavaliação
1. **P:** Por que o fine-tuning aproxima o intermediário do frontier só "na tarefa alvo"? **R:** Porque o ajuste especializa os pesos nos padrões da tarefa; a capacidade geral de raciocínio permanece a do modelo base.
2. **P:** Quando o intermediário é a escolha errada mesmo barato? **R:** Quando o custo do erro supera a economia — tarefa crítica com raciocínio longo.

## Onde vi isso

- Visto em: [[Categorias de modelos de IA]]
- Aprofundamento: [[Pesquisa - Custo e qualidade na seleção de modelos]]

## Ver também

- [[Modelo Frontier]] · [[Modelo Open-Weight]] · [[Fine-tuning]] · [[LoRA]]

---
*Atualizado em 2026-10-09*
