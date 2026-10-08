---
title: "IA multimodal"
tags:
  - "multimodal"
tipo: "guia"
date: "2026-10-06"
---

# IA multimodal

> **Meta:** entender o que significa "multimodal" e por que entender várias modalidades não significa ser boa em todas.

## Resumo em 3 frases

1. **Multimodal** é a IA que entende **mais de uma modalidade** — texto, imagem, áudio, código, vídeo.
2. Entender tudo **não** significa ser boa em tudo: cada modalidade tem um encoder, e o modelo acerta mais em algumas que em outras.
3. A consequência prática: um multimodal é um **trato** — você escolhe pelo que ele faz bem, não pelo que ele "entende".

## O que é uma modalidade

| Modalidade | O que é | Como entra no modelo |
| --- | --- | --- |
| **Texto** | tokens | tokenizer → embeddings |
| **Imagem** | pixels | encoder visual → projeções |
| **Áudio** | amostras de onda | encoder de áudio → projeções |
| **Vídeo** | quadros + áudio | ambos os caminhos |
| **Código** | texto com gramática rígida | tokenizer (é texto, mas com tokenização diferente) |

## A arquitetura: um encoder por modalidade

O ponto técnico que explica "não é boa em tudo":

```
imagem ──▶ encoder visual ──┐
texto ──▶ tokenizer ────────┼──▶ projeções no mesmo espaço ──▶ transformer
áudio ──▶ encoder de áudio ─┘
```

Cada modalidade tem seu **encoder** e sua resolução. O transformer_shared recebe tudo como vetores. Mas:

- O encoder de imagem é **bom** em formas e objetos, **ruim** em texto pequeno numa imagem
- O tokenizer de texto é **bom** em linguagem, **ruim** em geometria
- Nenhum deles é ótimo nos dois

> É a mesma razão pela qual um modelo de linguagem é excelente em texto e não vê nada.

## O que muda na prática

| | Modelo só de texto | Multimodal |
| --- | --- | --- |
| Entrada | texto | texto, imagem, áudio |
| O que você precisa descrever | tudo em palavras | pode apontar a imagem |
| Custo | menor | maior — mais tokens de entrada |
| Latência | menor | maior |
| Erros possíveis | alucinação | alucinação **+ erro de leitura** |

## Quando usar

✅ **Vale a pena:**
- Analisar documento com gráfico ou tabela (a visão lê o layout que o texto perde)
- Ler print de bug, screenshot de erro
- Extrair dado de documento digitalizado
- Descrever imagem para quem não tem acesso

❌ **Não vale:**
- Se o texto já está disponível estruturado — ler é mais barato e mais confiável
- Se a precisão importa mais que a comodidade: ler de imagem é **menos confiável** que ler o texto original
- Se o custo por chamada é sensível

> **Regra prática:** prefira o **texto original** quando existir. Multimodal é para quando a informação está na imagem e em nenhum outro lugar.

## Perguntas para validar

1. Por que o modelo multimodal ainda erra mais em texto dentro de imagem do que em texto puro?
2. Em um documento digitalizado com tabela, o que o multimodal ganha em relação a um modelo de texto?
3. Custo e latência de um multimodal: por que são maiores? (modos de entrada, resolução dos patches)

## Ver também

- [[O que é um LLM]] · [[Embedding]] · [[Janela de Contexto]] · [[Paper - InstructGPT]]
