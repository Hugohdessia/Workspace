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

def base(kicker, titulo, sub, legenda):
    fig = plt.figure(figsize=(10, 5.6), dpi=200, facecolor=BG)
    fig.text(.04, .925, kicker, color=UP, fontsize=9, fontweight="bold")
    fig.text(.04, .845, titulo, color=INK, fontsize=24, fontweight="bold")
    fig.text(.04, .79, sub, color=MUTED, fontsize=10.5)
    x = .04
    for cor, lab, w in legenda:
        fig.patches.append(plt.Rectangle((x, .725), .009, .016, transform=fig.transFigure, fc=cor))
        fig.text(x + .014, .726, lab, color=INK, fontsize=8, fontweight="bold")
        x += w
    ax = fig.add_axes([.06, .12, .90, .56], facecolor=BG)
    ax.set_xlim(2001.2, 2023.8); ax.set_ylim(0, 6.3)
    ax.set_xticks(range(2002, 2024, 4) if False else [2002, 2006, 2010, 2014, 2018, 2022])
    ax.set_xticklabels(["Eleição\n2002", "Eleição\n2006", "Eleição\n2010", "Eleição\n2014", "Eleição\n2018", "Eleição\n2022"],
                       color=INK, fontsize=9.5, fontweight="bold")
    ax.set_yticks(range(0, 7)); ax.set_yticklabels([f"R$ {t}" for t in range(0, 7)], color=MUTED, fontsize=8.5)
    ax.tick_params(length=0, pad=6)
    ax.grid(axis="y", color=GRID, lw=.8); ax.set_axisbelow(True)
    for sp in ax.spines.values(): sp.set_visible(False)
    fig.text(.96, .03, "Fonte: Banco Central (PTAX de venda, último dia útil do ano). Cotação de fim de ano.",
             color=MUTED, fontsize=7.5, ha="right", style="italic")
    fig.text(.04, .03, "Dólar em R$ no fim de cada ano", color=MUTED, fontsize=8)
    return fig, ax

def rot(v): return f"{v:+.1f}%".replace(".", ",").replace("-", "\u2212")

# ---- 1) Linha do tempo: 1 ano após cada eleição
fig, ax = base("BRASIL  ·  DÓLAR / REAL", "O dólar no 1º ano depois de cada eleição",
               "Cada trecho colorido liga o fim do ano da eleição ao fim do ano seguinte.",
               [(UP, "Dólar subiu", .11), (DOWN, "Dólar caiu", .11)])
for a in anos:
    v = um_ano[a]; c = UP if v > 0 else DOWN
    ax.axvline(a, color=GRID, lw=1.2, zorder=1)
    ax.plot([a, a + 1], [fim_ano[a], fim_ano[a + 1]], color=c, lw=4.5, solid_capstyle="round", zorder=3)
    ax.scatter([a], [fim_ano[a]], s=70, color=BG, edgecolor=INK, lw=1.8, zorder=4)
    ax.scatter([a + 1], [fim_ano[a + 1]], s=70, color=c, edgecolor=c, zorder=4)
    y = max(fim_ano[a], fim_ano[a + 1]) + .35
    ax.annotate(rot(v), (a + .5, y), ha="center", va="bottom", fontsize=12.5, fontweight="bold",
                color=INK, bbox=dict(boxstyle="round,pad=.3", fc=BG, ec=c, lw=1.6), zorder=5)
    ax.text(a, fim_ano[a] - .28, f"{fim_ano[a]:.2f}".replace(".", ","), ha="center", va="top", fontsize=8, color=MUTED)
    ax.text(a + 1.12, fim_ano[a + 1], f"{fim_ano[a + 1]:.2f}".replace(".", ","), ha="left", va="center", fontsize=8, color=MUTED)
fig.savefig("dolar_1_ano_pos_eleicao.png", facecolor=BG); plt.close(fig)

# ---- 2) Linha do tempo: ciclos de 4 anos
fig, ax = base("BRASIL  ·  DÓLAR / REAL", "Ciclos de 4 anos: o dólar subiu nos 3 últimos",
               "Do fim de um ano eleitoral ao fim do seguinte. O ciclo de 2022 ainda não terminou.",
               [(UP, "Dólar subiu", .11), (DOWN, "Dólar caiu", .11), (MUTED, "Em curso", .1)])
for k, a in enumerate(anos[:-1]):
    b = anos[k + 1]; v = quatro[a]; c = UP if v > 0 else DOWN
    if k % 2 == 0: ax.axvspan(a, b, color="#eaeee7", zorder=0)
    ax.plot([a, b], [fim_ano[a], fim_ano[b]], color=c, lw=4.5, solid_capstyle="round", zorder=3)
    ax.annotate(rot(v), ((a + b) / 2, 5.95), ha="center", va="top", fontsize=13.5, fontweight="bold",
                color=INK, bbox=dict(boxstyle="round,pad=.35", fc=BG, ec=c, lw=1.8), zorder=5)
    ax.text((a + b) / 2, 5.3, f"{a} \u2192 {b}", ha="center", va="top", fontsize=8.5, color=MUTED)
ax.plot([2022, 2023], [fim_ano[2022], fim_ano[2023]], color=MUTED, lw=3.5, ls=(0, (2, 2)), zorder=3)
ax.axvspan(2022, 2023.8, color="#eaeee7", zorder=0)
ax.text(2023.1, 5.3, "2022 \u2192 ?", ha="center", va="top", fontsize=8.5, color=MUTED)
ax.text(2023.1, 5.95, "em curso", ha="center", va="top", fontsize=11, fontweight="bold", color=MUTED)
for a in anos:
    ax.scatter([a], [fim_ano[a]], s=80, color=BG, edgecolor=INK, lw=2, zorder=4)
    ax.text(a, fim_ano[a] - .3, f"{fim_ano[a]:.2f}".replace(".", ","), ha="center", va="top", fontsize=8.5, color=INK, fontweight="bold")
fig.savefig("dolar_ciclo_4_anos.png", facecolor=BG); plt.close(fig)
