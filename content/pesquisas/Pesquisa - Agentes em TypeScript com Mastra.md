---
title: "Pesquisa - Agentes em TypeScript com Mastra"
tags:
  - "pesquisa"
  - "mastra"
  - "agentes"
tipo: "pesquisa"
date: "2026-10-15"
---

# Pesquisa — Agentes em TypeScript com Mastra

> **Pergunta que motivou esta pesquisa:** o que um framework de agentes
> adiciona além de um loop que chama a API do modelo com ferramentas?

## Resposta curta (TL;DR)

Adiciona **contrato, observabilidade e ciclo de vida**. O Mastra é um framework
TypeScript para agentes de IA com quatro peças: `Agent` (instruções + modelo +
tools), `createTool` (**tool tipada com zod** — preenchimento inválido morre na
validação, antes do `execute`), registro `Mastra` (ponto de entrada único) e
Studio (interface de trace/inspeção). O modelo é declarado como **string no
formato `provider/model`** (ex.: `openai/gpt-5-mini`) — o framework resolve o
provider pelas variáveis de ambiente. A frase que resume o ganho: sem schema, o
modelo **alucina argumentos**; com schema, ele escolhe entre opções válidas
([[Alucinação]] vira problema de interface, não de sorte).

## Resposta completa

### As primitivas (pela documentação oficial)

```ts
// 1. Tool — createTool é obrigatório: objeto simples falha em silêncio
import { createTool } from '@mastra/core/tools'
import { z } from 'zod'

export const weatherTool = createTool({
  id: 'get-weather',
  description: 'Get current weather for a location',
  inputSchema: z.object({ location: z.string().describe('City name') }),
  execute: async ({ location }) => { /* ... */ },
})

// 2. Agent — constructor { id, name, instructions, model, tools }
import { Agent } from '@mastra/core/agent'
export const weatherAgent = new Agent({
  id: 'weather-agent', name: 'Weather Agent',
  instructions: `You are a helpful weather assistant...`,
  model: 'openai/gpt-5-mini',        // string provider/model — sem import de provider
  tools: { weatherTool },
})

// 3. Registro — ponto de entrada único
export const mastra = new Mastra({ agents: { weatherAgent } })

// 4. Execução
const agent = mastra.getAgentById('weather-agent')
const response = await agent.generate('Weather in SF')
```

Quatro detalhes que a docs enfatiza **como correção de desatualização** (sinal de
que o ecossistema muda rápido):

1. **`createTool()` com `id`, `description`, `inputSchema` (zod), `execute`** —
   *"plain object tool definitions silently fail to execute"*. A ferramenta
   declarada errado não quebra: **some**. O framework prefere falha silenciosa a
   exceção — motivo mais forte ainda para seguir o contrato à risca.
2. **`execute(inputData, context)`** — assinatura única; `context` traz
   `requestContext`, `tracingContext`, `abortSignal` (cancelamento = controle de
   custo e de laço).
3. **`model` é string `provider/model`** — `openai/gpt-5-mini`, não
   `provider:model`, não objeto. O framework procura a env var do provider
   (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`...).
4. **Node 22.18+ roda TypeScript direto** — `node run.mjs` com imports locais
   terminados em `.ts`; sem build step para prototipar.

### O que o framework resolve que o loop caseiro não

| Camada | Loop caseiro | Mastra |
| --- | --- | --- |
| Validação de argumento | `if (!location) ...` ad hoc | zod na fronteira, rejeita antes do `execute` |
| Observabilidade | `console.log` | trace por passo (Studio: `mastra dev`) |
| Registro/descoberta | dicionário manual | `Mastra({ agents })` + `getAgentById` |
| Estado entre turnos | você inventa | memória/agenda como primitiva |
| Avaliação | ninguém avalia | evals de tool e de resposta |

A division of labor com o orquestrador fica nítida: **N8N decide o quando e o
fluxo; Mastra decide o que fazer e com qual ferramenta** — ver [[N8N]] e
[[Mastra]].

### Setup mínimo (uma das docs)

```bash
npm install @mastra/core@latest zod@latest typescript@latest @types/node@latest mastra@latest
# tsconfig: ES2022, moduleResolution bundler, strict
# npm create mastra@latest  → scaffold completo com workspace e tools
```

## Detalhes técnicos

- **zod como contrato**: `.describe()` em cada campo vira doc para o modelo —
  o schema É o prompt da ferramenta. Campo ambíguo = escolha errada mesmo
  com schema válido.
- **`description` da tool = decisão do modelo** — paralelo exato da `description`
  de skill ([[Agent Skills]]): dizer o que faz **e quando usar**.
- **`abortSignal`** no contexto: cancelamento propagado — base para timeouts de
  execução com custo limitado.
- **Studio** (`mastra dev`): UI com traces de execução, mensagens, tokens — o
  "por que errou" vira investigação de passo, não de conversa.
- **Skills para coding agents**: `npm create mastra@latest` instala skills do
  Mastra para o agente de código instalado — framework que se documenta para
  agentes usar.

## Limitações e riscos

- **Velocidade de mudança**: a própria docs pede que se confie nela sobre dados
  de treino — API de framework de agente tem janela de validade curta; tratar
  código de agente como código de integração (adaptação barata esperada).
- **Tools com efeito colateral** (gravar no banco) × **retry do modelo**: sem
  idempotência, a repetição duplica. `execute` deve ser seguro para rodar duas
  vezes.
- **Custo de observabilidade**: trace completo de execução longa acumula —
  reter seletivo.
- **Silent fail das tools**: objeto fora do padrão some — teste negativo
  obrigatório (ver [[Lab 04 - Agente Mastra com tools]]).
- **Framework ≠ garantia de segurança**: instruções frágilmente escritas +
  tool permissiva = prompt injection vira ação ([[Prompt Injection]]).

## O que isso muda na minha prática

1. **Tool sempre `createTool` + zod + `execute` com `inputData` validado** — e
   teste negativo na suíte (payload inválido deve falhar **antes** do execute).
2. **`instructions` é spec do comportamento** — escrita como
   [[Spec-Driven Development]], não como anotação de conversa.
3. **Trace antes de otimizar**: rodar com Studio e ler o passo que falhou.
4. **Modelo por string** — trocar de modelo = trocar de env var; custo de
   experimentação zero.

## Fontes

- https://mastra.ai/docs — documentação oficial (get started, agents, tools).
- https://mastra.ai/llms.txt — índice das páginas (markdown para agents).
- https://mastra.ai/models — tabela de modelos e variáveis de ambiente.

## Perguntas abertas

- Mastra vs **LangGraph** vs loop TypeScript de 50 linhas: em que tamanho de
  projeto o framework paga a curva de versão?
- Como versionar `instructions` — commit como código ou fixture de teste?
- Avaliação (evals) de agente: qual métrica mínima para dormir tranquilo com
  tool de escrita em produção?

## Ver também

- [[Mastra]] · [[N8N]] · [[Desenvolvimento de Software com IA]]
- [[Alucinação]] · [[Prompt Injection]] · [[Agent Skills]]
- [[Lab 04 - Agente Mastra com tools]]
