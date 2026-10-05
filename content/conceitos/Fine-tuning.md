---
title: "Fine-tuning"
tags:
  - "conceito"
  - "fine-tuning"
tipo: "conceito"
date: "2026-10-07"
---

# Fine-tuning

> **Definição em uma frase:** continuar o treinamento de um modelo pré-treinado com dados específicos, para mudar **como** ele se comporta.

## Explicação curta

Fine-tuning muda o **comportamento**: formato de saída, tom, estilo, adhering a um schema, executing uma tarefa. Ele **não é** a ferramenta para ensinar fatos — fatos mudam e o fine-tune custa caro para refazer.

## Como funciona (mecanismo)

Três níveis, do mais barato ao mais caro:

| Método | Params treináveis | Custo | Quando |
| --- | --- | --- | --- |
| **Prompting / ICL** | 0% | quase zero | formato simples, poucos exemplos |
| **LoRA / adapters** | 0,1–3% | baixo | adaptação de comportamento |
| **Full fine-tuning** | 100% | alto | pesquisa, modelo próprio |

**LoRA** é o padrão: $\Delta W = \frac{\alpha}{r}BA$ com $r \ll d$, pesos base congelados. E o ponto crucial: o delta pode ser **mesclado** nos pesos após o treino — **custo de inferência idêntico** ao original.

## Quando usar, quando não

| Necessidade | Ferramenta |
| --- | --- |
| Fato novo/atualizado | [[RAG]] |
| Formato, tom, estrutura | **Fine-tuning** |
| Tarefa com muitos exemplos rotulados | **Fine-tuning** |
| Capacidade nova (cálculo, rede, código) | **ferramentas** |

## Erro comum

> "Vou fazer fine-tuning para o modelo saber os documentos da empresa."

Caro, lento, desatualiza a cada documento novo, e não dá citação. Isso é [[RAG]]. Fine-tuning é para **forma**, não para **conteúdo**.

## Autoavaliação
1. **P:** Qual a vantagem operacional do LoRA em relação a adapters clássicos? **R:** o delta pode ser mesclado nos pesos — nenhuma alteração na arquitetura de inferência.
2. **P:** Você tem 200 exemplos rotulados do seu domínio. O que faz primeiro? **R:** prompt + [[RAG]] e medir. Se o formato ainda não sair, aí fine-tuning com LoRA. Medir antes de treinar.

## Onde vi isso

- Visto em: [[O que é um LLM, de verdade]]
- Paper: LoRA — https://arxiv.org/abs/2106.09685

## Ver também

- [[Modelo Base]] · [[RAG]]

---
*Atualizado em 2026-09-30*
