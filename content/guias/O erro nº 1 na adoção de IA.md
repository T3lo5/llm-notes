---
title: "O erro nº 1 na adoção de IA"
tags:
  - "fundamentos"
  - "estrategia"
  - "antipatrono"
tipo: "guia"
date: "2026-10-08"
---

# O erro nº 1 na adoção de IA

> **Meta:** nomear o erro de adoção mais comum e dar o sintoma observável de cada projeto que já caiu nele.

## Resumo em 3 frases

1. O erro nº 1 é inverter a ordem: **escolher a tecnologia primeiro** e procurar depois um problema para ela.
2. É por isso que a maioria dos pilotos de IA não vira produto — não falhou a tecnologia, falhou a seleção do problema.
3. O sintoma é um projeto que não consegue responder "qual número isso move?", só "que legal a demo fica".

## O erro, escrito de forma precisa

Não é "usar IA onde não dá". É:

> **Começar pela pergunta "o que dá para fazer com [modelo X]?" em vez de "qual problema está me custando mais, e por quê?"**

A segunda pergunta produz trabalho. A primeira produz ociosidade.

## As duas ordens

| | Começar pelo problema | Começar pela tecnologia |
| --- | --- | --- |
| Primeira pergunta | Qual custo/dor estamos medindo? | O que dá para fazer com um LLM? |
| Segunda | Onde o processo quebra hoje? | Qual caso parece demonstrável? |
| Sucesso é | um número que muda | uma demo que impressiona |
| Quando trava | ao descobrir que é difícil | ao tentar medir o ganho |
| Custo do erro | tarde, caro | cedo, barato |

## O sintoma

Um projeto está na ordem errada quando **ninguém na empresa consegue dizer qual métrica ele deveria mover** — e a resposta da equipe é "depende do modelo".

Dois sinais práticos:

- A proposta chega escrita em termos de tecnologia ("vamos implementar RAG"), não de problema.
- O sucesso é descrito como entrega ("o agente está rodando"), não como resultado ("o tempo de resposta caiu de 4h para 20min").

## Por que essa taxa de fracasso tão alta

Trabalhos públicos que circularam em 2025 apontam na mesma direção: a grande maioria dos pilotos de IA generativa em empresas reportou retorno nulo ou negativo, com motivos recorrentes — prova de valor inexistente, custo de Inference não raro, eolvidar que o gargalo raramente é o modelo.

Vale notar o método antes de citar o número: esse tipo de levantamento tem viés de seleção forte (empresas respondem por escolha). Trate como **sinal direcional, não como estatística**.

O padrão é consistente com a tese deste guia: o erro não é de modelo, é de seleção.

## O antídoto

1. Escreva a dor atual em uma frase, com número, sem mencionar IA.
2. Se você não consegue, o projeto ainda não está pronto.
3. Só então pergunte se IA resolve.

Teste rápido: **se você remover a palavra "IA" da proposta, o projeto ainda faz sentido?** Se não fizer, é tecnologia primeiro.

## Perguntas para validar

1. Dê um exemplo de um projeto que você viu que era "tecnologia primeiro".
2. Qual é o sinal mais precoce, na sua experiência, de que um projeto está na ordem errada?
3. Por que a ordem inversa — problema primeiro — continua sendo rara mesmo sabendo o problema?

## Ver também

- [[Que problemas a IA resolve]] · Antipatrones de adocao de IA · [[Projeto: avaliação de caso de uso de IA]]
