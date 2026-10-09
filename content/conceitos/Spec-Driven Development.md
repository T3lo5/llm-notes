---
title: "Spec-Driven Development"
tags:
  - "conceito"
  - "sdd"
  - "processo"
tipo: "conceito"
date: "2026-10-15"
---


# Spec-Driven Development (SDD)

> **Meta:** explicar SDD em uma frase (especificação como fonte de verdade, versionada
> antes do código) e descrever o ciclo spec → plano → implementação com um exemplo.

## O que é

Um estilo de desenvolvimento em que a **especificação é o artefato primário** —
escrita, revisada e versionada **antes** do código — e o código é *derivado* dela. Em
vez de "código é a documentação", a spec é o contrato: o código muda, a intenção fica
registrada e comparável.

No contexto de IA, o SDD ganhou força porque **o agente que precisa de uma spec para
trabalhar bem**: spec é o que vai no contexto dele e é o critério para dizer se o
resultado está certo ou errado.

## Por que importa (aqui e no projeto)

- Foi **item deste projeto** (fase "SDD — Spec-Driven Development") — o projeto é
  a demonstração de que spec-first e IA se complementam: a IA acelera a
  implementação, a spec segura a direção.
- É o antídoto processual contra o *vibe coding* descrito em
  [[Desenvolvimento de Software com IA]].
- Sem spec, a revisão de código gerado por IA vira opinião; **com spec, vira verificação**
  ("bate com os critérios 1, 2, 3?").

## O ciclo

```text
1. SPEC      o que e por quê: requisitos + critérios de aceite + fora de escopo
   ↓         (revisável por humanos — aqui ainda é barato mudar de ideia)
2. PLANO     como: arquivos, dependências, ordem de passos, riscos
   ↓
3. TASKS     fatias executáveis, cada uma com verificação (teste/lint)
   ↓
4. IMPL.     a IA executa tarefa a tarefa; humano aprova diffs
   ↓
5. FEEDBACK  divergência entre spec e realidade → atualiza a spec PRIMEIRO
```

Ferramentas do ecossistema: o **spec-kit** do GitHub popularizou comandos
`/specify → /plan → /tasks → /implement`; no repositório, o paralelo é o template da nota e o
checklist de aceite.

## Ideias-chave

- **Spec curta e testável vence spec gigante.** Uma spec que ninguém relê não governa
  nada; o valor está em critérios que respondem "como sei que está pronto?".
- **Critérios de aceite são asserts humanos.** "O usuário vê o preço antes de comprar"
  é verificável; "a UI deve ser boa" não é — o segundo não é spec, é desejo.
- **A spec versiona junto com o código.** Mudou a implementação de forma intencional?
  A spec muda no mesmo commit — senão ela vira mentira documentada.
- **Fora de escopo é meia spec.** Metade dos problemas em projeto com IA vem de escopo
  que a IA *assumiu* sozinha; declarar o que não fazer fecha a porta.
- **A spec é o prompt de maior alavancagem.** Um system prompt bem escrito é uma spec
  de micro-escala (ver [[Prompt Engineering - fundamentos]]) — a mesma disciplina, em
  outra granularidade.
- **SDD não elimina descoberta**, ela a localiza: explorar com spike é bom; descobrir
  requisito no diff de produção é ruim.

## Autoavaliação
- [ ] Definir SDD em uma frase, sem citar ferramentas.
- [ ] Escrever spec + 3 critérios de aceite para uma tarefa pequena sua (com "fora de escopo").
- [ ] Explicar por que SDD melhora especificamente o resultado de um **agente** de IA.
- [ ] Dizer o que fazer quando spec e implementação divergem (e em que ordem corrigir).
- [ ] Apontar a diferença entre um critério de aceite verificável e um desejo.

## Ver também

- [[Desenvolvimento de Software com IA]] · [[Prompt Engineering - fundamentos]]
- [[Agent Skills]] · [[N8N]] · [[Mastra]]
