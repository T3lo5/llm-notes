---
title: "Janela de Contexto"
tags:
  - "conceito"
  - "contexto"
tipo: "conceito"
date: "2026-10-01"
---

# Janela de Contexto

> **Definição em uma frase:** o limite, em tokens, de tudo que o modelo pode ver numa única chamada — entrada **e** saída somadas.

## Explicação curta

Não é memória do modelo. É o **orçamento de uma requisição**. Se não está na janela, o modelo não existe aquilo: não é "esquecido", é **inexistente** para aquela chamada.

## Como funciona (mecanismo)

- Entrada = system prompt + histórico + exemplos + documentos recuperados.
- Saída = o que o modelo vai gerar.
- As duas competem pelo mesmo orçamento.

Restrições derivam disso:

| Restrição | Causa |
| --- | --- |
| Custo cresce com o contexto | todo token de entrada é cobrado |
| Atenção é $O(T^2)$ | contexto longo encarece o prefill |
| Posição importa | ver [[Lost in the Middle]] |
| Memória do KV cache cresce | proporcional ao comprimento |

## Erro comum de projeto

> "Vou recuperar 30 chunks e colar todos no prompt."

Cada chunk é token de entrada cobrado. Trinta chunks quietos transformam a consulta em uma fatura. O número de chunks é uma decisão de arquitetura, não um parâmetro de default.

## Autoavaliação
1. **P:** O que ocupa a janela: só a entrada ou entrada e saída? **R:** as duas. Se o limite é 128k e o prompt tem 127k, há ~1k para a resposta.
2. **P:** Por que "dar mais contexto" pode piorar o resultado? **R:** além do custo e do $O(T^2)$, a informação relevante pode cair na posição onde o modelo atende pior (lost in the middle).

## Onde vi isso

- Visto em:, [[Sensibilidade de prompt: ordem importa]]

## Ver também

- [[Token]] · [[RAG]] · [[KV Cache]] · [[Alucinação]]
