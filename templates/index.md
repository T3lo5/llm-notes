---
title: LLMs por dentro
description: Notas de estudo sobre tokens, attention, transformers, sampling e engenharia de contexto.
tags:
  - llm
tipo: pagina
---

# LLMs por dentro

Notas de estudo sobre como modelos de linguagem funcionam por dentro: tokens e
custo, attention, sampling,KV cache, embeddings, RAG, fine-tuning e as falhas que
importam em produção.

O conteúdo vem de um vault pessoal do Obsidian e é regerado a partir dele. A
fonte da verdade é o vault, não este site.

<div class="home-grade">

## Por onde começar

<div class="home-coluna">

### Fundamentos

- [[Token]]
- [[Embedding]]
- [[Transformer]]
- [[Self-Attention]]
- [[Janela de Contexto]]
- [[Perplexidade]]

</div>

<div class="home-coluna">

### Geração e sampling

- [[Logits]]
- [[Temperatura]]
- [[Top-k Sampling]]
- [[Top-p Sampling]]
- [[Prefill]]
- [[KV Cache]]

</div>

<div class="home-coluna">

### Engenharia

- [[RAG]]
- [[Chunking]]
- [[Busca Semântica]]
- [[Similaridade de Cosseno]]
- [[Fine-tuning]]
- [[LoRA]]

</div>

<div class="home-coluna">

### Limites e riscos

- [[Alucinação]]
- [[Lost in the Middle]]
- [[Prompt Injection]]
- [[Modelo Base]]
- [[Teacher Forcing]]
- [[Positional Encoding]]

</div>

</div>

## Praticar

- [Banco de questões](/questoes) — 45 questões com nível de dificuldade e origem no módulo.
- [Labs](/labs) — código executável sobre tokens, embeddings, atenção e sampling.
- [Pesquisas](/pesquisas) — o que cada paper realmente mudou, e o que é só otimização de constante.
- [Papers](/papers) — Attention Is All You Need, Chinchilla, GQA, InstructGPT, LoRA, Mamba e RoPE.
- [Mapa dos conceitos](/mapa/mapa---funcionamento-de-llms) — as perguntas que as fichas respondem, em ordem.

## Nota de método

Estas são anotações de estudo, não documentação de referência. Onde a nota
contradiz o paper ou a documentação, o paper ganha. Os labs foram executados
localmente, mas os números hardware-dependem — leia a conclusão de cada um.

<style>
  .home-grade { margin: 2rem 0; }
  .home-coluna { }
  @media (min-width: 700px) {
    .home-grade > .home-coluna { display: inline-block; width: 46%; vertical-align: top; padding-right: 3%; }
  }
  .home-grade h2 { margin-top: 1.5rem; }
</style>
