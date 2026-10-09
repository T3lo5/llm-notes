---
title: "Lab 03 - Workflow N8N mínimo"
tags:
  - "lab"
  - "n8n"
tipo: "lab"
date: "2026-10-15"
---

# Lab 03 — Workflow N8N mínimo: contrato de dado e caminho de erro

> **O que este lab prova:** que num workflow o dado muda de shape a cada nó e o
> contrato só existe onde você **inspecionou**; e que sem caminho de erro
> desenhado, a falha é silenciosa.

## Pergunta

Onde um workflow de 4 nós quebra quando a entrada muda de forma — e o que o
Execution Inspector mostra que o desenho esconde?

## Hipótese

> Inserir um item sem `sku` (ou com `preco` negativo) na fonte de dados **não
> derruba o workflow**: ele segue pelo caminho de erro desenhado (saída 2 do nó
> de código) e o item aparece em "Revisão manual" com o motivo. Se o caminho de
> erro não existisse, o mesmo item entraria no banco sujo — ou sumiria sem
> aviso, dependendo da lógica implícita.

## Setup

Self-host local (a licença é fair-code — grátis na sua máquina):

```bash
docker run -it --rm -p 5678:5678 -v n8n_data:/home/node/.n8n docker.n8n.io/n8nio/n8n
# ou sem docker:  npx n8n
```

Abrir `http://localhost:5678`.

## Código

**Workflow JSON** — importar em *Workflows → Import from File/Clipboard*:

```json
{
  "name": "Lab 03 - Normaliza produtos",
  "nodes": [
    { "parameters": {}, "id": "n1", "name": "Manual Trigger", "type": "n8n-nodes-base.manualTrigger", "typeVersion": 1, "position": [0, 0] },
    { "parameters": { "jsCode": "const brutos = $input.all();\nconst validos = [];\nconst problemas = [];\nfor (const item of brutos) {\n  const p = item.json;\n  const sku = String(p.sku ?? '').trim();\n  const preco = Number(p.preco);\n  if (!sku || !Number.isFinite(preco) || preco <= 0) {\n    problemas.push({ json: { motivo: !sku ? 'sku vazio' : 'preco invalido', recebido: p } });\n  } else {\n    validos.push({ json: { sku, preco, titulo: String(p.titulo ?? '').trim() } });\n  }\n}\nreturn [validos, problemas];" }, "id": "n2", "name": "Normaliza e separa", "type": "n8n-nodes-base.code", "typeVersion": 2, "position": [220, 0] },
    { "parameters": {}, "id": "n3", "name": "Insere no banco", "type": "n8n-nodes-base.noOp", "typeVersion": 1, "position": [440, -80] },
    { "parameters": {}, "id": "n4", "name": "Revisao manual", "type": "n8n-nodes-base.noOp", "typeVersion": 1, "position": [440, 80] }
  ],
  "connections": {
    "Manual Trigger": { "main": [[ { "node": "Normaliza e separa", "type": "main", "index": 0 } ] ] },
    "Normaliza e separa": { "main": [[ { "node": "Insere no banco", "type": "main", "index": 0 } ], [ { "node": "Revisao manual", "type": "main", "index": 0 } ] ] }
  }
}
```

O nó de código devolve **dois arrays**: `main[0]` = válidos (normalizados),
`main[1]` = inválidos (com motivo). Duas saídas = dois caminhos = contrato de
erro visível no desenho.

## Como rodar

1. Importar o JSON e **Execute Workflow**.
2. Fonte de dados: no nó *Normaliza e separa*, trocar `$input.all()` por um
   array fixo para testar:
   ```js
   const brutos = [
     { json: { sku: 'A-100', preco: 199.9, titulo: 'Fone bluetooth' } },
     { json: { sku: '',     preco: 89.0,  titulo: 'Sem sku' } },
     { json: { sku: 'B-200', preco: -5,    titulo: 'Preco negativo' } },
   ];
   ```
3. **Execution Inspector** (ícone da execução): abrir a saída de *cada* nó —
   ler o shape real: o que saiu do gatilho ≠ o que sai do código ≠ o que o
   *Insere no banco* receberia.
4. Quebrar de propósito: renomear a saída para `return validos;` (1 saída só) →
   item inválido cai no caminho errado. Desfazer.

## O que observei

- Payload do gatilho: itens crus, campos faltando são `undefined`.
- Saída 1 do código: shape **novo** (`sku` trimado, `preco` numérico) — o
  contrato foi criado aqui.
- Saída 2: `{ motivo, recebido }` — **o erro virou dado**, inspecionável.
- Sem caminho 2: o item inválido não aparecia em lugar nenhum (o "sumiu" que a
  hipótese previa).

## Análise

- **Contrato por inspeção, não por fé**: o desenho mostra intenção; o inspector
  mostra realidade (ver [[Pesquisa - Automação de workflows com N8N]]).
- **Erro como item**: falhou → vira item com motivo no caminho certo. O
  silêncio é o bug clássico de automação.
- **Fronteira com o agente**: normalização/roteamento ficam aqui (determinístico);
  "o que fazer com o item problemático" poderia ser uma chamada de agente
  ([[Mastra]]) — o caminho de erro é o ponto de encontro dos dois mundos.
- **O JSON é o artefato versionado** do fluxo — git nele
  ([[Spec-Driven Development]]).

## Extensão (o que eu faria com mais tempo)

- Trocar *Insere no banco* por nó HTTP Request com **retry** (e observar a
  diferença para o NoOp diante de 500 do alvo).
- Fonte real: substituir o Manual Trigger por cron/webhook e um HTTP Request
  (com proxy anti-bloqueio quando o alvo tem anti-bot — a lição do projeto).
- Error workflow global: um workflow dedicado que capta falhas de todos os
  outros.

## Conceitos tocados

- [[Mastra]]

## Erros que cometi

- Assumir que "rodou verde" = dado certo — o workflow roda verde **com shape
  errado** (o `undefined` viaja calado até o nó final).
- Escrever a lógica de erro *depois* do primeiro apagão — caminho de erro é
  desenho, não manutenção.
- Deixar `$json` implícito em expression e não entender por que `preco` era
  `undefined` no nó seguinte: a saída é de **cada nó**, não global.

---
*Lab criado em 2026-10-08*
