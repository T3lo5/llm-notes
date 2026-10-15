---
title: "Lab 01 - Anatomia de um prompt"
tags:
  - "lab"
  - "prompt"
tipo: "lab"
date: "2026-10-15"
---

# Lab 01 — Anatomia de um prompt: o que as 4 partes compram

> **O que este lab prova:** que estruturar um prompt (papel, tarefa, contexto,
> formato) muda a saída de forma verificável e que o custo extra em tokens é
> ínfimo perto do custo de consertar resposta errada.

## Pergunta

Quantos tokens a estrutura custa — e o que ela compra na resposta?

## Hipótese

> O prompt estruturado atinge o formato pedido em **pelo menos 2 de 3
> execuções**; o prompt vago, em **no máximo 1 de 3**. O custo do estruturado é
> **< 3×** o do vago — e como o vago custa ~20 tokens, o delta absoluto é de
> dezenas de tokens: irrelevante perto de uma rodada de correção manual.

## Setup

```bash
pip install tiktoken
```

A parte de contagem roda **local, sem chave de API**. A parte de resposta usa
qualquer chat (seu assinatura, tier grátis, ou o [[OpenCode]] com modelo
disponível).

## Código

```python
# lab01_anatomia_prompt.py — compara custo dos dois prompts.
import tiktoken

enc = tiktoken.get_encoding("cl100k_base")

VAGO = "melhore este texto"

ESTRUTURADO = """Você é redator técnico sênior de produtos de software.

Tarefa: reescreva o texto abaixo para um público de gestores de TI, sem jargão.

Contexto: o texto anuncia uma ferramenta que reduz retrabalho em revisões de
código. O leitor tem 30 segundos por e-mail.

Formato: exatamente 3 frases. A primeira diz o benefício num número. A segunda
elimina a objeção principal (falta de tempo). A terceira é o chamado para ação,
com verbo no início.

Texto:
---
{texto}
---"""

texto = ("nossa ferramenta usa ia para achar problemas no codigo antes do deploy, "
         "ela revisa o diff e comenta, e vc pode testar gratis por 14 dias")

for nome, prompt in [("vago", VAGO), ("estruturado", ESTRUTURADO.format(texto=texto))]:
    tokens = enc.encode(prompt)
    print(f"{nome:12s} {len(tokens):4d} tokens  |  {len(prompt):4d} chars")
```

## Como rodar

**Fase 1 — custo (local):**

```bash
python3 lab01_anatomia_prompt.py
```

**Fase 2 — resposta (3 execuções cada, mesma sessão limpa):**

1. Envie o prompt **vago** 3× (sessão nova a cada envio) → cole as saídas.
2. Envie o prompt **estruturado** 3× → cole as saídas.
3. Pontue cada saída na rubrica abaixo (0–4).

**Rubrica (0 = não cumpriu, 1 = parcial, 2 = cumpriu):**

| Critério | Como verificar |
| --- | --- |
| Contagem | São exatamente 3 frases? |
| Número na 1ª frase | há algarismo e ele é benefício? |
| Sem jargão | "diff", "deploy", "IA" aparecem? (proibido na tarefa) |
| CTA com verbo inicial | 3ª frase começa com verbo? |

## O que observei

| Prompt | tokens | acerto de formato (0–8) | variação entre as 3 saídas |
| --- | --- | --- | --- |
| vago | | | |
| estruturado | | | |

## Análise

- **Custo**: o estruturado custa ~N× mais tokens — multiplique pelo preço do
  token (ver [[Token]]): o delta é centavos por chamada. A pergunta honesta é
  quantas rodadas de "não era isso que eu queria" o vago provoca.
- **Variação**: mesmo *com* estrutura, a saída varia — a estrutura **reduz**
  a variação de *formato*, não a de conteúdo. Formato é o que dá
  deterministicidade barata (relaciona com [[Temperatura]]).
- **O que a estrutura faz de fato**: isola as 4 camadas para que o modelo não
  misture tarefa com contexto — se a saída falhou, dá para apontar **qual**
  parte faltou. No vago, a falha é anônima.

## Extensão (o que eu faria com mais tempo)

- Automatizar a fase 2 com chamada de API e rubrica automática (contagem de
  frases por `re.split`) — 30 execuções, estatística de acerto real.
- Testar a 5ª parte: **exemplo** (few-shot) para formato mais difícil que
  "3 frases".
- Medir o efeito de pedir o formato **no fim vs no começo** do prompt (posição
  — ver [[Pesquisa - Sensibilidade de prompt e posição]]).

## Conceitos tocados

- [[Engenharia de prompt e contexto]]

## Erros que cometi

- Contar **caracteres** e achar que eram tokens — por isso a rubrica imprime
  os dois números (confundir os dois é o erro 1 deste lab).
- Rodar as 3 execuções na **mesma conversa** e concluir que "não varia": o
  histórico já entregou o formato. Sessão limpa por envio, sempre.
- Enquadrar a hipótese como "resposta melhor" (subjetivo) em vez de "formato
  cumprido" (contável) — o lab só é conclusível com critério verificável.

---
*Lab criado em 2026-10-08*
