---
title: "Perda de Contexto"
tags:
  - "conceito"
  - "falhas"
  - "contexto"
tipo: "conceito"
date: "2026-10-29"
---

# Perda de Contexto

> **Definição em uma frase:** a informação estava disponível, mas o modelo deixa de
> usá-la na resposta — por limite de janela, por posição no meio do contexto ou por
> contexto mal montado.

## Explicação curta

Não é o modelo "esquecer" como uma pessoa esquece: é a informação **sair do alcance** do
que ele consegue considerar, ou **perder força** no meio de muito texto. Aparece como
regra ignorada, decisão anterior contradita ou dado citado no início que some no final.

Na [[Alucinação e comportamentos]], perda de contexto foi tratada pelos dois
mecanismos: **limite de janela** e **atenção no meio** ([[Lost in the Middle]]).

## Os três mecanismos

| Mecanismo | O que acontece | Onde estudar |
| --- | --- | --- |
| **Limite de janela** | o contexto passa do tamanho máximo e o que é mais antigo é cortado | [[Janela de Contexto]] |
| **Atenção no meio** | a informação está dentro da janela, mas no meio de um contexto longo é menos usada que o começo e o fim | [[Lost in the Middle]] |
| **Contexto mal montado** | muito trecho irrelevante, ordem ruim, instrução diluída em histórico | [[Engenharia de prompt e contexto]] |

> Os dois primeiros são **estruturais** (não se corrigem pedindo "leia tudo com
> atenção"). O terceiro é de **engenharia** — e é onde há mais controle barato.

## Sintomas

- A regra dita no começo da conversa ("valores em centavos") deixa de valer 20 mensagens
  depois.
- O agente repete uma pergunta já respondida ou contradiz uma decisão anterior.
- A resposta ignora o documento recuperado que estava no meio do contexto.
- Quanto mais longo o histórico, pior a aderência — mesmo sem passar da janela.

## Como mitigar

| Controle | O que fazer |
| --- | --- |
| **Reancorar instruções** | repetir a regra crítica perto do ponto de uso, não só no início |
| **Posição estratégica** | o que é crítico vai no começo **e** no fim; o detalhe vai no meio |
| **Resumir/compactar** | trocar histórico longo por um resumo estruturado (decisões, regras, estado) |
| **Contexto sob demanda** | recuperar só os trechos relevantes ([[RAG]]), em vez de despejar tudo |
| **Estado explícito** | manter as decisões em um bloco fixo, não confiar na memória da conversa |
| **Teste de posição** | mover a evidência para o meio e ver se a resposta muda |

## Exemplo

Conversa de 40 mensagens: na terceira, você diz "todos os valores estão em centavos, não
divida por 100". Na trigésima, o agente entrega R$ 0,42 para uma venda de R$ 42,00 — dividiu
de novo. O dado não foi alucinado; a **regra saiu do contexto efetivo**. A correção não é
"pedir desculpa e repetir a regra": é reancorar a instrução no ponto de uso ou carregá-la
em um bloco de estado que não se perde.

## Confusões e aparências

- ❌ **Não é** [[Alucinação]]: a informação existia; o modelo só não a usou.
- ❌ **Não é** "contexto grande resolve": mais contexto pode piorar (mais ruído no meio).
- ❌ **Não é** falha só de conversa longa: acontece dentro de um único prompt com muitos
  documentos.
- ✅ **É** um problema de **arquitetura de contexto**: o que entra, em que ordem, e o que
  é reancorado.

## Autoavaliação
1. **P:** Por que aumentar a janela de contexto não elimina perda de contexto? **R:** porque
   o problema não é só capacidade: informação no meio de contextos longos é menos usada
   ([[Lost in the Middle]]), e mais texto relevante compete com mais ruído.
2. **P:** Qual o teste mais barato para saber se uma informação está sendo usada? **R:**
   mover/remover a informação e comparar a resposta — se nada muda, ela não estava
   ancorando a saída.

## Onde vi isso

- Visto em: [[Alucinação e comportamentos]]
- Aprofundamento: [[Janela de Contexto]] · [[Lost in the Middle]] · [[Engenharia de prompt e contexto]]

## Ver também

- [[Inconsistência]] · [[Ambiguidade]] · [[Alucinação]] · [[RAG]] · [[Alucinação e comportamentos]]

---
*Atualizado em 2026-10-22*
