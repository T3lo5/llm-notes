---
title: "Categorias de modelos de IA"
tags:
  - "selecao-de-modelos"
  - "frontier"
  - "open-weight"
tipo: "guia"
date: "2026-10-16"
---

# Categorias de modelos de IA

> **Meta:** conhecer as três categorias de modelos (frontier, intermediário e open-weight) e o que cada uma compra — e cobra.


## Resumo em 3 frases

1. Os modelos se dividem em três categorias por **onde rodam** e **quanto custam**: frontier (API cara, ponta de capacidade), intermediário (custo por token é o fator crítico) e open-weight (auto-hospedado, controle total).
2. Frontier é para tarefas complexas porque carrega a **máxima capacidade de raciocínio e linguagem** — e o custo alto é o preço do treinamento, da qualidade e do desenvolvimento por trás.
3. Open-weight não tem custo por chamada, mas a **infraestrutura, a manutenção e a observabilidade** viram conta de verdade — o "de graça" é só na API.

## As três categorias

| | Modelo Frontier\ | Modelo Intermediário\ | Modelo Open-Weight\ |
| --- | --- | --- | --- |
| **Onde roda** | API do provedor | API do provedor | sua infraestrutura |
| **Custo** | alto por token | baixo por token — decisivo em volume | zero por chamada; infra + manutenção + observabilidade |
| **Capacidade** | máxima em raciocínio e linguagem | cai em tarefas complexas | depende do modelo e do hardware |
| **Controle** | pouco (caixa-preta, SLA do provedor) | pouco | total (pesos, serving, dados) |
| **Quando usar** | tarefa complexa, crítica, baixo volume | tarefa direta, alto volume | dado sensível, controle total, escala constante |

### Frontier: o que o preço compra

- Máxima capacidade de raciocínio em tarefas longas e ambíguas (parecer, arquitetura, prova de conceito).
- O custo alto reflete treinamento, curadoria e desenvolvimento — não é margem arbitrária.
- Risco prático: **excesso de capacidade** — pagar frontier para classificar urgência de ticket é comprar caminhão para levar carta.

### Intermediários: o custo por token manda

- Em tarefa complexa a qualidade **cai visivelmente** — é a fronteira da categoria.
- **Fine-tuning** pode aproximá-los do nível frontier **na tarefa alvo**: o modelo não sobe de categoria geral, mas especializa onde importa (ver [[Fine-tuning]], [[LoRA]]).
- A conta de volume: em 1M de chamadas/mês, a diferença de preço por token entre intermediário e frontier decide o orçamento sozinha (ver [[Token]], [[Lab 01 - Contando tokens e medindo custo]]).

### Open-weight: controle total, conta real

- **Sem custo por chamada** — mas a infraestrutura (GPUs, serving), a manutenção (atualização de modelo, patches) e a observabilidade (monitoramento, avaliação) são custos fixos que existem mesmo com pouca demanda.
- Vantagem estratégica: dados não saem da sua infra; sem dependência do preço e das decisões de um provedor (ver vendor lock-in — tema da sequência de seleção).
- O termo correto é **open-weight** (pesos abertos): nem sempre a licença é open-source no sentido da OSI.

## Confusões comuns

- ❌ **Não é** "uma categoria melhor que as outras" — é uma troca de eixos (capacidade × custo × controle).
- ✅ **É** um espectro de decisão entre capacidade, custo e controle — escolher entre eles com critérios é o resto da disciplina.

## Perguntas para validar

1. Liste as três categorias e, para cada uma, o custo que ela carrega fora do preço por token.
2. Por que fine-tuning aproxima um intermediário do frontier só "na tarefa alvo"?
3. Em que situação um open-weight é a única opção viável, mesmo com infra cara?

## Ver também

- [[Modelo Frontier]] · [[Modelo Intermediário]] · [[Modelo Open-Weight]] · [[Trade-offs na escolha do modelo]] · [[Pesquisa - Custo e qualidade na seleção de modelos]]
