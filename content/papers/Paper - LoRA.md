---
title: "Paper - LoRA"
tags:
  - "paper"
  - "fine-tuning"
tipo: "paper"
date: "2026-10-21"
---

# Paper — LoRA: Low-Rank Adaptation of Large Language Models

> **Por que estou lendo isso:** porque responde "quando usar fine-tuning, e por que ele ficou barato" — a outra ponta de RAG.

## Ficha

| Campo | Valor |
| --- | --- |
| Título | LoRA: Low-Rank Adaptation of Large Language Models |
| Autores | Edward J. Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, Weizhu Chen |
| Ano / Venue | 2021 (arXiv) · ICML 2022 |
| Link | https://arxiv.org/abs/2106.09685 |
| Tópicos | Fine-tuning · PEFT · Eficiência |

## Resumo em 5 linhas

1. **Problema:** *full fine-tuning* de um modelo grande exige armazenar os gradientes de todos os parâmetros — caro em memória, mesmo se o treino for curto.
2. **Método:** congelar os pesos $W_0$ e aprender um delta **de baixo rank**: $\Delta W = \frac{\alpha}{r} BA$, com $B \in \mathbb{R}^{d\times r}$, $A \in \mathbb{R}^{r \times k}$, $r \ll d$.
3. **Resultado:** qualidade comparável ao *full fine-tuning* com ~0,1–1% dos parâmetros treináveis.
4. **Custo:** o otimizador só precisa guardar estado para $A$ e $B$; e **pode-se alternar entre múltiplos adapters** sem reload.
5. **Conclusão:** transformou o fine-tuning de modelos >10B em viável em GPU de consumo.

## O que eu levo embora

- **PEFT é a resposta padrão a "preciso adaptar, mas não posso retreinar".**
- Fine-tuning serve para **comportamento** (formato, tom, tarefa), não para **fatos** — para fatos, ver [[RAG]].

## Detalhes que merecem atenção

### A intuição

O pressuposto é que a atualização de um modelo pré-treinado tem **baixo rank intrínseco**: os ajustes finos são direções de baixa dimensão no espaço de pesos. Se isso é verdade, $\Delta W$ pode ser representado por duas matrizes estreitas.

### O truque que importa

**Nenhuma alteração no caminho de inferência.** $W = W_0 + \Delta W$ pode ser **mesclado** nos pesos após o treino. Ou seja: adapter treinado, custo de inferência idêntico ao original. Isso é o que torna LoRA útil em produção — não há sobreposição de arquitetura no deploy.

### Comparações

| Método | Params treináveis | Memória de otimizador | Impacto na inferência |
| --- | --- | --- | --- |
| Full fine-tuning | 100% | alto | — |
| Adapters (Houlsby et al.) | ~3,6% | baixo | **+camadas** |
| LoRA | 0,1–1% | baixo | **nenhum** (mescla) |

LoRA vence adapters porque **não altera a arquitetura em inferência**.

### Limitações

- Rank $r$ é uma hiperparâmetro sensível; modelos grandes costumam precisar de $r$ maior.
- Não resolve o gargalo de **dados** — precisa de bons exemplos rotulados.
- Multi-adapter em escala exige serving que carregue e troque adapters.

### Perguntas abertas

- [ ] E com QLoRA (4-bit + LoRA)? Qual a perda de qualidade?
- [ ] Quando o delta de baixo rank deixa de bastar? (→ full fine-tuning)

## Onde isso conecta

- Pesquisa: [[Pesquisa - O que é um LLM]]

## Rethinking

> A pergunta de decisão num projeto é sempre: "o que eu quero mudar?" — **fato** → RAG; **comportamento** → fine-tuning; **capacidade** → ferramenta. Misturar os três é a origem da maioria dos projetos mal desenhados.

## Notas de leitura

| Passada | Data | Conclusão |
| --- | --- | --- |
| 1 — 15 min | | |
| 2 — método | | |
| 3 — crítica | | |

---
*Lido em 2026-09-30*
