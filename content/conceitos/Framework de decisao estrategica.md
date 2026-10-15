---
title: "Framework de decisao estrategica"
tags:
  - "conceito"
  - "framework"
  - "decisao"
tipo: "conceito"
date: "2026-10-08"
---

# Framework de decisão estratégica

> Ferramenta para decidir **se** e **como** usar IA em um caso de uso — antes de escrever qualquer linha de prompt.

## As 8 perguntas

| # | Pergunta | Se a resposta for não |
| --- | --- | --- |
| 1 | O problema é **de IA**, ou é de processo/dado/decisão? | Pare. Resolva o que é. |
| 2 | Existe **volume alto** e tarefa recorrente? | Automação simples resolve. |
| 3 | Temos **dados** (exemplos do bom e do ruim)? | Gere o dado primeiro. |
| 4 | O **erro é tolerável** ou detectável? | Use IA só como sugestão. |
| 5 | Qual **alavanca**: custo, receita, velocidade ou qualidade? | Não há caso de uso. |
| 6 | Qual o **menor experimento** que testa a hipótese? | Não comece por projeto. |
| 7 | Como **medir** o antes e o depois? | Não há como provar ganho. |
| 8 | O que acontece se **errar**? Custo-teto? | Defina o teto antes. |

A pergunta 7 reprova mais projetos que qualquer outra — e é a que custa mais caro quando descoberta tarde.

## A matriz de pontuação

De 1 a 5 em cada dimensão. Serve para **comparar** casos, não para aprovar sozinho.

| Dimensão | 1 (desfavorável) | 5 (favorável) |
| --- | --- | --- |
| Volume | alguns por mês | milhares por dia |
| Recorrência | cada caso é único | idêntico toda semana |
| Estruturação do dado | bagunçado, sem padrão | já vem estruturado |
| Tolerância a erro | erro caro ou invisível | erro barato e detectável |
| Valor por unidade | ganho de segundos | ganho de horas |
| Latência exigida | precisa ser instantâneo | pode esperar segundos |
| Risco regulatório | alto, com trilha obrigatória | baixo |
| Facilidade de avaliação | sem como medir | métrica já existe |

## A saída: quatro números escritos

```
Hipótese:  Se <mudança>, então <métrica> vai de <antes> para <depois>.
Experimento: <o menor teste possível>, prazo <N> dias.
Custo-teto: <valor> / <horas>. Se passar, PARAR.
Critério de abandono: <condição observável> até <data>.
```

O **critério de abandono** é a parte que quase sempre falta — e é o que impede o antipadrão do piloto eterno.

## Origem


## Ver também

- [[Quando nao usar IA]] · [[Antipatrones de adocao de IA]] · [[Valor de negocio com IA]]

---
*Ficha criada em 2026-10-01*
