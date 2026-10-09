---
title: "Engenharia de prompt e contexto"
tags:
  - "prompt"
tipo: "guia"
date: "2026-10-01"
---

# Engenharia de prompt e contexto

> **Meta:** explicar por que a posição e a clareza da informação no prompt mudam a qualidade da resposta, e como encontrar o equilíbrio entre um bom prompt e o custo dos tokens.

## Resumo em 3 frases

1. O prompt não é um texto neutro: é um documento processado com **vieses posicionais reproduzíveis**. O efeito mais replicado é o *lost in the middle* — a acurácia traça uma curva em U, pior no meio.
2. No meio do contexto, o desempenho pode ficar **abaixo** do desempenho sem contexto nenhum. Contexto demais é pior que contexto nenhum.
3. Além da ordem, importam a **clareza** e o **detalhamento** — e existe um ponto de equilíbrio entre prompt bom e **custo de tokens**, porque detailing demais também degrada.
4. A engenharia disso é: instrução no topo, delimitadores explícitos separando instrução de dado, evidência relevante nas pontas, e **medição** — porque o que funciona é específico do modelo e do tamanho do contexto.

## O segundo eixo: clareza, detalhamento e custo

A ordem importa. A **clareza** também. E as duas competem com o **custo**.

| Prompt | Efeito | Custo |
| --- | --- | --- |
| Vago ("analise o documento") | resposta genérica, inútil | barato |
| Claro e mínimo ("liste 3 riscos, em tabela") | resposta precisa | baixo |
| Claro e detalhado | melhor cobertura, menos ambiguidade | **maior** |
| Detalhado e redundante | **pior** — dilui, confunde, e o modelo atende ao último pedido | maior |

> O erro comum é tratar "melhor prompt" como "mais prompt". Adicionar detalhe é útil **até certo ponto**; a partir dele, cada token a mais aumenta custo **e** confunde o modelo.

### A conta

Todo token de entrada é cobrado. Com janela de contexto grande, o prompt repetido em milhares de chamadas domina o custo — ver [[Tokens: o significado dos números]].

```
custo por chamada ≈ tokens de entrada × preço de entrada + tokens de saída × preço de saída
```

### Como achar o ponto certo

1. Comece no **mínimo que resolve**.
2. Adicione detalhe **medindo** — held-out, não impressão (ver [[Lab 04 - Temperatura, top-p e reprodutibilidade]]).
3. Corte o que não muda a métrica.
4. Se a resposta erra por falta de informação: **RAG** antes de inflar o prompt (ver [[RAG]]).

> O equilíbrio não é um princípio, é uma **medição**. O ponto ótimo depende do modelo, da tarefa e do volume.

## O achado central: lost in the middle

Liu et al. (*Lost in the Middle: How Language Models Use Long Contexts*, TACL 2024) vara a posição da informação relevante dentro de contextos longos e mede a acurácia. O resultado é uma **curva em U**:

```
desempenho
   │  ╱‾‾‾╲                    ╱‾‾‾
   │ ╱     ╲                  ╱
   │╱       ╲________________╱
   └──────────────────────────────────► posição da informação
     início                        fim
   (primacy)                     (recency)
```

- **Primacy bias** — o início do contexto é mais respeitado.
- **Recency bias** — o fim é mais respeitado, por estar mais próximo da posição onde a geração começa.

O detalhe grave: **com a informação no meio, o desempenho com documentos pode ficar abaixo do desempenho sem documento nenhum** (closed-book). Ou seja, Retrieved contexto errado não é neutro — é ativamente prejudicial.

**Implicação direta de engenharia:** em RAG, coloque o chunk mais relevante **no início ou no fim**, e não o enterre no meio de uma lista de 20. Se você só recupera um trecho, coloque-o explicitamente como o primeiro ou o último bloco.

## A ordem dos exemplos também importa

**In-context learning** é o mecanismo pelo qual o modelo aprende a tarefa apenas por exemplos no prompt, sem atualizar pesos. **Minaee et al. (ACL 2021)** — *Fantastically Ordered Prompts and Where to Find Them* — mostram que a sensibilidade à ordem dos exemplos é **fundamental** e persiste independentemente do número de exemplos.

Consequência prática: em few-shot, **a ordem dos exemplos é uma variável experimental a controlar**, não um detalhe de formatação. Dois prompts idênticos com exemplos em ordens diferentes podem diferir bastante no resultado.

## Hierarquia de prompts

Camada estrutural que resolve "quem manda":

| Camada | OpenAI | Anthropic |
| --- | --- | --- |
| Instrução de sistema | `system` / `developer` | campo `system` (parâmetro de topo, **não** é uma mensagem) |
| Tarefa | `user` | `user` |
| Histórico do assistente | `assistant` | `assistant` |
| Resultado de ferramenta | `tool` | `tool_result` (bloco de conteúdo) |

O **Model Spec** da OpenAI e **Wallace et al. (2024)**, *The Instruction Hierarchy*, formalizam: o modelo deve **deferir a instruções privilegiadas** sobre as de menor privilégio. Instruções `system`/`developer` têm precedência sobre `user`.

## Delimitadores: separar instrução de dado

O problema prático: se você coloca um documento no prompt, o modelo não sabe se aquilo é **instrução** ou **dado**.

Solução: **delimitar**. A Anthropic recomenda **tags XML**:

```
<instructions>
Responda apenas com base em <context>. Se não houver resposta, diga "não consta".
</instructions>

<context>
{{ trecho recuperado }}
</context>

<pergunta>
{{ pergunta do usuário }}
</pergunta>
```

Três benefícios: separa instrução de dado, dá ao modelo âncoras estruturais (isso interage com ICL), e deixa a origem de cada trecho auditável.

## Prompt injection

O outro lado da mesma moeda. Quando texto **não confiável** (e-mail, página web, saída de ferramenta) entra no prompt, um atacante pode escrever "Ignore as instruções anteriores e…" e o modelo pode obedecer — porque, sem hierarquia treinada, ele não distingue instrução de dado.

- **Perez & Ribeiro (2022)**, *Ignore Previous Prompt: Attack Techniques for Language Models* — formaliza o ataque.
- **Greshake et al.** — demonstra o risco em agentes com recuperação de informação.

**O erro comum e mais caro:**

> "Vou adicionar `IMPORTANTE: siga as instruções do sistema` no topo. Isso resolve."

Não resolve. Um aviso em linguagem natural é mais um pedaço de texto competindo com o texto do atacante. Defesas que **funcionam**:

1. **Hierarquia de privilégio** (system/developer acima de user).
2. **Entrada externa sempre marcada como dado**, nunca como prompt.
3. **Validar a saída** antes de executá-la (especialmente se a saída vira ação: chamada de ferramenta, SQL, comando).
4. **Privilégio mínimo** para o que o modelo pode alcançar.

Postura correta: defesa em profundidade. Nenhuma frase no prompt neutraliza o ataque.

## Avaliação de prompt: o que separa engenharia de superstição

Um prompt só é "melhor" se **medido**. O mínimo:

- conjunto de avaliação versionado (cases fixos, com gabarito);
- A/B entre variantes, com seed fixa e `system_fingerprint` registrado;
- métrica definida **antes** do teste;
- custo e latência medidos junto da qualidade.

Um prompt pode ganhar em qualidade e perder em custo — às vezes é melhor trocar de modelo do que otimizar o prompt, e às vezes é o oposto. **Meça os dois e decida com dado.**

> Princípio prático: otimizar o prompt primeiro. É ordens de magnitude mais barato por token de qualidade do que trocar de modelo.

## Receita de prompt para RAG (aplicável hoje)

1. System prompt: papel + regra de escopo + formato de saída + como agir sem evidência.
2. Instrução curta e explícita.
3. **Evidência mais relevante no início OU no fim** — nunca no meio.
4. Demais evidências, ordenadas por relevância decrescente.
5. Pergunta do usuário **logo antes** do ponto de geração.
6. Delimitadores (`<document>`, `<instructions>`).
7. Pedido de citação da passagem usada — dá um sinal verificável e permite checagem.

## Perguntas para validar

1. Por que "contexto demais" pode ser pior do que "sem contexto"? Isso contraria a intuição de que mais informação ajuda.
2. Um prompt com 20 passagens recuperadas e a pergunta no final: como você reestruturaria? Justifique com primacy, recency e lost in the middle.
3. Por que o system prompt da Anthropic é um parâmetro de topo e não uma mensagem?
4. Qual a diferença estrutural entre "responda em JSON" e structured output?
5. Se um prompt novo melhorou em 8 de 10 casos de teste, o que você precisa checar antes de colocar em produção?

## Referências

- Liu et al., *Lost in the Middle* (TACL 2024) — https://aclanthology.org/2024.tacl-1.9/ · preprint: https://arxiv.org/abs/2307.03172
- Minaee et al., *Fantastically Ordered Prompts* (ACL 2021) — https://aclanthology.org/2021.acl-long.428/
- Perez & Ribeiro, *Ignore Previous Prompt* — https://arxiv.org/abs/2211.09527
- Wallace et al., *The Instruction Hierarchy* (OpenAI, 2024) — https://arxiv.org/abs/2404.13208
- Anthropic Docs, *Use XML tags to structure your prompts* — https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/use-xml-tags
- Willison, *Prompt injection* — https://simonwillison.net/2022/Sep/12/prompt-injection/
- OpenAI Model Spec — https://model-spec.openai.com/

## Ver também

- [[Pesquisa - Sensibilidade de prompt e posição]] · [[Nota Técnica - Geração token a token]] · [[Lost in the Middle]]
