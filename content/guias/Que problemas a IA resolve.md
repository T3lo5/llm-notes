---
title: "Que problemas a IA resolve"
tags:
  - "fundamentos"
  - "estrategia"
tipo: "guia"
date: "2026-10-08"
---

# Que problemas a IA resolve

> **Meta:** converter a abstração de "IA resolve problemas" em um critério de triagem verificável.

## Resumo em 3 frases

1. IA resolve bem um padrão específico: **volume alto, tarefa recorrente, entrada não estruturada, erro tolerável**.
2. O caso de uso quase sempre é *transformar texto não estruturado em algo consultável ou acionável* — não "ter uma IA".
3. Se as quatro condições não estiverem presentes juntas, a[[Quando não usar inteligência artificial]] manda não usar.

## O padrão que a IA resolve

A estrutura é sempre a mesma:

```
volume alto × tarefa recorrente × entrada não estruturada × erro tolerável
 ↓
 transformar texto em algo estruturado
 ↓
 consultável, acionável, automatizável
```

O denominador comum é **volume de texto não estruturado**. É por isso que IA aparece tanto em suporte, jurídico, vendas, saúde e documentação: são domínios com muito texto e pouca estrutura.

## As seis famílias de problema

| Família | Entrada | Saída | Exemplo | Tolera erro? |
| --- | --- | --- | --- | --- |
| **Classificar / rotular** | texto | uma de N categorias | triagem de chamado, moderação | alto, se há revisão |
| **Extrair** | texto não estruturado | campos | nota fiscal, contrato, currículo | médio — campo errado tem custo |
| **Resumir** | texto longo | texto curto | ata de reunião, resumo de contrato | alto |
| **Transformar / gerar** | instrução + contexto | texto novo | redação, tradução, refatoração | alto |
| **Buscar / responder** | pergunta | trecho com fonte | RAG, busca semântica | **baixo** — alucinação incomoda |
| **Programar** | descrição | código | geração e revisão de código | médio — passa por teste |

## A triagem

Responda três perguntas. É preciso **sim** nas três:

1. **Existe volume?** Dez enquadros por semana não justifica IA — resolve com um formulário.
2. **A tarefa se repete?** Se cada caso é único e nunca se assemelha a outro, não há padrão para aprender.
3. **O erro é detectável?** Se ninguém consegue dizer que a resposta está errada, você não consegue avaliar nem corrigir.

A quarta condição — entrada não estruturada — quase sempre vem junto, porque é o que a IA faz de diferente.

## Quando o critério reprova

| Situação | Veredicto |
| --- | --- |
| Volume baixo, mas tarefa repetitiva | talvez — automação simples resolve |
| Volume alto, tarefa única e sem repetição | não — não há padrão |
| Volume alto e recorrente, mas erro inaceitável e invisível | **não** — ver [[Quando não usar inteligência artificial]] |
| Volume alto, mas o problema real é processo quebrado | **não** — a IA não conserta o processo |

## O deslocamento de custo

O motivo econômico: IA é cara **por chamada** e barata **por unidade de trabalho**. Se cada chamada custa centavos e economiza minutos, a conta fecha. Se economiza milissegundos, não fecha.

> Esse é o filtro que elimina a maioria das ideias ruins: **a conta por unidade, não a tecnologia**.

## Perguntas para validar

1. Para a família "buscar/responder", por que a tolerância a erro cai muito?
2. Um processo com 500 documentos por mês e resultado crítico — passa na triagem? Por quê?
3. Cite um problema do seu trabalho que passa na triagem e um que não passa.

## Ver também

- [[Quando não usar inteligência artificial]] · Framework de decisao estrategica · [[Framework de decisão estratégica]]
