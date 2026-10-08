---
title: "Antipadrões de adoção de IA"
tags:
  - "fundamentos"
  - "antipatrono"
  - "estrategia"
tipo: "guia"
date: "2026-10-05"
---

# Antipadrões de adoção de IA

> **Meta:** dar um catálogo nomeado e reconhecível, com o sintoma e o antídoto de cada um.

## Resumo em 3 frases

1. Os antipadrões são, em geral, **falhas de gestão**, não falhas de modelo.
2. Os três mais caros: piloto que nunca escala, projeto que mede modelo em vez de resultado, e ganho não realizado porque o fluxo não mudou.
3. Quase todos têm um sintoma observável em uma frase — o que os torna detectáveis **antes** do prejuízo.

## O catálogo

| # | Antipadrão | Sintoma em uma frase | Antídoto |
| --- | --- | --- | --- |
| 1 | **Piloto eterno** | "vamos escalar depois" há 8 meses | critério de abandono escrito [[Framework de decisão estratégica]] |
| 2 | **Tecnologia primeiro** | a proposta cita o modelo, não o problema | inverter a ordem [[O erro nº 1 na adoção de IA]] |
| 3 | **IA como desculpa** | o processo quebrado continua quebrado | consertar o processo primeiro |
| 4 | **Sem dono de negócio** | só a TI fala em ROI | nomear um dono com alçada |
| 5 | **Mede o modelo, não o resultado** | o relatório fala de acurácia e não de dinheiro | métrica de negócio junto |
| 6 | **Demo syndrome** | a demo de 4 minutos é o critério de sucesso | definir critério antes |
| 7 | **Ignorar o humano** | o time contorna a ferramenta | redesenhar o fluxo com quem usa |
| 8 | **Vendor lock-in sem saída** | o prompt é spaghetti e ninguém consegue migrar | camada de abstração própria |
| 9 | **Escalar antes de medir** | 500 usuários e nenhuma métrica | medir em piloto |
| 10 | **Custo invisível** | o ROI ignora supervisão e manutenção | custo total no modelo |

## Os três que mais custam

### 1. Piloto eterno

O projeto nunca falha, porque nunca é julgado. Sem critério de abandono, ele vira um item permanente de backlog que consome gente e não entrega.

**Custo típico:** anos de uma pessoa-chave sem resultado.

### 2. Medir o modelo em vez do resultado

A equipe se orgulha de "92% de acurácia" e o gestor não sabe se isso vale R$ 10 ou R$ 10 milhões.

Duas métricas sempre juntas: **qualidade do modelo** + **impacto em negócio**. A primeira sem a segunda não responde a pergunta que interessa.

### 3. Ganho não realizado

O sistema funciona, o número não muda. Causa quase sempre: o fluxo de trabalho não foi redesenhado. Ver [[Como a IA gera valor de negócio]].

## Por que são falhas de gestão

Repare que nenhum dos dez depende do modelo. Todos dependem de decisões sobre **quem decide, o que é medido e quando se para**.

É por isso que este bloco é estratégico: modelar melhor o problema de gestão não resolve um problema de gestão.

## Usar como checklist de diagnóstico

Antes de aprovar um projeto de IA, procure o sintoma na coluna 2. Um achado é uma pergunta. Dois ou mais, é um antipadrão — e vale parar para corrigir antes de escalar.

## Perguntas para validar

1. Qual antipadrão produz o pior custo quando ninguém percebe a tempo?
2. Por que o piloto eterno é o mais difícil de detectar de dentro?
3. Escreva o sintoma em uma frase do seu último projeto.

## Ver também

- [[Antipatrones de adocao de IA]] · [[O erro nº 1 na adoção de IA]] · [[Como a IA gera valor de negócio]]
