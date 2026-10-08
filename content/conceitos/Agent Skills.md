---
title: "Agent Skills"
tags:
  - "conceito"
  - "skills"
  - "agentes"
tipo: "conceito"
date: "2026-10-15"
---


# Agent Skills

> **Meta:** explicar o que é uma skill (instruções especializadas carregadas sob
> demanda) e descrever a anatomia de um `SKILL.md` — nome, descrição, instruções,
> arquivos de apoio.

## O que é

Uma **skill é um pacote de instruções e recursos que torna um agente de IA bom em uma
tarefa específica** — carregado *só quando necessário*. É como dar ao agente um
"manual de procedimento" na gaveta: em vez de encher o system prompt de tudo, você
deixa as instruções especializadas em arquivos no projeto e o agente busca a relevante
quando o trabalho aparece.

> **"UI da plataforma com skills" no projeto** — o projeto usou skills para melhorar a
> interface gerada: instruções de estilo/padrões da UI empacotadas como skill, para a
> IA produzir telas consistentes sem repetir a mesma pedida toda vez.

## Anatomia

```text
minha-skill/
├── SKILL.md # nome + descrição (QUANDO usar) + instruções (COMO fazer)
├── referências/ # docs, exemplos, padrões — carregados sob demanda
└── scripts/ # utilitários executáveis que a skill invoca
```

**O campo mais importante é a `description`** — é ela que decide se a skill é ativada.
"Guia de estilo de UI para gerar telas" ativa; "skills" (genérica) nunca ativa.

## Ideias-chave

- **Progressive disclosure:** o agente vê primeiro só *nome + descrição* (~palavras);
 o corpo entra no contexto quando a skill é chamada; os arquivos de apoio, quando
 referenciados. É **economia de contexto** aplicada — ver [[Janela de Contexto]].
- **Skill ≠ prompt:** prompt é a conversa do momento, skill é **conhecimento
 reutilizável e versionado no repositório** — vive no git, revisa como código, compartilha com o time.
- **Skill é a forma projetável do comportamento.** Onde o *vibe coding* repete
 preferências em cada sessão, a skill as transforma em ativo — o braço direito de
 [[Spec-Driven Development]] no nível da instrução.
- **Granularidade:** uma skill = uma capacidade ("escrever changelog", "gerar componentes
 no padrão X"). Skills gigantes falham em ativar; skills miradas ativam sempre.
- **Descrição é contrato de ativação.** Frase genérica = skill esquecida; frase com
 gatilho concreto ("use ao criar componente React") = ativação confiável.
- **Combinam com comandos e regras:** comandos (slash) invocam de propósito; regras de
 projeto (ex.: `AGENTS.md`) são o piso sempre-ativo; skills são o especializado sob
 demanda — os três camadas de instrução de um agente.

## Na prática — escrever uma skill que funciona

1. **Situação-gatilho:** "quando X acontecer…" — escrito do ponto de vista de quem chama.
2. **Critérios de qualidade:** o que torna o resultado bom (verificável, não estético vago).
3. **Exemplo mínimo:** um bom e um ruim (few-shot aplicado — ver [[Prompt Engineering - fundamentos]]).
4. **Referências externas:** se for longo, mova o detalhe para arquivo e linkie.
5. **Teste de ativação:** descreva a tarefa de forma indireta — a skill ativa sozinha?

## Autoavaliação
- [ ] Definir skill em uma frase e explicar por que ela não é só "um prompt longo".
- [ ] Descrever as 3 camadas da progressive disclosure e o que cada uma economiza.
- [ ] Escrever uma `description` com gatilho concreto para uma tarefa sua.
- [ ] Explicar por que versionar skills no git muda o jogo para o time.
- [ ] Diferenciar comando, regra de projeto e skill com um exemplo de uso de cada.

## Ver também

- [[OpenCode]] · [[Spec-Driven Development]] · [[Desenvolvimento de Software com IA]]
- [[Prompt Engineering - fundamentos]] · [[Janela de Contexto]]
