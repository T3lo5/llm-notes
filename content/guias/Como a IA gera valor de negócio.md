---
title: "Como a IA gera valor de negócio"
tags:
  - "fundamentos"
  - "valor"
  - "negocio"
tipo: "guia"
date: "2026-10-08"
---

# Como a IA gera valor de negócio

> **Meta:** sair da intuição de que "IA gera valor" para uma conta que o gestor consegue conferir.

## Resumo em 3 frases

1. Valor vem de quatro alavancas — **custo, receita, velocidade, qualidade** — e cada uma exige um número, não um adjetivo.
2. O ganho só se realiza se o **fluxo de trabalho muda**: automatizar sem redesenhar entrega o mesmo erro mais rápido.
3. O custo total quase sempre é maior que o da chamada ao modelo: avaliação, integração, supervisão humana e manutenção.

## As quatro alavancas

| Alavanca | Pergunta | Como se mede |
| --- | --- | --- |
| **Custo** | quanto trabalho some? | horas × custo da hora |
| **Receita** | o que antes não existia? | conversions, novos produtos |
| **Velocidade** | quanto tempo a menos? | time-to-market, SLA |
| **Qualidade** | o erro cai quanto? | taxa de erro, retrabalho |

Cada caso de uso é **um** desses, no máximo dois. "Melhorar tudo" é sinal de que o caso não foi definido.

## A conta

```
Valor líquido = (volume × ganho por unidade) − (custo total da solução)
```

O erro clássico é esquecer o **custo total**:

| Componente | Frequentemente esquecido |
| --- | --- |
| Chamadas ao modelo | quase nunca — é o visível |
| **Engenharia de integração** | sempre |
| **Avaliação** (criar e manter o conjunto de testes) | quase sempre |
| **Supervisão humana** da saída | quase sempre, e é o maior |
| **Manutenção** (o prompt degrada, o modelo muda) | sempre |
| Treinamento da equipe | quase sempre |

> O ponto que decide projetos: **supervisão humana costuma custar mais que a chamada ao modelo.** Se ninguém a contabiliza, o ganho é fictício.

## Ganho realizado vs. ganho teórico

Este é o tema central.

> **O ganho só existe se o processo mudou.** Automatizar um passo de um processo que ninguém mais altera entrega o mesmo resultado, mais rápido, com o mesmo desperdício.

Três camadas de ganho, e é comum confundir a primeira com a terceira:

| Camada | O que é | Realizado? |
| --- | --- | --- |
| **Teórico** | o modelo consegue fazer | sim, se a tarefa existe |
| **Técnico** | o sistema faz | depende da integração |
| **De negócio** | alguém mudou o fluxo e o número mudou | **só esta conta** |

## Quando o valor não aparece

| Sintoma | Causa provável |
| --- | --- |
| O sistema funciona, o número não muda | fluxo não foi redesenhado |
| O número muda, mas não se sustenta | erode com o tempo (drift) sem manutenção |
| Funciona para uma pessoa, não para a equipe | não foi desenhado para o processo real |
| O piloto funciona, a escala não | custo por unidade cresce ou supervisão explode |

Ver Antipatrones de adocao de IA — o terceiro sintoma é o "automação sem redesenho".

## Perguntas para validar

1. Em um caso de uso de atendimento, qual alavanca domina: custo, receita, velocidade ou qualidade?
2. Por que supervisão humana costuma custar mais que a chamada ao modelo?
3. Dê um exemplo de ganho técnico que não virou ganho de negócio.

## Ver também

- [[Framework de decisão estratégica]] · Antipatrones de adocao de IA · [[Projeto: avaliação de caso de uso de IA]]
