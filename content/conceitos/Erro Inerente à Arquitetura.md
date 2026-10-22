---
title: "Erro Inerente à Arquitetura"
tags:
  - "conceito"
  - "arquitetura"
  - "falhas"
tipo: "conceito"
date: "2026-10-29"
---

# Erro Inerente à Arquitetura

> **Definição em uma frase:** falha que vem de **como o modelo é construído**, não de um
> bug ou de um prompt mal escrito — por isso não se elimina; se contorna.

## Explicação curta

Todo sistema tem limites que não dependem de configuração. Em um LLM, os três que a
[[Erros Inerentes à Arquitetura]] destaca são: **estimar probabilidade em vez de
verificar verdade** (não há "pensamento" nem crença), **contexto finito** (janela e
atenção) e **pedido ambíguo** (a formulação do input admite mais de uma leitura e não
determina a resposta correta).

A consequência prática: aumentar o modelo, aumentar o contexto ou escrever um prompt
melhor **reduz a taxa**, mas não remove a natureza da falha. O que remove o risco é o que
está **em volta** do modelo — fonte real, validação, guardrails, humano e medição.

## As três causas

| Causa | O que é | Falha típica |
| --- | --- | --- |
| **Probabilidade** | o modelo gera a continuação mais provável; não tem modelo de verdade nem intenção | [[Alucinação]] · [[Inconsistência]] |
| **Contexto finito** | janela limitada + informação no meio do contexto perde força | [[Perda de Contexto]] |
| **Pedido ambíguo** | a formulação do input admite várias leituras e não determina qual resposta é correta | [[Ambiguidade]] |

> As três não são independentes: um contexto mal montado esconde a fonte e aumenta a
> alucinação; um pedido ambíguo gera respostas diferentes entre execuções.

## O que **não** é

- ❌ **Não é bug:** bug é desvio de uma regra escrita; aqui a regra é probabilística.
- ❌ **Não é falta de prompt:** prompt não cria fonte de verdade nem aumenta a janela.
- ❌ **Não é resolvido por modelo maior:** reduz a taxa, mantém a estrutura.
- ❌ **Não é "o modelo não sabe nada":** ele sabe gerar texto plausível — o que falta é
  verificação externa.

## O que fazer

| Controle | Ataca qual causa |
| --- | --- |
| [[Grounding]] com citação | probabilidade (dá lastro ao fato) |
| Validação de saída em código | probabilidade e inconsistência (barra o inválido) |
| Arquitetura de contexto (posição, resumo, estado) | contexto finito |
| Contrato de resposta + exemplo + schema | pedido ambíguo |
| [[Evals]] | mede o residual de todas |

## Exemplo

Um agente de suporte inventa um endpoint que não existe (probabilidade), muda o prazo
prometido entre duas conversas (contexto/estado) e interpreta "cancelar" como "estornar"
(ambiguidade). Nenhuma das três é corrigida por "seja mais cuidadoso": a primeira precisa
de documentação real, a segunda de estado fixo e a terceira de contrato na pergunta.

## Autoavaliação
1. **P:** Por que uma falha inerente não pode ser "corrigida"? **R:** porque não é desvio
   de uma regra — é consequência do mecanismo (probabilidade, janela finita, pedido ambíguo).
   O controle é redução de dano e detecção, não eliminação.
2. **P:** O que distingue erro inerente de erro de projeto? **R:** o inerente vem do
   modelo (não muda com prompt); o de projeto vem do sistema em volta (RAG mal
   configurado, validação ausente, contexto mal montado).

## Onde vi isso

- Visto em: [[Erros Inerentes à Arquitetura]]
- Relacionado: [[Alucinação e comportamentos]] · [[Riscos e falhas em projetos de IA]]

## Ver também

- [[Alucinação]] · [[Inconsistência]] · [[Ambiguidade]] · [[Perda de Contexto]] · [[Janela de Contexto]] · [[Lost in the Middle]] · [[Grounding]] · [[Guardrails]] · [[Evals]]

---
*Atualizado em 2026-10-22*
