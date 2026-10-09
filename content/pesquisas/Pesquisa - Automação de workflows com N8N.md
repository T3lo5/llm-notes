---
title: "Pesquisa - Automação de workflows com N8N"
tags:
  - "pesquisa"
  - "n8n"
  - "automacao"
tipo: "pesquisa"
date: "2026-10-15"
---

# Pesquisa — Automação de workflows com N8N

> **Pergunta que motivou esta pesquisa:** o que um orquestrador visual resolve
> que código puro não resolve — e onde ele começa a atrapalhar?

## Resposta curta (TL;DR)

O n8n resolve **integração e operação**: dezenas de sistemas conectados, gatilho
agendado/webhook, retentativa, histórico de execuções — tudo sem manter código de
conexão. Ele é uma ferramenta **fair-code** (src-available, licença própria:
self-host grátis, nuvem paga) que combina automação de processos com features de
IA. O modelo mental é o **grafo de nós**: cada nó transforma um item, as
conexões passam dados com **expressões** (`{{ $json.campo }}`), e a execução
guarda o payload de cada nó para inspeção. Onde atrapalha: lógica de negócio
complexa vira JavaScript escondido dentro de nós de código — a partir daí o
"fluxo visual" é mentira e o código real não tem testes.

## Resposta completa

### O modelo de execução

Da documentação oficial (docs.n8n.io), quatro conceitos estruturais:

1. **Workflow = grafo dirigido.** Nós (integração, lógica, código, IA) ligados
   por conexões; execução percorre o grafo com os dados transformados a cada
   passo.
2. **Dados são itens.** Cada nó recebe *items* (não um objeto único) e pode
   processá-los um a um — é o **item-based processing**. Um milhão de linhas é
   um milhão de itens, e um erro de shape afeta item a item, não tudo.
3. **Expressões.** A ligação entre nós é escrita em `{{ }}` sobre o JSON de saída
   do nó anterior (`{{ $json.preco }}`, `$('Nome do nó').item.json`) — a
   "transformação de dados" vive nas conexões, não nos nós.
4. **Execuções persistentes.** Toda execução roda e fica registrada (dados de
   entrada, saída, tempo, erro de cada nó) — o **Execution Inspector** é o
   debugger. Rodou uma vez fora do esperado? Reabra a execução e veja o payload
   real de cada nó.

### Gatilhos e tratamento de erro

- **Gatilhos**: cron, webhook, manual, evento de sistema — o gatilho define o
  *quando*; o grafo define o *o quê*.
- **Erro é caminho, não exceção**: error workflow (workflow dedicado que capta
  falhas de outros), retry com backoff por nó, continuação com item de erro.
  A documentação trata de "understand executions" como conceito-chave — porque
  **sem caminho de erro o workflow falha em silêncio**, que é o pior modo.
- **AI features**: o n8n trouxe nós de IA (agentes, RAG, chamadas de modelo) e
  **servidor MCP** — a própria documentação mostra integração com Claude
  Desktop, Claude Code e Codex CLI via MCP. O orquestrador conversa com
  agente nos dois sentidos.

### Fair-code: o que "grátis" significa aqui

Licença Sustainable Use (fair-code): **self-host é gratuito** (Docker oficial:
`docker.n8n.io/n8nio/n8n`), uso comercial permitido, revenda do concorrente não.
A nuvem (n8n cloud) é paga. Self-host traz: custo zero, dados na sua máquina,
e **responsabilidade** de atualização, backup e exposição do servidor de
execução (é uma interface de automação com permissão de chamar suas APIs —
regra de ouro: expor só com autenticação).

### Onde o n8n encaixa vs código puro

| Cenário | n8n vence | Código puro vence |
| --- | --- | --- |
| N integrações × N eventos | ✔ conexões prontas, retentativa | |
| Lógica de negócio densa | | ✔ testável, refatorável |
| Operação 24h sem dev on-call | ✔ execução agendada + histórico | |
| Time não-dev precisa editar fluxo | ✔ visual | |

No projeto guiado, a divisão ficou: **n8n orquestra (determinístico: buscar →
filtrar → gravar), o agente decide (raciocínio e linguagem)** — ver [[Mastra]] e
[[N8N]].

## Detalhes técnicos

- **Expressions**: `$json` (nó atual), `$('Nó anterior')` (acesso histórico),
  `$now`, `$if`, funções JS comuns — a expressão é avaliada por item.
- **Code node**: JavaScript/Python dentro do fluxo, com `pairedItem` para
  manter o rastro do item de origem — é a válvula de escape **e** a armadilha
  (vira monólito escondido).
- **Webhooks**: endpoint por workflow; o payload chega como item — base do
  padrão "evento externo → fluxo".
- **Versionamento/ambientes**: workflows exportam como JSON (o formato do
  [[Lab 03 - Workflow N8N mínimo]]) — JSON no git é o equivalente da spec
  versionada ([[Spec-Driven Development]]).

## Limitações e riscos

- **Lógica complexa em nó de código** = código sem CI, sem review, escondido em
  tela. Regra: se o nó de código passa de ~30 linhas, é módulo no repositório.
- **Debug visual engana**: o grafo mostra o desenho, não o dado — só o inspector
  mostra o que trafegou de fato.
- **Vendor lock de ecossystem**: nós de terceiros desatualizam; API do alvo muda
  e o nó quebrado falha em agendamento (silêncio de novo).
- **Segredos vivem no fluxo**: credenciais configuradas no n8n são patrimônio do
  servidor — exportar o JSON exporta referências, não segredos; manter
  separado (ver [[Ambiente de Desenvolvimento com IA]]).
- **Escala**: execução longa com muitos itens consome memória do container
  self-hosted — rate limit do alvo é o teto real.

## O que isso muda na minha prática

1. **Contrato de shape por inspeção**: antes de confiar no fluxo, abrir o
   Execution Inspector e ler a saída de cada nó (o hábito do
   [[Lab 03 - Workflow N8N mínimo]]).
2. **Caminho de erro desenhado junto** — nó de erro/URL de alerta desde o
   primeiro dia, não depois do primeiro apagão.
3. **Fronteira n8n × agente escrita na spec**: o que é determinístico fica no
   grafo; o que exige julgamento vai para o agente.
4. **JSON do workflow no git** — fluxo é artefato versionado.

## Fontes

- https://docs.n8n.io/ — documentação oficial (welcome, build, flow logic).
- https://docs.n8n.io/build/flow-logic.md — fluxo, condições, loops.
- https://docs.n8n.io/build/understand-workflows/understand-executions.md —
  modelo de execução e inspeção.

## Perguntas abertas

- Quando migrar um workflow do n8n para serviço no repositório — qual o sintoma
  exato de fronteira?
- n8n vs alternativas (Make, Zapier, Temporal) quando o requisito é
  **auditoria** — o que a inspeção de execução do n8n cobre e o que não cobre?
- Automação + agente: quem é dono do estado quando o agente chama o workflow e
  o workflow chama o agente?

## Ver também

- [[N8N]] · [[Mastra]] · [[Spec-Driven Development]]
- [[Desenvolvimento de Software com IA]] · [[Ambiente de Desenvolvimento com IA]]
- [[Lab 03 - Workflow N8N mínimo]]
