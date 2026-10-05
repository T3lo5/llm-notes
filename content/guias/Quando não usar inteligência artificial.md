---
title: "Quando não usar inteligência artificial"
tags:
  - "fundamentos"
  - "estrategia"
  - "decisao"
tipo: "guia"
date: "2026-10-08"
---

# Quando não usar inteligência artificial

> **Meta:** aprender a dizer não — a competência que mais evita dinheiro jogado fora em projeto de empresa.

## Resumo em 3 frases

1. Existe uma classe de problema em que **usar IA é o erro**: regra conhecida, erro inaceitável, ausência de dados ou ausência de valor.
2. A regra prática: se um sistema de regras resolve 90% do caso, use o sistema de regras — é mais barato e mais auditável.
3. Há também o caso em que o problema não é IA: é processo quebrado, dados faltando ou alguém sem autoridade de decisão.

## As seis razões para não usar

| # | Razão | Teste | Alternativa |
| --- | --- | --- | --- |
| 1 | **A regra é conhecida** | dá para escrever a condição "se/então"? | software de regras |
| 2 | **O erro é inaceitável** | uma resposta errada custa mais que o serviço inteiro? | revisão humana obrigatória, ou não usar |
| 3 | **Não há dados** | você tem exemplos do bom e do ruim? | primeiro, gerar o dado |
| 4 | **Não há valor** | a conta por unidade fecha? | não fazer |
| 5 | **A latência não permite** | a resposta precisa chegar em X ms? | modelo pequeno, cache, ou não usar |
| 6 | **Não é problema de IA** | o que está quebrado é processo, dado ou decisão? | consertar aquilo |

## A regra das 90%

> **Se um sistema de regras resolve 90% do caso, use o sistema de regras.**

Três Razões pelas quais isso é certo:

1. **Custo**: o de IA é sempre maior — chamada, integração, avaliação, supervisão.
2. **Auditabilidade**: um sistema de regras se explica; um modelo probabilístico precisa de amostra para ser explicado.
3. **Comportamento previsível**: regra não tem cauda. Modelo tem.

Na prática: os 10% restantes frequentemente são o núcleo do negócio — e são exatamente onde vale a IA. A ordem certa é **regras primeiro, IA na cauda**.

## Quando o erro é inaceitável

O ponto merece mais detalhe, porque é onde a regulação aparece:

| Cenário | IA aceitável? |
| --- | --- |
| Erro revisto por humano antes de agir | sim — o humano é o gate |
| Erro detectado depois, cheaply | sim — com amostragem de auditoria |
| Erro silencioso que ninguém vê | **não** — você perde o sinal |
| Erro com consequência legal/regulatória | **não** sem trilha e explicação |

O padrão é o mesmo de qualquer sistema: a IA pode propor, mas a **decisão precisa ter autor identificado**.

## O caso mais subestimado: o problema não é IA

Antes de culpar a tecnologia, verifique:

- **Falta dado ou falta de registro?** Sem histórico, nem pessoa resolve.
- **O processo está quebrado?** Automatizar um processo ruim só faz o erro mais rápido.
- **Falta decisão de quem manda?** Ninguém pode aprovar o resultado.
- **Falta dono?** Projeto sem dono não passa da fase piloto.

> Em muitos casos a resposta correta é "não usamos IA, e contratamos alguém para resolver X". É uma resposta legítima e às vezes é a única.

## Perguntas para validar

1. Cite um caso em que você usaria software de regras mesmo sendo mais trabalhoso.
2. Por que "erro revisto por humano" muda completamente a aceitabilidade?
3. Como distinguir "o problema não é IA" de "a IA não é boa o suficiente"?

## Ver também

- [[Que problemas a IA resolve]] · Antipatrones de adocao de IA · Framework de decisao estrategica
