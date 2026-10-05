---
title: "Lab 01 - Contando tokens e medindo custo"
tags:
  - "lab"
  - "tokens"
tipo: "lab"
date: "2026-10-07"
---

# Lab 01 — Contando tokens e medindo custo

> **O que este lab prova:** que contagem de tokens é propriedade do modelo, que a proxy `len(text.split())` erra sistematicamente, e que o custo de uma conversa cresce de forma superlinear.

## Pergunta

Quanto um texto custa em tokens, e quanto a diferença entre proxies (palavras vs. caracteres vs. tokens reais) distorce a estimativa?

## Hipótese

> O tokenizador real produz contagens **substancialmente diferentes** de `len(split())`, especialmente em português; e a razão tokens/palavra varia entre idiomas e entre encodings do mesmo provedor.

## Setup

```bash
pip install tiktoken
```

## Código

```python
import tiktoken

ENCODINGS = ["cl100k_base", "o200k_base"]

TEXTOS = {
 "en": "Natural language processing is a fascinating field of artificial intelligence.",
 "pt": "O processamento de linguagem natural é um campo Fascinante da inteligência artificial.",
 "es": "El procesamiento de lenguaje natural es un campo fascinante de la inteligencia artificial.",
 "de": "Die Verarbeitung natürlicher Sprache ist ein faszinierendes Gebiet der künstlichen Intelligenz.",
 "ru": "Обработка естественного языка — это увлекательная область искусственного интеллекта.",
}

print(f"{'enc':<14}{'idioma':<8}{'tokens':>8}{'palavras':>10}{'chars':>8}{'tok/palavra':>14}")
print("-" * 62)
for enc_name in ENCODINGS:
 enc = tiktoken.get_encoding(enc_name)
 for idioma, txt in TEXTOS.items():
 n_tok = len(enc.encode(txt))
 n_pal = len(txt.split())
 print(f"{enc_name:<14}{idioma:<8}{n_tok:>8}{n_pal:>10}{len(txt):>8}{n_tok/n_pal:>14.2f}")
 print()

# --- Verificação 1: o tokenizador é reversível ---
enc = tiktoken.get_encoding("o200k_base")
assert enc.decode(enc.encode("Olá, mundo! 123 🧠")) == "Olá, mundo! 123 🧠"
print("✓ tokenização reversível")

# --- Verificação 2: o mesmo texto, encodings diferentes ---
txt = TEXTOS["pt"]
a = len(tiktoken.get_encoding("cl100k_base").encode(txt))
b = len(tiktoken.get_encoding("o200k_base").encode(txt))
print(f"cl100k={a} o200k={b} (mesmo texto, tokenizadores diferentes)")

# --- Verificação 3: custo de conversa longa ---
print("\n--- custo acumulado de uma conversa ---")
turnos = ["Turno de usuário e resposta, cerca de 300 tokens por turno."] * 20
total_input = 0
for i in range(1, len(turnos) + 1):
 # a cada turno o histórico inteiro (i blocos) é reenviado
 total_input += i * 300
 print(f"turno {i:>2}: entrada acumulada = {total_input:>7} tokens")
print(f"\nTotal: {total_input} tokens de entrada")
print(f"Se cada chamada fosse isolada: {20 * 300} tokens")
print(f"Overhead do histórico: {total_input / (20 * 300):.1f}x")
```

## Como rodar

```bash
python lab01_tokens.py
```

## O que observei

| Métrica | Valor | Interpretação |
| --- | --- | --- |
| tokens/palavra em EN | ~1.3 | baseline do inglês |
| tokens/palavra em PT/ES | ~1.5–2.0 | idioma paga mais caro |
| cl100k vs o200k em PT | difere | trocar de modelo muda a conta |
| overhead de 20 turnos | ~10x | conversa longa custa muito mais do que parece |

> **Preencha com os números que você realmente obteve.**

## Análise

- [ ] Minha hipótese se confirmou?
- [ ] Qual idioma da sua área de interesse é mais penalizado?
- [ ] Em quanto o `len(split())` erra em português?

## Extensão (o que eu faria com mais tempo)

- [ ] Incluir japonês e chinês (eficientes por caractere, não por palavra).
- [ ] Comparar 3 modelos de provedores diferentes no mesmo texto.
- [ ] Implementar um contador de custo que simule prompt caching (prefixo fixo vs. variável).
- [ ] Escrever um teste que falha se alguém usar `len(split())` como proxy de custo.

## Conceitos tocados


## Erros que cometi

> Não apague — é o registro.

- 

---
*Atualizado em 2026-09-30*
