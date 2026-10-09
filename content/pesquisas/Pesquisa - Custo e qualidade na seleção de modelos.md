---
title: "Pesquisa - Custo e qualidade na seleção de modelos"
tags:
  - "pesquisa"
  - "selecao-de-modelos"
  - "custo"
  - "roteamento"
tipo: "pesquisa"
date: "2026-10-16"
---

# Pesquisa — Custo e qualidade na seleção de modelos

> **Pergunta que motivou esta pesquisa:** existe relação entre preço e qualidade em LLMs de API — e, se não existe, como decidir entre modelo caro e barato com dados em vez de opinião?

## Resposta curta (TL;DR)

Não existe relação monotônica entre preço e adequação: os preços de API variam em até **duas ordens de grandeza** sem variação proporcional de qualidade (FrugalGPT), e os líderes de leaderboard medem média, não o *seu* caso (Chatbot Arena, HELM). A literatura de engenharia mostra a saída: **cascata e roteamento** — usar o modelo barato por padrão e escalar para o caro só quando a tarefa exige — reduzem custo em **2× a 98%** sem perder qualidade (RouteLLM, FrugalGPT). Conclusão prática: o "melhor modelo" é o do seu contexto, e a decisão boa junta **benchmark no seu domínio + conta de custo no seu volume + documentação da escolha** (Model Cards).

## Resposta completa

### Preço não é qualidade

Chen, Zaharia & Zou (FrugalGPT, Stanford, 2023) mediram a precificação das APIs de LLM populares e acharam **heterogeneidade de até 100× entre provedores**. Preço alto compra capacidade média maior, mas a adequação por tarefa não acompanha na mesma proporção: em HEADLINES, o GPT-4 errava ~6% dos casos que um modelo muito mais barato acertava. Preço é oferta, não garantia — reforça o mito desmontado na [[O mito do melhor modelo]].

### O que um número só de leaderboard esconde

- **Chatbot Arena** (Chiang et al., UC Berkeley, 2024) documenta os riscos do benchmark estático: **contaminação** (dados de treino que vazam para o teste), **saturação**, **overfitting** e falta de alinhamento com preferência humana. A resposta foi avaliação ao vivo por voto humano (240k+ votos, ranking por Bradley–Terry).
- **HELM** (Liang et al., Stanford CRFM, TMLR 2023) mostra que avaliação com um número só esconde trade-offs: com **7 métricas** (acurácia, calibração, robustez, fairness, viés, toxicidade, eficiência) sobre **16 cenários**, melhorar acurácia pode piorar calibração. Antes do HELM, modelos eram avaliados em 17,9% dos cenários; com padronização, 96% — e as comparações passaram a expor os custos de cada escolha.

**Implicação:** a qualidade do critério 1 do [[Critérios de seleção de IA]] só existe medida **na sua tarefa**, com **mais de uma métrica**.

### A saída de engenharia: cascata e roteamento

| Abordagem | Ideia | Evidência |
| --- | --- | --- |
| **Cascata** (FrugalGPT) | tenta do mais barato ao mais caro; para no primeiro que passa num verificador | até **98% menos custo** mantendo/acrescendo acurácia; 80% menos e +1,5pp em HEADLINES vs. GPT-4 |
| **Roteamento aprendido** (RouteLLM) | um router binário treinado com preferência humana decide, por consulta, se manda para modelo forte ou fraco | **>2× de economia** sem sacrificar qualidade; generaliza para modelos não vistos no treino |
| **Modelo único** | baseline: sempre o mesmo modelo | simples, mas paga o teto de capacidade em toda consulta |

O RouteLLM treinou o router com **80k batalhas humanas** do Chatbot Arena + ~120k rótulos de juiz LLM (custo de anotação: ~$700) — o ponto não é o número, é que **rotular preferência é barato comparado ao que o roteamento economiza**.

### Documentar a decisão

**Model Cards** (Mitchell et al., FAT\* 2019) propõem que todo modelo publicado venha com uso pretendido, condições de avaliação e desempenho por grupo. Para seleção, o que importa é a disciplina: a decisão de modelo vira um documento com finalidade, alternativas consideradas e limites conhecidos — exatamente a "linha de decisão" da [[Trade-offs na escolha do modelo]].

## Detalhes técnicos

Cascata mínima em pseudocódigo — o verificador é o coração (sem ele, cascata é só sorte):

```python
def cascata(prompt, verificavel):
    for modelo in [barato, medio, caro]:          # do barato ao caro
        r = modelo.responder(prompt)
        if verificavel(r):                        # schema válido, checker, score acima do limiar
            return r
    return modelo_caro.responder(prompt)          # fallback
```

O roteamento aprendido troca a regra por um modelo: `P(forte_vence | consulta) > α → forte`, com α calibrando o ponto da curva custo × qualidade.

## Comparações

| Abordagem A | Abordagem B | Quando usar cada |
| --- | --- | --- |
| Cascata por regra | Roteamento aprendido | regra quando há verificador barato; aprendido quando o custo justifica dados rotulados |
| Benchmark público | Eval no seu domínio | público para triagem; **seu domínio para decidir** |
| Um modelo | Cascata | um modelo em volume baixo e crítico; cascata em volume misto |

## Limitações e riscos

- FrugalGPT e RouteLLM usam preços e modelos de 2023–2024: **os números envelhecem**, os mecanismos não.
- Cascata exige **exemplos rotulados** para treinar/comparar — em tarefa sem verificador, o gate de qualidade vira gargalo.
- Leaderboard público sofre contaminação; usar só para descartar, nunca para escolher.
- Preços variam por região e data: **sempre conferir a página do provedor** antes de citar número (ver [[Pesquisa - Tokens, custo e tokenização]]).

## O que isso muda na minha prática

- [ ] Rodar um mini-benchmark com **2 modelos** (um frontier, um intermediário) no meu domínio antes de qualquer decisão (planejado para o MC3)
- [ ] Montar a conta de custo com o **meu volume real**, não com o preço por token isolado
- [ ] Escrever a decisão no formato "modelo + critérios + alternativa descartada + data de revisão"
- [ ] Avaliar cascata com verificador de schema onde o volume justificar

## Fontes

1. **FrugalGPT: How to Use Large Language Models While Reducing Cost and Improving Performance** — Chen, Zaharia & Zou, Stanford, 2023. https://arxiv.org/abs/2305.05176 — *preços variam 2 ordens de grandeza; cascata reduz custo até 98%*
2. **RouteLLM: Learning to Route LLMs with Preference Data** — Ong et al., UC Berkeley, ICLR 2025. https://arxiv.org/abs/2406.18665 — *router aprendido com preferência humana: >2× de economia*
3. **Chatbot Arena: An Open Platform for Evaluating LLMs by Human Preference** — Chiang et al., 2024. https://arxiv.org/abs/2403.04132 — *avaliação ao vivo por voto humano; riscos do benchmark estático*
4. **Holistic Evaluation of Language Models (HELM)** — Liang et al., Stanford CRFM, TMLR 2023. https://arxiv.org/abs/2211.09110 — *avaliação multi-métrica expõe trade-offs*
5. **Model Cards for Model Reporting** — Mitchell et al., FAT\* 2019. https://arxiv.org/abs/1810.03993 — *documentação de uso pretendido e desempenho por condição*
6. **Preços dos provedores** — páginas oficiais de pricing (OpenAI, Anthropic, Google) — *[VERIFICAR antes de usar números]*

## Perguntas abertas

- [ ] Qual é o desempenho dos dois modelos candidatos **no meu domínio**? (medir antes de escolher)
- [ ] O volume do meu caso de uso justifica cascata ou self-hosted?

## Ver também

- [[Trade-offs na escolha do modelo]] · [[Modelo Frontier]] · [[Modelo Open-Weight]] · [[Latência]] · [[Pesquisa - Tokens, custo e tokenização]]

---
*Atualizado em 2026-10-09*
