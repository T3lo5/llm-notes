---
title: "Paper - InstructGPT"
tags:
  - "paper"
  - "alinhamento"
tipo: "paper"
date: "2026-10-14"
---

# Paper — Training Language Models to Follow Instructions with Human Feedback (InstructGPT)

> **Por que estou lendo isso:** porque é o paper que definiu o pipeline de alinhamento pelo qual todo modelo de chat passou. E porque o resultado é contraintuitivo.

## Ficha

| Campo | Valor |
| --- | --- |
| Título | Training Language Models to Follow Instructions with Human Feedback |
| Autores | Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida, Carroll L. Wainwright, Pamela Mishkin, Chong Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, John Schulman, Jacob Hilton, Fraser Kelton, Luke Miller, Maddie Simens, Amanda Askell, Peter Welinder, Paul Christiano, Jan Leike, Ryan Lowe |
| Ano / Venue | 2022 (arXiv) · NeurIPS 2022 |
| Link | https://arxiv.org/abs/2203.02155 |
| Tópicos | Alignment · SFT · RLHF · Preference |

## Resumo em 5 linhas

1. **Problema:** modelos pré-treinados são **completadores** — continuam texto, ignoram instruções. Como torná-los úteis sem retreinar do zero?
2. **Método:** pipeline de três etapas — **SFT** em demonstrações humanas → **modelo de recompensa** treinado em rankings → **PPO** otimizando contra esse modelo de recompensa.
3. **Resultado principal (o contraintuitivo):** o modelo de **1,3B alinhado** foi preferido ao de **175B não alinhado** (GPT-3).
4. **Custo:** treinar o modelo de recompensa é o gargalo (muita anotação humana) — é a origem do RLAIF e da Constitutional AI depois.
5. **Conclusão:** alinhamento ≠ treinar mais. Uma pequena quantidade de dados de preferência muda mais do que mais capacidade.

## O que eu levo embora

- **SFT ensina o formato; RLHF ensina as preferências.** São etapas distintas com funções distintas.
- **Capacidade não é sinônimo de utilidade.** Um modelo 130× menor e alinhado ganha de um muito maior e cru.
- O gargalo do alinhamento é **dado humano**, não compute.

## Detalhes que merecem atenção

### As três etapas

| Etapa | Dados | O que ensina |
| --- | --- | --- |
| **1. SFT** | demonstrações (instrução → resposta) | formato, estilo, seguir instrução |
| **2. Reward Model** | rankings de saídas por humanos | o que é *preferido* |
| **3. PPO** | otimização contra o RM | internalizar a preferência |

### O detalhe de método mais importante

Os **rankings humanos** são a parte escassa. Quando a preferência é pareada (A melhor que B), o RM aprende a funcionar como um **classificador binário** — muito mais barato de treinar do que gerar rótulos absolutos de qualidade. E é por isso que Constitutional AI usa **feedback de IA** guiado por princípios escritos, escalando sem humanos.

### Limitações declaradas

- **Performance mais fraca fora do domínio** do texto demonstrativo — o alinhamento é um viés para o conjunto de instruções humano.
- **"Verdadeiro" não é o objetivo.** O RM generaliza preferences humanas, que têm viés e erro. Alucinação persiste.
- **Capacidade fica retida**: o modelo de 175B alinhado ainda é mais capaz em tarefas abertas do que o de 1,3B.
- O RLHF pode introduzir **length bias** (respostas mais longas tendem a ser preferidas).

### Perguntas que o paper deixa abertas

- [ ] Como escalar o reward model sem humano? (→ Constitutional AI)
- [ ] Como evitar o viés de tamanho (length bias)? (→ DPO, sem modelo de recompensa)
- [ ] O alinhamento de um modelo base forte é diferente do alinhamento de um modelo já instruído?

## Onde isso conecta

- Pesquisa: [[Pesquisa - O que é um LLM]]

## Rethinking

> O resultado mais útil do paper é **negativo**: ele mostra que "capacidade" e "utilidade" são eixos separados. Isso invalida a heurística de "escolha o maior modelo que couber no orçamento" e reforça: **o alinhamento é o que converte capacidade em serviço**.

## Notas de leitura

| Passada | Data | Conclusão |
| --- | --- | --- |
| 1 — 15 min | | |
| 2 — método | | |
| 3 — crítica | | |

---
*Lido em 2026-09-30*
