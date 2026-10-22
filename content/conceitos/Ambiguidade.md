---
title: "Ambiguidade"
tags:
  - "conceito"
  - "falhas"
  - "ambiguidade"
  - "prompt"
tipo: "conceito"
date: "2026-10-29"
---

# Ambiguidade

> **Definição em uma frase:** uma entrada ou saída que admite mais de uma leitura
> válida; o modelo escolhe uma delas e a resposta pode não ser a que foi pedida.

## Explicação curta

Ambiguidade não é o modelo "errar o fato" — é o pedido **não determinar** qual resposta
é a correta. Duas pessoas (ou duas execuções) podem interpretar o mesmo texto de formas
diferentes e ambas conseguem defender que responderam ao pedido.

Na [[Alucinação e comportamentos]], o bullet associa ambiguidade a **prompt
ruim** — "geralmente", não sempre. É a falha mais barata de corrigir: muitas vezes o
problema está na pergunta, não no modelo.

Na [[Erros Inerentes à Arquitetura]], o recorte é explícito: **ambiguidade do
pedido** — a formulação do input não determina a resposta correta. Não é a ambiguidade da
linguagem natural em geral, embora essa seja a razão pela qual o pedido consegue ser
ambíguo.

## Os três lugares onde a ambiguidade aparece

| Lugar | Exemplo | Quem resolve |
| --- | --- | --- |
| **No pedido** | "faça um resumo das vendas" — resumo de quê? para quem? em quanto espaço? | quem escreve o prompt |
| **No domínio** | "média de vendas por mês" — média por venda, por dia ou total do mês? | quem conhece a regra de negócio |
| **Na saída** | texto que pode ser lido como recomendação ou como constatação | formato/estrutura da resposta |

## Por que acontece

- Linguagem natural é **subespecificada** por natureza: o modelo precisa preencher
  lacunas para continuar o texto.
- O modelo **resolve a ambiguidade sozinho**, escolhendo a continuação mais provável —
  não pergunta "o que você quis dizer?" por padrão.
- Falta de **exemplo de saída**: sem um modelo do formato desejado, cada execução inventa
  um critério.
- [[Perda de Contexto]] pode criar ambiguidade retroativa: a regra que resolvia o pedido
  estava no histórico e sumiu.

## Como detectar

1. **Teste das duas respostas:** dá para responder de duas formas e ambas "cabem" no
   pedido? Então há ambiguidade.
2. **Teste da paráfrase:** reescrever o pedido sem mudar o sentido muda a resposta? Se
   muda, o critério não estava no pedido.
3. **Perguntar o critério:** "o que faria uma resposta ser considerada errada?" Se não há
   resposta objetiva, o prompt está aberto demais.

## Como mitigar

| Controle | O que fazer |
| --- | --- |
| **Especificar o contrato** | dizer objetivo, público, formato, tamanho e o que **não** fazer |
| **Dar exemplo** | um exemplo de entrada/saída vale mais que um adjetivo ("resumo curto") |
| **Saída estruturada** | schema obriga campos e reduz interpretações livres |
| **Pedir clarificação** | instruir o modelo a perguntar quando faltar dado crítico |
| **Testar com paráfrases** | o mesmo pedido escrito de 3 jeitos deve produzir a mesma decisão |

> Ambiguidade se combate **antes** da inferência. Depois que o modelo escolheu uma
> leitura, o máximo que se faz é detectar e corrigir — não "desambiguar" a resposta.

## Exemplo

"Faça um resumo das vendas" pode significar: (a) total por mês; (b) média por venda;
(c) comparação com o mês anterior; (d) texto executivo para a diretoria. Quatro respostas
defensáveis, uma pergunta. O modelo não errou o cálculo — ele respondeu a uma pergunta
que não estava escrita.

## Confusões e aparências

- ❌ **Não é** imprecisão: a resposta pode ser exata para uma das leituras.
- ❌ **Não é** [[Alucinação]]: não há fato inventado; há critério ausente.
- ✅ **É** ausência de contrato: o pedido não define o que conta como resposta correta.

## Autoavaliação
1. **P:** Por que "seja mais específico no prompt" não é resposta suficiente? **R:** porque
   especificidade sem **critério de correção** só aumenta o texto; o que resolve é definir
   o que a saída precisa conter e como será validada.
2. **P:** Como ambiguidade e inconsistência se relacionam? **R:** uma pergunta ambígua
   permite que cada execução escolha uma leitura — o resultado aparece como
   [[Inconsistência]] entre execuções.

## Onde vi isso

- Visto em: [[Alucinação e comportamentos]] · [[Erros Inerentes à Arquitetura]] · [[Ambiguidade e riscos na IA]]
- Aprofundamento: [[Engenharia de prompt e contexto]]

## Ver também

- [[Inconsistência]] · [[Perda de Contexto]] · [[Alucinação]] · [[Alucinação e comportamentos]]

---
*Atualizado em 2026-10-22*
