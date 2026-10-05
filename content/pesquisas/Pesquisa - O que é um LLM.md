---
title: "Pesquisa - O que é um LLM"
tags:
  - "pesquisa"
  - "llm"
tipo: "pesquisa"
date: "2026-10-07"
---

# Pesquisa — O que é um LLM

> **Pergunta que motivou esta pesquisa:** se a tarefa de treino é apenas "qual token vem a seguir", por que o resultado se comporta como se entendesse?

## Resposta curta (TL;DR)

Porque "continuar texto" é uma tarefa de compressão tão densa que, para fazê-la bem, o modelo precisa internalizar gramática, fatos, raciocínio e estilo — tudo em um único objetivo. Não há símbolo de "verdade" no objetivo, e é por isso que alucinação é consequência e não defeito. E é por isso que a distinção operacional entre **parâmetros** (conhecimento comprimido, caro de atualizar) e **contexto** (conhecimento fornecido agora, barato de atualizar) é a que organiza toda engenharia de LLMs em produção.

## Resposta completa

### A definição formal

$$p_\theta(x_{t+1}\mid x_{1:t})$$

A saída é uma **distribuição**, não um token. A escolha é feita na amostragem (ver [[Logits]]).

### O argumento da suficiência

A tarefa "qual token vem a seguir" é barata o suficiente para ser rotulada em escala planetária e tão informativa que força o modelo a construir representações internas de:

- sintaxe e morfologia;
- fatos do mundo (memorizados como parte da transição);
- raciocínio (padrões de cadeia dethought presentes no texto);
- estilo e registro.

Isso é **compressão estatística**. É por isso que há quem diga que o modelo "é um dicionário comprimido do mundo" — a metáfora é útil até onde vai: ela quebra no ponto em que se espera que ele **consulte** algo. Não há consulta.

### O que não existe dentro do modelo

| Não existe | Consequência prática |
| --- | --- |
| Banco de dados | não há lookup; há transição statistics |
| Memória persistente | estado = pesos + janela |
| Verificador de verdade | nada distingue "verdadeiro" de "plausível" |
| Simulador de mundo | raciocínio é padrão aprendido, não mecanismo garantido |

### Pré-treino → pós-treino

| Fase | Objetivo | Dados | Resultado |
| --- | --- | --- | --- |
| Pré-treino | próximo token | trilhões de tokens | [[Modelo Base]] |
| SFT | seguir instruções | 10k–1M pares curados | formato correto |
| RLHF / RLAIF / DPO | preferências | comparações ranqueadas | modelo de chat |
| Distilação | compressão | saídas de um professor | modelo menor |

### Scaling: o que a literatura mostra

**Kaplan et al. (2020)** — *Scaling Laws*: perda de validação segue lei de potência em parâmetros ($N$), dados ($D$) e compute ($C$). Previsibilidade alta o suficiente para planejar experimentos.

**Hoffmann et al. (2022)** — *Chinchilla*: ao corrigir o método (treinar centenas de modelos), concluíram que para compute ótimo **parâmetros e tokens escalam na mesma proporção**. A capacidade dos modelos grandes vinha sendo subutilizada — undertrained, não subdimensionado.

A consequência prática para quem **usa** modelos: qualidade não é só "quantos parâmetros". É o produto entre capacidade e treinamento.

### Conhecimento nos parâmetros vs. no contexto

| | Parâmetros | Contexto |
| --- | --- | --- |
| Natureza | estáticos | dinâmico |
| Tipo | *model knowledge* | *in-context knowledge* |
| Atualizar | re-treinar (dias/semanas) | editar o prompt (instantâneo) |
| Limite | trilhões de parâmetros | [[Janela de Contexto]] |

**Por que RAG funciona sem alterar pesos:** a atenção trata os tokens do contexto como parte da sequência, lendo-os na inferência. Nenhum gradiente é calculado. O contexto **complementa** (e pode sobrepor) o conhecimento paramétrico.

Essa é a razão pela qual quase toda engenharia de LLMs é, na verdade, engenharia de contexto: o que não cabe nos pesos, cabe na janela.

### Alucinação: por que é esperada

O objetivo é plausibilidade linguística, não veracidade. Uma resposta falsa e bem formulada é **um ótimo resultado** segundo a função de perda. Não há bug — há objetivo mal especificado para o uso pretendido.

**Lewis et al. (2020)**, *Retrieval-Augmented Generation*, formaliza a resposta de engenharia: combinar um recuperador (conhecimento não-paramétrico, atualizável) com um gerador paramétrico.

Mitigações e custos: ver [[Alucinação]].

### Quando cada ferramenta entra

| Necessidade | Ferramenta |
| --- | --- |
| fato novo/atualizado | **RAG** |
| formato, tom, estrutura | **fine-tuning** |
| capacidade nova (cálculo, rede) | **ferramentas** |
| conhecimento pessoal mutável | memória externa |

Usar fine-tuning para ensinar fato é caro e desatualiza. Usar RAG para ensinar formato é desperdício de tokens.

## Detalhes técnicos

```python
# O LLM inteiro, em pseudocódigo de 6 linhas.
def gerar(prompt, modelo, T=0.7, max_tokens=100):
 tokens = tokenizer.encode(prompt)
 saida = []
 for _ in range(max_tokens):
 logits = modelo(tokens) # transformer: densa e paralela
 p = softmax(logits / T) # temperatura NOS LOGITS
 p = top_p_filter(p, 0.9) # trunca a cauda não confiável
 t = sample(p, rng) # <- ÚNICO ponto estocástico
 saida.append(t)
 if t == EOS: break
 tokens.append(t) # o token gerado volta ao contexto
 return tokenizer.decode(saida)
```

## Limitações e riscos

- A metáfora "compressão do mundo" induz a erro se aplicada literalmente: forget a de que não há consulta.
- "Emergent capabilities" é um termo-loaded: aemarcação pode ser efeito de métrica, não do modelo. Cuidado ao citar.
- Números de preço, benchmark e leaderboard envelhecem rápido — sempre verificar na fonte.

## O que isso muda na minha prática

- [x] Parar de tratar o modelo como fonte. Tratar como mecanismo de raciocínio que precisa de fonte.
- [x] Definir a ferramenta pelo que a necessidade é (fato / formato / capacidade), não pela moda.
- [ ] Ler Chinchilla e Able antes de qualquer trabalho sobre escala.

## Fontes

1. **Language Models are Few-Shot Learners** — Brown et al., NeurIPS 2020. https://arxiv.org/abs/2005.14165
2. **Scaling Laws for Neural Language Models** — Kaplan et al., 2020. https://arxiv.org/abs/2001.08361
3. **Training Compute-Optimal Large Language Models** — Hoffmann et al., NeurIPS 2022. https://arxiv.org/abs/2203.15556
4. **Training Language Models to Follow Instructions with Human Feedback** — Ouyang et al., NeurIPS 2022. https://arxiv.org/abs/2203.02155
5. **Constitutional AI** — Bai et al., 2022. https://arxiv.org/abs/2212.08073
6. **Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks** — Lewis et al., NeurIPS 2020. https://arxiv.org/abs/2005.11401

## Perguntas abertas

- [ ] Como "capacidade latente" se manifesta em um caso concreto do meu domínio?
- [ ] Que perguntas de avaliação exigem distinguir "sabe" de "tem no contexto"?

## Ver também

- [[O que é um LLM, de verdade]] · [[Modelo Base]] · [[RAG]] · [[Alucinação]]

---
*Atualizado em 2026-09-30*
