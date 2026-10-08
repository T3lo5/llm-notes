---
title: "Desenvolvimento de Software com IA"
tags:
  - "conceito"
  - "dev-ia"
tipo: "conceito"
date: "2026-10-15"
---


# Desenvolvimento de Software com IA

> **Meta:** descrever o fluxo de trabalho real de quem desenvolve com IA hoje — onde a
> IA entra, onde o humano continua decidindo — e listar os 3 riscos que tornam o
> processo diferente de "pedir o código e colar".

## O que é

É a prática de **projetar, escrever, revisar e manter software com assistência de
modelos de linguagem** — variando do *par de programação* (você digita, a IA sugere)
ao *agente* (a IA executa tarefas inteiras: ler o repositório, editar vários arquivos,
rodar testes). A mudança de fondo não é "a IA escreve código": é que **o custo de
gerar código despencou, e o gargalo virou revisar, especificar e confiar**.

## Por que importa (aqui e no projeto)

- Foi o **tema de abertura deste projeto** — a abordagem parte da premissa de
 que este é o fluxo de trabalho padrão em 2026.
- No projeto (plataforma de avaliação de produtos com Claude + N8N + Mastra), o código
 foi gerado com IA de ponta a ponta — por isso as regras de processo importam: sem
 elas, o resultado é *vibe coding* que ninguém consegue manter.
- É a base para [[Spec-Driven Development]], [[Agent Skills]] e [[OpenCode]] — estas notas mostram **as três alavancas** (processo, instruções, ferramenta).

## Ideias-chave

- **Gerar barato ≠ confiar barato.** O que mudou é a razão custo/geração; a
 responsabilidade pela correção continua humana. Teste e revisão são o produto real.
- **Especificação vira artefato.** Quando um agente escreve o código, o que você
 *escreveu antes* (spec, critérios, testes) é o que garante que o resultado bate com o
 que você queria — ver [[Spec-Driven Development]].
- **Contexto é o recurso escasso.** A IA só é boa no que está no contexto: repositório,
 convenções, dependências. Isso conecta direto com [[Janela de Contexto]] e
 [[Lost in the Middle]] (estudados na D2).
- **Humano no loop, em pontos definidos.** Não "revisar tudo no final": revisar em
 portões — spec aprovada, diffs pequenos, testes verdes.
- **Riscos concretos:** alucinação de APIs inexistentes (ver [[Alucinação]]), secrets
 vazados em prompt, prompt injection vinda de conteúdo externo que o agente lê
 (ver [[Prompt Injection]]), e código que funciona mas ninguém entende.
- **Agente = ferramenta com permissão.** Ele lê/escreve arquivos e roda comandos; o
 desenho das permissões faz parte do processo, não é detalhe de configuração.

## Na prática — o ciclo que funciona

1. **Spec curta** — problema, critérios de aceite, o que está fora do escopo.
2. **Plano** — arquivos prováveis, comandos de verificação (test/lint).
3. **Execução em fatias pequenas** — diff por diff, nunca a feature inteira de uma vez.
4. **Verificação automática** — testes e linters rodam antes da revisão humana.
5. **Revisão humana do diff** — lê o código como se fosse de terceiros (porque é).

> Neste projeto, este ciclo aparece combinado com [[Spec-Driven Development]] na
> fase de arquitetura e com [[Agent Skills]] na fase de UI.

## Autoavaliação
- [ ] Explicar a diferença entre *sugestão*, *par de programação* e *agente* sem usar as palavras "mágico" ou "mágica".
- [ ] Citar 3 riscos reais de desenvolver com IA e um controle para cada um.
- [ ] Dizer o que é o "gargalo atual" (e por que não é mais gerar código).
- [ ] Apontar onde o humano entra no ciclo de 5 passos acima — e o que acontece se ele sair.
- [ ] Relacionar: por que uma spec curta melhora o resultado de um agente?

## Ver também

- [[Spec-Driven Development]] · [[Prompt Engineering - fundamentos]] · [[Agent Skills]]
- [[N8N]] · [[Mastra]] · [[OpenCode]] · [[Ambiente de Desenvolvimento com IA]]
- [[Alucinação]] · [[Prompt Injection]]
