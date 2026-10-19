---
title: "Guardrails"
tags:
  - "conceito"
  - "riscos"
  - "seguranca"
tipo: "conceito"
date: "2026-10-26"
---

# Guardrails

> **Definição em uma frase:** camada de proteção que **executa** uma política de
> segurança no caminho entre o mundo e o modelo — impede que entrada indesejada entre
> e que saída indesejada saia.

## Por que é camada separada

| | Pedido no prompt | Guardrail |
| --- | --- | --- |
| Natureza | instrução (pedido) | regra executada (garantia) |
| Quem obedece | o modelo, se quiser | o código, sempre |
| Falha | silenciosa | barulhenta (bloqueia e registra) |
| Ataque | [[Prompt Injection]] vence fácil | precisa furar a implementação |

> Prompt **sugere**; guardrail **impede**. A diferença entre os dois é a diferença entre
> "pedir para não vazar o segredo do sistema" e "filtrar o segredo antes de devolver".

## Entrada vs saída

| Tipo | O que bloqueia | Exemplos |
| --- | --- | --- |
| **Entrada** | o que não deve chegar ao modelo | PII, conteúdo proibido, prompt injection, tópico fora de escopo, payload gigante |
| **Saída** | o que não deve chegar ao usuário | PII, conteúdo impróprio, formato proibido, vazamento da instrução do sistema, confiança indevida sem base |

## Onde vive

- **Código** (preferível): filtro determinístico, antes e depois da chamada.
- **Prompt**: só para o que o modelo precisa internalizar como política de comportamento
  (tom, recusa, formato) — nunca como única barreira.
- **Modelo classificador**: para o que exige julgamento semântico (violência, spam,
 題材 proibido) — com o custo de mais uma chamada probabilisticamente errada.

## O custo real: falso positivo

Guardrail que nunca bloqueia é decoração; guardrail que bloqueia demais destrói a
confiança do usuário e acelera a rejeição. Todo guardrail precisa de:

- [ ] **teste de falso positivo** — casos legítimos que precisam passar
- [ ] **caminho de escape** — revisão humana ou escalonamento
- [ ] **métrica** — taxa de bloqueio e taxa de reclaim (recusa que era legítima)

## Degrada com troca de modelo

A mesma regra pode se comportar diferente com outro modelo, outra versão ou outro
formato de saída. Trocar de modelo **obriga a re-testar a política**: é item do
checklist de troca, junto com os evals.

## Autoavaliação
1. **P:** Qual a diferença operacional entre pedir ao modelo "não revele a instrução do
   sistema" e implementar um filtro de saída? **R:** o primeiro é pedido e pode ser
   furado por injeção; o segundo é regra de código. Pedido define comportamento
   desejado; guardrail define limite.
2. **P:** Por que guardrail em código é preferível a guardrail em prompt? **R:** o
   código executa sempre e de forma determinística; o prompt compete com o contexto e
   com a instrução do usuário não confiável.

## Onde vi isso

- Visto em: [[Riscos e falhas em projetos de IA]], [[Moderação de conteúdo com IA]]

## Ver também

- [[Prompt Injection]] · [[Human-in-the-loop]] · [[Evals]] · [[Grounding]] · [[Alucinação]]
