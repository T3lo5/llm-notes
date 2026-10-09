---
title: "O que e e nao e IA"
tags:
  - "conceito"
  - "fundamentos"
tipo: "conceito"
date: "2026-10-08"
---

# O que é (e não é) IA

> Taxonomia para decidir se um caso é de IA, de software comum, ou de nada.

## A hierarquia

```
Inteligência Artificial          → o campo
  └─ Machine Learning             → aprende de dados, sem regras escritas à mão
       ├─ supervisionado
       ├─ não supervisionado
       └─ por reforço
  └─ (fora de ML) Sistemas baseados em regras
```

Um [[O que é um LLM]] é um caso específico: ML supervisionado, objetivo de prever o próximo token, em escala enorme.

Quando alguém diz "IA" num projeto, as três camadas estão misturadas — e quase sempre o que se quer é a terceira.

## A distinção que decide o projeto

| | Software tradicional | IA |
| --- | --- | --- |
| Como decide | regra escrita por humano | distribuição aprendida dos dados |
| Mesma entrada | mesma saída, sempre | pode variar |
| Erro | resposta errada | resposta plausível e errada |
| Verificabilidade | total | parcial — precisa de amostra |
| Custo marginal | ~0 | centavos por chamada |
| Quando o preço de errar é altíssimo | **use software** | evite |

## Escopo estreito

Todo sistema de IA em produção é de **escopo estreito**: bom em uma tarefa, inútil fora dela. O marketing diz "IA" onde caberia "classificador" — e isso cria expectativa que o sistema não cumpre.

## O que IA não é

- **Não é consciente** nem entende o que faz — calcula a continuação mais provável de um texto.
- **Não é fonte de verdade.** Não consulta nada; tem estatística comprimida nos pesos.
- **Não é determinística.** Ver [[Temperatura e previsibilidade]].
- **Não generaliza** de forma confiável fora do treino. Acerta raciocínio; não há garantia.
- **Não substitui o domínio.** Quem julga se a resposta está boa é alguém que entende do assunto.

## Origem

- [[O que é (e o que não é) inteligência artificial]]
