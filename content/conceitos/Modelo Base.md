---
title: "Modelo Base"
tags:
  - "conceito"
  - "alinhamento"
tipo: "conceito"
date: "2026-10-01"
---

# Modelo Base

> **Definição em uma frase:** o modelo após o pré-treino, antes do pós-treino — ele completa texto, mas não segue instruções.

## Base vs. Chat

| | Modelo base | Modelo de chat |
| --- | --- | --- |
| Objetivo do treino | próximo token | próximo token + SFT + preferências |
| Comportamento | completa, continua | responde, pergunta, recusa |
| Inspeção | diz "Claro! Aqui está..." e desvia | segue o pedido |

## As três fases do pós-treino

1. **SFT** (Supervised Fine-Tuning) — pares (instrução, resposta) curados. Ensina o **formato**.
2. **Alinhamento** (RLHF, RLAIF, DPO, Constitutional AI) — comparações ranqueadas por humanos ou por IA segundo princípios escritos. Ensina as **preferências**.
3. **Distilação** — comprimir um modelo professor em um menor.

## A ideia de capacidade latente

InstructGPT mostrou que o modelo de 1,3B alinhado era preferido ao de 175B não alinhado. Interpretação: **as capacidades já estavam no modelo base; o alinhamento as expõe de forma controlada.**

É uma metáfora útil — e com limites. Dizer que "o modelo sabe X" quando ele só consegue produzir X sob condições estreitas de prompt é exatamente o tipo de erro que o alinhamento tenta corrigir.

## Autoavaliação
1. **P:** O que exatamente muda entre base e chat? **R:** os pesos mudam (SFT + alinhamento), mas a arquitetura é a mesma. Não é uma rede nova.
2. **P:** Por que SFT sozinho não resolve? **R:** ensina o formato, mas o modelo não tem sinal sobre o que é *melhor* entre respostas plausíveis. Isso vem das preferências.
3. **P:** Quando o fine-tuning é a ferramenta certa? **R:** para tom, formato e estrutura estável; para tarefas com muitos exemplos rotulados. **Não** para ensinar fatos — isso é RAG.

## Onde vi isso

- Visto em: [[O que é um LLM]]

## Ver também

- [[Fine-tuning]] · [[Alucinação]] · [[Pesquisa - O que é um LLM]]

---
*Atualizado em 2026-09-30*
