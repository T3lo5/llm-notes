---
title: "Evals"
tags:
  - "conceito"
  - "avaliacao"
  - "riscos"
tipo: "conceito"
date: "2026-10-26"
---

# Evals

> **Definição em uma frase:** conjunto **versionado de casos com gabarito**, rodado a
> cada mudança do sistema, que mede se a qualidade subiu ou desceu — o único jeito de
> otimizar no escuro.

## O que um eval é

| Parte | Pergunta que responde |
| --- | --- |
| **Dataset** | em que casos eu testo? |
| **Gabarito** | o que seria a resposta aceitável? |
| **Métrica** | como comparo a saída com o gabarito? |
| **Runner** | como executo e versiono? |

Sem as quatro, não é eval — é amostragem informal com sorte.

## Para que serve

1. **Regressão**: a mudança do prompt/modelo melhorou ou piorou?
2. **Cobertura de segurança**: o caso adversarial está no dataset?
3. **Comparação justa**: mesmo dataset, mesmo prompt, mesmas condições — é a mesma lógica
   do [[Benchmark]], mas do seu domínio (ver [[Benchmarks: como medir o desempenho]]).
4. **Memória**: cada incidente real vira caso, e volta como teste.

## Tipos de caso que não podem faltar

| Tipo | Exemplo | Por que importa |
| --- | --- | --- |
| **Nominal** | caso comum, resposta óbvia | linha de base |
| **Adversarial** | prompt injection, contexto contraditório | o que a regra não pega |
| **De borda** | valor no limite do schema, campo opcional | onde a validação quebra |
| **De cauda** | raro e caro | o que define o impacto real |
| **De formatação** | saída que viola o schema | falha de máquina, não de conteúdo |

## Onde roda

- **CI, a cada mudança** — é o que impede a regressão silenciosa.
- **Antes de trocar de modelo** — o substituto precisa passar nos mesmos evals
  (ver [[Vendor lock-in]]).
- **Periodicamente, contra o mundo real** — a distribuição de produção diverge da do
  dataset.

## Armadilhas

- **Eval de prompt, não de qualidade**: mede se o modelo obedeceu a instrução, não se a
  resposta é boa.
- **Gabarito que não distingue**: se tudo passa, o número é decorativo.
- **Contaminação**: caso de teste vazado no treino ou no dataset público.
- **Dataset de demo**: sem dado real do domínio, o eval mede o provider genérico — não
  o seu caso.
- **Métrica sem limiar**: um número sem ponto de corte não decide nada — defina
  "passa" antes de rodar.

## Autoavaliação
1. **P:** Por que "rodei 10 exemplos e deu bom" não é um eval? **R:** não é versionado,
   não tem gabarito explícito, não tem métrica e não roda a cada mudança — não serve
   nem para comparar nem para detectar regressão.
2. **P:** O que um eval precisa ter para ser comparável entre dois modelos? **R:** o
   mesmo dataset, o mesmo prompt, a mesma métrica e o mesmo limiar — comparação justa
   é critério de aceitação, não sorte.

## Onde vi isso

- Visto em: [[Riscos e falhas em projetos de IA]], [[Moderação de conteúdo com IA]]

## Ver também

- [[Benchmark]] · [[Benchmarks: como medir o desempenho]] · [[Guardrails]] · [[Human-in-the-loop]] · [[Vendor lock-in]]
