---
title: "Tokens: o significado dos números"
tags:
  - "tokens"
tipo: "guia"
date: "2026-10-01"
---

# Tokens: o significado dos números

> **Meta:** explicar por que o modelo segmenta texto em subpalavras, e por que a mesma frase custa uma quantidade diferente de dinheiro dependendo do idioma e do que você enfiou na janela.

## Resumo em 3 frases

1. Um token é uma unidade de **subpalavra** aprendida por um algoritmo de merge (BPE) sobre bytes. Ele existe porque o vocabulário é aberto: qualquer texto real tem palavras que o modelo nunca viu, e um token por palavra não cobriria isso.
2. A API cobra **todo token de entrada e de saída**, incluindo histórico de conversa, exemplos de few-shot e documentos recuperados por RAG. Custo de LLM é, antes de tudo, uma conta de tokens.
3. Tokenização é **propriedade do modelo, não do idioma**: idiomas românicos geram mais tokens por palavra que o inglês, e trocar de modelo pode trocar essa conta.

## Por que não palavra, nem caractere

Se o vocabulário fosse por palavra: um corpus real tem milhões de formas, quase todas raras. Uma tokenização por palavra estouraria o vocabulário (e o custo da camada de embeddings) sem nunca cobrir o suficiente.

Se fosse por caractere: o vocabulário é minúsculo (256 bytes), mas a sequência fica longa, e o modelo teria que aprender uma unidade de conceito em 4 caracteres. Péssimo para aprender morfologia.

**Subpalavra** é o ponto de equilíbrio: vocabulário de 32k–256k unidades que cobre tudo e cujas partes reaproveitam-se.

## BPE em 60 segundos

1. Comece com os 256 bytes.
2. Conte os pares de tokens adjacentes mais frequentes no corpus.
3. Funde o par mais frequente em um token novo (`e`+`s` → `es`).
4. Repita até atingir o tamanho de vocabulário desejado.

O resultado é um vocabulário hierárquico: tokens como `pro`, `cess`, `amento` existem, e palavras raras são compostas por eles. O "espaçamento de subpalavras" é o que permite ao modelo generalizar para combinações que nunca viu.

- **WordPiece** (BERT) — funde o par que maximiza a verossimilhança do corpus, em vez do mais frequente.
- **Unigram LM / SentencePiece** (Google, LLaMA, T5) — mantém uma distribuição de probabilidade sobre subpalavras e pode amostrar múltiplas segmentações, o que funciona como regularização.

**Byte-level** é a garantia final: se o vocabulário começar pelos 256 bytes, nenhum texto é impossível de representar. É isso que elimina o conceito de "palavra desconhecida".

## Na prática

```python
import tiktoken

enc = tiktoken.get_encoding("o200k_base")   # ~200k tokens (GPT-4o)
enc2 = tiktoken.get_encoding("cl100k_base") # GPT-4 / GPT-3.5

pt = "O processamento de linguagem natural é um campo fascinante."
en = "Natural language processing is a fascinating field."

print(len(enc.encode(pt)), len(pt.split()))
print(len(enc.encode(en)), len(en.split()))
```

> ⚠️ **Regra de ouro:** conte tokens com o tokenizador do modelo que você está chamando. `len(text.split())` e `len(text)` não são estimativas aceitáveis — a diferença pode passar de 2× em português.

## Por que isso vira dinheiro

O billing é por **1 milhão de tokens**, separado para entrada e saída. Tudo que entra na janela entra na conta:

| Fonte de custo | Como aparece na fatura |
| --- | --- |
| Prompt do sistema | input, a cada chamada |
| Histórico da conversa | **input de novo, a cada turno** |
| Exemplos few-shot | input, a cada chamada |
| Documentos do RAG | input, a cada consulta |
| Resposta gerada | output, mais caro por token na maioria dos modelos |

Dois efeitos que passam despercebidos:

- **Conversas longas custam superlinearmente.** A cada turno o histórico inteiro é reenviado. Em N turnos, o total de tokens de entrada acumula ~N(N+1)/2. É o principal custo oculto de agentes conversacionais.
- **Prompt caching** cobre prefixos repetidos (system prompt + exemplos) por desconto. Se seu system prompt é fixo, colocar o conteúdo variável **depois** dele é o que permite o cache. Ordem do prompt tem impacto financeiro, não só de qualidade (ver [[Engenharia de prompt e contexto]]).

> Preços variam por modelo, por região e por data. **Sempre confirme em** `platform.openai.com/docs/pricing` **antes de colocar número em slide ou trabalho.** Não memorize tabela de preço — ela envelhece.

## A desigualdade entre idiomas

Em tokenizadores BPE modernos, o inglês fica em torno de **1,3 token por palavra**; português, espanhol e francês ficam em torno de **1,5–2×**. A causa é morfológica e ortográfica: palavras mais longas, mais sufixos, mais acentuação, menos regularidade.

- **Japonês e chinês** são eficientes **por caractere**, não por palavra.
- **Árabe e birmanês** são os piores casos em relação ao inglês (relatórios de custo apontam fatores de ~5×).

Implicação de projeto: um sistema multilíngue não pode assumir custo uniforme. Se você multiplicar o custo por usuário sem normalizar, os usuários de línguas de menor recurso pagam mais caro pelo mesmo serviço — uma decisão que é ao mesmo tempo de custo, de produto e de ética.

## Perguntas para validar

1. Por que a tokenização é definida como **propriedade do modelo**, e não do idioma?
2. Se o histórico da conversa é reenviado a cada turno, por que o crescimento é quadrático e não linear?
3. Um modelo A custa 3× mais por token que o modelo B, mas o B tem janela 2× maior. Quando cada um vence?
4. Onde ficaria o "prompt" do sistema no layout para exploited prompt caching?

## Referências

- Sennrich, Haddow & Birch, *Neural Machine Translation of Rare Words with Subword Units* — https://aclanthology.org/P16-1162/
- Kudo & Richardson, *SentencePiece* — https://aclanthology.org/D18-2012/
- Kudo, *Subword Regularization* — https://arxiv.org/abs/1804.10959
- `openai/tiktoken` — https://github.com/openai/tiktoken
- OpenAI Cookbook, *How to count tokens with tiktoken* — https://developers.openai.com/cookbook/examples/how_to_count_tokens_with_tiktoken
- Petrov et al., *Do All Languages Cost the Same?* (EMNLP 2023) — https://aclanthology.org/2023.emnlp-main.614/
- Karpathy, *Let's build the GPT Tokenizer* — https://www.youtube.com/watch?v=zduSFxRajkE

## Ver também

- [[Pesquisa - Tokens, custo e tokenização]] · [[Lab 01 - Contando tokens e medindo custo]] · [[Token]]
