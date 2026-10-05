#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exporta o conteudo publico do vault Obsidian para o site Quartz.

Gera:
  content/         .md com frontmatter normalizado (sem prefixo de pasta)
  quartz/static/dados/questions.json   banco de questoes servido via fetch()
  content/questoes.md                   pagina do quiz, vinda de templates/

Fonte:  o vault Obsidian, configurado em LLM_NOTES_VAULT
Destino: a raiz deste repositorio (ou a variavel LLM_NOTES_DIR)

Este arquivo e a parte limpa: layout do site, frontmatter, links, slugs. Tudo
que descreve a origem do material -- caminhos do vault, o que entra, o
vocabulario a remover -- vem de `scripts/origem.py`, que NAO e versionado,
porque o repositorio e publico e o material de origem e privado. Um filtro que
remove um termo precisa conter o termo; por isso essa parte mora fora do git.

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

try:
    from origem import (
        NOTAS_PUBLICAS,
        BANCOS,
        NOTA_EQUIVALENTE,
        NUNCA,
        PASTA_AULAS,
        PASTAS_SITE,
        PUBLICA,
        PUBLICA_ARQUIVOS,
        RE_ALVO_NUMERADO,
        RE_CODIGO_NO_TITULO,
        RE_ITEM_NUMERADO,
        RE_NUMERO_ARQUIVO,
        RE_NUMERO_H1,
        RE_PREFIXO,
        RE_PROVENIENCIA,
        RE_REFERENCIA_NUMERADA,
        RE_RODAPE,
        REGRAS_AVALIACAO,
        REGRAS_PROSA,
        REGRAS_TITULO,
        ROTULOS_TEMA,
        TAGS_DESCARTADAS,
        TERMOS_ENUNCIADO,
        TIPOS,
        VAZAMENTOS,
        achatar_nome,
    )
except ImportError:
    print(
        "erro: scripts/origem.py nao encontrado.\n"
        "      Ele guarda os caminhos do vault e o vocabulario que o\n"
        "      exportador remove, e nao e versionado. See README.",
        file=sys.stderr,
    )
    sys.exit(1)

SITE = os.environ.get("LLM_NOTES_DIR") or os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)
# Sem caminho padrao: o vault e privado e o caminho dele e configuracao local
# de cada maquina. Fixar um valor aqui publicaria esse caminho no repo. Sem a
# variavel o exportador aborta, em vez de gerar um content/ quase vazio sem
# avisar.
VAULT = os.environ.get("LLM_NOTES_VAULT")
CONTENT = os.path.join(SITE, "content")
# quartz/static/** e copiado para public/static/** pelo build, entao o JSON
# fica acessivel por fetch() sem depender do roteamento de paginas.
STATIC_DATA = os.path.join(SITE, "quartz", "static", "dados")
TEMPLATES = os.path.join(SITE, "templates")

# Preenchido em main() com as notas que foram exportadas, para que o
# reescritor de referencias saiba o que virou link e o que virou texto.
pares_global = []

# As notas numeradas viram a secao "Guias": o mesmo conteudo, sem a numeracao e
# sem qualquer palavra que nomeie a origem. Fica em pasta propria porque o
# titulo publico perde o prefixo numerado, e o link entre guias precisa resolver
# para o titulo novo, nao para o nome do arquivo no vault.
PASTA_GUIAS = ("guias", "Guias", "Temas escritos em prosa, do enquadramento à mecânica.")

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
    # Tags que descrevem a origem nao descrevem o conteudo tecnico. Fica so o
    # que a nota e.
    tags = [t for t in tags if not TAGS_DESCARTADAS.fullmatch(t)]

    # O `tipo` do vault nomeia a origem da nota; o publico nao. Sem essa troca
    # o painel de propriedades entrega de onde ela veio, mesmo com o titulo
    # ja limpo.
    tipo = TIPOS.get(
        str(dados.get("tipo", "")).strip().lower(), dados.get("tipo", "conceito")
    )

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


def questoes_formato_heading(texto, banco, origem):
    """
    Formato com heading: '### Qn · `D` · [[fonte]]' seguido da pergunta em
    prosa.

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
        fonte = m.group(3).strip()
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
            "id": f"q{banco}{num:02d}",
            "banco": banco,
            "numero": num,
            "nivel": nivel,
            "fonte": fonte,
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


def questoes_formato_numerada(corpo, banco, origem):
    """Lista '1. pergunta' com continuacoes indentadas."""
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
            "id": f"q{banco}{num:02d}",
            "banco": banco,
            "numero": num,
            "nivel": "",
            "fonte": "",
            "enunciado": enunciado,
            "detalhes": extras,
            "resposta": gabarito.get(num, ""),
            "origem": origem,
        })

    return questoes


def extrair_questoes():
    """Exporta os bancos. Cada um usa um formato; ver `origem.BANCOS`."""
    todas = []
    for caminho, banco in BANCOS:
        full = os.path.join(VAULT, caminho)
        if not os.path.exists(full):
            print(f"  aviso: banco nao encontrado -> {caminho}", file=sys.stderr)
            continue

        texto = open(full, encoding="utf-8").read()
        dados, corpo = ler_frontmatter(texto)
        origem = os.path.splitext(os.path.basename(caminho))[0]

        qs = questoes_formato_heading(corpo, banco, origem)
        if not qs:
            qs = questoes_formato_numerada(corpo, banco, origem)

        todas.extend(qs)

    # renumera sequencialmente mantendo o id tematico
    for n, q in enumerate(todas, 1):
        q["seq"] = n

    return todas


# Termos que so aparecem em rodape de navegacao do Obsidian ou em prosa
# interna estao em `origem.VAZAMENTOS`.
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


# Titulos que pressupoeem uma estrutura que o site nao tem estao em
# `origem.REGRAS_TITULO`.
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
    Troca por equivalentes neutros os titulos que entregam a estrutura de
    origem. As regras estao em `origem.REGRAS_TITULO`.

    A secao "Lacunas do mapa" e worksheet pessoal — checkboxes vazios para o
    autor preencher. Nao ha como preencher num site, entao a secao inteira sai em
    vez de virar "[ ] [ ]".
    """
    for padrao, troca in REGRAS_TITULO:
        corpo = re.sub(padrao, troca, corpo, flags=re.M)

    m = re.search(r"\n##\s*Lacunas do mapa.*?(?=\n##\s|\n```|\Z)", corpo, re.S)
    if m:
        corpo = corpo[: m.start()] + "\n" + corpo[m.end():]

    return ajustar_contagens(corpo)


def numeros_publicados(renomeia):
    """Nome de arquivo no vault -> numero: {17: 'Tokens e por que eles custam'}."""
    numeros = {}
    for stem, titulo in renomeia.items():
        m = RE_NUMERO_ARQUIVO.match(stem)
        if m:
            numeros[int(m.group(1))] = titulo
    return numeros


def resolver_referencias(corpo, por_numero):
    """
    Troca referencias a uma nota numerada por link para a nota que cobre o
    mesmo assunto.

    "ver a nota 22" e "nota 17" existiam porque o numero identifica a fonte. Num
    site publico o numero nao diz nada, e a coluna fica com a palavra solta. O
    leitor precisa do link, que ja existe no site.

    A prioridade e o guia: se a nota virou guia, o link vai para o guia, pelo
    titulo publico. So as que nao viraram guia caem em `origem.NOTA_EQUIVALENTE`,
    e ainda assim apenas quando o conceito existe no site.
    """
    publicados = {p[4] for p in pares_global}

    def sub(m):
        n = int(m.group(2))
        if n in por_numero:
            return f"[[{por_numero[n]}]]"
        alvo = NOTA_EQUIVALENTE.get(n, "")
        if not alvo or alvo not in publicados:
            return ""
        return f"[[{alvo}]]"

    # "com parêntese: (ver nota 22)", "(nota 21)"
    corpo = re.sub(RE_REFERENCIA_NUMERADA, sub, corpo)

    # Nao colapsa espacos: a indentacao carrega significado em mermaid
    # (mindmap depende dela para montar a hierarquia) e em listas de codigo.
    return corpo


# Rotulos que nomeiam a avaliacao de origem. O conteudo (pergunta e resposta) e
# autoral e util; so o rotulo entrega de onde vem. Padroes e trocas em
# `origem.REGRAS_AVALIACAO`.
def neutralizar_rotulo_de_avaliacao(corpo):
    for padrao, troca in REGRAS_AVALIACAO:
        flags = re.M | re.I if padrao.startswith("^") else re.I
        corpo = re.sub(padrao, troca, corpo, flags=flags)
    return corpo


def cortar_vazamento(corpo):
    """Ultimo recurso: remove linhas que ainda citam material de origem."""
    linhas = []
    for l in corpo.split("\n"):
        if any(t in l for t in VAZAMENTOS):
            continue
        # Secao "Onde isso conecta" nos papers: a linha "- Nota:16 - ..." vira
        # "- Nota: ..." depois que o wikilink e resolvido, e o numero solto
        # identifica a fonte. A linha seguinte (a pesquisa) ja cobre o
        # mesmo papel, entao a entrada inteira sai.
        if RE_ITEM_NUMERADO.match(l):
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


# --------------------------------------------------------------- guias
# O aviso que abre a nota dizendo de onde ela saiu, e o rodape de data, estao
# em `origem.RE_PROVENIENCIA` e `origem.RE_RODAPE`. O aviso sai inteiro, nao por
# substituicao: reescrever deixaria a frase no lugar-comando, apontando para
# algo que nao existe no site.
def limpar_proveniencia(corpo):
    """Remove o aviso de origem da nota e o rodape de data."""
    linhas, saida, i = corpo.split("\n"), [], 0

    while i < len(linhas):
        l = linhas[i]
        if RE_PROVENIENCIA.match(l):
            while i < len(linhas) and linhas[i].startswith(">"):
                i += 1
            continue
        if RE_RODAPE.match(l):
            i += 1
            continue
        saida.append(l)
        i += 1

    saida = "\n".join(saida)
    # o separador `---` que antecedia o rodape fica orfao no fim do arquivo
    saida = re.sub(r"\n+---\s*\Z", "", saida)
    return saida.rstrip() + "\n"


def aplicar_regras_de_prosa(corpo):
    """Remove da prosa o vocabulario de origem. Padroes em `origem.REGRAS_PROSA`."""
    for padrao, troca in REGRAS_PROSA:
        corpo = re.sub(padrao, troca, corpo, flags=re.M)
    # as regras removem palavras e deixam espacos duplos onde havia frase
    return re.sub(r"[ \t]{2,}", " ", corpo)


def titulo_publico(corpo, stem):
    """
    Descobre o titulo publico da nota: o H1 sem o prefixo numerado.

    O H1 e a fonte preferida porque traz a acentuacao e a pontuacao que o
    nome do arquivo perdeu (o vault grava "O que e e nao e inteligencia
    artificial", o H1 traz "O que é (e o que não é) inteligência artificial").
    Sem H1, cai no nome do arquivo, tambem sem o prefixo. Padroes em
    `origem.RE_NUMERO_H1` e `origem.RE_PREFIXO`.
    """
    m = RE_NUMERO_H1.search(corpo)
    if m and m.group(1).strip():
        return m.group(1).strip()
    return RE_PREFIXO.sub("", stem).strip() or stem


def reescrever_links_de_origem(corpo, renomeia):
    """
    Troca [[<nota numerada> - Tokens e por que eles custam]] por
    [[Tokens e por que eles custam]] quando a nota virou guia.

    Precisa rodar antes do `resolver`. Depois dele o wikilink ja virou texto
    solto e o resto do nome fica orfao na frase, do tipo "nota 17
    - Tokens e por que eles custam". Aqui o nome inteiro e resolvido de uma vez.

    Wiki que aponta para nota que NAO virou guia fica como estava: o
    `resolver` escolhe entre texto e conceito, como antes. Alias, secao e
    bloco sao preservados, porque o nome so e substituido no comeco.
    """

    def sub(m):
        dentro = m.group(1)
        nome = re.split(r"[|#^]", dentro, maxsplit=1)[0].strip()
        if nome in renomeia:
            return f"[[{renomeia[nome]}{dentro[len(nome):]}]]"
        return m.group(0)

    return re.sub(r"\[\[([^\]]+)\]\]", sub, corpo)


def coletar_guias():
    """
    Le as notas numeradas da allowlist e devolve (pares, renomeia).

    `pares` tem o mesmo formato do resto do exportador. `renomeia` mapeia o
    nome do arquivo no vault para o titulo publico, para que os wikilinks
    entre as notas resolvam para o titulo novo.
    """
    pares, renomeia = [], {}

    for pasta, numeros in NOTAS_PUBLICAS.items():
        rel = PASTA_AULAS[pasta]
        origem = os.path.join(VAULT, rel)
        if not os.path.isdir(origem):
            print(f"  aviso: pasta de notas nao encontrada -> {rel}", file=sys.stderr)
            continue

        por_numero = {}
        for arquivo in os.listdir(origem):
            m = RE_NUMERO_ARQUIVO.match(arquivo)
            if m:
                por_numero.setdefault(int(m.group(1)), arquivo)

        for n in numeros:
            arquivo = por_numero.get(n)
            if not arquivo:
                print(f"  aviso: nota {n:02d} nao encontrada em {rel}", file=sys.stderr)
                continue

            stem = os.path.splitext(arquivo)[0]
            texto = open(os.path.join(origem, arquivo), encoding="utf-8").read()
            dados, corpo = ler_frontmatter(texto)

            titulo = titulo_publico(corpo, stem)
            fm, _ = normalizar_frontmatter(os.path.join(rel, arquivo), dados)
            # O title do frontmatter do vault e o nome com prefixo; aqui o
            # titulo publico manda.
            fm["title"] = titulo

            pares.append((PASTA_GUIAS[0], f"{titulo}.md", fm, corpo, titulo))
            renomeia[stem] = titulo

    return pares, renomeia


# --------------------------------------------------------------- main
def main():
    if not VAULT:
        print(
            "erro: LLM_NOTES_VAULT nao esta definida.\n"
            "      aponte para a raiz do vault e rode de novo:\n"
            "      LLM_NOTES_VAULT=/caminho/do/vault npm run sync",
            file=sys.stderr,
        )
        sys.exit(1)
    if not os.path.isdir(VAULT):
        print(f"erro: vault nao encontrado -> {VAULT}", file=sys.stderr)
        sys.exit(1)

    if os.path.isdir(CONTENT):
        shutil.rmtree(CONTENT)
    os.makedirs(CONTENT, exist_ok=True)
    os.makedirs(STATIC_DATA, exist_ok=True)

    exportados = []

    # 1. coleta as notas publicaveis em memoria antes de escrever, para
    #    resolver wikilinks depois que todos os titulos forem conhecidos.
    pares = []  # (subpasta, nome_arquivo, frontmatter, corpo)

    for pasta in PUBLICA:
        origem = os.path.join(VAULT, pasta)
        if not os.path.isdir(origem):
            print(f"  aviso: pasta nao encontrada -> {pasta}", file=sys.stderr)
            continue
        for arquivo in sorted(os.listdir(origem)):
            if not arquivo.endswith(".md") or arquivo in NUNCA:
                continue
            src = os.path.join(origem, arquivo)
            texto = open(src, encoding="utf-8").read()
            dados, corpo = ler_frontmatter(texto)
            fm, _ = normalizar_frontmatter(os.path.join(pasta, arquivo), dados)
            nome = os.path.splitext(arquivo)[0]
            destino_pasta = PASTAS_SITE.get(pasta, (slug(pasta), None, None))
            INDICES_PASTA[destino_pasta[0]] = (destino_pasta[1], destino_pasta[2])
            pares.append((destino_pasta[0], arquivo, fm, corpo, nome))

    for caminho in PUBLICA_ARQUIVOS:
        src = os.path.join(VAULT, caminho)
        if not os.path.exists(src):
            continue
        texto = open(src, encoding="utf-8").read()
        dados, corpo = ler_frontmatter(texto)
        fm, _ = normalizar_frontmatter(caminho, dados)
        pares.append(("mapa", os.path.basename(caminho), fm, corpo,
                      os.path.splitext(os.path.basename(caminho))[0]))

    # as notas de origem entram depois das pastas, para que o mapa de renomeia
    # ja esteja pronto quando os wikilinks forem resolvidos
    guias, guias_renomeia = coletar_guias()
    pares.extend(guias)
    guias_numeros = numeros_publicados(guias_renomeia)
    INDICES_PASTA[PASTA_GUIAS[0]] = (PASTA_GUIAS[1], PASTA_GUIAS[2])

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

    def resolver(corpo):
        """Wikilink para nota nao publicada vira texto simples."""
        def sub(m):
            alvo = m.group(1).split("|")[-1].strip()
            if alvo in published:
                return m.group(0)
            return achatar_nome(m.group(1).split("|")[0].strip())
        return re.sub(r"\[\[([^\]]+)\]\]", sub, corpo)

    for sub, arquivo, fm, corpo, _ in pares:
        destino = os.path.join(CONTENT, sub, arquivo) if sub else os.path.join(CONTENT, arquivo)
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        # o codigo do material de origem no titulo da secao sai aqui
        base = reescrever_links_de_origem(RE_CODIGO_NO_TITULO.sub(r"\1", corpo), guias_renomeia)
        base = aplicar_regras_de_prosa(limpar_proveniencia(base))
        limpo = resolver(neutralizar_titulos(limpar_checkboxes_vazios(limpar_rodape(base))))
        limpo = injetar_correcao_mermaid(limpo)
        limpo = resolver_referencias(limpo, guias_numeros)
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

    # `fonte` traz a numeracao da nota de origem e `origem` o nome do arquivo
    # do banco. Os dois identificam de onde o material veio, entao nenhum vai
    # para o payload.
    publicas = [
        {k: v for k, v in q.items() if k not in ("fonte", "origem")}
        for q in questoes
    ]

    # O codigo do banco expoe a estrutura de origem. No site vira rotulo
    # neutro, e o campo tambem: `banco` nao diz nada para o leitor. Rotulos em
    # `origem.ROTULOS_TEMA`.
    for q in publicas:
        codigo = q.pop("banco", "")
        q["tema"] = ROTULOS_TEMA.get(codigo, codigo)

    # Enunciado que cita pelo nome o material de origem: faz sentido sem a
    # referencia, entao o termo e normalizado. Ver `origem.TERMOS_ENUNCIADO`.
    for q in publicas:
        for termo, troca in TERMOS_ENUNCIADO.items():
            if termo in q["enunciado"]:
                q["enunciado"] = q["enunciado"].replace(termo, troca)

    payload = {
        "gerado_em": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "origem": "bancos de questões do vault de estudo",
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
    print(f"  {len(guias)} guias em content/{PASTA_GUIAS[0]}/")
    print(f"  {len(questoes)} questoes -> quartz/static/dados/questions.json")
    print(f"  {payload['com_resposta']} com gabarito")
    print(f"  {achatados} links para notas nao publicadas convertidos em texto")


if __name__ == "__main__":
    main()