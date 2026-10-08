---
title: Banco de questões
description: 61 questões de fundamentos e funcionamento de LLMs, com nível de dificuldade e tema de origem.
tags:
  - exercicios
  - revisao
tipo: pagina
---

# Banco de questões

Questões extraídas do banco de questões do vault. Responda antes de revelar — o
interesse está no esforço, não na resposta.

<div id="quiz-app">
  <p class="quiz-carregando">Carregando questões…</p>
</div>

<script type="application/json" id="quiz-data-url">/static/dados/questions.json</script>

<script>
(function () {
  const CDN_JSON = "/static/dados/questions.json";

  // Cache em memoria: o JSON nao muda durante a sessao, entao uma leitura
  // por pagina basta.
  let banco = null;
  let carregando = null;

  const esc = (s) =>
    String(s == null ? "" : s).replace(/[&<>"']/g, (c) => ({
      "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
    })[c]);

  const NIVEL = { facil: "Fácil", media: "Média", dificil: "Difícil" };

  // O gabarito vem do vault em markdown: negrito, lista e `codigo`.
  // Sem isso apareceria "**GQA**" literalmente na resposta.
  function md(texto) {
    let s = esc(texto);
    s = s.replace(/`([^`]+)`/g, "<code>$1</code>");
    s = s.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
    s = s.replace(/(?<!\*)\*([^*\n]+)\*(?!\*)/g, "<em>$1</em>");

    const linhas = s.split("\n");
    const fora = [];
    let lista = null;

    for (const l of linhas) {
      const num = l.match(/^\s*(\d+)\.\s+(.*)$/);
      const topico = l.match(/^\s*[-*]\s+(.*)$/);
      if (num || topico) {
        const tag = topico ? "ul" : "ol";
        if (lista !== tag) {
          if (lista) fora.push("</" + lista + ">");
          fora.push("<" + tag + ">");
          lista = tag;
        }
        fora.push("<li>" + (num ? num[2] : topico[1]) + "</li>");
      } else {
        if (lista) { fora.push("</" + lista + ">"); lista = null; }
        if (l.trim()) fora.push("<p>" + l + "</p>");
      }
    }
    if (lista) fora.push("</" + lista + ">");
    return fora.join("");
  }

  function buscar() {
    if (banco) return Promise.resolve(banco);
    if (carregando) return carregando;

    const base = document.body.dataset.basepath || "/";
    const url = base.replace(/\/$/, "") + CDN_JSON;

    carregando = fetch(url)
      .then((r) => {
        if (!r.ok) throw new Error("HTTP " + r.status);
        return r.json();
      })
      .then((d) => {
        banco = d;
        carregando = null;
        return d;
      })
      .catch((e) => {
        carregando = null;
        throw e;
      });

    return carregando;
  }

  function iniciar() {
    const app = document.getElementById("quiz-app");
    if (!app) return;

    // Sem este guard: o micromorph reaproveita o mesmo no e devolve o
    // innerHTML para "Carregando questoes…". Re-renderizar e barato porque
    // `banco` ja esta em memoria.
    const marcar = () => {
      const atual = document.getElementById("quiz-app");
      if (!atual) return null;
      atual.dataset.pronto = "sim";
      atual.innerHTML = '<p class="quiz-carregando">Carregando questões…</p>';
      return atual;
    };
    marcar();

    buscar()
      .then((data) => {
        // O micromorph pode ter trocado o no entre a escrita acima e a
        // chegada do JSON. Pegar o elemento de novo -- em vez de confiar no
        // capturado -- evita voltar a ficar em "Carregando questoes…".
        const atual = document.getElementById("quiz-app");
        if (!atual) return;
        render(atual, data.questoes || [], data);
      })
      .catch((err) => {
        const atual = document.getElementById("quiz-app");
        if (!atual) return;
        atual.innerHTML =
          '<p class="quiz-erro">Não foi possível carregar o banco: ' +
          esc(err.message) +
          "</p>";
      });
  }

  // O script inline mora no <body>, e o SPA do Quartz (micromorph) so
  // re-executa scripts do <head>. Na primeira visita funciona; na segunda, o
  // script nao roda e o HTML recem-trocado fica em "Carregando questoes…".
  //
  // Pior: o micromorph reaproveita o mesmo no #quiz-app em vez de recria-lo.
  // Por isso nao da para confiar em identidade de no nem no flag `pronto` --
  // o innerHTML volta a ser "Carregando…" enquanto o no e o mesmo de antes.
  // A solucao e reagir ao evento `nav` e renderizar de novo, sem condicao.
  document.addEventListener("nav", () => {
    requestAnimationFrame(() => setTimeout(iniciar, 0));
  });

  vigiar();

  function vigiar() {
    // Cobre trocas de DOM que nao passam pelo `nav` (history API direta,
    // extensoes que trocam o conteudo). Observa o pai para nao se disparar
    // no loop das proprias escritas em app.innerHTML.
    const observar = () => {
      const app = document.getElementById("quiz-app");
      if (!app || !app.parentNode) return;
      new MutationObserver(() => {
        const atual = document.getElementById("quiz-app");
        if (atual && atual !== app) iniciar();
      }).observe(app.parentNode, { childList: true, subtree: true });
    };

    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", () => {
        iniciar();
        observar();
      });
    } else {
      iniciar();
      observar();
    }
  }

  function render(app, questoes, meta) {
    if (!questoes.length) {
      app.innerHTML = "<p>Nenhuma questão encontrada.</p>";
      return;
    }

    const temas = [...new Set(questoes.map((q) => q.tema))].sort();
    const niveis = [...new Set(questoes.map((q) => q.nivel).filter(Boolean))];

    app.innerHTML = [
      '<div class="quiz-controles">',
      '  <label>Tema <select id="q-tema"><option value="">todos</option>',
      ...temas.map((m) => `<option value="${esc(m)}">${esc(m)} (${count(questoes, m, "")})</option>`),
      "  </select></label>",
      '  <label>Nível <select id="q-nivel"><option value="">todos</option>',
      ...niveis.map((n) => `<option value="${esc(n)}">${esc(NIVEL[n] || n)} (${count(questoes, "", n)})</option>`),
      "  </select></label>",
      '  <label>Ordenar <select id="q-ordem">',
      '    <option value="tema">por tema</option>',
      '    <option value="dificuldade">por dificuldade</option>',
      "  </select></label>",
      '  <button id="q-embaralhar" type="button">embaralhar</button>',
      '  <button id="q-revelar-todas" type="button">revelar todas</button>',
      '  <button id="q-recolher-todas" type="button">recolher</button>',
      "</div>",
      '<p class="quiz-resumo"><span id="q-visiveis"></span> de ' + questoes.length + " questões" +
        (meta && meta.gerado_em ? " · gerado em " + esc(meta.gerado_em.slice(0, 10)) : "") +
      "</p>",
      '<ol class="quiz-lista" id="q-lista"></ol>',
    ].join("");

    const lista = document.getElementById("q-lista");
    let visiveis = questoes;
    let embaralhadas = false;

    function count(base, tem, niv) {
      return base.filter(
        (q) => (!tem || q.tema === tem) && (!niv || q.nivel === niv)
      ).length;
    }

    function ordenar(base) {
      const copia = base.slice();
      const modo = document.getElementById("q-ordem").value;
      if (modo === "dificuldade") {
        const peso = { facil: 0, media: 1, dificil: 2 };
        copia.sort(
          (a, b) =>
            (peso[a.nivel] ?? 1) - (peso[b.nivel] ?? 1) ||
            String(a.tema).localeCompare(String(b.tema)) ||
            a.seq - b.seq
        );
      } else {
        copia.sort((a, b) => a.tema.localeCompare(b.tema) || a.seq - b.seq);
      }
      if (embaralhadas) {
        for (let i = copia.length - 1; i > 0; i--) {
          const j = Math.floor(Math.random() * (i + 1));
          [copia[i], copia[j]] = [copia[j], copia[i]];
        }
      }
      return copia;
    }

    function item(q) {
      const tags = [];
      if (q.nivel) tags.push(NIVEL[q.nivel] || q.nivel);
      if (q.tema) tags.push(q.tema);
      const detalhes = (q.detalhes || []).filter(Boolean);

      return [
        '<li class="quiz-item" data-tema="' + esc(q.tema) + '">',
        '  <div class="quiz-enunciado">' + md(q.enunciado) + "</div>",
        detalhes.length
          ? '  <ul class="quiz-detalhes">' +
              detalhes.map((d) => "<li>" + esc(d) + "</li>").join("") +
              "</ul>"
          : "",
        tags.length
          ? '  <p class="quiz-tags">' +
              tags.map((t) => '<span class="quiz-tag">' + esc(t) + "</span>").join("") +
              "</p>"
          : "",
        '  <button class="quiz-revelar" type="button">revelar</button>',
        '  <div class="quiz-resposta" hidden>' +
          (q.resposta
            ? md(q.resposta)
            : '<p class="quiz-sem-resposta">Ainda sem gabarito no vault.</p>') +
          (q.origem ? '<p class="quiz-origem">' + esc(q.origem) + "</p>" : "") +
        "</div>",
        "</li>",
      ].join("");
    }

    function pintar() {
      lista.innerHTML = ordenar(visiveis).map(item).join("");
      document.getElementById("q-visiveis").textContent = visiveis.length;

      // Sem isto, um filtro sem resultado mostra so "0 de 45", sem dizer
      // que a combinacao escolhida nao existe no banco.
      let aviso = lista.nextElementSibling;
      if (!aviso || aviso.id !== "q-vazio") {
        aviso = document.createElement("p");
        aviso.id = "q-vazio";
        aviso.className = "quiz-vazio";
        lista.after(aviso);
      }
      aviso.textContent = visiveis.length
        ? ""
        : "Nenhuma questão com esses filtros. Uma parte do banco não informa nível de dificuldade, então combiná-lo com ela não retorna nada.";

      lista.querySelectorAll(".quiz-revelar").forEach((btn) => {
        btn.addEventListener("click", () => {
          const box = btn.nextElementSibling;
          const aberto = !box.hidden;
          box.hidden = aberto;
          btn.textContent = aberto ? "revelar" : "revelar menos";
        });
      });
    }

    function filtrar() {
      const tem = document.getElementById("q-tema").value;
      const niv = document.getElementById("q-nivel").value;
      visiveis = questoes.filter(
        (q) => (!tem || q.tema === tem) && (!niv || q.nivel === niv)
      );

      // atualiza contadores nos selects
      document.querySelectorAll("#q-tema option").forEach((o) => {
        const m = o.value;
        o.textContent = (m || "todos ") + "(" + count(questoes, m, niv) + ")";
      });
      document.querySelectorAll("#q-nivel option").forEach((o) => {
        const n = o.value;
        o.textContent = (n ? NIVEL[n] || n : "todos") + " (" + count(questoes, tem, n) + ")";
      });

      pintar();
    }

    document.getElementById("q-tema").addEventListener("change", filtrar);
    document.getElementById("q-nivel").addEventListener("change", filtrar);
    document.getElementById("q-ordem").addEventListener("change", pintar);
    document.getElementById("q-embaralhar").addEventListener("click", () => {
      embaralhadas = !embaralhadas;
      pintar();
    });

    const todos = (abrir) => () =>
      lista.querySelectorAll(".quiz-resposta").forEach((b) => {
        b.hidden = !abrir;
      });
    document.getElementById("q-revelar-todas").addEventListener("click", todos(true));
    document.getElementById("q-recolher-todas").addEventListener("click", todos(false));
    document.getElementById("q-revelar-todas").addEventListener("click", () => {
      lista.querySelectorAll(".quiz-revelar").forEach((b) => (b.textContent = "revelar menos"));
    });
    document.getElementById("q-recolher-todas").addEventListener("click", () => {
      lista.querySelectorAll(".quiz-revelar").forEach((b) => (b.textContent = "revelar"));
    });

    filtrar();
  }
})();
</script>

<style>
  #quiz-app { margin-top: 1.5rem; }
  .quiz-controles {
    display: flex; flex-wrap: wrap; gap: 0.75rem 1.25rem;
    align-items: flex-end; padding: 1rem;
    border: 1px solid var(--lightgray); border-radius: 8px;
  }
  .quiz-controles label {
    display: flex; flex-direction: column; gap: 0.25rem;
    font-size: 0.85rem; color: var(--darkgray);
  }
  .quiz-controles select, .quiz-controles button {
    font: inherit; font-size: 0.9rem; padding: 0.35rem 0.6rem;
    border: 1px solid var(--lightgray); border-radius: 6px;
    background: var(--light); color: var(--dark); cursor: pointer;
  }
  .quiz-controles button:hover { border-color: var(--secondary); }
  .quiz-resumo { font-size: 0.85rem; color: var(--darkgray); }
  .quiz-carregando, .quiz-erro { color: var(--darkgray); font-style: italic; }
  .quiz-lista { padding-left: 1.5rem; }
  .quiz-item { margin-bottom: 1.75rem; }
  .quiz-enunciado { margin-bottom: 0.35rem; }
  .quiz-enunciado p { margin: 0; }
  .quiz-enunciado ol, .quiz-enunciado ul { margin: 0.35rem 0; padding-left: 1.4rem; }
  .quiz-detalhes {
    font-size: 0.9rem; color: var(--darkgray);
    margin: 0.25rem 0; padding-left: 1.25rem;
  }
  .quiz-tags { margin: 0.4rem 0; display: flex; gap: 0.4rem; flex-wrap: wrap; }
  .quiz-tag {
    font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.05em;
    padding: 0.15rem 0.5rem; border-radius: 999px;
    background: var(--lightgray); color: var(--darkgray);
  }
  .quiz-revelar {
    font: inherit; font-size: 0.8rem; padding: 0.25rem 0.7rem;
    border: 1px solid var(--lightgray); border-radius: 6px;
    background: transparent; color: var(--secondary); cursor: pointer;
  }
  .quiz-revelar:hover { background: var(--lightgray); }
  .quiz-resposta {
    margin-top: 0.5rem; padding: 0.75rem 1rem;
    border-left: 3px solid var(--secondary);
    background: var(--lightgray);
    border-radius: 0 6px 6px 0;
  }
  .quiz-resposta p { margin: 0; }
  .quiz-sem-resposta { color: var(--darkgray); font-style: italic; }
  .quiz-origem { font-size: 0.75rem; color: var(--darkgray); margin-top: 0.4rem; }
</style>
