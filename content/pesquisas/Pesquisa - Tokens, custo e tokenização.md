---
title: "Pesquisa - Tokens, custo e tokenização"
tags:
  - "pesquisa"
  - "tokens"
tipo: "pesquisa"
date: "2026-10-07"
---

# Pesquisa — Tokens, custo e tokenização

> **Pergunta que motivou esta pesquisa:** por que a mesma frase custa uma quantidade diferente de dinheiro dependendo do idioma, e por que o billing de uma conversa longa cresce mais rápido que o número de turnos?

## Resposta curta (TL;DR)

O token é uma unidade de **subpalavra** construída por merge iterativo de pares frequentes (BPE), começando dos 256 bytes — o que garante cobertura total sem palavra desconhecida. Como o vocabulário é treinado majoritariamente sobre texto em inglês, idiomas românicos fragmentam em ~1,3–2× mais tokens por palavra. E como o billing é por token de entrada **e** de saída, tudo que entra na janela é cobrado a cada chamada — inclusive o histórico integral da conversa, o que faz o custo acumulado crescer de forma aproximadamente quadrática no número de turnos.

## Resposta completa

### O problema do vocabulário

Um texto real tem vocabulário aberto: formas novas, nomes próprios, erros de digitação, símbolos. Uma tokenização por palavra exigiria um vocabulário gigantesco e ainda assim deixaria buracos. Uma tokenização por caractere resolve cobertura mas fragmenta demais: o modelo teria que aprender conceito em unidades de 4 caracteres.

**Subpalavra** é o meio-termo, e é o que BPE produz.

### BPE, passo a passo

Sennrich, Haddow & Birch (2016) introduziram BPE em NMT. O algoritmo:

1. inicializa com os 256 bytes;
2. conta pares adjacentes mais frequentes;
3. funde o par mais frequente;
4. repete até o vocabulário alvo.

O detalhe decisivo: **byte-level**. Começando pelos bytes, nenhum texto é impossível — o que elimina o conceito de OOV. Compare com o WordPiece original (BERT), que operava sobre caracteres e precisava de um token `[UNK]`.

### Variantes

| Variante | Autor | Ideia |
| --- | --- | --- |
| **BPE** | Sennrich et al. (2016) | funde o par mais frequente |
| **WordPiece** | Google (BERT) | funde o par que maximiza a verossimilhança do corpus |
| **Unigram LM** | Kudo (2018) | distribuição de probabilidade sobre subpalavras; permite amostrar segmentações = regularização |
| **SentencePiece** | Kudo & Richardson (2018) | biblioteca independente de idioma, implementa BPE e Unigram |

### Tokenizers em produção

| Encoding | Vocabulário | Usado em |
| --- | --- | --- |
| `cl100k_base` | ~100k | GPT-4, GPT-3.5-turbo |
| `o200k_base` | ~200k | GPT-4o e derivados |

**Consequência de engenharia:** trocar de modelo pode trocar a contagem de tokens. Um sistema de contagem/custo precisa ser parametrizado pelo modelo, nunca hard-coded.

### Por que isso vira dinheiro

Billing por **1 milhão de tokens**, separado para entrada e saída:

| Fonte de custo | Como aparece |
| --- | --- |
| System prompt | input, a cada chamada |
| Histórico da conversa | **input de novo, a cada turno** |
| Exemplos few-shot | input, a cada chamada |
| Documentos do RAG | input, a cada consulta |
| Resposta | output (normalmente mais caro por token) |

**O custo quadrático dos agentes.** Se a conversa cresce ~$C$ tokens por turno, o total de tokens de entrada em $N$ turnos é ~$C \cdot N(N+1)/2$. Em um loop agêntico com 20 turnos, você paga o equivalente a ~10 chamadas completas em conteúdo já visto. É o principal custo oculto de sistemas conversacionais longos.

Mitigações: **prompt caching** (prefixos repetidos por desconto), resumir o histórico, ou externalizar a memória.

> Preços por token variam por modelo, região e data. **Sempre confirme em** `platform.openai.com/docs/pricing` **antes de citar número.**

### A desigualdade entre idiomas

Evidência: Petrov et al., *Do All Languages Cost the Same?* (EMNLP 2023) documenta Systematicamente que tokenização moderna é otimizada para inglês, e que idiomas de menor recurso pagam proporcionalmente mais.

Ordens de grandeza típicas em tokenizadores BPE modernos:

| Idioma | Tokens por palavra (aprox.) |
| --- | --- |
| Inglês | ~1,3 |
| Português, espanhol, francês | ~1,5–2 |
| Japonês/chinês | eficientes **por caractere**, não por palavra |

A causa é morfológica e ortográfica: palavras mais longas, mais sufixos, mais acentuação.

**Implicação de projeto:** custo por usuário não é uniforme num produto multilíngue. Isso é decisão de custo, de produto **e** de ética.

## Detalhes técnicos

```python
import tiktoken

enc = tiktoken.get_encoding("o200k_base")

pt = "O processamento de linguagem natural é um campo Fascinante da inteligência artificial."
en = "Natural language processing is a fascinating field of artificial intelligence."

for nome, txt in [("pt", pt), ("en", en)]:
    toks = enc.encode(txt)
    print(f"{nome}: {len(toks)} tokens | {len(txt.split())} palavras | {len(toks)/len(txt.split()):.2f} tok/palavra")

# O tokenizer também é reversível:
assert enc.decode(enc.encode(pt)) == pt
```

Função de contagem para um sistema real — **sempre parametrizada pelo modelo**:

```python
def count_tokens(text: str, model: str = "gpt-4o") -> int:
    try:
        enc = tiktoken.encoding_for_model(model)
    except KeyError:
        enc = tiktoken.get_encoding("o200k_base")
    return len(enc.encode(text))
```

## Limitações e riscos

- Contagens **em cache de modelos desatualizados** envelhecem mal — valide o encoding, não assuma.
- O custo real inclui o que você **não** vê: tool calls, respostas de ferramentas, mensagens de sistema repetidas.
- Contagens estimadas por `len(text.split())` subestimam em português e superestimam em japonês. Não use como base de cobrança.

## O que isso muda na minha prática

- [x] Parametrizar toda contagem de token pelo modelo usado na chamada.
- [x] Nunca usar `len(text.split())` como proxy de custo.
- [ ] Ao projetar produto multilíngue, reportar custo **por idioma**, não a média.
- [ ] Auditar custo de conversas longas antes de escalar.

## Fontes

1. **Neural Machine Translation of Rare Words with Subword Units** — Sennrich, Haddow & Birch, ACL 2016. https://aclanthology.org/P16-1162/ — *origem do BPE em NMT*
2. **Subword Regularization** — Kudo, ACL 2018. https://arxiv.org/abs/1804.10959 — *Unigram LM*
3. **SentencePiece** — Kudo & Richardson, EMNLP 2018. https://aclanthology.org/D18-2012/ — *biblioteca independente de idioma*
4. **Do All Languages Cost the Same?** — Petrov et al., EMNLP 2023. https://aclanthology.org/2023.emnlp-main.614/ — *evidência da desigualdade entre idiomas*
5. **openai/tiktoken** — https://github.com/openai/tiktoken — *implementação em Rust*
6. **How to count tokens with tiktoken** — OpenAI Cookbook. https://developers.openai.com/cookbook/examples/how_to_count_tokens_with_tiktoken
7. **Pricing** — https://platform.openai.com/docs/pricing — *[VERIFICAR antes de usar números]*

## Perguntas abertas

- [ ] Qual é o custo real do meu sistema por idioma? (medir no lab 01)
- [ ] Prompt caching vale para o padrão de chamadas do meu sistema?

## Ver também

-[[Token]] · [[Token]] · [[Lab 01 - Contando tokens e medindo custo]]

---
*Atualizado em 2026-09-30*
