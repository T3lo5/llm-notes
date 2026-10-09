---
title: "Latência"
tags:
  - "conceito"
  - "selecao-de-modelos"
  - "latencia"
  - "inferencia"
tipo: "conceito"
date: "2026-10-16"
---

# Latência

> **Definição em uma frase:** o tempo entre enviar a chamada e receber a resposta, medido em percentis (p50/p99) e decomposto em TTFT (até o primeiro token) e tempo por token (a partir daí).

## Explicação curta

Latência é um dos 5 critérios de seleção (ver [[Critérios de seleção de IA]]) e a razão pela qual "qual modelo usar" não se resolve só com qualidade e custo. Ela tem duas partes com causas diferentes: o **TTFT** (time to first token), dominado pelo [[Prefill]] — processar todo o prompt de uma vez —, e o **decode**, o tempo de cada token gerado depois, que é sequencial. Um modelo maior demora nos dois; um prompt maior demora no prefill.

## Como funciona (mecanismo)

```
latência total = TTFT (prefill paralelo) + n_tokens × tempo_por_token (decode sequencial)
```

- **Prefill** é paralelo sobre todos os tokens de entrada — é GPU trabalhando em matriz.
- **Decode** gera um token por passo: cada passo lê bilhões de parâmetros e todo o [[KV Cache]] — o gargalo é banda de memória, não FLOPs (ver [[Nota Técnica - Geração token a token]]).
- **Streaming** melhora a *percepção* (o usuário vê o primeiro token rápido), **não** a latência total.

## Exemplos de medição

| Métrica | O que diz | Armadilha |
| --- | --- | --- |
| TTFT | quando o usuário "sente" a resposta começar | varia com o tamanho do prompt |
| p50 | mediana — o caso típico | esconde a cauda |
| **p99** | o caso ruim que define SLA | medir só p50 entrega previsão otimista |

No MC2 medimos latência p50 por braço de prompt e o resultado contraintuitivo apareceu: prompt longo foi **mais rápido** que curto — a latência não é monotônica no tamanho do prompt, depende do modelo e do que o system_fingerprint expõe (ver [[Temperatura e previsibilidade]]).

## Confusões e aparências

- ❌ **Não é** "velocidade do streaming" — streaming muda a percepção; a latência total é a mesma.
- ❌ **Não é** só rede — rede entra, mas o prefill e o decode do modelo dominam na maioria dos casos.
- ✅ **É** o critério que puxa para modelos menores: em chat interativo, p95 < 2s muda o produto.

## Autoavaliação
1. **P:** Por que o decode é limitado por banda de memória? **R:** Cada passo gera 1 token lendo todos os pesos e todo o KV cache da GPU — é leitura massiva para pouca computação.
2. **P:** Por que medir p50 e p99, e não média? **R:** A distribuição é assimétrica; a média é puxada pela cauda e esconde o pior caso que define o SLA.

## Onde vi isso

- Visto em: [[Critérios de seleção de IA]]

## Ver também

- [[Prefill]] · [[KV Cache]] · [[Modelo Intermediário]] · [[Trade-offs na escolha do modelo]]

---
*Atualizado em 2026-10-09*
