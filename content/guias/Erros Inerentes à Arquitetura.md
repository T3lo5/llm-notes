---
title: "Erros Inerentes à Arquitetura"
tags:
  - "riscos"
  - "arquitetura"
  - "falhas"
tipo: "guia"
date: "2026-10-29"
---

# Erros Inerentes à Arquitetura

> **Meta:** separar o que é **erro de implementação** do que é **limitação de
> arquitetura**: a IA erra porque estima probabilidade (não "pensa"), porque o contexto é
> finito e porque a linguagem é ambígua. Essas falhas não se eliminam — se contornam.


## Resumo em 3 frases

1. A IA **estima a probabilidade do próximo token**; não existe um "eu" pensando antes de
   responder, nem verificação interna de verdade.
2. As três causas estruturais são: **natureza probabilística**, **limitações de contexto**
   e **ambiguidade da linguagem** — no recorte, **ambiguidade do pedido** — e cada
   uma produz um tipo de falha.
3. Essas falhas **não são exceções**: são comportamento natural da tecnologia; por isso a
   mitigação é **arquitetura em volta** (fonte, validação, contexto e clareza), não "pedir
   ao modelo para não errar".

## O que a seção aborda (escopo declarado)

- Os **quatro tipos principais de falha**: alucinação, inconsistência, ambiguidade e
  perda de contexto.
- Como a **natureza probabilística** da IA influencia o funcionamento e produz respostas
  imprecisas ou erradas.
- Como a **formulação do input** impacta significativamente o resultado.
- Por que essas falhas **não são exceções, mas comportamentos naturais** da tecnologia.
- Que a **mitigação** é o que permite uso eficaz e seguro em aplicações práticas.

## Objetivos

- [ ] Identificar os tipos de falhas em IA
- [ ] Compreender a natureza probabilística da IA
- [ ] Analisar a influência do contexto nas respostas
- [ ] Mapear a ambiguidade na formulação de perguntas
- [ ] Aprender a mitigar riscos associados a falhas de IA

## As três causas estruturais

| Causa (bullet) | O que significa | Falha que produz |
| --- | --- | --- |
| **Estima probabilidade — não tem pensamento em si** | o modelo calcula a continuação mais provável, não "decide" nem "acredita" em nada; plausível ≠ verdadeiro | [[Alucinação]] · [[Inconsistência]] |
| **Limitações de contexto** | a janela é finita e a informação no meio de um contexto longo perde força | [[Perda de Contexto]] |
| **Ambiguidade da linguagem** | no recorte, **ambiguidade do pedido**: a formulação do input admite mais de uma leitura e não determina qual resposta é correta | [[Ambiguidade]] |

> As causas se combinam: um pedido ambíguo pode gerar respostas diferentes entre
> execuções (inconsistência) e um contexto mal montado pode esconder a fonte que evitaria
> a alucinação. Separar a causa ajuda a escolher o controle — não a culpar o modelo.

## "Não tem pensamento em si" — o que isso quer dizer

- Não há **intenção**, **crença** ou **verificação interna**: existe cálculo de
  probabilidade sobre tokens. O modelo não sabe se o que escreveu é verdade; ele sabe o
  que é provável (ver [[Modelos de Linguagem: como funcionam]] e [[O que é um LLM]]).
- **Fluência não é raciocínio.** O texto pode parecer uma cadeia de pensamento e ainda
  assim ser só continuação plausível — inclusive quando "explica" um erro.
- **Não existe sinal de dúvida confiável.** Pedir "só responda se tiver certeza" não cria
  calibração: cria texto mais cauteloso, não mais verdadeiro.
- Consequência de projeto: a verificação tem de ser **externa** — documento real, schema,
  ferramenta, humano, [[Evals]].

## Quatro falhas × causa estrutural

| Falha | Causa principal | Por que é estrutural |
| --- | --- | --- |
| **Alucinação** | probabilidade | o objetivo premia plausibilidade; não há acesso à verdade |
| **Inconsistência** | amostragem + ausência de estado | a mesma entrada pode seguir caminhos diferentes ([[Temperatura]]) |
| **Ambiguidade** | formulação do pedido | o input não determina uma única resposta correta |
| **Perda de contexto** | janela + atenção | o que está longe ou no meio do contexto perde influência |

## Por que "resolver no prompt" não resolve

| Tentativa | Por que falha | O que realmente resolve |
| --- | --- | --- |
| "Não invente" | instrução não cria fonte de verdade | [[Grounding]] + validação em código |
| "Seja consistente" | não elimina a amostragem | temperatura 0 + critério fixo + cache/idempotência |
| "Leia tudo com atenção" | não muda a janela nem a atenção | reancorar, posicionar e resumir o contexto |
| "Seja claro" (para o modelo) | a ambiguidade está no **pedido** | contrato de resposta + exemplo + schema |

> O padrão: **prompt pede; arquitetura garante.** Cada linha da tabela é uma falha
> estrutural sendo tratada como se fosse instrução.

## Exemplo concreto (ilustrativo, meu)

**Cenário:** suporte técnico em que o cliente pergunta "consigo cancelar meu pedido?".

| Falha | O que aconteceria | Causa estrutural |
| --- | --- | --- |
| **Alucinação** | o agente cita o endpoint `/v2/orders/{id}/refund`, que não existe na API | probabilidade: o formato parece plausível |
| **Inconsistência** | o mesmo pedido recebe prazo de 5 dias hoje e 7 dias amanhã | amostragem/critério: não há estado fixo |
| **Ambiguidade** | "cancelar" é tratado como estorno, mas o pedido ainda não foi enviado | pedido: o input não definiu o caso |
| **Perda de contexto** | a regra "não prometer prazo" dita no início some depois de 20 mensagens | janela/atenção: a instrução deixou de influenciar |

## Estrutural × de projeto

| Estrutural (não muda com prompt) | De projeto (muda com engenharia) |
| --- | --- |
| estimar probabilidade em vez de verificar verdade | ancorar em fonte real ([[Grounding]]) |
| janela finita e atenção no meio | resumir, posicionar e reancorar contexto |
| linguagem natural ambígua | contrato de resposta + exemplo + clarificação |
| ausência de estado entre chamadas | estado explícito + cache/idempotência |

> É essa distinção que dá nome à seção: o erro **inerente** não é corrigido — é
> **previsto e contornado**. O que é de projeto é onde ainda há escolha.

## Mitigação (o que fazer com isso)

1. **Fonte antes de geração** — responder com documento real e citar o trecho; sem fonte,
   recusar ([[Grounding]]).
2. **Validação em código** — schema, ranges, regras de domínio e checagem de citações
   ([[Guardrails]], [[Evals]]).
3. **Arquitetura de contexto** — o crítico no começo/fim, resumo do histórico, estado
   explícito e recuperação sob demanda ([[Perda de Contexto]]).
4. **Contrato de pergunta** — objetivo, formato, exemplo e o que **não** fazer
   ([[Ambiguidade]]).
5. **Medição contínua** — casos reais versionados; sem [[Evals]], cada defesa é achismo.

## Erros comuns / armadilhas

- ❌ Tratar falha estrutural como **bug** e abrir issue de "corrigir o modelo".
- ❌ Achar que **modelo maior** elimina a limitação: reduz a taxa, não muda a natureza.
- ❌ Confundir **"não tem pensamento"** com "não serve para nada": serve — desde que a
  verificação não seja delegada a ele.
- ✅ Tratar falha como **taxa** e projetar camadas para o residual ([[Riscos e falhas em projetos de IA]]).

## Perguntas em aberto

- [x] **Resolvido:** "ambiguidade de linguagem" na seção é a ambiguidade **do pedido** —
      a formulação do input não determina a resposta correta. Não é a ambiguidade da
      linguagem natural em geral; a ficha [[Ambiguidade]] cobre as duas, mas o recorte é o input.
- [ ] "Não tem pensamento em si" inclui **raciocínio**? Cadeia de pensamento é geração de
      texto, não deliberação interna — confirmar o enquadramento.
- [ ] Qual é a fronteira entre **erro inerente** e **erro de implementação**? Um RAG mal
      configurado é falha de arquitetura do sistema, mas não do modelo.

## Referências


- Ver também: [[Alucinação e comportamentos]] · [[Riscos e falhas em projetos de IA]] · [[Modelos de Linguagem: como funcionam]] · [[O que é um LLM]] · [[Arquitetura Transformers e Attention]] · [[Temperatura e previsibilidade]]
- Fichas: [[Erro Inerente à Arquitetura]] · [[Alucinação]] · [[Inconsistência]] · [[Ambiguidade]] · [[Perda de Contexto]] · [[Janela de Contexto]] · [[Lost in the Middle]] · [[Temperatura]] · [[Grounding]] · [[Guardrails]] · [[Evals]]

