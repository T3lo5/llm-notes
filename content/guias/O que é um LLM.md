---
title: "O que é um LLM"
tags:
  - "llm"
tipo: "guia"
date: "2026-10-01"
---

# O que é um LLM

> **Meta:** dar a definição formal de LLM, listar o que ele *não* é, e explicar por que a tarefa "qual token vem a seguir" é suficiente para produzir comportamento que parece compreensão.

## Resumo em 3 frases

1. Um LLM é uma função treinada para estimar $P(x_{t+1} \mid x_{1:t}; \theta)$ — a distribuição do próximo token dado o contexto. Tudo o mais é implementação dessa equação.
2. O corpus de pré-treino é comprimido em parâmetros; o modelo de chat adiciona um pós-treino (SFT + preferências) que **expõe** capacidades que já existiam de forma latente.
3. Consequência disso: ele não tem fonte de verdade interna. Quem tem de fornecer o fato é o **contexto** — por isso RAG funciona e por que alucinação é esperada, e não um bug.

## A definição formal

$$p_\theta(x_{t+1} \mid x_{1:t})$$

- $x_{1:t}$ — os tokens já presentes
- $\theta$ — os parâmetros (os pesos)
- A saída é uma **distribuição** sobre o vocabulário inteiro, não um token. A escolha é feita na etapa de amostragem ([[Nota Técnica - Geração token a token]]).

Treinado por **máxima verossimilhança**, que equivale a minimizar a entropia cruzada. Ponto crucial: **a única coisa que o modelo aprende é a distribuição de continuação de texto**. Não existe, no objetivo de treino, nenhum termo que diga "seja verdadeiro".

## Anatomia: o que existe dentro de um LLM

| Peça | O que faz | Onde é detalhada |
| ------------------ | ---------------------------------------- | --------------------------------------------------------- |
| Tokenizer | Texto ↔ inteiros (BPE/Unigram) | [[Tokens: o significado dos números]] |
| Embeddings | Inteiro → vetor denso | [[Embeddings e vetorização]] |
| Blocos Transformer | Refina cada vetor usando o contexto todo | [[Arquitetura Transformers e Attention]] |
| Projeção final | Vetor → logits sobre o vocabulário | [[Nota Técnica - Geração token a token]] |
| Sampler | Logits → token escolhido | [[Temperatura e previsibilidade]] |
| Detokenizador | Inteiros → texto | [[Tokens: o significado dos números]] |

### Parâmetros e memória de inferência

O número de parâmetros dita o tamanho em memória **não quantizada** — aproximadamente 2 bytes por parâmetro em FP16/BF16.

| Modelo | FP16/BF16 | INT8 | INT4 (GGUF) |
| --- | --- | --- | --- |
| 7B | ~14 GB | ~7 GB | ~4 GB |
| 70B | ~140 GB | ~70 GB | ~40 GB |
| 405B | ~810 GB | ~405 GB | ~230 GB |

*(ordem de grandeza: ~2 bytes/param em FP16, ~1 em INT8, ~0,5 em INT4)*

- **Quantização pós-treino (PTQ)** vs. **quantization-aware training (QAT)**: a primeira converte um modelo já treinado; a segunda treina tendo a quantização em mente.
- **GGUF** — formato single-file do `llama.cpp`, com metadados e quantização por tensor.
- **AWQ / GPTQ** — métodos de quantização só-pesos (W4A16), com calibração em amostra pequena; AWQ preserva pesos considerados salientes.

Em contexto longo, quem domina a memória é o [[KV Cache]], não os pesos.

## Pré-treino vs. pós-treino

| Fase | Objetivo | Volume de dados | Resultado |
| --- | --- | --- | --- |
| **Pré-treino** | Prever próximo token | Trilhões de tokens | [[Modelo Base]]: completa texto, ignora instruções |
| **SFT** | Seguir instruções | 10k–1M pares curados (prompt/resposta) | Modelo no formato certo, ainda inseguro |
| **RLHF / RLAIF / DPO** | Preferências humanas | Comparações ranqueadas | Modelo "de chat": útil, mais seguro |
| **Distilação** | Compressão | Saídas de um modelo professor | Modelo menor com comportamento parecido |

Duas frases que resolvem metade das confusões sobre LLMs:

- **SFT ensina o formato; o alinhamento ensina as preferências.**
- **O modelo base tem as capacidades latentes; o modelo de chat as expõe de forma controlada.** O 1.3B alinhado foi preferido ao 175B não alinhado — ver a ficha de InstructGPT no acervo.

## Contexto vs. parâmetros

| | Parâmetros | Contexto |
| --- | --- | --- |
| Natureza | estáticos (pesos) | dinâmico (prompt + KV cache) |
| Tipo de conhecimento | "model knowledge" — fatos comprimidos | "in-context knowledge" — o que está na janela |
| Como se altera | re-treino / fine-tune (caro, lento) | editar o prompt (instantâneo) |
| Limite | trilhões de parâmetros | [[Janela de Contexto]] (4k–1M tokens) |

É essa coluna da direita que explica quase toda a engenharia de LLMs em produção: **o que não cabe nos pesos, cabe na janela**. RAG, few-shot, memória de conversa e ferramentas são todas variações de "colocar mais coisa no contexto".

E explica por que *trocar de modelo* é uma decisão caro e por que *melhorar o prompt* quase sempre é o primeiro movimento.

## Alucinação: por que é esperada

Se o objetivo de treino é plausibilidade e não veracidade, então uma resposta falsa e bem formulada é **um ótimo resultado** segundo a função de perda. Não há defeito a ser corrigido — há um objetivo mal especificado para o uso pretendido.

Mitigações, em ordem de custo crescente:

1. **Contexto fundamentado** (RAG, citação obrigatória) — reduz, não elimina.
2. **Ferramentas** (busca, calculadora, interpretador de código) — torna a resposta *executável* e verificável.
3. **Temperatura baixa** — reduz a amostragem sobre a cauda da distribuição, onde mora o risco.
4. **Verificação externa** — extrair claims da resposta, recuperar evidência, checar entailment.
5. **Auto-consistência** — várias amostras e maioria.

## O que um LLM não é (levar a sério)

- **Não é banco de dados.** Não há consulta nem documento armazenado; há estatística comprimida nos pesos.
- **Não tem memória persistente.** Estado = pesos + janela de contexto. Nada sobrevive à chamada sem mecanismo externo.
- **Não verifica verdade.** Não há "consulta ao oráculo" em momento algum.
- **Não raciocina de forma confiável.** Pode acertar raciocínio; não tem garantia de que acerte. Saída plausível ≠ saída correta.
- **Não é determinístico.** Ver [[Temperatura e previsibilidade]].

## Perguntas para validar

1. Por que o modelo base "completa frases" e o modelo de chat "responde perguntas"? O que mudou nos pesos em cada caso?
2. Se eu colocar um documento no contexto e ele contradizer o que o modelo "sabe", quem vence? Por quê?
3. Qual a diferença de engenharia entre "não tenho esse dado" e "o modelo sabe isso mas está desatualizado"? resposta: RAG resolve o primeiro; o segundo exige re-treino ou contexto externo
4. Em que sentido "capacidade latente" é uma boa metáfora? Onde ela falha?

## Referências

- Brown et al., *Language Models are Few-Shot Learners* — arXiv:2005.14165
- Ouyang et al., *Training Language Models to Follow Instructions with Human Feedback* — arXiv:2203.02155
- Bai et al., *Constitutional AI* — arXiv:2212.08073
- Sennrich et al., *Neural Machine Translation of Rare Words with Subword Units* — aclanthology.org/P16-1162/
- Guo et al., *Scaling Laws for Neural Language Models* — arXiv:2001.08361
- Hoffmann et al., *Training Compute-Optimal Large Language Models* — arXiv:2203.15556
