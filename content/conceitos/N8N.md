---
title: "N8N"
tags:
  - "conceito"
  - "n8n"
  - "automacao"
tipo: "conceito"
date: "2026-10-15"
---


# N8N

> **Meta:** descrever o que é o N8N (automação de workflows em grafo, self-hosted) e
> explicar o papel de *nó*, *gatilho* e *tratamento de erro* num fluxo de busca e
> inserção de produtos.

## O que é

Plataforma de **automação de workflows** onde você desenha um **grafo de nós** num
editor visual: cada nó faz uma coisa (HTTP, transformação, condição, chamada de IA) e
os nós se conectam passando dados adiante. É open-core — roda **na sua máquina
(self-hosted)** ou em nuvem — e combina bem com LLMs porque trouxe nós de IA nativos
(agentes, RAG, chamadas de modelo).

Neste projeto, o N8N é o **motor de automação** da plataforma de avaliação de
produtos: busca produtos (ex.: Amazon), insere no sistema e conversa com o agente
customizado feito em [[Mastra]].

## Anatomia de um workflow

| Conceito | O que é | Exemplo no projeto |
| --- | --- | --- |
| **Gatilho (trigger)** | o que inicia o fluxo | cron, webhook, evento manual |
| **Nó (node)** | uma etapa atômica | requisição HTTP, filtro, merge |
| **Payload** | o dado passando pelos nós | JSON do produto encontrado |
| **Expressões** | lógica nos conexões | `{{ $json.preco }}` |
| **Erro** | caminho de falha | retry, nó de tratamento, parada |

## Ideias-chave

- **Workflow = contrato de dados.** Cada nó **entra com um shape e sai com outro** —
 a maior parte dos bugs de N8N é shape inesperado, não lógica. Inspecionar a saída de
 cada nó é o primeiro instinto.
- **Tratamento de erro é nó, não afterthought.** Retry com backoff, caminho `on error`,
 alerta — automação sem caminho de falha falha em silêncio, que é o pior modo.
- **Integrações reais têm atrito real.** No projeto, a Amazon bloqueava requisição
 automatizada (anti-bot/CAPTCHA) e a solução foi um serviço de scraper intermediário —
 lição: **todo caminho de dados externos assume falha e bloqueio**, e prever
 isso é parte do desenho (ver [[Spec-Driven Development]] — o "fora de escopo" e os
 riscos vão na spec).
- **Rate limit e custo:** cada chamada de nó de IA consome tokens ([[Token]]) —
 cachear e filtrar *antes* do nó de modelo é a diferença entre barato e caro.
- **N8N orquestra, o agente decide.** Fluxos determinísticos (buscar → filtrar →
 gravar) ficam no N8N; raciocínio e linguagem ficam no agente [[Mastra]] — separar os
 dois deixa o sistema testável.
- **Self-hosted = sua responsabilidade.** Rodar local traz custo zero e controle;
 também traz atualização, backup e segurança do servidor de execução.

## Na prática — o fluxo do projeto

```text
[cron: a cada X]
 → nó HTTP: busca produto (com proxy anti-bot)
 → nó IF: produto novo?
 → nó IA: gera descrição/resumo (chamada de modelo)
 → nó DB: insere produto
 → erro? → retry → webhook de alerta
```

## Autoavaliação
- [ ] Definir N8N e diferenciar *workflow* de *agente* numa frase cada.
- [ ] Nomear as 4 peças de um workflow (gatilho, nó, payload, erro) com um exemplo do projeto.
- [ ] Explicar por que tratamento de erro deve ser desenhado como nó.
- [ ] Justificar por que a bloqueio anti-bot da Amazon era previsível na spec.
- [ ] Dizer o que cabe no N8N e o que cabe no agente — e o critério da separação.

## Ver também

- [[Mastra]] · [[Spec-Driven Development]] · [[Desenvolvimento de Software com IA]]
- [[Token]] · [[Prompt Engineering - fundamentos]]
