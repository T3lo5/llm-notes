---
title: "Projeto: avaliação de caso de uso de IA"
tags:
  - "fundamentos"
  - "projeto"
tipo: "guia"
date: "2026-10-05"
---

# Projeto: avaliação de caso de uso de IA


## Resumo em 3 frases

1. O documento não é um protótipo — é uma **decisão documentada** de construir, não construir ou mudar de problema.
2. A estrutura é: diagnóstico com o framework → viabilidade → experimento de baixo custo → métrica antes/depois → recomendação.
3. Sem métrica de linha de base medida **antes**, não existe como provar que houve ganho.

## O documento

Cinco seções, nesta ordem:

### 1. Diagnóstico com o framework

As 8 perguntas de [[Framework de decisão estratégica]] respondidas, com a matriz de pontuação. Se alguma resposta crítica for "não", o projeto termina aqui — e isso é uma entrega válida.

### 2. Viabilidade

| Dimensão | O que verificar |
| --- | --- |
| Dados | volume, qualidade, permissão de uso |
| Técnica | qual abordagem serve (prompt, RAG, fine-tune — ) |
| Operacional | quem revisa, quanto custa |
| Legal/segurança | dado sensível sai do ambiente? |
| Dependência | o que acontece se o fornecedor mudar preço ou sair? |

### 3. Experimento de baixo custo

O **menor** teste que pode falsificar a hipótese. Não é um MVP — é um teste.

- Em vez de integrar ao sistema: um script e uma planilha.
- Em vez de 3 meses: 1 semana.
- Em vez de 200 usuários: 20 casos.

### 4. Métrica antes/depois

Medida **antes**, sem o sistema. Este é o passo que a maioria pula e é o que torna todo o resto verificável.

| | Métrica | Como medir |
| --- | --- | --- |
| Antes | tempo médio de atendimento | 50 casos cronometrados |
| Depois | mesmo cálculo, com IA | os mesmos 50 casos |

### 5. Recomendação

Três saídas possíveis, todas válidas:

- **Construir** — a hipótese se confirmou, o ganho cobre o custo
- **Não construir** — ganho insuficiente ou risco alto
- **Mudar o problema** — o caso é real, mas a abordagem está errada

> Recomendar "não construir" com boa fundamentação demonstra mais domínio do que recomendar "construir".

## Checklist do documento

- [ ] Caso de uso descrito em uma frase, **sem mencionar IA**
- [ ] Framework das 8 perguntas respondido
- [ ] Matriz de pontuação preenchida
- [ ] Viabilidade nas 5 dimensões
- [ ] Hipótese escrita com métrica, valor antes e valor depois
- [ ] Experimento definido com custo-teto e prazo
- [ ] Critério de abandono escrito **antes** de rodar
- [ ] Linha de base medida
- [ ] Recomendação: construir / não construir / mudar o problema
