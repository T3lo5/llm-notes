# AGENTS — llm-notes

Site público de notas de estudo (Quartz) exportadas de um vault pessoal do Obsidian.

- **Exportação:** `scripts/exportar.py` copia notas do vault (`LLM_NOTES_VAULT=...`) para `content/` e gera `quartz/static/dados/questions.json`.
- **Allowlist:** só entra no site o que está em `NOTAS_PUBLICAS` (aulas) e nos bancos de `BANCOS` (questões). Tudo que não está na allowlist é convertido em texto simples (links desfazem).

## Diretriz de direitos autorais (obrigatória — 2026-10-09)

**Nada publicado aqui pode replicar material do curso com autoria da pós.** Em particular:

- ❌ **Enunciados** de projetos/micro-capstones (texto integral ou paráfrase fiel que reproduza escopo, entregáveis, métricas e critérios de aceitação do enunciado original)
- ❌ Qualquer menção à **pós**, à **Cod3rs/coders** ou ao **capstone como enunciado** do curso
- ❌ Transcrição de material didático (videos, PDFs, listas de exercícios, avaliações)

✅ **Permitido:** publicar um **lab parecido** — o próprio tema com enunciado autoral, escopo e critérios próprios, sem copiar o original. As guias de aulas são resumos/redações próprias do estudante sobre os conceitos, sem reproduzir o material.

**Teste antes de adicionar em `NOTAS_PUBLICAS`:** se a nota citar "pós", "Cod3rs" ou contiver o enunciado de um capstone/projeto do curso, ela **não publica** — reescreva como lab autoral ou mantenha só no vault.

Nota afetada: `Aula 30 - Micro Capstone - IA para SaaS` (enunciado do curso) fica **excluída da allowlist permanentemente**.
