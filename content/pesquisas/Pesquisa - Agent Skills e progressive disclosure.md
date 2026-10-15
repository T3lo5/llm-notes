---
title: "Pesquisa - Agent Skills e progressive disclosure"
tags:
  - "pesquisa"
  - "skills"
tipo: "pesquisa"
date: "2026-10-15"
---

# Pesquisa — Agent Skills e progressive disclosure

> **Pergunta que motivou esta pesquisa:** como dar conhecimento especializado a um
> agente sem estourar a janela de contexto — e o que faz uma skill disparar (ou
> nunca disparar)?

## Resposta curta (TL;DR)

Skill é **conhecimento no filesystem, carregado em três níveis**: (1) metadata
(`name` + `description`, ~100 tokens, **sempre** no contexto); (2) instruções do
`SKILL.md`, carregadas **só quando a skill dispara** (<5k tokens); (3) recursos —
referências e scripts — lidos **só quando referenciados** (custo zero até lá). O
mecanismo se chama **progressive disclosure** e é o antídoto direto do
[[Janela de Contexto]]: instalar 50 skills custa ~5k tokens; usadas, custam o que
cada tarefa exige. O campo que decide tudo é a `description` — ela precisa dizer
**o que a skill faz E quando usá-la**, porque é o que o modelo casa com o pedido.

## Resposta completa

### Os três níveis (tabela da própria documentação)

| Nível | O que é | Quando carrega | Custo em tokens |
| --- | --- | --- | --- |
| **1 · Metadata** | frontmatter YAML (`name`, `description`) | startup | ~100 por skill |
| **2 · Instruções** | corpo do `SKILL.md` | skill disparada | <5k |
| **3 · Recursos** | `FORMS.md`, `REFERENCE.md`, `scripts/*.py` | quando referenciados | 0 até acesso |

Detalhe que muda o jogo: **o código de um script nunca entra no contexto** — o
agente roda via bash e consome só a **saída**. Gerar o mesmo script de forma
iterativa custaria dezenas de milhares de tokens; executar um pronto custa o
stdout. Determinismo e economia no mesmo artefato.

### Anatomia (requisitos da documentação)

```markdown
---
name: pdf-processing                          # ≤64 chars, minúsculas/números/hífen
description: Extract text and tables from PDF  # ≤1024 chars; O QUE + QUANDO
                                               # ("Use when the user mentions...")
---
# PDF Processing
## Quick start ...
```

- `name`: restrito (sem "anthropic"/"claude", sem XML) — é identificador.
- `description`: **obrigatória e semântica** — se ela não contém o gatilho
  (sinônimos do que o usuário digita), a skill é um arquivo lindo que nunca abre.
- Struct: diretório = skill; arquivos irmãos são os recursos do nível 3.

### Onde roda (e o que isso implica)

- **Claude API**: skills sobem por `/v1/skills`, rodam em container **sem rede e
  sem instalação de pacotes** — dependências precisam vir pré-instaladas.
- **Claude Code**: skills são **filesystem-based** em `~/.claude/skills/`
  (pessoal) ou `.claude/skills/` (projeto) — versionáveis com o repositório.
- **claude.ai**: upload de zip; Pro/Max/Team/Enterprise com code execution.
- **Cross-surface não sincroniza** — skill subida na API não aparece no Claude
  Code. Cada superfície tem seu depósito.

### Segurança — a parte que todo mundo ignora

A documentação é explícita: *"treat like installing software"*. Skill maliciosa
= instrução que redireciona execução, exfiltra dados, faz chamadas de rede.
Recomendações oficiais: auditar todos os arquivos da skill, desconfiar de skills
que buscam conteúdo de URLs externas (o conteúdo buscado pode conter instruções —
ponte para [[Prompt Injection]]), restringir skills de terceiros em ambientes com
dados sensíveis. **Skill é código com permissão**, não documento.

## Detalhes técnicos

- **Descoberta**: no startup, o `description` de cada skill vai junto do system
  prompt; o modelo decide disparar com base no pare entre pedido e descrição —
  ativação é **busca semântica sobre a descrição**, não keyword exata (daí
  testar com sinônimos — ver [[Lab 02 - Escrevendo uma skill que ativa]]).
- **Templates vs scripts**: instrução flexível = markdown; operação
  determinística = script (só output entra); fato de consulta = arquivo de
  referência. Colocar fato em markdown é gastar tokens com texto que o modelo
  já "sabe peneirar"; colocar lógica em script é travar o que não deve variar.
- **Composição**: skills combinam — mas cada combinação disputa o nível 1; 200
  skills genéricas = ruído de discovery. Granularidade fina vence amplitude.

## Limitações e riscos

- **Ativação é probabilística.** Descrição ruim = nunca dispara; descrição
  larga demais = dispara fora de hora (dois modos de falha, mesma causa).
- **Skills não sincronizam entre superfícies** — manter duas cópias é drift
  garantido.
- **Ambiente restrito na API**: sem rede, sem `pip install` — a skill que assume
  internet quebra silenciosamente lá e funciona no Claude Code.
- **Fonte única.** A arquitetura é da Anthropic; OpenCode e outros implementam
  formatos parecidos mas não idênticos — conferir a docs do agente alvo
  ([[OpenCode]]).
- **ZDR não cobre Agent Skills** (aviso da própria docs) — dado sensível em
  skill é retenção de dado sensível.

## O que isso muda na minha prática

1. **Description é contrato de ativação** — escrever "Use ao <gatilho concreto>",
   nunca o nome da tarefa.
2. **Três camadas de instrução do agente**: regra sempre-ativa (piso, barato),
   comando/slash (invocação deliberada), skill (especializado sob demanda).
   Encaixar cada tipo no seu lugar — misturar tudo no system prompt é perder a
   progressive disclosure.
3. Script para o determinístico (linters, formatadores), markdown para o
   julgamento.
4. Auditar skill de terceiros como instalaria binário de terceiros.

## Fontes

- https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview — visão
  geral oficial: níveis, requisitos, segurança, limitações.
- https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
  — post de engenharia: arquitetura e aplicações.
- https://github.com/anthropics/skills — repositório de skills open-source.

## Perguntas abertas

- Granularidade ótima: 1 skill por capacidade estreita ou skill-padrão com
  seções? A docs diz "como um guia de onboarding" — onboarding de quanto?
- Skills vs **MCP**: conhecimento (skill) vs capability remota (MCP) — onde
  exatamente está a fronteira?
- Como testar ativação em CI — a skill é cobertura de qual suíte?

## Ver também

- [[Agent Skills]] · [[OpenCode]] · [[Janela de Contexto]]
- [[Prompt Injection]] · [[Prompt Engineering - fundamentos]]
- [[Lab 02 - Escrevendo uma skill que ativa]]
