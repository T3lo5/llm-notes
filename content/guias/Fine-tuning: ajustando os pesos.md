---
title: "Fine-tuning: ajustando os pesos"
tags:
  - "fine-tuning"
  - "lora"
  - "rlhf"
tipo: "guia"
date: "2026-10-06"
---

# Fine-tuning: ajustando os pesos

> **Meta:** entender o que é fine-tuning, quais técnicas existem, e como decidir entre fine-tuning e prompt engineering.


## Resumo em 3 frases

1. **Fine-tuning é ajustar os pesos** de um modelo já treinado para ele performar melhor em algo específico que você quer que ele saiba agora.
2. Os pesos são **parâmetros numéricos** — matematicamente, transformações lineares que ajustam o vetor de entrada em cada camada. "Entender" é ajustar essas transformações.
3. A decisão entre fine-tuning e prompt engineering é principalmente **econômica e de manutenção**: custo de implementação, custo recorrente, e o que acontece quando o dado muda.

## O que são os pesos

O modelo forward é uma cadeia de transformações:

```
h → W₁h + b₁ → ativação → W₂h + b₂ → ... → logits
```

- **W** (pesos) — matrizes que transformam o vetor
- **b** (viés) — deslocamentos
- São ajustados por gradiente para reduzir a perda

> Um LLM tem **bilhões** desses parâmetros. Atualizá-los todos exige GPU, dados e tempo — é isso que torna fine-tuning caro e por isso que [[LoRA]] existe.

## As três técnicas

| Técnica | O que ajusta | Quando |
| --- | --- | --- |
| **Instruction tuning** | todos os pesos, com pares (instrução, resposta) | ensinar o modelo a **obedecer** a instruções |
| **LoRA / PEFT** | matrizes pequenas de baixo posto, inseridas ao lado | adaptar a um **domínio ou tarefa** com pouco custo |
| **RLHF** | pesos, com sinal de preferência humana | alinhar **comportamento** — útil, seguro e prestativo |

Ordem histórica: pré-treino → **SFT/instruction tuning** → **RLHF** (ver [[Modelo Base]]).

### LoRA em uma frase

Em vez de aprender ΔW inteiro, aprende-se ΔW = B·A, onde A e B são matrizes muito menores. O resultado: uma fração do custo de treinamento, com qualidade próxima à do ajuste completo.

> A ficha completa está em [[Paper - LoRA]]. Ver também [[Paper - Chinchilla]] para o ponto "mais dados > mais parâmetros".

## Fine-tuning vs. prompt engineering

| | Prompt engineering | Fine-tuning |
| --- | --- | --- |
| **O que muda** | só a entrada | os pesos do modelo |
| **Custo de implementação** | ~zero | alto — dados, GPU, engenharia |
| **Custo de mudar** | instantâneo | novo treino |
| **Quando o dado muda** | edita o prompt | re-treina |
| **Formato fixo** | difícil | fácil de ensinar |
| **Conhecimento novo** | entra pelo contexto | **entra nos pesos** |
| **Escala** | limitado pelo contexto | escalável |

### Quando usar cada um

> **Regra prática:** use prompt engineering até o limite. Fine-tune quando a tarefa é **repetida em escala** e o prompt não está mais rendendo.

Use **fine-tuning** quando:
- o mesmo comportamento é pedido milhares de vezes com variação pequena
- o formato é rígido e o modelo não obedece
- o custo por chamada domina e o prompt ficou enorme

Use **prompt engineering** quando:
- a tarefa varia ou é rara
- o conhecimento muda com frequência
- você quer testar rápido

> Ver [[RAG]] como a terceira via: quando o que falta é **fato**, não **comportamento**.

## Perguntas para validar

1. Por que fine-tuning é caro se a mudança é pequena em termos de comportamento? (o espaço de parâmetros é enorme)
2. Instruction tuning e RLHF: o que cada um muda no comportamento do modelo?
3. Se o conhecimento muda toda semana, por que fine-tuning é a escolha errada?
4. Quando RAG é melhor que os dois? (fato novo, alta rotatividade)

## Referências

- Hu et al., *LoRA: Low-Rank Adaptation of Large Language Models* — arXiv:2106.09685
- Ouyang et al., *Training Language Models to Follow Instructions with Human Feedback* — arXiv:2203.02155
- Wei et al., *Finetuned Language Models Are Zero-Shot Learners* (FLAN) — arXiv:2109.01652
- Dettmers et al., *QLoRA* — arXiv:2305.14314
