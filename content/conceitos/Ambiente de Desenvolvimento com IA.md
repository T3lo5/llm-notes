---
title: "Ambiente de Desenvolvimento com IA"
tags:
  - "conceito"
  - "ambiente"
  - "ferramentas"
tipo: "conceito"
date: "2026-10-15"
---


# Ambiente de Desenvolvimento com IA

> **Meta:** listar as 5 peças mínimas de um ambiente de IA (terminal, chave de API,
> cliente do agente, repositório, verificação automática) e dizer onde cada credencial
> e custo vive.

## O que é

O **arranjo de ferramentas e configurações** que permite rodar um assistente de IA no
seu projeto: de onde sai o terminal, como o agente autentica nos modelos, o que ele
pode tocar e como você verifica o resultado. É o "preparando ambiente" do Projeto
Prático — a parte chata que decide se o resto funciona.

## As 5 peças mínimas

| Peça | Função | Exemplo no projeto |
| --- | --- | --- |
| **Terminal/CLI** | onde o agente vive | terminal do sistema + git |
| **Autenticação de modelo** | quem paga a conta | chave de API / OAuth / provedor gratuito |
| **Cliente do agente** | o programa que conversa e edita arquivos | [[OpenCode]] (a escolha do projeto) |
| **Repositório** | rede de segurança do que a IA mexe | git com commits limpos antes de começar |
| **Verificação** | como saber se está certo | testes, lint, build |

## Ideias-chave

- **Repositório antes de agente.** O primeiro comando não é pedir código, é garantir
  que um `git checkout` desfaz tudo — ver [[Desenvolvimento de Software com IA]].
- **Chave de API ≠ assinatura.** Nem todo acesso a modelo é pago: há camadas gratuitas,
  modelos abertos locais e provedores com tier grátis. O item "Não possui uma IA paga?"
  do projeto existe exatamente para isso — e o caminho indicado é o [[OpenCode]].
- **Custo mora no contexto, não na conversa.** Cada envio cobra os tokens do histórico
  (ver [[Token]] e [[Janela de Contexto]]) — ambiente bem configurado corta ruído, não
  corta qualidade.
- **Permissões são parte do ambiente.** Definir o que o agente pode executar sem
  perguntar (leitura, escrita, comandos) é configuração de segurança, não conforto.
- **Segredos nunca entram no prompt.** `.env` no gitignore; se um segredo foi para o
  contexto do modelo, ele já vazou — relaciona com [[Prompt Injection]].
- **Reprodutibilidade:** versões fixadas (lockfile, runtime) evitam "funciona na minha
  máquina" — o agente reproduz bugs do ambiente com a mesma facilidade que os seus.

## Na prática — setup mínimo do zero

1. Instalar git e um terminal confortável.
2. Escolher o acesso ao modelo (pago, tier grátis ou local) e guardar a credencial fora do repositório.
3. Instalar o cliente do agente — no projeto: [[OpenCode]].
4. `git init` (ou clonar) + commit do estado atual.
5. Rodar a **verificação de baseline** (testes/build verdes) **antes** da primeira
   interação — depois disso, qualquer vermelho veio da mudança.

## Autoavaliação
- [ ] Nomear as 5 peças do ambiente e a função de cada uma.
- [ ] Explicar por que o commit de segurança vem antes da primeira prompt.
- [ ] Dizer a diferença entre chave de API, assinatura e tier gratuito — com um exemplo de cada.
- [ ] Apontar onde uma credencial NUNCA deve aparecer.
- [ ] Justificar por que rodar os testes antes de começar muda a qualidade da revisão.

## Ver também

- [[OpenCode]] · [[Agent Skills]] · [[Desenvolvimento de Software com IA]]
- [[Token]] · [[Janela de Contexto]] · [[Prompt Injection]]
