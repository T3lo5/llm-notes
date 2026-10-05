---
title: "Respostas diferentes para perguntas iguais"
tags:
  - "prompt"
  - "avaliacao"
tipo: "guia"
date: "2026-10-06"
---

# Respostas diferentes para perguntas iguais

> **Meta:** entender por que a mesma pergunta produz respostas diferentes, e como isso depende da **formulação** e do **contexto** — e não de aleatoriedade Pura.


## Resumo em 3 frases

1. A IA responde à **pergunta que recebeu**, não à pergunta que estava na sua cabeça. Reformular muda o resultado — às vezes mais do que mejorar o conteúdo.
2. A variação tem duas fontes: a **amostragem** (estocástica, inherent ao modelo) e a **variação de entrada** (contexto e formulação diferentes).
3. Consequência prática: comparar duas respostas como se fossem medição de qualidade exige **fixar a entrada**. Sem isso, você mede ruído.

## Duas fontes de variação

| Fonte | Natureza | Controlável? |
| --- | --- | --- |
| **Amostragem** | o modelo escolhe entre tokens plausíveis; temperatura e top-p alteram a distribuição | sim, parcialmente |
| **Formulação e contexto** | a mesma intenção, escrita diferente, produz contexto diferente | **sim, totalmente** |

A segunda é a que interessa aqui, porque é a que está sob seu controle no momento em que você escreve o prompt.

## Como a formulação muda a resposta

| Mudança | O que acontece |
| --- | --- |
| Adicionar um exemplo | ancora o formato e o nível de detalhe |
| Trocar "explique" por "liste 3" | força estrutura e reduz a resposta vaga |
| Dar contexto ("para um público técnico") | ajusta vocabulário e profundidade |
| Especificar formato ("em tabela") | elimina o guia de prosa |
| Retirar um detalhe | o modelo volta ao padrão mais provável |

> O detalhe final é o mais subestimado: **tirar** informação do prompt também é engenharia. Um prompt supercarregado empurra o modelo para a média.

## Contexto muda mais que a pergunta

O mesmo texto perguntado em contextos diferentes gera respostas diferentes, porque o **contexto é a fonte de verdade** — ver [[O que é um LLM, de verdade]].

- Pergunta sem documento → responde a partir dos parâmetros (pode alucinar)
- Pergunta com o documento que confirma → segue o documento
- Pergunta com o documento que **contradiz** → o documento vence (ver [[Lost in the Middle]])

## Como medir sem se enganar

Três regras para não tirar conclusão de uma amostra:

1. **Fixe a entrada** antes de comparar abordagens.
2. **Rode várias vezes** com a mesma entrada e temperatura 0 (ver [[Lab 04 - Temperatura, top-p e reprodutibilidade]]).
3. **Avalie em conjunto**, não por impressão de uma resposta — é o que o formaliza.

> A[[Como o modelo gera respostas, token a token]] mostra por que isso importa: se cada execução é um caminho diferente no espaço de tokens, comparar respostas exige controlar o caminho.

## Perguntas para validar

1. Se a temperatura é 0, por que ainda pode haver variação pequena? (kernel não determinístico)
2. Reformular a pergunta mudando **uma** palavra pode mudar a resposta? Em que condições?
3. Qual é a diferença entre "o modelo é inconsistente" e "eu não controlei a entrada"?

## Ver também

- [[Como o modelo gera respostas, token a token]] · [[Sensibilidade de prompt: ordem importa]] · [[Temperatura]] · [[Alucinação]]
