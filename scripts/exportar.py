#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exporta o conteudo publico do vault Obsidian para o site Quartz.

Gera:
  content/         .md com frontmatter normalizado (sem prefixo de pasta)
  quartz/static/dados/questions.json   banco de questoes servido via fetch()
  content/questoes.md                   pagina do quiz, vinda de templates/

Fonte:  o vault Obsidian, configurado em VAULT (ou a variavel CODERS_VAULT)
Destino: a raiz deste repositorio (ou a variavel LLM_NOTES_DIR)

Regra de inclusao: so entram arquivos com `publicar: true` no frontmatter,
ou que estejam nas pastas listadas em PUBLIC_DIRS.

O vault e privado e nao entra no repositorio. A exportacao roda so na sua
maquina; o CI apenas executa `npx quartz build` sobre o `content/` versionado.
"""

import json
import os
import re
import shutil
import sys
import unicodedata
from datetime import datetime, timezone

SITE = os.environ.get("LLM_NOTES_DIR") or os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)
VAULT = os.environ.get("CODERS_VAULT") or os.path.expanduser(
    "~/Documentos/coders-pos/coders-pos"
)
CONTENT = os.path.join(SITE, "content")
# quartz/static/** e copiado para public/static/** pelo build, entao o JSON
# fica acessivel por fetch() sem depender do roteamento de paginas.
STATIC_DATA = os.path.join(SITE, "quartz", "static", "dados")
TEMPLATES = os.path.join(SITE, "templates")

M01 = "02 - Módulos/M01 - Funcionamento de Modelos de Linguagem"

# Preenchido em main() com as notas que foram exportadas, para que o
# reescritor de referencias saiba o que virou link e o que virou texto.
pares_global = []

# Pastas que entram no site, sem filtro de frontmatter.
# Contexto de conteúdo: LLMs e engenharia. Fora: curso, diário, trabalhos.
PUBLIC_DIRS = [
    f"{M01}/02 Conceitos",
    f"{M01}/03 Pesquisas",
    f"{M01}/04 Labs",
    "03 - Acervo",
]

# Arquivos publicados mesmo fora dessas pastas.
PUBLIC_FILES = [
    f"{M01}/07 Mapas/Mapa - Funcionamento de LLMs.md",
]

# Nunca publicar, mesmo dentro de PUBLIC_DIRS.
NEVER = {
    "Como ler um paper.md",   # metodo pessoal, nao conteudo
    # O indice de papers e o plano de leitura do curso: traz a trilha dos 12
    # modulos e o que cada um exige. E conteudo do curso, nao conteudo tecnico.
    "Índice de papers.md",
}

# Pasta do site para cada pasta do vault. O valor e (slug, titulo, descricao):
# o slug vira o caminho, o titulo e a descricao viram o index da pasta.
PASTAS_SITE = {
    f"{M01}/02 Conceitos": (
        "conceitos",
        "Conceitos",
        "Uma ficha por termo. O que é, por que importa e onde costuma ser mal entendido.",
    ),
    f"{M01}/03 Pesquisas": (
        "pesquisas",
        "Pesquisas",
        "Aprofundamentos com fonte primária: o que um paper resolveu, e o que é só otimização de constante.",
    ),
    f"{M01}/04 Labs": (
        "labs",
        "Labs",
        "Experimentos com código que testam uma hipótese. Cada lab diz o que ele prova e onde falha.",
    ),
    "03 - Acervo": (
        "papers",
        "Papers",
        "Resumos dos papers que sustentam as fichas de conceito, com o resultado principal de cada um.",
    ),
}

# Título e descrição do índice de cada pasta, injetados na build.
INDICES_PASTA = {}


# --------------------------------------------------------------- frontmatter
def ler_frontmatter(texto):
    """Devolve (dict, corpo) ou ({}, texto) se nao houver frontmatter."""
    if not texto.startswith("---"):
        return {}, texto
    fim = texto.find("\n---", 3)
    if fim == -1:
        return {}, texto
    bloco = texto[3:fim]
    corpo = texto[fim + 4:].lstrip("\n")
    dados, atual = {}, None
    for linha in bloco.split("\n"):
        if not linha.strip():
            continue
        # item de lista, continuando a chave aberta
        if linha.startswith((" ", "\t", "- ")) and atual:
            # a chave pode ter sido declarada sem valor ("tags:"), caso em que
            # ainda é string. Só vira lista quando aparece o primeiro item.
            if not isinstance(dados.get(atual), list):
                dados[atual] = []
            dados[atual].append(linha.strip().lstrip("- ").strip())
            continue
        if ":" in linha:
            chave, _, valor = linha.partition(":")
            chave = chave.strip()
            valor = valor.split("#")[0].strip() if "#" in valor else valor.strip()
            if valor.startswith("[") and valor.endswith("]"):
                valor = [v.strip().strip("\"'") for v in valor[1:-1].split(",") if v.strip()]
            elif valor.lower() in ("true", "false"):
                valor = valor.lower() == "true"
            dados[chave] = valor
            atual = chave
    return dados, corpo


def normalizar_frontmatter(caminho_rel, dados):
    """Frontmatter limpo para o Quartz: so o que ele usa."""
    nome = os.path.splitext(os.path.basename(caminho_rel))[0]
    pasta = os.path.dirname(caminho_rel)

    tags = dados.get("tags") or []
    if isinstance(tags, str):
        tags = [tags]
    tags = [str(t).strip() for t in tags if str(t).strip()]
    # Tags de modulo (m01, pos) e a tag generica do curso nao descrevem o
    # conteudo tecnico e expoem a estrutura da turma. Fica so o que a nota e.
    tags = [
        t for t in tags
        if not re.fullmatch(r"(m\d+|pos|modulo|módulo)", t, re.I)
    ]

    tipo = dados.get("tipo", "conceito")

    # o title do frontmatter vence o nome do arquivo, para os templates
    # (index, questoes) poderem ter um titulo propio
    titulo = dados.get("title") or nome

    fm = {"title": titulo, "tags": tags}

    desc = dados.get("descricao") or dados.get("description")
    if desc:
        fm["description"] = desc

    if tipo:
        fm["tipo"] = tipo

    # data de atualizacao, util para ordenar no site
    atualizado = dados.get("revisar") or dados.get("criado") or dados.get("atualizado")
    if isinstance(atualizado, str) and re.match(r"^\d{4}-\d{2}-\d{2}$", atualizado):
        fm["date"] = atualizado

    return fm, pasta


def render_yaml(fm):
    linhas = ["---"]
    for chave, valor in fm.items():
        if isinstance(valor, list):
            linhas.append(f"{chave}:")
            for v in valor:
                linhas.append(f"  - {json.dumps(v, ensure_ascii=False)}")
        elif isinstance(valor, bool):
            linhas.append(f"{chave}: {str(valor).lower()}")
        else:
            linhas.append(f"{chave}: {json.dumps(valor, ensure_ascii=False)}")
    linhas.append("---")
    return "\n".join(linhas)


# --------------------------------------------------------------- questoes
def gabarito_de_tabela(corpo):
    """Secao 'Gabarito em uma linha' com | N | resposta |."""
    mapa = {}
    m = re.search(r"##\s*Gabarito.*?\n(.*?)(?=\n##\s|\Z)", corpo, re.S)
    if not m:
        return mapa
    for linha in m.group(1).split("\n"):
        if not linha.strip().startswith("|"):
            continue
        cel = [c.strip() for c in linha.strip().strip("|").split("|")]
        if len(cel) == 2 and cel[0].isdigit():
            mapa[int(cel[0])] = cel[1]
    return mapa


def questoes_formato_heading(texto, modulo, origem):
    """
    Formato do M01: heading '### Qn · `D` · [[Aula ...]]' seguido da
    pergunta em prosa.

    O gabarito vem num <details><summary>Gabarito</summary>. Ele e extraido
    para o campo `resposta` — deixar no corpo faria o gabarito aparecer
    aberto na pagina, estragando o exercicio.
    """
    linhas = texto.split("\n")

    questoes = []
    i = 0
    while i < len(linhas):
        m = re.match(r"^#{2,4}\s*Q(\d+)\s*·\s*`([FMD])`\s*·\s*\[\[(.+?)\]\]", linhas[i])
        if not m:
            i += 1
            continue

        num = int(m.group(1))
        nivel = {"F": "facil", "M": "media", "D": "dificil"}[m.group(2)]
        aula = m.group(3).strip()
        i += 1

        # enunciado: paragrafos ate a proxima heading Q ou de secao.
        # Uma heading de secao (## Conceituais, ## Autoavaliacao) tambem
        # encerra a questao, senao ela vaza para o texto seguinte.
        partes = []
        while i < len(linhas):
            l = linhas[i]
            if re.match(r"^#{2,4}\s*Q\d+\s*·", l):
                break
            if re.match(r"^#{1,4}\s", l):
                break
            if l.strip():
                partes.append(l.strip())
            i += 1

        corpo = "\n".join(partes)
        resposta, corpo_limpo = extrair_gabarito_details(corpo)
        enunciado = limpar_enunciado(corpo_limpo)

        questoes.append({
            "id": f"q{modulo}{num:02d}",
            "modulo": modulo,
            "numero": num,
            "nivel": nivel,
            "aula": aula,
            "enunciado": enunciado,
            "detalhes": extras_da_pergunta(corpo_limpo, enunciado),
            "resposta": resposta,
            "origem": origem,
        })

    return questoes


def extrair_gabarito_details(corpo):
    """Pega <details><summary>Gabarito</summary>...</details> e devolve o texto."""
    m = re.search(
        r"<details>\s*<summary>\s*Gabarito\s*</summary>(.*?)</details>",
        corpo,
        re.S | re.I,
    )
    if not m:
        return "", corpo
    resposta = m.group(1).strip()
    return resposta, corpo[: m.start()] + corpo[m.end():]


def limpar_enunciado(corpo):
    """
    Isola o enunciado: tira o prefixo '**P.**' e separadores `---`, que
    aparecem quando o gabarito em <details> foi removido do corpo.
    """
    linhas = []
    for l in str(corpo).split("\n"):
        s = l.strip()
        if not s:
            continue
        if set(s) <= {"-", "*", "_"} and len(s) >= 3:
            continue
        if s.startswith("#"):
            continue
        linhas.append(s)

    enunciado = " ".join(linhas)
    enunciado = re.sub(r"^\*\*P\.\*\*\s*", "", enunciado)
    enunciado = enunciado.replace("**P.**", "").strip()
    return re.sub(r"\s+", " ", enunciado)


def enunciados_iguais(a, b):
    """Compara enunciados ignorando o prefixo '**P.**' e espacos."""
    normal = lambda s: re.sub(r"\s+", " ", limpar_enunciado(s)).strip()
    return normal(a) == normal(b)


def extras_da_pergunta(corpo, enunciado_limpo):
    """
    Linhas extras da questao.

    Descarta separadores `---`, linhas de metadado do banco ("Banco criado
    em..."), legenda da tabela de autoavaliacao e repeticoes do enunciado.
    """
    extras = []
    for l in corpo.split("\n"):
        s = l.strip()
        if not s or s.startswith("#") or s.startswith("|"):
            continue
        if set(s) <= {"-", "*", "_"} and len(s) >= 3:
            continue
        if re.match(r"^\*(Banco|criado|atualizado|c[oó]digos)", s, re.I):
            continue
        if enunciados_iguais(s, enunciado_limpo):
            continue
        extras.append(s)
    return extras


def questoes_formato_numerada(corpo, modulo, origem):
    """Formato do M00: lista '1. pergunta' com continuacoes indentadas."""
    gabarito = gabarito_de_tabela(corpo)
    linhas = corpo.split("\n")
    questoes = []
    i = 0
    while i < len(linhas):
        m = re.match(r"^(\d+)\.\s+(.+)$", linhas[i])
        if not m:
            i += 1
            continue

        num = int(m.group(1))
        enunciado = m.group(2).strip()
        i += 1

        extras = []
        while i < len(linhas):
            prox = linhas[i]
            if re.match(r"^\d+\.\s+", prox) or prox.startswith("#"):
                break
            if prox.startswith(("   ", "\t")):
                extras.append(prox.strip())
            elif prox.strip() == "":
                if i + 1 < len(linhas) and linhas[i + 1].startswith(("   ", "\t")):
                    i += 1
                    continue
                break
            else:
                extras.append(prox.strip())
            i += 1

        questoes.append({
            "id": f"q{modulo}{num:02d}",
            "modulo": modulo,
            "numero": num,
            "nivel": "",
            "aula": "",
            "enunciado": enunciado,
            "detalhes": extras,
            "resposta": gabarito.get(num, ""),
            "origem": origem,
        })

    return questoes


def extrair_questoes():
    """Exporta os dois bancos. M01 usa headings Qn; M00 usa lista numerada."""
    caminhos = [
        ("02 - Módulos/M00 - Fundamentos da IA Moderna/05 Perguntas/Banco de perguntas - M00.md", "m00"),
        (f"{M01}/05 Perguntas/Banco de perguntas - M01.md", "m01"),
    ]

    todas = []
    for caminho, modulo in caminhos:
        full = os.path.join(VAULT, caminho)
        if not os.path.exists(full):
            print(f"  aviso: banco nao encontrado -> {caminho}", file=sys.stderr)
            continue

        texto = open(full, encoding="utf-8").read()
        dados, corpo = ler_frontmatter(texto)
        origem = os.path.splitext(os.path.basename(caminho))[0]

        qs = questoes_formato_heading(corpo, modulo, origem)
        if not qs:
            qs = questoes_formato_numerada(corpo, modulo, origem)

        todas.extend(qs)

    # renumera sequencialmente mantendo o id tematico
    for n, q in enumerate(todas, 1):
        q["seq"] = n

    return todas


# Termos que so aparecem em rodape de navegacao do Obsidian ou em prosa
# interna do curso. Se sobrar um deles, o exportador corta a linha em vez de
# publicar referencia a material que nao vai para o site.
VAZAMENTOS = (
    "00 - Painel",
    "Revisão espaçada",
    "Roadmap da Pós",
    "Glossário da Pós",
    "micro-capstone",
    "Micro-Capstone",
    "caders",
    "01 - Diário",
)


def limpar_checkboxes_vazios(corpo):
    """
    Checkbox sem rotulo nao serve para nada num site: e um "[ ]" vazio que
    ninguem pode marcar com sentido. No vault ele e placeholder para o autor
    preencher; aqui vira item de texto, ou some se nao houver contexto.

    O padrao do Obsidian "- [ ] " (com espaco e nada depois) tambem nao e
    reconhecido pelo GFM, entao precisa ser tratado antes.
    """
    linhas = []
    for l in corpo.split("\n"):
        if re.match(r"^\s*[-*]\s*\[\s?\]\s*$", l):
            # placeholder vazio: descarta a linha
            continue
        # "- [ ] texto" precisa de um espaco antes do rotulo para o GFM aceitar
        linhas.append(re.sub(r"^(\s*[-*]\s*\[\s?\])\s*(\S)", r"\1 \2", l))
    return "\n".join(linhas)


def limpar_rodape(corpo):
    """
    Remove a navegacao que o Obsidian injeta no fim das notas.

    Sao duas formas: uma secao "## Ver também" que so linka notas internas, e
    uma linha solta de links separados por "·". Nenhuma das duas sobrevive ao
    site, porque os alvos nao sao publicados.
    """
    linhas = corpo.split("\n")
    saida, i = [], 0

    while i < len(linhas):
        l = linhas[i]

        if re.match(r"^#{2,3}\s+(Ver também|Navega|See also)", l, re.I):
            bloco, j = [], i + 1
            while j < len(linhas) and not linhas[j].startswith("#"):
                bloco.append(linhas[j])
                j += 1
            if not any(t in "\n".join(bloco) for t in VAZAMENTOS):
                saida.extend([l] + bloco)
            i = j
            continue

        # Linha solta so com links internos, sem prosa. Uma linha que comeca
        # com "**Categoria** —" e lista de wikilinks e conteudo, nao rodape.
        if "·" in l and l.count("[[") >= 2 and not re.match(
            r"^\s*(\*\*|-\s*\*\*)", l
        ):
            i += 1
            continue

        saida.append(l)
        i += 1

    return "\n".join(saida)


# Titulo de secao que pressupoe um conteudo que o site nao tem (modulo,
# disciplina). Sem isso, "as perguntas que um modulo deve responder" entrega
# que existe uma Estrutura de curso por tras.
# Titulo de secao que pressupoe um conteudo que o site nao tem (modulo,
    # disciplina). Sem isso, "as perguntas que um modulo deve responder" entrega
    # que existe uma estrutura de curso por tras.
    #
    # A secao "Lacunas" e um worksheet pessoal: checkboxes vazios para o autor
    # preencher. Nao ha como preencher num site, entao a secao inteira sai em
    # vez de virar "[ ] [ ]".
    FORCA_NEUTRA = [
        (r"^(\#{2,4}\s*)As \d+ perguntas que um m[oó]dulo de LLM deve responder",
         r"\g<1>As perguntas que este site tenta responder"),
        (r"^(\#{2,4}\s*)Lab para esperar", r"\g<1>Labs disponíveis"),
    ]

    # secao de worksheet: remove o titulo e tudo ate o proximo titulo
    m = re.search(
        r"\n##\s*Lacunas do mapa.*?(?=\n##\s|\n```|\Z)", corpo, re.S
    )
    if m:
        corpo = corpo[: m.start()] + "\n" + corpo[m.end():]


# Titulo de secao que pressupoe um conteudo que o site nao tem (modulo,
# disciplina). Sem isso, "as perguntas que um modulo deve responder" entrega
# que existe uma estrutura de curso por tras.
FORCA_NEUTRA = [
    (r"^(\#{2,4}\s*)As \d+ perguntas que um m[oó]dulo de LLM deve responder",
     r"\g<1>As perguntas que este site tenta responder"),
    (r"^(\#{2,4}\s*)Lab para esperar", r"\g<1>Labs disponíveis"),
]


def ajustar_contagens(corpo):
    """
    O mapa diz "Conceitos-chave (18 fichas)", mas o bloco lista 20. Numero
    escrito a mao envelhece sozinho; aqui vem da contagem real do bloco.

    Nota: conta os wikilinks distintos listados, nao o total de conceitos
    publicados — o mapa e uma trilha de leitura, nao o catalogo inteiro.
    """
    if "Conceitos-chave" not in corpo:
        return corpo

    bloco = re.search(
        r"(## Conceitos-chave[^\n]*\n\s*\n)((?:\*\*[^\n]*\n?)+)", corpo
    )
    if not bloco:
        return corpo

    alvos = set()
    for l in bloco.group(2).strip().split("\n"):
        alvos.update(re.findall(r"\[\[([^\]|]+)", l))

    n = len(alvos)
    cabecalho = re.sub(
        r"\(\d+\s+fichas?\)", f"({n} nesta trilha)", bloco.group(1)
    )
    return corpo[: bloco.start(1)] + cabecalho + bloco.group(2) + corpo[bloco.end(2):]


def neutralizar_titulos(corpo):
    """
    Troca titulos que entregam a estrutura do curso por equivalentes neutros.

    "As 6 perguntas que um modulo de LLM deve responder" diz que existe um
    modulo; no site, a pergunta e sobre o que o site cobre.

    A secao "Lacunas do mapa" e worksheet pessoal — checkboxes vazios para o
    autor preencher. Nao ha como preencher num site, entao a secao inteira sai
    em vez de virar "[ ] [ ]".
    """
    for padrao, troca in FORCA_NEUTRA:
        corpo = re.sub(padrao, troca, corpo, flags=re.M)

    m = re.search(r"\n##\s*Lacunas do mapa.*?(?=\n##\s|\n```|\Z)", corpo, re.S)
    if m:
        corpo = corpo[: m.start()] + "\n" + corpo[m.end():]

    return ajustar_contagens(corpo)


def limpar_referencias_de_aula(corpo):
    """
    Troca referencias a aula por links para o conceito equivalente.
    "ver aula 22" e "aula 17" existiam porque o numero identifica a fonte. Num
    site publico o numero nao diz nada, e a coluna fica com um "aula" solto. O
    leitor precisa do link para o conceito, que ja existe no site.
    """
    mapa = {
        15: "Aula 15 - Boas-vindas - Como funcionam os LLMs",
        16: "Aula 16 - O que é um LLM de verdade",
        17: "Token",
        18: "Embedding",
        19: "Transformer",
        20: "Temperatura",
        21: "Logits",
        22: "Prefill",
        23: "Self-Attention",
        24: "Janela de Contexto",
        25: "Top-p Sampling",
        26: "Fine-tuning",
        27: "Modelo Base",
    }
    publicados = {p[4] for p in pares_global}

    def sub(m):
        n = int(m.group(2))
        alvo = mapa.get(n)
        if not alvo:
            return ""
        if alvo in publicados:
            return f"[[{alvo}]]"
        return alvo.replace("Aula ", "")

    # "com parêntese: (ver aula 22)", "(aula 21)"
    corpo = re.sub(r"\(?\s*(?:ver\s+)?([Aa]ula)s?\s+(\d+)\)?", sub, corpo)

    # Nao colapsa espacos: a indentacao carrega significado em mermaid
    # (mindmap depende dela para montar a hierarquia) e em listas de codigo.
    return corpo


# "Perguntas de prova" e "Autoavaliacao" nomeiam a avaliacao do curso. O
# conteudo (pergunta e resposta) e autoral e util; so o rotulo entrega de
# onde vem. Vira "Autoavaliacao" em todos os casos.
def neutralizar_rotulo_de_avaliacao(corpo):
    corpo = re.sub(
        r"^(\#{2,4})\s*(?:Perguntas de prova|Prova|Autoavaliação|Autoavaliacao)\s*$",
        r"\1 Autoavaliação",
        corpo,
        flags=re.M | re.I,
    )
    # "nesta trilha", "o modulo 01 descreve": a estrutura do curso aparecia
    # no rotulo. O conteudo nao muda, so o nome do recorte.
    corpo = re.sub(r"\bnesta trilha\b", "neste mapa", corpo, flags=re.I)
    corpo = re.sub(r"\bo m[oó]dulo \d{2}\b", "o mapa", corpo, flags=re.I)
    corpo = re.sub(r"\bperguntas de prova\b", "perguntas de avaliação", corpo, flags=re.I)
    return corpo


def cortar_vazamento(corpo):
    """Ultimo recurso: remove linhas que ainda citam material do curso."""
    linhas = []
    for l in corpo.split("\n"):
        if any(t in l for t in VAZAMENTOS):
            continue
        # Bloco "Onde isso conecta" nos papers: a linha "- Aula:16 - ..." vira
        # "- Aula: ..." depois que o wikilink e resolvido, e o numero solto
        # identifica a fonte. A linha seguinte (a pesquisa) ja cobre o
        # mesmo papel, entao a entrada inteira sai.
        if re.match(r"^\s*[-*]?\s*Aula\s*:\s*", l, re.I):
            continue
        linhas.append(l)
    return "\n".join(linhas)


# ---------------------------------------------------------------- mermaid
# O Quartz le `innerText` do <code class="mermaid"> para alimentar o Mermaid.
# Em alguns diagramas esse innerText chega vazio — o elemento ja foi
# processado — e o render sai como <svg><g></g></svg>, sem erro no console.
# Reproduzido: os 4 blocos do mapa, dos quais so o mindmap renderizava.
#
# A saida e um script que refaz o render a partir do atributo data-clipboard,
# que preserva o codigo original. Roda depois do Quartz e so substitui o
# conteudo quando o SVG veio vazio, entao nao interfere nos casos que
# funcionam.
SCRIPT_MERMAID = """
<script>
// Correcao do Mermaid no Quartz 5.0.0.
//
// O Quartz le `innerText` do <code class="mermaid"> para alimentar o Mermaid.
// Em parte dos diagramas esse innerText chega vazio e o render sai como
// <svg><g></g></svg>, sem erro no console. Reproduzido nos 4 blocos do mapa,
// dos quais so o mindmap renderizava.
//
// A correcao espera o SVG existir antes de medir: rodar antes faz o script
// ver zero diagramas e sair cedo. O timeout cobre o caso em que o Mermaid
// nem carregou (CDN bloqueado), para nao esperar para sempre.
(() => {
  const CDN =
    "https://cdnjs.cloudflare.com/ajax/libs/mermaid/11.4.0/mermaid.esm.min.mjs";

  const vazios = () =>
    [...document.querySelectorAll("code.mermaid")].filter((n) => {
      const svg = n.querySelector("svg");
      return svg && svg.querySelectorAll("path,rect,polygon,circle").length === 0;
    });

  const fonte = (n) =>
    (n.getAttribute("data-clipboard") || "")
      .replace(/^"|"$/g, "")
      .replace(/\\\\"/g, '"')
      .replace(/\\\\n/g, "\\n")
      .replace(/&lt;/g, "<")
      .replace(/&gt;/g, ">")
      .replace(/\\\\\\\\/g, "\\\\");

  const corrigir = (alvo) => {
    import(CDN)
      .then((m) => {
        m.default.initialize({ startOnLoad: false, securityLevel: "loose" });
        return Promise.all(
          alvo.map(async (n, i) => {
            try {
              const { svg } = await m.default.render("corrige-" + i, fonte(n));
              n.innerHTML = svg;
            } catch (e) {
              console.warn("mermaid: falhou um diagrama", fonte(n).slice(0, 40), e);
            }
          })
        );
      })
      .catch((e) => console.warn("mermaid: CDN indisponivel", e));
  };

  // Tenta varias vezes: o SVG do Quartz pode aparecer depois do DOMContentLoaded.
  let tentativas = 0;
  const tentar = () => {
    const alvo = vazios();
    if (alvo.length > 0) return corrigir(alvo);
    if (tentativas++ < 20) setTimeout(tentar, 500);
  };

  if (document.readyState === "complete") setTimeout(tentar, 1500);
  else window.addEventListener("load", () => setTimeout(tentar, 1500));
})();
</script>
"""


def injetar_correcao_mermaid(corpo):
    """Anexa o script de correcao a notas que tem blocos mermaid."""
    if "```mermaid" not in corpo:
        return corpo
    return corpo.rstrip() + "\n" + SCRIPT_MERMAID


# --------------------------------------------------------------- slugs
def slug(texto):
    texto = unicodedata.normalize("NFKD", texto)
    texto = texto.encode("ascii", "ignore").decode("ascii")
    texto = re.sub(r"[^a-zA-Z0-9]+", "-", texto).strip("-").lower()
    return texto or "nota"


# --------------------------------------------------------------- main
def main():
    if os.path.isdir(CONTENT):
        shutil.rmtree(CONTENT)
    os.makedirs(CONTENT, exist_ok=True)
    os.makedirs(STATIC_DATA, exist_ok=True)

    exportados = []

    # 1. coleta as notas publicaveis em memoria antes de escrever, para
    #    resolver wikilinks depois que todos os titulos forem conhecidos.
    pares = []  # (subpasta, nome_arquivo, frontmatter, corpo)

    for pasta in PUBLIC_DIRS:
        origem = os.path.join(VAULT, pasta)
        if not os.path.isdir(origem):
            print(f"  aviso: pasta nao encontrada -> {pasta}", file=sys.stderr)
            continue
        for arquivo in sorted(os.listdir(origem)):
            if not arquivo.endswith(".md") or arquivo in NEVER:
                continue
            src = os.path.join(origem, arquivo)
            texto = open(src, encoding="utf-8").read()
            dados, corpo = ler_frontmatter(texto)
            fm, _ = normalizar_frontmatter(os.path.join(pasta, arquivo), dados)
            nome = os.path.splitext(arquivo)[0]
            destino_pasta = PASTAS_SITE.get(pasta, (slug(pasta), None, None))
            INDICES_PASTA[destino_pasta[0]] = (destino_pasta[1], destino_pasta[2])
            pares.append((destino_pasta[0], arquivo, fm, corpo, nome))

    for caminho in PUBLIC_FILES:
        src = os.path.join(VAULT, caminho)
        if not os.path.exists(src):
            continue
        texto = open(src, encoding="utf-8").read()
        dados, corpo = ler_frontmatter(texto)
        fm, _ = normalizar_frontmatter(caminho, dados)
        pares.append(("mapa", os.path.basename(caminho), fm, corpo,
                      os.path.splitext(os.path.basename(caminho))[0]))

    # templates/ entram como estao: tem wikilinks [[Token]] e precisa resolver
    for arquivo in sorted(os.listdir(TEMPLATES)) if os.path.isdir(TEMPLATES) else []:
        if not arquivo.endswith(".md"):
            continue
        texto = open(os.path.join(TEMPLATES, arquivo), encoding="utf-8").read()
        dados, corpo = ler_frontmatter(texto)
        fm, _ = normalizar_frontmatter(arquivo, dados)
        pares.append(("", arquivo, fm, corpo, os.path.splitext(arquivo)[0]))

    # titulos publicos, para decidir o fateio de cada wikilink
    published = {p[4] for p in pares}
    pares_global[:] = pares

    # Rótulo de módulo em heading solto ("## Ordem de leitura para o M01").
    # A seção em si é útil, o rótulo é que entrega do curso. Some só o
    # código, e o conectivo antes dele, para a frase não ficar capenga.
    def sem_modulo(corpo):
        return re.sub(
            r"^(\#{2,4}\s.*?)\s+(?:para|do|da|de)?\s*M0[0123]\b",
            r"\1",
            corpo,
            flags=re.M,
        )

    def resolver(corpo):
        """Wikilink para nota nao publicada vira texto simples."""
        def sub(m):
            alvo = m.group(1).split("|")[-1].strip()
            if alvo in published:
                return m.group(0)
            nome = m.group(1).split("|")[0].strip()
            nome = re.sub(r"^Aula\s+(\d+).*", r"aula \1", nome)
            return nome
        return re.sub(r"\[\[([^\]]+)\]\]", sub, corpo)

    for sub, arquivo, fm, corpo, _ in pares:
        destino = os.path.join(CONTENT, sub, arquivo) if sub else os.path.join(CONTENT, arquivo)
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        limpo = resolver(neutralizar_titulos(limpar_checkboxes_vazios(limpar_rodape(sem_modulo(corpo)))))
        limpo = injetar_correcao_mermaid(limpo)
        limpo = limpar_referencias_de_aula(limpo)
        limpo = neutralizar_rotulo_de_avaliacao(limpo)
        with open(destino, "w", encoding="utf-8") as f:
            f.write(render_yaml(fm) + "\n\n" + cortar_vazamento(limpo))
        exportados.append(destino)

    # 2. indice de cada pasta, com titulo e descricao proprios. Sem isso o
    #    Quartz usa o nome cru da pasta como titulo e a lista em ingles.
    for sub, (titulo, descricao) in INDICES_PASTA.items():
        if not titulo:
            continue
        pasta = os.path.join(CONTENT, sub)
        os.makedirs(pasta, exist_ok=True)
        fm = {"title": titulo, "tags": []}
        if descricao:
            fm["description"] = descricao
        with open(os.path.join(pasta, "index.md"), "w", encoding="utf-8") as f:
            f.write(render_yaml(fm) + f"\n\n# {titulo}\n")
        exportados.append(os.path.join(pasta, "index.md"))

    # 3. questoes
    questoes = extrair_questoes()

    # `aula` traz o titulo e a numeracao do curso; `origem` traz o nome do
    # arquivo do banco, que tambem identifica o curso. Nenhum dos dois vai
    # para o payload. `modulo` ja basta para filtrar.
    publicas = [
        {k: v for k, v in q.items() if k not in ("aula", "origem")}
        for q in questoes
    ]

    # O codigo do modulo no vault (m00, m01) expoe a estrutura do curso. No
    # site vira rotulo neutro, suficiente para filtrar.
    rotulos = {"m00": "fundamentos", "m01": "modelos de linguagem"}

    # Questao que cita o entregavel do curso pelo nome. O enunciado faz
    # sentido sem a referencia, entao o termo e normalizado.
    termos = {
        "micro-capstone": "documento de decisão",
        "microcapstone": "documento de decisão",
        "Micro-Capstone": "documento de decisão",
    }

    for q in publicas:
        q["modulo"] = rotulos.get(q["modulo"], q["modulo"])
        for termo, troca in termos.items():
            if termo in q["enunciado"]:
                q["enunciado"] = q["enunciado"].replace(termo, troca)

    payload = {
        "gerado_em": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "origem": "bancos de perguntas do vault de estudo",
        "total": len(publicas),
        "com_resposta": sum(1 for q in publicas if q["resposta"]),
        "questoes": publicas,
    }

    destino_json = os.path.join(STATIC_DATA, "questions.json")
    with open(destino_json, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    # 4. relatorio de links achatados
    achatados = 0
    for _, _, _, corpo, _ in pares:
        for alvo in re.findall(r"\[\[([^\]]+)\]\]", corpo):
            if alvo.split("|")[-1].strip() not in published:
                achatados += 1

    print(f"  {len(exportados)} paginas exportadas")
    print(f"  {len(questoes)} questoes -> quartz/static/dados/questions.json")
    print(f"  {payload['com_resposta']} com gabarito")
    print(f"  {achatados} links para notas do curso convertidos em texto")


if __name__ == "__main__":
    main()