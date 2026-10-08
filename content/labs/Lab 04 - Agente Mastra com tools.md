---
title: "Lab 04 - Agente Mastra com tools"
tags:
  - "lab"
  - "mastra"
  - "agentes"
tipo: "lab"
date: "2026-10-15"
---

# Lab 04 — Agente Mastra com tools tipadas

> **O que este lab prova:** que a `inputSchema` (zod) mata alucinação de
> argumento **antes** do `execute`, e que `createTool` obrigatório (objeto
> simples falha em silêncio) é diferença entre tool que roda e tool que some.

## Pergunta

O que acontece quando o modelo (ou você) preenche a tool com argumento fora do
schema?

## Hipótese

> Payload inválido na fronteira do schema **gera ZodError antes de qualquer
> efeito colateral** — o `execute` nem é chamado. E o agente escolhe entre as 2
> tools corretamente em 3/3 perguntas de escopo claro, sem chamar ferramenta
> fora de hora. Uma tool definida como objeto simples (`{ id, execute }`) não
> levanta erro: **silencia**.

## Setup

Node **22.18+** (roda TS/ESM direto) e chave do provedor no modelo que você
usar:

```bash
mkdir lab04-mastra && cd lab04-mastra
npm init -y && node -e "require('fs').writeFileSync('package.json', JSON.stringify({...require('./package.json'), type:'module'}, null, 2))"
npm install @mastra/core@latest zod@latest
export OPENAI_API_KEY=... # ou ANTHROPIC_API_KEY / provedor do modelo escolhido
```

## Código

**`tools.mjs`** — duas tools do domínio (preço e resumo):

```js
import { createTool } from '@mastra/core/tools'
import { z } from 'zod'

const BANCO = {
 'A-100': { titulo: 'Fone bluetooth', preco: 199.9, rating: 4.5 },
 'B-200': { titulo: 'Teclado mecanico', preco: 349.0, rating: 4.2 },
}

export const buscarProduto = createTool({
 id: 'buscar-produto',
 description: 'Busca um produto pelo codigo sku. Use quando o usuario pedir preco, titulo ou ficha de um produto conhecido.',
 inputSchema: z.object({ sku: z.string().describe('Codigo sku, ex: A-100') }),
 execute: async ({ sku }) => BANCO[sku] ?? { erro: 'sku nao encontrado', sku },
})

export const resumirCatalogo = createTool({
 id: 'resumir-catalogo',
 description: 'Devolve contagem e ticket medio do catalogo. Use para perguntas agregadas sobre todos os produtos.',
 inputSchema: z.object({}),
 execute: async () => {
 const itens = Object.values(BANCO)
 return { total: itens.length, ticket_medio: itens.reduce((s, p) => s + p.preco, 0) / itens.length }
 },
})
```

**`agente.mjs`** — agente + registro:

```js
import { Agent } from '@mastra/core/agent'
import { buscarProduto, resumirCatalogo } from './tools.mjs'

export const agente = new Agent({
 id: 'lab04',
 name: 'Agente de precos',
 instructions: `Voce responde sobre produtos do catalogo.
Regras: sempre cite o sku; se o sku nao existir, diga que nao encontrou — nao invente preco.`,
 model: 'openai/gpt-5-mini', // string provider/model; troque conforme o provedor
 tools: { buscarProduto, resumirCatalogo },
})
```

**`teste-negativo.mjs`** — a prova do schema (roda **sem** chave de API):

```js
import { buscarProduto } from './tools.mjs'

// 1. Fronteira do schema: payload invalido mora aqui.
try {
 buscarProduto.inputSchema.parse({ sku: 123 }) // esperado: number, recebi...?
 console.log('FALHA: schema deixou passar')
} catch (e) {
 console.log('OK: ZodError antes do execute ->', e.issues[0].path, e.issues[0].message)
}

// 2. Tool silenciosa: objeto fora do padrao nao levanta erro — some depois.
const toolQuebrada = { id: 'x', description: 'y', execute: async () => 1 }
console.log('tool quebrada aceita sem reclamar:', typeof toolQuebrada.execute === 'function')
```

## Como rodar

```bash
node teste-negativo.mjs # sem custo: prova o contrato do schema
node -e "import('./agente.mjs').then(async ({agente}) => {
 console.log((await agente.generate('Quanto custa o A-100?')).text);
 console.log((await agente.generate('Qual a previsão do tempo?')).text);
})"
# com a chave: npm install mastra@latest && npx mastra dev → Studio (trace por passo)
```

**Roteiro de observação (3 perguntas):**

| Pergunta | Esperado |
| --- | --- |
| "Quanto custa o A-100?" | chama `buscar-produto`, cita preço real da tool |
| "Qual o ticket médio do catálogo?" | chama `resumir-catalogo` |
| "Qual a previsão do tempo?" | **nenhuma** tool; recusa por falta de escopo |

## O que observei

- `inputSchema.parse({ sku: 123 })` → ZodError apontando `path: ['sku']` — o
 `execute` **não rodou** (nada impresso pelo efeito colateral).
- A instrução "não invente preço" + tool errando `sku nao encontrado` → resposta
 honesta — a recusa vem da **ferramenta**, não da boa-vontade do modelo.
- Rota de trace no Studio: escolha da tool → argumentos → resultado → texto —
 o "por que errou" vira passo inspecionável.

## Análise

- **Schema é o muro da alucinação**: ver [[Alucinação]] — sem schema o modelo
 preenche o que parece; com schema, o domínio é fechado na fronteira.
- **`description` da tool = prompt da ferramenta** — mesma disciplina da
 `description` de skill ([[Agent Skills]]): o que faz **e quando usar**; a
 rotação 3 da tabela é o teste disso.
- **`instructions` é spec de comportamento** — escrito e versionado como tal
 ([[Spec-Driven Development]]).
- **Conexão com o orquestrador**: estas tools são exatamente o que o [[N8N]]
 chamaria no caminho "decidir" do fluxo do projeto.

## Extensão (o que eu faria com mais tempo)

- Idempotência: `execute` que grava deve ser seguro para repetir (retry do
 modelo) — adicionar chave de idempotência ao `buscar-produto` com efeito
 colateral real.
- Teste negativo no CI (o `teste-negativo.mjs` como suíte).
- Camada de avaliação: 10 perguntas com respostas esperadas × ferramenta
 escolhida — a suíte mínima de um agente.

## Conceitos tocados


## Erros que cometi

- Definir tool como **objeto simples** e não entender por que o agente nunca a
 chamava — o silêncio é literalmente documentado: *"silently fail"*.
- Escrever `model: openai('gpt-...')` (formato antigo de SDK) — no Mastra atual
 é **string** `provider/model`; o erro aparece na hora, mas custa um loop.
- Colocar o preço "de mentira" no `instructions` para o teste funcionar — aí o
 lab prova minha mentira, não a ferramenta.

---
*Lab criado em 2026-10-08*
