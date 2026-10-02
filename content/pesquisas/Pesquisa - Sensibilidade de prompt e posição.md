---
title: "Pesquisa - Sensibilidade de prompt e posição"
tags:
  - "pesquisa"
  - "prompt"
tipo: "pesquisa"
date: "2026-10-07"
---

# Pesquisa — Sensibilidade de prompt e posição

> **Pergunta que motivou esta pesquisa:** como estruturar um prompt de RAG para que o modelo **use** a evidência que recuperamos, e por que a posição importa tanto?

## Resposta curta (TL;DR)

O prompt é processado com vieses posicionais reproduzíveis: **primacy** (início) e **recency** (fim). O resultado é uma curva em U — pior no meio, e em alguns casos **pior que não ter documento nenhum**. A engenharia disso é mecânica: instrução no topo, delimitadores separando instrução de dado, evidência mais relevante nas pontas, nunca no meio. E tudo isso precisa ser **medido**: o que funciona é específico do modelo e do tamanho do contexto.

## Resposta completa

### Lost in the middle (Liu et al., TACL 2024)

O experimento: variar a posição da informação relevante dentro de contextos longos e medir a acurácia. Resultado em U.

**Primacy bias** — início mais respeitado.
**Recency bias** — fim mais respeitado, por estar mais próximo da posição onde a geração começa.

O achado mais importante para projeto:

> **Com a informação no meio, o desempenho pode ficar abaixo do desempenho sem documento nenhum.**

Contexto retrieved não é neutro. Contexto mal posicionado é ativamente prejudicial, e você paga tokens por isso.

### Ordem dos exemplos (Minaee et al., ACL 2021)

**Fantastically Ordered Prompts and Where to Find Them** mostra que a sensibilidade à ordem dos exemplos em in-context learning é **fundamental** e persiste independentemente do número de exemplos.

Implicação: em few-shot, **a ordem dos exemplos é uma variável experimental a controlar**, não detalhe de formatação. Dois prompts idênticos com exemplos reordenados podem diferir bastante.

### Hierarquia de prompts

| Camada | OpenAI | Anthropic |
| --- | --- | --- |
| Instrução de sistema | `system` / `developer` | campo `system` (parâmetro de topo — **não** é mensagem) |
| Tarefa | `user` | `user` |
| Histórico do assistente | `assistant` | `assistant` |
| Resultado de ferramenta | `tool` | `tool_result` (bloco de conteúdo) |

**Wallace et al. (2024)**, *The Instruction Hierarchy*, formaliza: o modelo deve **deferir a instruções privilegiadas** sobre as de menor privilégio. O Model Spec da OpenAI explicita a mesma precedência.

### Delimitadores

Problema: o modelo não sabe se um texto é **instrução** ou **dado**. Solução: delimitar.

```
<instructions>
Responda apenas com base em <context>. Se não houver resposta no contexto, diga exatamente "não consta".
</instructions>

<context>
{{ trecho recuperado }}
</context>

<pergunta>
{{ pergunta }}
</pergunta>
```

Três benefícios: separa instrução de dado; dá âncoras estruturais (interage com ICL); torna a origem de cada trecho auditável.

### Prompt injection

**Perez & Ribeiro (2022)** formalizam o ataque (*Ignore Previous Prompt*).

O erro mais caro é acreditar que um aviso em linguagem natural resolve:

> "IMPORTANTE: siga as instruções do sistema" — não resolve. É mais um pedaço de texto competindo com o do atacante.

Defesas que funcionam: hierarquia de privilégio; entrada externa **marcada como dado**; saída validada antes de executar; privilégio mínimo. Postura: defesa em profundidade.

### Avaliação de prompt

Um prompt só é "melhor" se **medido**. Mínimo necessário:

1. conjunto de avaliação versionado, com gabarito;
2. A/B entre variantes, seed fixa, `system_fingerprint` registrado;
3. métrica definida **antes** do teste;
4. custo e latência medidos junto da qualidade.

> Princípio prático: **otimizar o prompt primeiro.** É ordens de magnitude mais barato por token de qualidade do que trocar de modelo.

## Detalhes técnicos

Template de prompt de RAG seguindo tudo acima:

```text
<system>
Você é um assistente que responde APENAS com base no contexto fornecido.
Se a resposta não estiver no contexto, responda exatamente: "Não consta no contexto".
Cite o identificador do trecho usado, entre colchetes, como [doc-3].
Não use conhecimento externo. Não faça suposições.
</system>

<context>
[doc-7] {chunk mais relevante}      <-- ponta superior
[doc-2] {segundo chunk}
...
[doc-5] {último chunk}
</context>

<pergunta>
{pergunta do usuário}
</pergunta>
```

Checklist de revisão de prompt:

- [ ] Instrução de sistema define papel, escopo, formato e comportamento sem evidência?
- [ ] Entradas externas delimitadas e marcadas como dado?
- [ ] Evidência mais relevante na ponta (início ou fim), não no meio?
- [ ] Existe regra explícita para "não consta"?
- [ ] A saída é validada antes de virar ação?
- [ ] Existe conjunto de avaliação versionado medindo a mudança?

## Comparações

| Aspecto | Estrutura explicitada | Prompt "simples e amigável" |
| --- | --- | --- |
| Separar dado de instrução | ✅ tags | ❌ mistura |
| Auditabilidade da fonte | ✅ identificadores | ❌ |
| Resistência a injeção | ✅ hierarquia + validação | ❌ só texto |
| Manutenção | ✅ campos nomeados | ❌ spaghetti |

## Limitações e riscos

- **Isso é propriedade do modelo.** A curva muda entre modelos e entre tamanhos de contexto. Meça.
- **Tags XML não são segurança.** São organização. A segurança vem da hierarquia e da validação de saída.
- **Over-delineação custa tokens.** Delimitadores repetidos em chunks pequenos inflam o custo. Equilibre.

## O que isso muda na minha prática

- [x] Evidência mais relevante nas pontas do contexto.
- [x] Sempre definir comportamento para "sem evidência".
- [ ] Versionar prompts no git e medir antes/depois de cada mudança.
- [ ] Tratar entrada externa como dado, com validação de saída.

## Fontes

1. **Lost in the Middle: How Language Models Use Long Contexts** — Liu et al., TACL 2024. https://aclanthology.org/2024.tacl-1.9/ — preprint: https://arxiv.org/abs/2307.03172
2. **Fantastically Ordered Prompts and Where to Find Them** — Minaee et al., ACL 2021. https://aclanthology.org/2021.acl-long.428/ — preprint: https://arxiv.org/abs/2104.08786
3. **Ignore Previous Prompt: Attack Techniques for Language Models** — Perez & Ribeiro, 2022. https://arxiv.org/abs/2211.09527
4. **The Instruction Hierarchy** — Wallace et al., OpenAI, 2024. https://arxiv.org/abs/2404.13208
5. **Use XML tags to structure your prompts** — Anthropic Docs. https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/use-xml-tags
6. **Prompt injection** — Simon Willison, 2022. https://simonwillison.net/2022/Sep/12/prompt-injection/
7. **Model Spec** — https://model-spec.openai.com/

## Perguntas abertas

- [ ] A curva em U se reproduz no modelo que eu uso? Testar.
- [ ] Qual a posição ótima no meu sistema: início ou fim?

## Ver também

-[[Janela de Contexto]] · [[Lost in the Middle]] · [[RAG]] · [[Prompt Injection]]

---
*Atualizado em 2026-09-30*
