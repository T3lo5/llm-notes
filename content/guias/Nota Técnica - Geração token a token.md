---
title: "Nota Técnica - Geração token a token"
tags:
  - "decodificacao"
tipo: "guia"
date: "2026-10-01"
---

# Nota Técnica — Geração token a token

> **Meta:** entender como a IA enxerga e contextualiza um token, percorrendo token a token até a resposta completa por aproximação — e por que a resposta não é fixa, mas probabilística.

## Resumo em 3 frases

1. Geração é um **loop autoregressivo**: logits → distribuição → um token → reinserido no contexto → repete. O passo sequencial é o gargalo; o processamento do contexto é paralelo.
2. O [[KV Cache]] existe porque, sem ele, cada passo reprocessaria todo o contexto — custo quadrático. Com ele, cada passo custa uma leitura de memória proporcional ao contexto.
3. Cada passo é uma **aproximação**: o modelo não "sabe" a resposta, ele escolhe o token mais provável *dado o que já gerou*. Por isso a resposta é **probabilística**, não fixa.
4. Daí decorre a separação entre **TTFT** (prefill, dominado por computação) e **tokens/s** (decode, dominado por **banda de memória**). Otimizar um não otimiza o outro.

## Como o modelo "vê" um token

O modelo **não vê caracteres nem palavras**. Ele vê **tokens** — ids inteiros mapeados para vetores (ver [[Token]] e [[Embedding]]).

Para cada posição, três perguntas:

1. **Qual é este token?** (embedding — o que ele representa)
2. **Em que contexto está?** (atenção — quem é relevante aqui)
3. **Qual o próximo mais provável?** (saída sobre o vocabulário)

O passo 3 devolve uma **distribuição**, não um token. A escolha é feita na amostragem (ver [[Temperatura]] e [[Top-p Sampling]]).

## Token a token, por aproximação

A resposta **não é projetada de uma vez**. Ela é construída em passos, e cada passo muda o contexto dos próximos:

```
passo 1: "A"      → contexto mínimo, previsão mais genérica
passo 2: "A" + "empresa" → agora o modelo pode especializar
passo 3: "A empresa de"... → segue o padrão mais provável
   ...
passo n: "A empresa de e-commerce reduziu..." → fim
```

Três consequências que decorrem disso:

| Consequência | Por quê |
| --- | --- |
| **A resposta não é fixa** | em cada passo há escolha entre alternativas plausíveis |
| **Não há revisão retroativa** | o modelo não volta e troca um token ruim já gerado |
| **O início carrega mais peso** | os primeiros tokens definem o caminho (ver [[Lost in the Middle]]) |

> É por isso que "o mesmo prompt gera respostas diferentes" não é defeito: é consequência de a geração ser um caminho amostrado em um espaço de possibilidades. Ver [[Ambiguidade e riscos na IA]].

## O loop

Dado um prefixo $x_{1:t-1}$:

$$z_t = f_\theta(x_{1:t-1}) \in \mathbb{R}^{V}, \qquad p_t = \mathrm{softmax}(z_t), \qquad x_t \sim p_t$$

Repete-se até condição de parada: token EOS, `max_tokens`, ou `stop` sequence.

Três pontos que valem fixar:

- O softmax recebe **logits**, não probabilidades.
- Dividir por $T$ **não altera o ranking** — só a concentração.
- Cada token gerado **volta a entrar no contexto**. O modelo nunca "corrige" o que já emitiu. É por isso que um erro no início contamina o resto.

## Treinamento: teacher forcing

No treino, o alvo em cada passo é o token **real** da sequência, nunca um token sorteado. O gradiente flui por todos os passos em paralelo — é isso que torna o treino viável em GPU.

$$\mathcal{L} = -\frac{1}{T}\sum_{t=1}^{T} \log p_\theta(x_t \mid x_{1:t-1})$$

$$\text{Perplexidade} = \exp\!\left(\frac{1}{T}\sum_{t} -\log p_\theta(x_t \mid x_{1:t-1})\right) = e^{\mathrm{NLL}}$$

A perplexidade é o **médio geométrico da probabilidade por token**: quanto menor, mais previsível é o texto para o modelo.

⚠️ Ela **não mede qualidade nem raciocínio**. Mede ajuste a um corpus. Holtzman et al. argumentam que usar perplexidade como critério de decodificação é enganoso justamente porque as distribuições resultantes de maximum likelihood são muito suavizadas — é isso que produz a cauda não confiável do slide anterior.

## KV Cache

Em cada passo de decodificação é preciso attention de cada token novo contra **todos** os anteriores. Sem cache, recalcula-se $K$ e $V$ do contexto inteiro a cada token → $O(T^2)$.

O **KV cache** guarda as proções de chave e valor já calculadas. A cada passo só se computa $K, V$ do token novo:

$$\text{tamanho} \propto 2 \cdot n_{\text{camadas}} \cdot n_{\text{cabeças KV}} \cdot d_{\text{cabeça}} \cdot T$$

Duas consequências de projeto:

- **GQA/MQA** reduz o número de cabeças K/V → encolhe o cache → decode mais rápido. É otimização de constante, mas numa constante que domina.
- **vLLM / PagedAttention** pagina o cache como memória virtual, eliminando fragmentação e permitindo compartilhar prefixo (system prompt) entre requisições. É o que tornou serving viável.

## Latência: duas perguntas diferentes

| Métrica | Fase | O que domina | Como melhorar |
| --- | --- | --- | --- |
| **TTFT** (time to first token) | prefill (prompt processado em paralelo) | **cálculo** — atenção $O(T^2)$ | FlashAttention, reduzir contexto, quantizar pesos |
| **Tokens/s** (após o primeiro token) | decode (um token por vez) | **banda de memória** — ler pesos + KV cache | GQA, quantização, batching, speculative decoding |

**Exemplo de prova:** contexto de 32k tokens, resposta de 500 tokens, prefill leva 3 s, decode a 80 tokens/s.

- (a) O que domina a latência **percebida**? As duas, em regiões diferentes: o usuário espera 3 s para o primeiro token, e depois lê a 80 tokens/s. Se a resposta for curta, o prefill domina; se for longa, o decode.
- (b) Dobrar o batch: o TTFT tende a **subir** (mais sequências competem, mais padding) enquanto o throughput agregado **sobe bastante** (o custo de memória por passo é compartilhado). É o compromisso clássico latência × vazão que justifica serving dedicado por workload.

## Controlar a saída: logits processors

Além de temperatura e truncamento, é possível **modificar os logits antes do sampling**:

- `logit_bias` — adiciona um valor em $[-100, 100]$ a tokens específicos (ex.: forçar o modelo a começar por `{`).
- `stop` / `stop_sequences` — interrompem a geração.
- **Structured output / constrained decoding** — a cada passo, mascara os logits para que só tokens válidos segundo um JSON Schema possam ser emitidos. O modelo **nunca tem chance** de produzir JSON inválido. É garantia por construção, não por disciplina.
- **Tool calling** — o modelo emite uma chamada estruturada (nome + argumentos), validada pela API contra o schema.

Diferença conceitual que importa: pedir "por favor, responda só em JSON" é um pedido. Structured output é uma **restrição**. Só a segunda garante.

## Estratégias de decodificação

| Estratégia | Ideia | Quando |
| --- | --- | --- |
| **Greedy** (argmax) | sempre o máximo | tarefas determinísticas; risco de repetição |
| **Top-k / top-p / min-p** | amostra da cauda truncada | padrão de geração aberta |
| **Typical** (Meister et al., 2022) | mantém tokens cuja informação $-\log p$ está próxima da entropia condicional | evita o "previsível demais" e o "surpreendente demais" |
| **Beam search** | mantém as $k$ sequências parciais de maior score | resposta canônica única (tradução, sumarização); **evite para chat** |

Beam caiu de graça para chat porque maximiza likelihood sobre texto aberto — exatamente o que produz degeneração.

## Speculative decoding

Modelo **draft** pequeno gera $k$ candidatos em paralelo; modelo **target** grande verifica todos em **um forward pass** e aceita/rejeita por *rejection sampling modificada*. Resultado: 2–3× de speedup **sem alterar a distribuição de saída** — o texto gerado tem a mesma estatística do modelo grande. É a otimização de inferência mais elegante que existe, porque não há trade-off de qualidade.

## Perguntas para validar

1. Por que o decoder precisa da máscara causal, e o que acontece se ela for removida?
2. O que exatamente o KV cache armazena, e por que o custo de memória é proporcional ao número de cabeças K/V?
3. Por que aumentar o batch melhora throughput e piora TTFT?
4. Structured output e "responda em JSON" — qual dos dois garante validade, e por quê?
5. Speculative decoding acelera sem mudar a distribuição. Por que isso é melhor do que trocar por um modelo menor?

## Referências

- Jurafsky & Martin, *Speech and Language Processing*, cap. 3 — https://web.stanford.edu/~jurafsky/slp3/
- Holtzman et al., *The Curious Case of Neural Text Degeneration* — https://arxiv.org/abs/1904.09751
- Meister et al., *Typical Decoding* — https://arxiv.org/abs/2202.00666
- Hewitt, Manning & Liang, *Truncation Sampling as LM Desmoothing* — https://aclanthology.org/2022.findings-emnlp.249/
- Ainslie et al., *GQA* — https://arxiv.org/abs/2305.13245
- Kwon et al., *Efficient Memory Management for LLM Serving (vLLM)* — https://arxiv.org/abs/2309.06180
- Leviathan et al., *Fast Inference from Transformers via Speculative Decoding* — https://arxiv.org/abs/2211.17192

## Ver também

- [[Pesquisa - Amostragem e reprodutibilidade]] · [[Lab 04 - Temperatura, top-p e reprodutibilidade]] · [[Temperatura e previsibilidade]]
