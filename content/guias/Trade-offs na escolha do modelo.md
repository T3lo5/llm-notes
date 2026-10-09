---
title: "Trade-offs na escolha do modelo"
tags:
  - "selecao-de-modelos"
  - "tradeoff"
  - "decisao"
tipo: "guia"
date: "2026-10-16"
---

# Trade-offs na escolha do modelo

> **Meta:** transformar os 5 critérios em decisão: a tabela modelo caro × modelo barato, e o princípio de que a escolha é análise — nunca achismo.


## Resumo em 3 frases

1. Toda escolha de modelo é um **trade-off entre custo e os outros critérios** (qualidade, latência, confiabilidade, risco) — não existe escolha que otimize tudo ao mesmo tempo.
2. **Aplicação crítica paga o modelo caro** porque o custo do erro domina a diferença de preço; **parte de alto volume exige modelo barato** porque o custo unitário domina o total.
3. A decisão é **100% análise**: remove-se achismo com critérios e números — não existe resposta universal, e toda escolha se justifica com fundamentos.

## Modelo caro × modelo barato

| | Modelo caro (frontier) | Modelo barato (intermediário / open-weight) |
| --- | --- | --- |
| **Qualidade** | maior em tarefa complexa e raciocínio longo | cai em tarefa complexa; resolve tarefa direta |
| **Custo** | alto por token | baixo por token — ou zero por chamada com conta de infra |
| **Quando usar** | erro é caro, volume é baixo, tarefa é complexa | volume é alto, tarefa é direta, erro é recuperável |
| **Por quê** | o custo do erro supera a diferença de preço | o custo unitário multiplicado pelo volume supera a diferença de qualidade |

## Os dois princípios que decidem

1. **Aplicação crítica → modelo caro.** Parecer jurídico, análise financeira, diagnóstico: o incidente custa mais que um ano de diferença de preço. E mesmo assim: revisão humana no fluxo.
2. **Alto volume → modelo barato.** 100k classificações por dia: 5× o preço por token é 5× o orçamento. A diferença de qualidade que sobra se resolve com [[Fine-tuning]], saída estruturada ou um ponto de revisão humana no que importa.

O meio-termo engenheiresco não é escolher um: é **não usar um só** — cascata e roteamento mandam a tarefa fácil para o barato e escalam para o caro só quando precisa (ver [[Pesquisa - Custo e qualidade na seleção de modelos]]).

## Removendo o achismo

Ponto central: a decisão é **análise, não opinião**. Na prática, a decisão vira uma linha escrita:

```
Decisão: usar <modelo> para <tarefa>.
Critérios: qualidade = <eval no meu domínio, %> · custo = R$<X>/1M tokens × <volume/mês>
           latência = <p95 medido> · risco = <o que acontece se errar>
Alternativa descartada: <outro modelo> porque <número>.
Revisão: <data> ou quando <gatilho — preço mudar, volume dobrar, modelo novo>.
```

Sem números, é achismo com verniz. Com números, é decisão auditável — e **data de revisão**, porque o mercado muda (preços caem, modelos novos aparecem).

## Exemplo completo

Tarefa: extrair dados de nota fiscal em escala (500k/mês).

| | Frontier | Intermediário | Open-weight |
| --- | --- | --- | --- |
| Qualidade no eval | 97% | 94% | 92–95% (com fine-tuning) |
| Custo/mês | ~R$ 15k | ~R$ 1,5k | infra ~R$ 3k + 0,5 FTE |
| Latência p95 | 4s | 1,5s | depende do hardware |
| Risco | dado sai da infra | dado sai da infra | dado fica na infra |

**Decisão:** intermediário com validação por schema — 94% resolve com fila de exceção humana, e 10× o custo não se justifica. Se o dado não pode sair da empresa, a conta vira open-weight.

## Perguntas para validar

1. Por que uma aplicação crítica "vale pagar" o modelo caro — e o que ainda assim continua obrigatório junto com ele?
2. Por que parte de alto volume "exige" modelo barato? Faça a conta com 100k chamadas/dia.
3. Escreva a linha de decisão para um caso do seu trabalho, com números e data de revisão.

## Ver também

- [[Critérios de seleção de IA]] · [[Pesquisa - Custo e qualidade na seleção de modelos]] · [[Modelo Frontier]] · [[Modelo Intermediário]] · [[Modelo Open-Weight]]
