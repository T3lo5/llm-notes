---
title: "Alucinação"
tags:
  - "conceito"
  - "avaliacao"
tipo: "conceito"
date: "2026-10-01"
---

# Alucinação

> **Definição em uma frase:** resposta fluentemente formulada e factualmente incorreta — o resultado **esperado** quando o objetivo de treino é plausibilidade e não veracidade.

## Por que acontece

A função de perda otimiza $- \log p(\text{texto})$. Ela não distingue "verdadeiro" de "falso": os dois são igualmente plausíveis como continuação de texto em termos de linguagem. Uma resposta falsa e bem escrita é **um ótimo resultado** segundo o objetivo.

Não é bug. É objetivo mal especificado para o uso pretendido.

## Taxonomia

| Tipo | Exemplo |
| --- | --- |
| **Intrínseca** | contradiz o contexto fornecido |
| **Extrínseca** | afirma algo falso sobre o mundo |
| **Factual** | número, data ou nome incorretos |
| **Lógica** | passo de raciocínio inválido |
| **Fabricação** | cita artigo, autor ou lei inexistente |

## Mitigações (em ordem de custo)

| Camada | Custo | Reduz? |
| --- | --- | --- |
| **Contexto fundamentado** (RAG + citação) | baixo | bastante |
| **Temperatura baixa** | zero | pouco |
| **Ferramentas** (busca, calculadora, código) | médio | muito (verificável) |
| **Verificação externa** (extrair claims → NLI/entailment) | alto | muito |
| **Auto-consistência** (N amostras, maioria) | alto (N×) | razoável |
| **Fine-tuning com dado curado** | alto | pouco por si só |

## Erro de projeto

> "Vou resolver alucinação com prompt engineering e mais contexto."

Contexto fundamentado reduz; não elimina. E contexto **errado** piora (ver [[Lost in the Middle]]). A defesa real é combinar recuperação verificável + ferramentas + validação de saída.

## Autoavaliação
1. **P:** Alucinação é bug ou consequência? **R:** consequência do objetivo de treino. Não existe "correção" que a elimine sem mudar o objetivo ou tirar a fonte de verdade do modelo (ferramenta/RAG).
2. **P:** Por que temperatura baixa reduz alucinação? **R:** concentra a amostragem no topo da distribuição, que é onde o modelo tem mais confiança estatística. Não elimina tokens errados que estão no topo.

## Onde vi isso

- Visto em: [[O que é um LLM, de verdade]]

## Ver também

- [[RAG]] · [[Janela de Contexto]] · [[Lost in the Middle]]

---
*Atualizado em 2026-09-30*
