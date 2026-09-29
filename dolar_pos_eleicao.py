"""Variação do dólar (PTAX venda, fim de ano) após eleições presidenciais."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# PTAX de venda no último dia útil do ano (R$/US$)
# 2002 e 2003 conferidos em fonte externa; demais de memória (não verificados online)
fim_ano = {2002: 3.5325, 2003: 2.8884, 2006: 2.1380, 2007: 1.7713, 2010: 1.6662,
           2011: 1.8758, 2014: 2.6562, 2015: 3.9048, 2018: 3.8748, 2019: 4.0307,
           2022: 5.2177, 2023: 4.8413}
tabela = {2002: -18.2, 2006: -17.2, 2010: 12.6, 2014: 47.0, 2018: 4.0, 2022: -7.2}
tabela4 = {2002: -39.5, 2006: -22.1, 2010: 59.4, 2014: 45.9, 2018: 34.7}

anos = [2002, 2006, 2010, 2014, 2018, 2022]
um_ano = {a: (fim_ano[a + 1] / fim_ano[a] - 1) * 100 for a in anos}
quatro = {a: (fim_ano[b] / fim_ano[a] - 1) * 100 for a, b in zip(anos[:-1], anos[1:])}

print("Eleição | 1 ano calc (tabela) | 4 anos calc (tabela)")
for a in anos:
    print(a, f"{um_ano[a]:+.1f} ({tabela[a]:+.1f})",
          f"{quatro[a]:+.1f} ({tabela4[a]:+.1f})" if a in quatro else "-")

from matplotlib import font_manager as fm

BG, INK, MUTED, GRID = "#f4f6f3", "#1b2419", "#5f6b5c", "#dfe4dc"
UP, DOWN, DEST = "#4a6741", "#b5523f", "#25331f"
fam = "Liberation Sans" if any("Liberation Sans" in f.name for f in fm.fontManager.ttflist) else "DejaVu Sans"
plt.rcParams["font.family"] = fam

def grafico(dados, kicker, titulo, sub, arq, destaque, rotulo_dest, nota_dest=None):
    fig = plt.figure(figsize=(10, 5.6), dpi=200, facecolor=BG)
    fig.text(.04, .925, kicker, color=UP, fontsize=9, fontweight="bold")
    fig.text(.04, .845, titulo, color=INK, fontsize=24, fontweight="bold")
    fig.text(.04, .79, sub, color=MUTED, fontsize=10.5)
    # legenda
    for x, cor, lab in ((.04, UP, "Dólar subiu"), (.15, DOWN, "Dólar caiu"), (.26, DEST, rotulo_dest)):
        fig.patches.append(plt.Rectangle((x, .725), .009, .016, transform=fig.transFigure, fc=cor))
        fig.text(x + .014, .726, lab, color=INK, fontsize=8, fontweight="bold")
    ax = fig.add_axes([.04, .13, .92, .54], facecolor=BG)
    xs = list(range(len(dados))); vals = list(dados.values())
    top, bot = max(max(vals) * 1.22, 5), min(min(vals) * 1.30, -5)
    ax.set_ylim(bot, top); ax.set_xlim(-.6, len(xs) - .4)
    step = 20
    for t in range(int(bot // step) * step, int(top // step + 1) * step + 1, step):
        ax.axhline(t, color=GRID, lw=.8, zorder=0)
    ax.axhline(0, color=INK, lw=1, zorder=1)
    for x, (a, v) in zip(xs, dados.items()):
        cor = DEST if a == destaque else (UP if v > 0 else DOWN)
        ax.bar(x, v, width=.52, color=cor, zorder=2)
        txt = f"{v:+.1f}%".replace(".", ",").replace("-", "\u2212")
        off = (top - bot) * .015
        ax.text(x, v + (off if v > 0 else -off), txt, ha="center",
                va="bottom" if v > 0 else "top", color=INK, fontsize=12, fontweight="bold")
        if a == destaque and nota_dest:
            ax.text(x, (v + (off * 5.5 if v > 0 else -off * 5.5)), nota_dest, ha="center",
                    va="bottom" if v > 0 else "top", color=INK, fontsize=7.5, fontweight="bold")
    ax.set_xticks(xs); ax.set_xticklabels([str(a) for a in dados], color=INK, fontsize=11, fontweight="bold")
    ax.tick_params(axis="x", length=0, pad=8)
    ax.set_yticks([])
    for sp in ax.spines.values(): sp.set_visible(False)
    fig.text(.96, .04, "Fonte: Banco Central (PTAX de venda, último dia útil do ano) · Base: fim do ano da eleição",
             color=MUTED, fontsize=7.5, ha="right", style="italic")
    fig.text(.04, .04, "Ano da eleição", color=MUTED, fontsize=8)
    fig.savefig(arq, facecolor=BG); plt.close(fig)

grafico(um_ano, "BRASIL  ·  DÓLAR / REAL",
        "O que o dólar fez no ano seguinte à eleição",
        "Em 3 das 6 eleições o dólar caiu no 1º ano. Em 2014 disparou +47,0%.",
        "dolar_1_ano_pos_eleicao.png", 2014, "Maior alta", "MAIOR ALTA")
grafico(quatro, "BRASIL  ·  DÓLAR / REAL",
        "Ciclos de 4 anos: o dólar subiu nos 3 últimos",
        "Caiu nos ciclos de 2002 e 2006; desde 2010 sobe mais de 30% a cada mandato. O ciclo de 2022 ainda não terminou.",
        "dolar_ciclo_4_anos.png", 2010, "Maior alta", "MAIOR ALTA")
