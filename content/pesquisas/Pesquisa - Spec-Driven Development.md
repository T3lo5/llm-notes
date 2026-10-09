---
title: "Pesquisa - Spec-Driven Development"
tags:
  - "pesquisa"
  - "spec-driven"
tipo: "pesquisa"
date: "2026-10-15"
---

# Pesquisa — Spec-Driven Development

> **Pergunta que motivou esta pesquisa:** escrever a especificação antes do código
> vale o custo quando a IA gera o código de graça — ou é burocracia que a
> velocidade da IA tornou obsoleta?

## Resposta curta (TL;DR)

Vale, e por um motivo que não é moral: **quando gerar código é barato, o gargalo
vira decidir se o código está certo** — e a spec é o único artefato que responde
isso antes de você gastar o ciclo de geração. O GitHub formalizou a prática no
**spec-kit** (MIT, +140k stars): um toolkit que dá ao agente de código um processo
estruturado — `constitution → specify → plan → tasks → implement → converge` — no
qual **a especificação é versionada como fonte de verdade** e o código é derivado
dela. A frase de abertura do projeto é a tese inteira: *"define what and why
before deciding how to build it"*.

## Resposta completa

### O que o spec-kit de fato faz

O repositório não é uma opinião — é um toolkit executável que instala com
`uv tool install specify-cli` e injeta **agent skills** no projeto
(`/speckit-constitution`, `/speckit-specify`, `/speckit-plan`, `/speckit-tasks`,
`/speckit-implement`, `/speckit-converge`). Três observações importam:

1. **SDD é o processo, os comandos são skills.** Cada `/speckit-*` é uma instrução
   empacotada que o agente carrega quando invocada — o mesmo mecanismo descrito em
   [[Agent Skills]]. A spec vive em arquivos no repositório (`.specify/`,
   `specs/`), não na conversa.
2. **O ciclo tem loop de convergência.** `implement → converge` se repete até o
   relatório dizer **Converged** — ou seja, o método assume que a primeira
   implementação NÃO bate com a spec e formaliza o ciclo de correção.
3. **Não é o único processo.** O toolkit traz bug fixing (`assess → fix → test`) e
   idea assessment (`intake → research → define → shape → decide`) como entradas
   independentes — a avaliação de ideia com evidência antes de escrever código é
   SDD no sentido mais amplo: **decisão documentada antes de execução**.

### Por que isso ganhou força agora (e não em 2015)

Spec-first não é novo (foi moda como "design by contract", depois "user stories
bem escritas"). O que mudou é **quem executa**:

- Antes: spec documentada → humano implementa aos poucos → divergências aparecem
  baratas, no dia a dia.
- Agente: spec ausente → o agente **preenche lacunas com suposições plausíveis** —
  e suposição plausível é o pior tipo de erro: passa revisão de olho-grosso.
- Com spec: a lacuna vira *pergunta antes da geração*, quando corrigir custa uma
  linha de markdown.

O custo de gerar código despencou; o custo de **revisar** não. A spec é o
dispositivo de revisão posicionado o mais cedo possível. Ver
[[Desenvolvimento de Software com IA]] para o fluxo completo.

### O que a spec precisa ter para funcionar

Do reading do spec-kit e da prática, quatro propriedades:

| Propriedade | Teste | Fraude comum |
| --- | --- | --- |
| **Critérios de aceite** | "como sei que está pronto?" tem resposta verificável | "a UI deve ser boa" |
| **Fora de escopo declarado** | o que a IA *não* deve tocar está escrito | escopo implícito = o agente decide |
| **Versionada com o código** | mudança intencional atualiza a spec no mesmo commit | spec de janeiro, código de outubro |
| **Curta o bastante para reler** | cabe numa leitura de 3 minutos | spec de 12 páginas que ninguém abre |

A spec é também o **prompt de maior alavancagem** do projeto: o system prompt do
agente é uma spec de micro-escala — mesma disciplina, outra granularidade (ver
[[Prompt Engineering - fundamentos]]).

## Detalhes técnicos

- **Estrutura típica do spec-kit**: `.specify/memory/` (constitution e templates),
  `specs/<feature>/` com `spec.md`, `plan.md`, `tasks.md`, `research.md`,
  `data-model.md` — tudo markdown diffável.
- **Constitution** = princípios estáveis do projeto (qualidade de código, testes,
  manutenibilidade), escritos **uma vez** e relidos a cada feature — é o
  "semântico" da spec; o resto é sintático.
- **Convergence report** é artefato: o ciclo só para quando a implementação
  responde a cada critério — paralelo humano do nosso checklist de autoavaliação.
- Integrações: Copilot, Cursor, Claude Code, opencode — o processo é
  agnóstico de agente (justamente porque o processo mora em arquivos).

## Limitações e riscos

- **Spec vira ficção se ninguém revisa.** O artefato barato de escrever também é
  o barato de deixar desatualizado — o vínculo commit-a-commit é o único antídoto.
- **Overhead em tarefa de 10 minutos.** Spec completo para corrigir typo é teatro;
  a régua é: *mudança reversível + verificável em 1 minuto → sem spec*.
- **Converge pode loopar.** Sem critério de parada (quantas rodadas? quem
  aprova?), o agente converge contra a própria spec — a spec precisa de dono
  humano.
- **Não substitui descoberta.** Requisito desconhecido não se escreve antes de
  ver; spikes e protótipos continuam legítimos — desde que a descoberta
  atualize a spec antes do próximo ciclo.

## O que isso muda na minha prática

1. Escrever a spec **antes** de abrir o agente — 3 blocos: problema, critérios,
   fora de escopo.
2. Tratar o system prompt como spec (revisável, versionada).
3. Fechar o ciclo: divergência spec × implementação corrige **a spec primeiro** —
   se a implementação "venceu", foi decisão, não acidente; registre.
4. Aplicar o padrão ao lab: [[Lab 03 - Workflow N8N mínimo]] e
   [[Lab 04 - Agente Mastra com tools]] começam com a pergunta, não com o código.

## Fontes

- https://github.com/github/spec-kit — repositório oficial (MIT): processos,
  comandos, templates.
- https://github.com/github/spec-kit/blob/main/spec-driven.md — metodologia SDD
  completa em um documento.
- https://github.github.com/spec-kit/concepts/sdd.html — filosofia do SDD.

## Perguntas abertas

- Spec markdown vs **spec executável** (critérios como testes): quando o código do
  critério vence a prosa do critério?
- Como escrever spec para **código legado** sem transformar a auditoria em
  projeto de meses?
- O converge do spec-kit é o mesmo que "definition of done" com retry — ou
  muda algo essencial?

## Ver também

- [[Spec-Driven Development]] · [[Desenvolvimento de Software com IA]]
- [[Agent Skills]] · [[Prompt Engineering - fundamentos]]
- [[Lab 03 - Workflow N8N mínimo]] · [[Lab 04 - Agente Mastra com tools]]
