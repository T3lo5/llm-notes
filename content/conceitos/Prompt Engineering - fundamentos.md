---
title: "Prompt Engineering - fundamentos"
tags:
  - "conceito"
  - "prompt"
tipo: "conceito"
date: "2026-10-15"
---


# Prompt Engineering — fundamentos

> **Meta:** montar um prompt completo (papel, tarefa, contexto, formato) de cabeça e
> apontar qual das 4 partes está faltando quando a resposta vem genérica.

## O que é

A disciplina de **comunicar intenção a um modelo de linguagem de forma que a resposta
saia utilizável na primeira vez** — escolhendo o que dizer, em que ordem e com quanta
estrutura. Não é "achar a frase mágica": é **especificação de entrada**, análoga a
escrever uma boa issue para um desenvolvedor.

> Esta nota cobre os **fundamentos** (o básico que o projeto ensina). O
> aprofundamento — ordem das instruções, custo do contexto, posição —
> está em [[Engenharia de prompt e contexto]].

## As 4 partes de um prompt completo

| Parte | Responde a | Exemplo |
| --- | --- | --- |
| **Papel** | *Quem* deve responder? | "Você é um revisor de contratos" |
| **Tarefa** | *O que* fazer, exatamente? | "Liste as cláusulas de risco deste texto" |
| **Contexto** | *Com base em quê*? | trecho, dados, público-alvo |
| **Formato** | *Como* entregar? | tabela, JSON, bullet de 1 linha cada |

Na prática soma-se: **exemplos** (few-shot) quando o formato é difícil, e **restrições**
(o que *não* fazer).

## Ideias-chave

- **Instruções positivas funcionam melhor** que negações: "responda em 3 bullets" vence
  "não seja prolixo" — o modelo não sabe o que *fazer* no lugar do proibido.
- **Contexto explícito, tarefa isolada.** Misturar tarefa e contexto numa frase só é a
  causa nº 1 de resposta genérica — delimitadores (tags, aspas, `---`) separam camadas.
- **Formato declarado é meio caminho.** Pedir JSON com schema, ou bullet com limite de
  palavras, elimina a etapa manual de "consertar a resposta".
- **O prompt vive dentro de um sistema.** System prompt define regras permanentes; a
  mensagem do usuário é a tarefa do momento — misturar os dois enfraquece ambos.
- **Sensibilidade não é defeito, é propriedade.** A mesma pergunta com palavras
  diferentes dá respostas diferentes — daí a importância de
  [[Pesquisa - Sensibilidade de prompt e posição]] e de testar variações.
- **Perigos correlatos:** o modelo obedece instruções vindas *de dentro dos dados*
  ([[Prompt Injection]]), confia demais em padrão confiante ([[Alucinação]]) e esquece
  o meio do contexto longo ([[Lost in the Middle]]).

## Na prática — o checklist de revisão

Antes de enviar um prompt que importa:

1. [ ] A tarefa está em **uma frase, com verbo no comando**?
2. [ ] O contexto está **delimitado** (e é só contexto — sem misturar com a tarefa)?
3. [ ] O formato de saída está **declarado** (com exemplo, se o formato for complexo)?
4. [ ] Removi instruções **negativas redundantes**?
5. [ ] Se o prompt é longo, o que está **no começo e no fim** é o mais importante?

> Regra prática: **se você não pode avaliar se a resposta está boa, o prompt está
> incompleto** — falta dizer o critério. Um prompt sem critério de aceite não é
> especificação, é aposta.

## Autoavaliação
- [ ] Escrever um prompt com as 4 partes para uma tarefa sua da semana — e identificar qual parte você costuma pular.
- [ ] Explicar por que "não seja prolixo" é um prompt fraco e como reescrevê-lo.
- [ ] Diferenciar system prompt de mensagem do usuário com um exemplo.
- [ ] Relacionar: por que variação de palavras muda a resposta (e o que isso implica para testes)?
- [ ] Explicar quando usar few-shot em vez de só descrever o formato.

## Ver também

- [[Engenharia de prompt e contexto]] · [[Spec-Driven Development]]
- [[Prompt Injection]] · [[Alucinação]] · [[Lost in the Middle]] · [[Temperatura]]
- [[Pesquisa - Sensibilidade de prompt e posição]] · [[Lab 05 - Rodando o experimento de sensibilidade de prompt]]
