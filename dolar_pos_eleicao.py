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

from matplotlib.patches import FancyBboxPatch

BG, FG, MUTED, GRID = "#0f1115", "#f2f4f8", "#8b93a3", "#232733"
UP, DOWN = "#2ecc8f", "#ff5c6c"
plt.rcParams["font.family"] = ["DejaVu Sans"]

def grafico(dados, titulo, sub, arq, nota, ncls=None):
    fig = plt.figure(figsize=(10, 6.2), dpi=200, facecolor=BG)
    ax = fig.add_axes([.08, .14, .86, .60], facecolor=BG)
    xs = list(range(len(dados)))
    vals = list(dados.values())
    lim = max(abs(v) for v in vals) * 1.28
    ax.set_ylim(min(min(vals) * 1.35, -lim * .08), max(max(vals) * 1.25, lim * .1))
    ax.set_xlim(-.6, len(xs) - .4)
    for v in range(-100, 101, 20):
        ax.axhline(v, color=GRID, lw=.8, zorder=0)
    ax.axhline(0, color=MUTED, lw=1.1, zorder=1)
    for x, v in zip(xs, vals):
        c = UP if v > 0 else DOWN
        ax.bar(x, v, width=.56, color=c, zorder=2)
        txt = f"{v:+.1f}%".replace(".", ",").replace("-", "\u2212")
        ax.text(x, v + (lim * .03 if v > 0 else -lim * .03), txt, ha="center",
                va="bottom" if v > 0 else "top", color=FG, fontsize=14, fontweight="bold")
    ax.set_xticks(xs)
    ax.set_xticklabels([str(a) for a in dados], color=FG, fontsize=13, fontweight="bold")
    ax.tick_params(axis="x", length=0, pad=10)
    ax.set_yticks([t for t in range(-100, 101, 20) if -lim <= t <= lim])
    ax.set_yticklabels([f"{t}%".replace("-", "\u2212") for t in ax.get_yticks()], color=MUTED, fontsize=10)
    ax.tick_params(axis="y", length=0)
    for sp in ax.spines.values(): sp.set_visible(False)
    fig.text(.08, .93, titulo, color=FG, fontsize=22, fontweight="bold")
    fig.text(.08, .875, sub, color=MUTED, fontsize=11.5)
    # legenda
    fig.patches.append(plt.Rectangle((.08, .795), .012, .02, transform=fig.transFigure, fc=UP))
    fig.text(.098, .797, "Dólar subiu", color=FG, fontsize=10.5)
    fig.patches.append(plt.Rectangle((.21, .795), .012, .02, transform=fig.transFigure, fc=DOWN))
    fig.text(.228, .797, "Dólar caiu", color=FG, fontsize=10.5)
    fig.text(.08, .05, "Ano da eleição", color=MUTED, fontsize=10)
    fig.text(.08, .02, nota, color=MUTED, fontsize=8.5)
    fig.savefig(arq, facecolor=BG); plt.close(fig)

fonte = "Fonte: PTAX de venda (Banco Central), último dia útil de cada ano. Base: fim do ano da eleição."
grafico(um_ano, "Dólar 1 ano após a eleição",
        "Variação do dólar em reais, do fim do ano eleitoral ao fim do ano seguinte",
        "dolar_1_ano_pos_eleicao.png", fonte)
grafico(quatro, "Dólar em ciclos de 4 anos",
        "Variação do dólar em reais até a eleição seguinte (ciclo de 2022 ainda em curso)",
        "dolar_ciclo_4_anos.png", fonte)
