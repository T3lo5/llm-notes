---
title: "Modelo Open-Weight"
tags:
  - "conceito"
  - "selecao-de-modelos"
  - "open-weight"
  - "self-hosted"
tipo: "conceito"
date: "2026-10-16"
---

# Modelo Open-Weight

> **Definição em uma frase:** modelo cujos **pesos** são publicados e que roda na **sua infraestrutura**: sem custo por chamada e com controle total — mas com conta de infraestrutura, manutenção e observabilidade.

## Explicação curta

Open-weight libera os pesos do modelo (arquivos de 1GB a centenas de GB) para você servir onde quiser: sua nuvem, seu datacenter, sua GPU. Na prática isso compra três coisas: **controle total** (pesos, configuração, fine-tuning), **soberania de dados** (nada sai da sua infra) e **ausência de custo por chamada**. E cobra três outras: **infraestrutura** (hardware para carregar e rodar o modelo), **manutenção** (atualizar modelo, aplicar correções, acompanhar versões) e **observabilidade** (monitorar qualidade, latência e falhas sem o painel do provedor).

## Como funciona (a conta real)

- Os pesos vêm quantizados em vários tamanhos — Quantização (FP16 → INT8 → INT4) troca memória por leve perda de qualidade.
- O serving usa servidores de inferência (ex.: vLLM, TGI) que mantêm o [[KV Cache]] na GPU e fazem batching.
- O custo fixo existe mesmo com pouca demanda: GPU ociosa ainda é paga. A equação vira:

```
custo self-hosted/mês = GPU + operação + 1/2 FTE de manutenção   (fixo)
custo API/mês         = chamadas × preço por token                (variável)
```

O **crossover** é o ponto em que o volume alto faz o self-hosted vencer — abaixo dele, a API barata ganha.

## Exemplos

| Caso | Por que open-weight |
| --- | --- |
| Dado sensível (saúde, jurídico, financeiro) que não sai da empresa | soberania de dados |
| Volume alto e estável (10M de chamadas/mês) | custo fixo dilui; API cobraria por tudo |
| Domínio próprio com fine-tuning | adaptação profunda sem subir dados para terceiro |

## Confusões e aparências

- ❌ **Não é** "de graça" — é **sem custo por chamada**; infra, manutenção e observabilidade continuam custando.
- ❌ **Não é** necessariamente open-source — open-weight libera os **pesos**; a licença nem sempre é aberta no sentido da OSI (algumas proíbem uso comercial).
- ✅ **É** a categoria com controle total: você decide modelo, versão, alocação e onde o dado mora.

## Autoavaliação
1. **P:** Cite as três contas que o open-weight carrega fora do preço por token. **R:** Infraestrutura (hardware), manutenção (versões, patches) e observabilidade (monitoramento e avaliação).
2. **P:** Por que open-weight ≠ open-source? **R:** Porque open-weight libera pesos; open-source exige licença livre — e nem toda licença de pesos é livre.

## Onde vi isso

- Visto em: [[Categorias de modelos de IA]]
- Aprofundamento: [[Pesquisa - Custo e qualidade na seleção de modelos]]

## Ver também

- [[Modelo Frontier]] · [[Modelo Intermediário]] · Quantização · [[KV Cache]]

---
*Atualizado em 2026-10-09*
