---
title: "OpenCode"
tags:
  - "conceito"
  - "opencode"
  - "ferramentas"
tipo: "conceito"
date: "2026-10-15"
---


# OpenCode

> **Meta:** explicar o que é o OpenCode (agente de código aberto no terminal, BYOK) e
> citar 3 recursos dele que mudam a prática: provedores, skills e permissões.

## O que é

O **OpenCode é um agente de programação de código aberto que roda no terminal** —
uma interface onde você conversa com um modelo de linguagem que **lê, edita arquivos e
executa comandos** no seu projeto. Ele não vende modelo: você conecta o **provedor que
quiser** (API paga, tier gratuito, modelo local), daí o nome do item do projeto —
*"não possui uma IA paga? conheça o OpenCode"*.

## Por que importa (aqui e no projeto)

- Foi a **ferramenta indicada neste projeto** para quem não tem assinatura de IA
 paga — o projeto foi desenhado para rodar com ele.
- É o caso concreto deste projeto: o [[Ambiente de Desenvolvimento com IA]] no qual
 ele vive, as [[Agent Skills]] que o estendem, e o fluxo de
 [[Desenvolvimento de Software com IA]] que ele executa.
- **Open ≠ grátis:** o *software* é aberto e gratuito; o *modelo* conectado pode ter
 custo — separar as duas coisas evita surpresa na fatura.

## Ideias-chave

- **Arquitetura agente + provedor.** O agente (loop de ler contexto → escolher ação →
 executar → observar resultado) é o OpenCode; o cérebro (o LLM) vem de fora —
 Anthropic, OpenAI, provedores com tier grátis, modelos locais.
- **BYOK — *bring your own key*.** A conta de modelo é sua, configurada por provedor;
 trocar de modelo é trocar de configuração, não de ferramenta (ver [[Ambiente de Desenvolvimento com IA]]).
- **Permissões explícitas.** O agente pede aprovação para ações de risco conforme o
 modo — a confiança é escalonada, não total de cara.
- **Skills estendem o agente** — o mesmo mecanismo da nota [[Agent Skills]]: instruções
 especializadas no projeto, carregadas sob demanda.
- **Configuração no próprio repositório** (regras de agente, preferências) faz o
 comportamento viajar com o código — mesma lógica do [[Spec-Driven Development]].
- **Sessões e histórico** permitem retomar contexto depois; ainda assim, o contexto é
 finito ([[Janela de Contexto]]) — sessão limpa muitas vezes rende mais que uma
 conversa de 40 turnos.

## Na prática — primeira execução segura

1. Instalar e abrir no terminal dentro do repositório.
2. Configurar o provedor (chave ou tier gratuito) — credencial fora do git.
3. Conferir o modo de permissão (o que ele pode sozinho).
4. Commit de segurança (ver [[Ambiente de Desenvolvimento com IA]]).
5. Pedir uma tarefa **pequena e verificável** primeiro ("rode os testes e resuma o que falha") —
 calibre a confiança antes de entregar algo grande.

## Autoavaliação
- [ ] Explicar a diferença entre *código aberto do agente* e *custo do modelo*.
- [ ] Descrever o loop agente (ler → agir → observar) com suas palavras.
- [ ] Nomear 3 recursos do OpenCode relevantes para o seu fluxo e para que serve cada um.
- [ ] Dizer o que é BYOK e onde a credencial deve ficar.
- [ ] Justificar por que uma tarefa pequena e verificável é o primeiro pedido certo.

## Ver também

- [[Ambiente de Desenvolvimento com IA]] · [[Agent Skills]]
- [[Desenvolvimento de Software com IA]] · [[Spec-Driven Development]] · [[Prompt Engineering - fundamentos]]
