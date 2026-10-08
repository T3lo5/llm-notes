---
title: "Quando nao usar IA"
tags:
  - "conceito"
  - "decisao"
  - "estrategia"
tipo: "conceito"
date: "2026-10-08"
---

# Quando não usar IA

> A competência de dizer não. É o que evita dinheiro jogado fora em projeto de empresa.

## As seis razões

| # | Razão | Teste | Alternativa |
| --- | --- | --- | --- |
| 1 | **A regra é conhecida** | dá para escrever a condição "se/então"? | software de regras |
| 2 | **O erro é inaceitável** | a resposta errada custa mais que o serviço inteiro? | revisão humana, ou não usar |
| 3 | **Não há dados** | você tem exemplos do bom e do ruim? | primeiro, gerar o dado |
| 4 | **Não há valor** | a conta por unidade fecha? | não fazer |
| 5 | **A latência não permite** | a resposta precisa chegar em X ms? | modelo pequeno, cache, ou nada |
| 6 | **Não é problema de IA** | o que está quebrado é processo, dado ou decisão? | consertar aquilo |

## A regra das 90%

> **Se um sistema de regras resolve 90% do caso, use o sistema de regras.**

Três razões:

1. **Custo** — o de IA é sempre maior: chamada, integração, avaliação, supervisão.
2. **Auditabilidade** — regra se explica; modelo probabilístico exige amostra.
3. **Previsibilidade** — regra não tem cauda. Modelo tem.

Na prática, os 10% restantes são frequentemente o núcleo do negócio — e é exatamente onde a IA vale. A ordem certa é **regras primeiro, IA na cauda**.

## Quando o erro é inaceitável

| Cenário | IA aceitável? |
| --- | --- |
| Erro revisto por humano antes de agir | sim — o humano é o portão |
| Erro detectado depois, com custo baixo | sim — com amostragem de auditoria |
| Erro silencioso que ninguém vê | **não** — você perde o sinal |
| Erro com consequência legal ou regulatória | **não**, sem trilha e explicação |

O padrão é o de qualquer sistema: a IA pode proposer, mas a **decisão precisa ter autor identificado**.

## O caso mais subestimado

Antes de culpar a tecnologia, verifique se o problema é realmente de IA:

- **Falta dado ou falta de registro?** Sem histórico, nem pessoa resolve.
- **O processo está quebrado?** Automatizar um processo ruim só faz o erro mais rápido.
- **Falta decisão de quem manda?** Ninguém pode aprovar o resultado.
- **Falta dono?** Projeto sem dono não passa da fase piloto.

"Não usamos IA, e contratamos alguém para resolver X" é uma resposta legítima — e às vezes é a única.

## Origem

- [[Quando não usar inteligência artificial]]

## Ver também

- [[Framework de decisao estrategica]] · [[Antipatrones de adocao de IA]] · [[Que problemas a IA resolve]]

---
*Ficha criada em 2026-10-01*
