---
title: "Token"
tags:
  - "conceito"
  - "tokens"
tipo: "conceito"
date: "2026-10-01"
---

# Token

> **Definição em uma frase:** a menor unidade de texto que o modelo recebe e devolve — normalmente uma subpalavra aprendida por BPE.

## Explicação curta

O modelo não trabalha com palavras nem com caracteres. Ele trabalha com **tokens**, que são índices numéricos de um vocabulário fixo (32k a 256k unidades). O texto vira tokens na entrada (tokenização) e volta a virar texto na saída (detokenização).

## Como funciona (mecanismo)

O vocabulário é construído por **merge iterativo** de pares frequentes (BPE), começando dos 256 bytes:

1. conta os pares de tokens adjacentes mais frequentes;
2. funde o par mais frequente em um token novo;
3. repete até o tamanho desejado.

Como o vocabulário nasce dos **bytes**, nenhum texto é impossível de representar — não existe "palavra desconhecida".

## Exemplos

| Termo | Como é segmentado (ilustrativo) |
| --- | --- |
| `tokenizer` | `token` + `izer` |
| `processamentos` | `process` + `amento` + `s` |
| `standalone` | possivelmente 1 token |
| `🧠` (emoji) | vários bytes → vários tokens |

## Confusões e aparências

- ❌ **Não é** uma palavra, nem um sinônimo de palavra.
- ❌ **Não é** o mesmo em todos os modelos. O tokenizador é propriedade do modelo; trocou de modelo, trocou a contagem.
- ✅ **É** a unidade de cobrança de APIs e de custo computacional (atenção é $O(T^2)$ em $T$ = nº de tokens).

## Por que importa (engenharia)

- Custo financeiro é direto: tokens de entrada × preço + tokens de saída × preço.
- Limite de contexto é contado em tokens.
- Idiomas românicos usam ~1,3–2× mais tokens por palavra que o inglês.

```python
import tiktoken
enc = tiktoken.get_encoding("o200k_base")
n = len(enc.encode("processamento"))
```

## Autoavaliação
1. **P:** Por que começar o vocabulário pelos 256 bytes? **R:** para garantir que qualquer texto, em qualquer idioma ou símbolo, possa ser representado — elimina OOV.
2. **P:** Por que a mesma frase custa mais tokens em português? **R:** BPE é treinado majoritariamente em inglês; morfologia rica e acentuação fragmentam palavras em mais subpalavras.

## Onde vi isso

- Visto em: [[Tokens e por que eles custam]]
- Aprofundamento: [[Pesquisa - Tokens, custo e tokenização]]

## Ver também

- [[Janela de Contexto]] · [[Embedding]] · [[Logits]]

---
*Atualizado em 2026-09-30*
