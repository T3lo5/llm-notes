---
title: "LoRA"
tags:
  - "conceito"
  - "fine-tuning"
  - "lora"
  - "peft"
tipo: "conceito"
date: "2026-10-06"
---

# LoRA

> **Low-Rank Adaptation.** A técnica que torna fine-tuning viável em modelos grandes.

## O problema

Ajustar todos os pesos de um modelo de 7B–70B parâmetros exige GPU, tempo e dados — proibitivo para adaptar um modelo a uma tarefa específica.

## A ideia

Em vez de aprender a atualização ΔW inteira (mesma dimensão de W), aprende-se uma fatoração de **baixo posto**:

```
ΔW = B · A A ∈ ℝ^(r×k) B ∈ ℝ^(d×r) com r << min(d, k)
```

Os pesos originais **congelam**. Só A e B treinam — uma fração minúscula dos parâmetros.

## Por que funciona

As atualizações de baixo posto capturam a maior parte da variação de pesos entre modelos próximos. Ou seja: o que uma tarefa acrescenta ao modelo vive em poucas direções.

## Números

| Métrica | Fine-tuning completo | LoRA |
| --- | --- | --- |
| Parâmetros treináveis | 100% | ~0,1%–1% |
| Memória de GPU | muito alta | baixa |
| Checkpoint | tamanho do modelo | megabytes |
| Qualidade | referência | próxima (às vezes igual) |

## Variantes

| Variante | Ideia |
| --- | --- |
| **QLoRA** | quantiza o modelo base (4-bit) e treina só os adaptadores — cabe em GPU de consumidor |
| **DoRA** | decompõe os pesos em magnitude + direção, acelerando a convergência |
| **AdaLoRA** | aloca o posto por camada, adaptando a capacidade |

## Quando usar

✅ Tarefa repetida em escala · formato rígido · mesmo domínio · custo por chamada importa
❌ Fato novo rotativo (use [[RAG]]) · tarefa rara · protótipo rápido (use prompt engineering)

## Origem

- Hu et al., *LoRA: Low-Rank Adaptation of Large Language Models* — arXiv:2106.09685
- Dettmers et al., *QLoRA: Efficient Finetuning of Quantized LLMs* — arXiv:2305.14314
- [[Paper - LoRA]]

## Ver também

- [[Fine-tuning]] · [[Fine-tuning: ajustando os pesos]] · [[RAG]] · [[Paper - Chinchilla]]

---
*Ficha criada em 2026-10-01*
