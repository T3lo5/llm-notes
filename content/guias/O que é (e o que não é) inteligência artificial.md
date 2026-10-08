---
title: "O que é (e o que não é) inteligência artificial"
tags:
  - "fundamentos"
  - "conceitos"
tipo: "guia"
date: "2026-10-08"
---

# O que é (e o que não é) inteligência artificial

> **Meta:** sair da palavra "IA" e chegar a uma taxonomia que permita decidir se um caso é de IA, de software comum, ou de nada.

## Resumo em 3 frases

1. IA é um campo amplo; **machine learning** é uma técnica dentro dele; **LLM** é uma técnica dentro de ML.
2. Todo sistema de IA em produção hoje é de **escopo estreito** — bom em uma tarefa, inútil fora dela.
3. A distinção prática que decide o projeto: **sistema determinístico** (regra fixa) vs. **sistema estatístico** (distribuição aprendida).

## A taxonomia

```
Inteligência Artificial → o campo
 └─ Machine Learning → aprende a partir de dados, sem regras escritas à mão
 ├─ Aprendizado supervisionado
 ├─ Aprendizado não supervisionado
 └─ Aprendizado por reforço
 └─ (fora de ML) Sistemas baseados em regras / Expert Systems
```

Um **LLM** (ver [[O que é um LLM]]) é um caso específico: ML supervisionado, com objetivo de prever o próximo token, em escala enorme.

Quando alguém diz "IA" num projeto, essas três camadas estão misturadas — e quase sempre o que se quer é a terceira.

## A distinção que decide: determinístico vs. estatístico

| | Software tradicional | IA |
| --- | --- | --- |
| Como decide | regra escrita por humano | distribuição aprendida dos dados |
| Mesma entrada | mesma saída, sempre | pode variar |
| Erro | produz resposta errada | produz resposta plausível e errada |
| Verificabilidade | total — teste a regra | parcial — precisa de amostra |
| Custo marginal | ~0 | ~0.01–0.10 USD por chamada típica |
| Quando o preço de errar é altíssimo | **use software** | evite |

Essa tabela é a base de [[Quando não usar inteligência artificial]].

## IA de escopo estreito vs. geral

| | Estreito (tudo que existe) | Geral (AGI) |
| --- | --- | --- |
| Escopo | uma tarefa delimitada | qualquer tarefa intelectual |
| Exemplos | classificar e-mail, resumir doc, gerar código | — |
| Comportamento fora do escopo | inútil ou inventado | — |

O marketing usa "IA" onde caberia "classificador". Se o sistema só faz uma coisa, chamar de IA não o torna mais capaz — apenas cria expectativa que ele não cumpre.

## O que IA não é

- **Não é consciente** nem entende o que faz — ela calcula a continuação mais provável de um texto.
- **Não é fonte de verdade.** Não tem consulta a nada; tem estatística comprimida nos pesos.
- **Não é determinística.** A mesma entrada pode gerar saídas diferentes (ver [[Temperatura e previsibilidade]]).
- **Não generaliza fora do treino** de forma confiável. Ela acerta raciocínio; não há garantia de que acerte.
- **Não substitui o domínio.** Quem define se a resposta está boa é alguém que entende o assunto — não o modelo.

## Por que a confusão de escopo é cara

Prometer "IA que resolve o problema X" quando o sistema faz 80% do problema X gera duas consequências:

1. **Operacional:** revisão humana constante, que consome o ganho.
2. **Estratégica:** quando o ganho não aparece, o projeto é declarado fracasso — e a conclusão errada é "IA não funciona neste caso".

Ver [[Antipatrones de adocao de IA]].

## Perguntas para validar

1. Classifique cada um em "software tradicional" ou "IA": validação de CPF, recomendação de filme, redação de e-mail, contador.
2. Por que um sistema determinístico é preferível quando o custo de um erro é alto?
3. Se tudo que existe é IA de escopo estreito, o que a palavra "IA" promete além do que o sistema entrega?
