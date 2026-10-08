---
title: "Lab 02 - Escrevendo uma skill que ativa"
tags:
  - "lab"
  - "skills"
tipo: "lab"
date: "2026-10-15"
---

# Lab 02 — Escrevendo uma skill que ativa

> **O que este lab prova:** que a `description` da skill — e só ela — decide a
> ativação; que o corpo da skill custa zero tokens até disparar; e que skill boa
> **também sabe não ativar** fora do escopo.

## Pergunta

O que separa uma skill que dispara de uma que nunca vê a luz — e como saber que
ela não está disparando demais?

## Hipótese

> Skill com `description` contendo **gatilho concreto** ("use quando o usuário
> pedir X, Y ou Z") ativa em **3/3 pedidos indiretos** (sinônimos, sem citar a
> palavra-chave). A mesma descrição genérica ("ajuda com documentação") ativa em
> **≤1/3**. E nos 2 casos **fora do escopo**, ambas **não devem ativar** —
> ativação errada é falha tão séria quanto não-ativação.

## Setup

Sem instalação obrigatória: um agente com suporte a skills no projeto
([[OpenCode]], Claude Code) e o linter em Python abaixo (stdlib puro).

```bash
mkdir -p .agents/skills/changelog
```

## Código

**`changelog/SKILL.md` — a skill do experimento:**

```markdown
---
name: changelog
description: Escreve e padroniza entradas de CHANGELOG (Keep a Changelog, semântica
 de versões). Use quando pedirem para gerar, revisar ou reescrever o changelog,
 resumir commits em notas de versão, ou preparar release notes.
---

# Changelog

## Formato
- Seções: Added / Changed / Fixed / Removed — em inglês, mesmo com texto PT-BR.
- Uma linha por mudança; começa com verbo no passado ("Adicionou", "Corrigiu").
- Referência a issue: `(#123)` no fim da linha.

## Proibido
- Advérgios de marketing ("incrível", "revolucionário").
- Mudanças internas sem efeito para quem usa (refatoração pura).

## Exemplo
### Added
- Exportação do relatório em CSV (#214)
```

**`lint_skill.py` — valida as regras da plataforma:**

```python
# lint_skill.py <caminho do SKILL.md>
import re, sys
from pathlib import Path

p = Path(sys.argv[1])
texto = p.read_text(encoding="utf-8")
falhas = []

m = re.match(r"^---\n(.*?)\n---", texto, re.S)
if not m:
 falhas.append("frontmatter ausente"); fm = ""
else:
 fm = m.group(1)

nome = re.search(r"^name:\s*(.+)$", fm, re.M)
desc = re.search(r"^description:\s*(.+?)(?=\n\w+:|\Z)", fm, re.S | re.M)

if not nome:
 falhas.append("name obrigatorio")
else:
 n = nome.group(1).strip()
 if len(n) > 64: falhas.append(f"name com {len(n)} chars (max 64)")
 if not re.fullmatch(r"[a-z0-9-]+", n): falhas.append("name: so minusculas, numeros, hifen")

if not desc:
 falhas.append("description obrigatoria")
else:
 d = " ".join(desc.group(1).split())
 if len(d) > 1024: falhas.append(f"description com {len(d)} chars (max 1024)")
 if not re.search(r"\b(use quando|when|use when|use ao|use em)\b", d, re.I):
 falhas.append("description sem gatilho de ativacao (diga QUANDO usar)")

print("\n".join(falhas) if falhas else "ok")
sys.exit(1 if falhas else 0)
```

## Como rodar

1. `python3 lint_skill.py .agents/skills/changelog/SKILL.md` → deve dar `ok`.
2. **Teste de ativação** — 5 pedidos, sessão nova cada um, registrar ✓/✗:

| # | Pedido | Escopo? | Esperado |
| --- | --- | --- | --- |
| 1 | "Escreva o changelog dos últimos commits" | ✔ | ativa |
| 2 | "Prepara as notas de release dessa versão" (sem dizer changelog) | ✔ | ativa |
| 3 | "Resume os commits pro email do time" (sinônimo distante) | ✔ | ativa? |
| 4 | "Me ajuda com o README" | ✘ | **não** ativa |
| 5 | "Qual a previsão do tempo?" | ✘ | **não** ativa |

3. **Teste de custo**: peça a lista de skills carregadas (ou observe o startup)
 e confirme que até disparar, só `name` + `description` entram no contexto.
4. **Iteração**: o pedido 3 falhou? Reescreva **só a description** (o corpo
 intocado) e repita — uma variável por rodada.

## O que observei

| Pedido | Ativou? | O quê entrou no contexto |
| --- | --- | --- |
| 1 | | SKILL.md inteiro |
| 2 | | |
| 3 | | |
| 4 | | só metadata (esperado) |
| 5 | | só metadata (esperado) |

## Análise

- **Ativação é pare entre descrição e pedido** — sinônimo ("release notes") é o
 teste real; palavra-chave exata prova pouco.
- **Não-ativação correta é resultado**: pedido 4/5 sem ativação = a skill não
 virou "ajuda geral". Ver [[Pesquisa - Agent Skills e progressive disclosure]].
- **Custo em camadas**: metadata ~100 tokens sempre; corpo só ao disparar — a
 mesma economia de [[Janela de Contexto]] aplicada a instrução.

## Extensão (o que eu faria com mais tempo)

- Medir taxa de ativação com 10 pedidos antes/depois da reescrita da
 description (o lab vira experimento de verdade).
- Adicionar `scripts/validate.py` à skill e testar o nível 3 (só o output
 entra no contexto).
- Portar a skill para outra plataforma e comparar o formato do gatilho.

## Conceitos tocados

- [[Prompt Engineering - fundamentos]]

## Erros que cometi

- Escrever description só com **o que** ("gera changelog") e passar dias sem
 ativação — o **quando** é metade do campo.
- Testar os pedidos na **mesma sessão**: depois do 1º, o contexto já tinha a
 skill, e "ativação" era memória da conversa.
- Fazer a skill fazer **coisa demais** (changelog + README + commits) — virou
 ativação em tudo, que é ativação em nada.

---
*Lab criado em 2026-10-08*
