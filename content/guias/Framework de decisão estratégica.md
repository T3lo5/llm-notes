---
title: "Framework de decisão estratégica"
tags:
  - "fundamentos"
  - "framework"
  - "decisao"
tipo: "guia"
date: "2026-10-05"
---

# Framework de decisão estratégica

> **Meta:** sair com um framework utilizável, aplicável a qualquer caso de uso em minutos.

## Resumo em 3 frases

1. Um framework de decisão para IA deve ser **respondível em uma folha** e aplicável **antes** de escrever qualquer linha de prompt.
2. As perguntas são nesta ordem: o problema é de IA? há dados? o erro é tolerável? qual alavanca de valor? qual o menor experimento?
3. A saída não é sim ou não — é **experimento, custo-teto, métrica de sucesso e critério de abandono**.

## O framework em 8 perguntas

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

A pergunta 7 é a que mais reprova projetos, e é a que mais tarde custa caro: **sem linha de base medida antes, não existe ganho para provar**.

## A matriz de pontuação

Dê nota de 1 a 5 para cada dimensão. Serve para **comparar casos**, não para aprovar sozinho.

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

**Leitura do resultado:** a pontuação não aprova nada. Ela serve para comparar dois casos e dizer qual testar primeiro — e para enxergar **qual dimensão** está segurando o projeto.

## A saída do framework

Um framework de decisão deve terminar em **quatro números escritos**, não em uma opinião:

```
Hipótese: Se <mudança>, então <métrica> vai de <antes> para <depois>.
Experimento: <o menor teste possível>, prazo <N> dias.
Custo-teto: <valor> / <horas>. Se passar, PARAR.
Critério de abandono: <condição observável> até <data>.
```

O **critério de abandono** é a parte que quase sempre falta. Sem ele, o projeto nunca morre — e projeto que nunca morre consome a organização.

Ver [[Antipatrones de adocao de IA]] para o antipadrão exato do piloto eterno.

## Aplicação

O framework está aplicado ao seu caso, escrito na [[Projeto: avaliação de caso de uso de IA]].



## Perguntas para validar

1. Em qual das 8 perguntas a maioria dos projetos reprova?
2. Por que a pergunta 7 (medir) é mais difícil que as outras?
3. O que aconteceria se o critério de abandono fosse definido só depois do resultado?

## Ver também

- [[Framework de decisao estrategica]] · [[Que problemas a IA resolve]] · [[Como a IA gera valor de negócio]]
