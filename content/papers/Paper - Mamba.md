---
title: "Paper - Mamba"
tags:
  - "paper"
  - "arquitetura"
tipo: "paper"
date: "2026-11-04"
---

# Paper — Mamba: Linear-Time Sequence Modeling with Selective State Spaces

> **Por que estou lendo isso:** porque é a pergunta mais relevante sobre o futuro do Transformer, e a[[Transformers, de um jeito simples]] termina apontando pra cá.

## Ficha

| Campo | Valor |
| --- | --- |
| Título | Mamba: Linear-Time Sequence Modeling with Selective State Spaces |
| Autores | Albert Gu, Tri Dao (Carnegie Mellon / Princeton) |
| Ano / Venue | 2023 (arXiv) |
| Link | https://arxiv.org/abs/2312.00752 |
| Tópicos | Arquitetura · SSM · Complexidade linear |

## Resumo em 5 linhas

1. **Problema:** a atenção é $O(n^2)$ em tempo e memória; SSMs anteriores eram lineares mas com matrizes de transição **fixas**, o que impede raciocínio baseado em conteúdo.
2. **Método:** *selective state space model* (S6) — as matrizes de transição $\mathbf{A}, \mathbf{B}, \mathbf{C}$ passam a depender **da própria entrada**, permitindo copiar e induzir.
3. **Resultado:** complexidade linear em tempo e memória, e desempenho comparável a Transformers de mesmo tamanho em vários benchmarks.
4. **Custo:** ecossistema maduro menor; hardware-aware kernels próprios.
5. **Conclusão:** ameaça concreta ao paradigma Transformer em contextos longos.

## O que eu levo embora

- **É aqui que a distinção "complexidade vs. constante" vira argumento de paper.** FlashAttention e GQA compram fatores; Mamba muda o regime.
- SSM **seletivo** ≠ SSM linear. A seletividade (dependência da entrada) é o que dá poder.

## Detalhes que merecem atenção

### O argumento central

| | Atenção | SSM fixo | SSM seletivo (Mamba) |
| --- | --- | --- | --- |
| Complexidade | O(n²) | O(n) | **O(n)** |
| Depende do conteúdo | sim | **não** | **sim** |
| Copiar da entrada | sim | não | **sim** |

SSMs lineares anteriores (como DSS) eram lineares mas **blindados**: a transição não depende do que está sendo processado. Mamba torna $B$, $C$ e o passo de discretização funções da entrada — daí "selective".

### Comparações

| Arquitetura | Tempo | Memória | Ecossistema |
| --- | --- | --- | --- |
| Transformer | O(n²) | O(n) + cache | enorme (HF, vLLM, Triton) |
| Mamba | O(n) | O(n) | pequeno, mas crescendo |

### Limitações

- **A janela de atenção effectively curta** aparece nos benchmarks de dependência longa.
- Inferência em-sequence: SSMs têm estado fixo (menor constante) mas perdem o acesso aleatório ao histórico.
- Comparações com Transformer em 2023 usavam modelos menores do que os disponíveis hoje. **Tratar os números com cuidado.**

### Perguntas que o paper deixa abertas

- [ ] Modelos híbridos (atenção + SSM) fazem sentido para o meu problema?
- [ ] E quando combinamos GQA + FlashAttention + janela esparsa? A quantidade de otimização de constante já justifica a troca de paradigma?

## Onde isso conecta

- Pesquisa: [[Pesquisa - Transformer e self-attention]]

## Rethinking

> A pergunta para um pós em 2026 não é "Mamba venceu". É: **quantas otimizações de constante eu preciso acumular antes de mudar de paradigma?** E a resposta honesta é: depende do length distribution dos seus prompts, e isso se mede.

## Notas de leitura

| Passada | Data | Conclusão |
| --- | --- | --- |
| 1 — 15 min | | |
| 2 — método | | |
| 3 — crítica | | |

---
*Lido em 2026-09-30*
