---
title: Sobre
description: Como este site é gerado, o que entra nele e o que fica de fora.
tags:
  - sobre
tipo: pagina
---

# Sobre

## O que é isto

Um conjunto de notas sobre modelos de linguagem, gerado a partir de um vault
pessoal do Obsidian. O vault é a fonte da verdade; este site é uma projeção dele,
limitada ao que é publicável.

## O que entra

- Conceitos: token, embedding, attention, transformer, sampling, KV cache, RAG, fine-tuning, LoRA, alucinação, prompt injection.
- Labs: código executável sobre tokens, embeddings, attention e sampling.
- Papers: resumos de Attention Is All You Need, Chinchilla, GQA, InstructGPT, LoRA, Mamba e RoPE.
- Banco de questões autorais sobre os temas estudados.

## O que fica de fora

Diário pessoal, material de terceiros e qualquer coisa com credencial ou dado
pessoal. O exportador só copia pastas explicitamente listadas, então um arquivo
novo fora dessas pastas não entra no site sem que a lista mude.

## Procedência

Cada nota foi escrita do zero por mim, a partir de fontes primárias: os papers
originais, a documentação das bibliotecas e o código. Onde cito uma fonte, ela
aparece linkada. Nenhum texto aqui é copiado de material de terceiros.

## Como é gerado

```
vault (Obsidian)
   │  scripts/exportar.py
   ▼
content/                          notas com frontmatter normalizado
quartz/static/dados/questions.json  banco de questões
   │  npx quartz build
   ▼
public/                           site estático
```

O comando é `npm run sync`. Ele exporta, valida e faz o build. Ver o README do
repositório para o passo a passo completo.

## Licença

Conteúdo de estudo pessoal. Os papers referenciados continuam sendo dos autores
originais.
