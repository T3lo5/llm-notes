---
title: "Valor de negocio com IA"
tags:
  - "conceito"
  - "valor"
  - "negocio"
tipo: "conceito"
date: "2026-10-08"
---

# Valor de negócio com IA

> Como transformar "IA gera valor" em uma conta que o gestor consegue conferir.

## As quatro alavancas

| Alavanca | Pergunta | Como se mede |
| --- | --- | --- |
| **Custo** | quanto trabalho some? | horas × custo da hora |
| **Receita** | o que antes não existia? | conversões, produtos novos |
| **Velocidade** | quanto tempo a menos? | time-to-market, SLA |
| **Qualidade** | o erro cai quanto? | taxa de erro, retrabalho |

Cada caso de uso é **um** desses, no máximo dois. "Melhorar tudo" é sinal de que o caso não foi definido.

## A conta

```
Valor líquido = (volume × ganho por unidade) − (custo total da solução)
```

## O custo total

| Componente | Frequentemente esquecido |
| --- | --- |
| Chamadas ao modelo | quase nunca — é o visível |
| **Engenharia de integração** | sempre |
| **Avaliação** (criar e manter testes) | quase sempre |
| **Supervisão humana** da saída | quase sempre, e é o maior |
| **Manutenção** (o prompt degrada, o modelo muda) | sempre |
| Treinamento da equipe | quase sempre |

> **Supervisão humana costuma custar mais que a chamada ao modelo.** Se ninguém a contabiliza, o ganho é fictício.

## Ganho realizado vs. teórico

> **O ganho só existe se o processo mudou.** Automatizar um passo de um fluxo que ninguém altera entrega o mesmo resultado, mais rápido, com o mesmo desperdício.

| Camada | O que é | Realizado? |
| --- | --- | --- |
| **Teórico** | o modelo consegue fazer | sim, se a tarefa existe |
| **Técnico** | o sistema faz | depende da integração |
| **De negócio** | alguém mudou o fluxo e o número mudou | **só esta conta** |

É comum confundir a primeira com a terceira.

## Quando o valor não aparece

| Sintoma | Causa provável |
| --- | --- |
| O sistema funciona, o número não muda | fluxo não foi redesenhado |
| O número muda, mas não se sustenta | erode com o tempo sem manutenção |
| Funciona para uma pessoa, não para a equipe | não foi desenhado para o processo real |
| O piloto funciona, a escala não | custo por unidade cresce ou supervisão explode |

## Origem

- [[Como a IA gera valor de negócio]]

## Ver também

- [[Antipatrones de adocao de IA]] · [[Framework de decisao estrategica]] · [[Projeto: avaliação de caso de uso de IA]]

---
*Ficha criada em 2026-10-01*
