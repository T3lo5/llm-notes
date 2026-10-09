---
title: "Escolha final e conclusão"
tags:
  - "selecao-de-modelos"
  - "conclusao"
  - "decisao"
tipo: "guia"
date: "2026-10-16"
---

# Escolha final e conclusão

> **Meta:** fechar a disciplina com o único achamento que sobrevive a tudo: **não existe o melhor modelo — existe o certo para o contexto certo**.


## Resumo em 3 frases

1. **Não existe o melhor modelo; existe o certo para o contexto certo** — e "contexto" é tarefa, volume, orçamento, latência e risco juntos, nunca um deles sozinho.
2. O caminho até essa conclusão foi um método: levantamento → categorias → 5 critérios → trade-offs → lock-in → benchmarks → estratégia híbrida.
3. A conclusão vira prática: **eval no seu domínio, conta no seu volume, plano de troca documentado e data de revisão** — escolha auditável, nunca definitiva.

## A síntese do percurso

| Etapa | Pergunta que respondeu | Ferramenta |
| --- | --- | --- |
| Levantamento (21) | o que a aplicação exige? | tarefa, volume, orçamento, tolerância a erro |
| Mito do melhor modelo (22) | existe vencedor absoluto? | não — adequação é contextual |
| Categorias (23) | que opções existem? | frontier, intermediário, open-weight |
| Critérios (24) | o que medir? | qualidade, custo, latência, confiabilidade, risco |
| Trade-offs (25) | como decidir? | crítica → cara; volume → barata; linha de decisão escrita |
| Lock-in (26) | como não ficar preso? | interface única, formatos abertos, evals de troca |
| Benchmarks (27) | como comparar de verdade? | dados reais, estatística séria, variações cobertas |
| Híbrida (28) | e se nenhum sozinho resolve? | barato por padrão, caro no estritamente necessário |

## O checklist final da escolha

- [ ] **Levantamento escrito** — tarefa, volume, orçamento, latência, tolerância a erro.
- [ ] **Eval no seu domínio** — comparando pelo menos dois candidatos, com dados reais e repetição.
- [ ] **Conta no seu volume** — custo/mês com o preço in/out e o volume real, não o preço por token isolado.
- [ ] **Plano de troca** — camada de acesso, prompts genéricos, evals que o substituto precisa passar (ver [[Vendor lock-in]]).
- [ ] **Data de revisão** — preço muda, modelos novos aparecem; a escolha vale até o gatilho definido.
- [ ] **Gate de risco** — o que vai para modelo caro ou humano, com o custo do erro em número.

## O que muda na prática

- Decisão de modelo deixa de ser discussão de preferência e vira **documento auditável**: critérios, números, alternativa descartada.
- **Multi-modelo vira o padrão**, não exceção — a arquitetura assume troca desde o início.
- Revisão periódica deixa de ser esforço extra e vira rotina — o mercado se move mais rápido que o contrato.

> **Conclusão da disciplina:** o "melhor modelo" é uma pergunta sem resposta; "qual modelo para **este** contexto" é uma pergunta com método. O que separa as duas é exatamente o trabalho das aulas anteriores.

## Perguntas para validar

1. Reformule a conclusão "não existe o melhor modelo" com o que "contexto certo" significa na prática.
2. Por que a escolha precisa de data de revisão — o que justifica isso economicamente e tecnicamente?
3. Se a arquitetura não previu troca (sem camada de acesso, sem evals), o que a conclusão muda para o projeto?

## Ver também

- [[Seleção de modelos: por onde começar]] · [[Vendor lock-in]] · [[Benchmark]] · [[Roteamento de modelos]] · [[Pesquisa - Custo e qualidade na seleção de modelos]]
