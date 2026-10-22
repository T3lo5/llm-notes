---
title: "Inconsistência"
tags:
  - "conceito"
  - "falhas"
  - "consistencia"
tipo: "conceito"
date: "2026-10-29"
---

# Inconsistência

> **Definição em uma frase:** a mesma entrada — mesma pergunta, mesmo contexto, mesmo
> dado — produz saídas diferentes, ou uma saída que se contradiz, sem que nada tenha
> mudado no mundo.

## Explicação curta

É a falha de **estabilidade**, não de factualidade. A resposta de hoje pode estar
"certa" e a de amanhã também — mas são incompatíveis entre si. O sintoma clássico é o
que eu anotei na [[Alucinação e comportamentos]]: **busco algo que antes
retornava de um jeito e agora retorna diferente**.

A definição acima é uma **interpretação minha** (o bullet não detalhava o
mecanismo). Ela cobre dois casos que vale separar:

| Tipo | O que é | Exemplo |
| --- | --- | --- |
| **Entre execuções** | a mesma entrada gera saídas diferentes em chamadas diferentes | o total do relatório muda de 10:00 para 10:05 |
| **Dentro da resposta** | a própria saída se contradiz | diz "12 vendas" no texto e "15" na tabela |

## Por que acontece

- **Amostragem probabilística:** o modelo escolhe o próximo token por distribuição; com
  [[Temperatura]] > 0, duas execuções podem seguir caminhos diferentes (ver
  [[Temperatura e previsibilidade]]).
- **Contexto diferente sem eu perceber:** histórico da conversa, ordem dos documentos,
  data/hora, resultados de ferramentas — qualquer mudança de entrada muda a saída.
- **Modelo ou prompt mudou:** versão do provedor, prompt editado, ferramenta com
  comportamento novo. A "mesma" chamada não é a mesma por baixo.
- **Ambiguidade não resolvida:** se a pergunta admite mais de uma leitura, cada execução
  pode escolher uma — ver [[Ambiguidade]]. Inconsistência e ambiguidade andam juntas.

## Como detectar

1. **Rodar duas vezes com a mesma entrada** e comparar campo a campo (não só o texto).
2. **Guardar a saída + versão do prompt + versão do modelo** — sem isso, não se sabe o
   que mudou.
3. **Checar contradição interna:** o número do resumo bate com o da tabela? A conclusão
   contradiz os dados citados?
4. **Perguntar o inverso:** "se eu repetir amanhã, o que garantiria o mesmo resultado?"

## Como mitigar

| Controle | O que faz | Limite |
| --- | --- | --- |
| **Temperatura 0** | concentra a amostragem no topo da distribuição | reduz, não elimina — o modelo ainda pode variar |
| **Saída estruturada + validação** | schema e regras conferem o resultado antes de entregar | não pega dois resultados válidos e diferentes |
| **Cache / idempotência** | mesma entrada reaproveita a mesma saída | não resolve conteúdo novo |
| **Fixar versão** | modelo e prompt versionados | o provedor pode descontinuar a versão |
| **[[Evals]] com repetição** | mede a variação entre execuções, não só a média | custo de N execuções por caso |

> Regra prática: **consistência é requisito de produto**, não detalhe de inferência. Se o
> usuário vê dois números diferentes para a mesma pergunta, ele para de confiar no
> sistema — mesmo que um dos dois esteja certo.

## Exemplo

No cenário do relatório de vendas: na segunda-feira o agente responde "média mensal de
R$ 42.300"; na terça, mesma pergunta e mesmo CSV, responde "R$ 38.900". Nenhum dado
mudou. Ele trocou a regra de agregação (média das vendas × média dos dias) sem avisar.
Não é alucinação de um fato: é **inconsistência de critério**.

## Confusões e aparências

- ❌ **Não é** [[Alucinação]]: a resposta pode estar factualmente correta e ainda assim
  ser inconsistente com a anterior.
- ❌ **Não é** "o modelo mudou de opinião": não há opinião — há amostragem e entrada.
- ✅ **É** um problema de **reprodutibilidade** e de contrato de saída.

## Autoavaliação
1. **P:** Por que temperatura 0 não garante consistência? **R:** ela reduz a variação da
   amostragem, mas não controla mudanças de contexto, versão do modelo, ferramentas ou
   critérios ambíguos — e o provedor não garante determinismo bit a bit.
2. **P:** Inconsistência e alucinação podem ocorrer juntas? **R:** sim — a mesma resposta
   pode inventar um dado e, na execução seguinte, inventar outro. O controle é diferente:
   fonte/validação para alucinação; fixação de critério e repetição para consistência.

## Onde vi isso

- Visto em: [[Alucinação e comportamentos]]
- Relacionado: [[Temperatura e previsibilidade]] · [[Alucinação]]

## Ver também

- [[Ambiguidade]] · [[Perda de Contexto]] · [[Temperatura]] · [[Evals]] · [[Alucinação e comportamentos]]

---
*Atualizado em 2026-10-22*
