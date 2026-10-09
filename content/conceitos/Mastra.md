---
title: "Mastra"
tags:
  - "conceito"
  - "mastra"
  - "agentes"
tipo: "conceito"
date: "2026-10-15"
---


# Mastra

> **Meta:** explicar o que é o Mastra (framework de agentes em TypeScript) e descrever
> suas 4 primitivas — agente, tools, workflow, memória — com um exemplo do projeto.

## O que é

**Mastra é um framework open source para construir agentes de IA em TypeScript/Node** —
a camada de código onde você **define o agente**: qual modelo usa, quais *ferramentas*
ele pode chamar, qual fluxo de trabalho executa, o que lembra entre turnos. Se o N8N é
o editor visual que **orquestra etapas**, o Mastra é o **código que implementa o cérebro**
do agente customizado do projeto.

Neste projeto, ele é o componente que cria o **agente customizado** da plataforma
de avaliação de produtos — o que conversa com o usuário e decide quais ações tomar.

## As 4 primitivas

| Primitiva | Papel | No projeto |
| --- | --- | --- |
| **Agent** | modelo + instruções + ferramentas | agente que responde sobre produtos |
| **Tools** | ações tipadas que o agente chama | buscar produto, inserir no banco |
| **Workflow** | passos determinísticos com controle | cadeia consulta → recuperação → resposta |
| **Memory / RAG** | contexto entre turnos e conhecimento | histórico e base de produtos (ver [[RAG]]) |

## Ideias-chave

- **Ferramenta tipada = contrato.** Cada tool tem schema de entrada/saída (no ecossistema
  TS, tipagem/zod) — **contrato explícito reduz alucinação de parâmetros**, porque o
  modelo é obrigado a preencher uma forma válida (relaciona com [[Alucinação]]).
- **O agente escolhe, o workflow garante.** Deixar o LLM livre para qualquer sequência
  é imprevisível; envolver a tarefa num workflow com passos definidos ganha
  confiabilidade sem perder flexibilidade — é o mesmo espírito do [[Spec-Driven Development]].
- **System prompt é spec do agente.** As instruções do agente (papel, limites, formato)
  são [[Prompt Engineering - fundamentos]] aplicada à produtividade.
- **Observabilidade vem de fábrica.** Traços de cada execução (chamadas, tokens, latência)
  transformam "a IA errou" em "o passo 3 falhou" — debug vira investigação de fluxo.
- **Memória é custo e privacidade.** Lembrar tudo = contexto sempre crescente
  ([[Janela de Contexto]]) e dado guardado — reter o necessário, com janela e
  descarte definidos.
- **N8N × Mastra na mesma frase:** N8N **desenha e executa** a automação; Mastra
  **implementa o agente** que a automação chama. Integração via webhook/HTTP.

## Na prática — esqueleto do agente do projeto

```ts
const agente = new Agent({
  model: openai("gpt-4o-mini"),      // 1. cérebro
  instructions: SYSTEM_DE_SPEC,       // 2. spec do comportamento
  tools: { buscarProduto, inserirProduto },  // 3. ações tipadas
  memory: janelaDescartavel,          // 4. contexto entre turnos
});
```

Fluxo completo do projeto: **N8N (gatilho + etapas) → Mastra (decisão + ferramentas) →
banco/UI**.

## Autoavaliação
- [ ] Definir Mastra e diferenciá-lo de um modelo de linguagem e de um orquestrador como o N8N.
- [ ] Nomear as 4 primitivas e dizer o que quebra se a tool não tiver schema.
- [ ] Explicar por que workflow determinístico + liberdade do LLM é a combinação certa.
- [ ] Dizer o que o system prompt de um agente tem a ver com engenharia de prompt.
- [ ] Descrever o fluxo do projeto (N8N → Mastra → banco) indicando quem faz o quê.

## Ver também

- [[N8N]] · [[Desenvolvimento de Software com IA]] · [[Spec-Driven Development]]
- [[Prompt Engineering - fundamentos]] · [[RAG]] · [[Alucinação]] · [[Janela de Contexto]]
