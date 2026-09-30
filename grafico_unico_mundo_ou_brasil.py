"""Um gráfico só: variação do dólar nos 12 meses após cada eleição = parte do mundo (DXY) + parte do real.

Soma simples em pontos percentuais: dólar no Brasil (%) = DXY (%) + efeito do real (pontos percentuais).
Base: fechamento de novembro do ano da eleição a novembro do ano seguinte. Fonte: Investing (USD/BRL mensal e DXY futuros mensal).
"""
import csv, datetime as dt
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib import font_manager as fm

def ler(a):
    s = {}
    for r in csv.DictReader(open(a, encoding="utf-8-sig")):
        d = dt.datetime.strptime(r["Data"], "%d.%m.%Y").date(); s[(d.year, d.month)] = float(r["Último"].replace(",", "."))
    return s
brl = ler("dados/usdbrl_mensal.csv"); dxy = ler("dados/dxy_futuros_mensal.csv")
ELE = [2002, 2006, 2010, 2014, 2018, 2022]
rows = []
for e in ELE:
    tot = (brl[(e + 1, 11)] / brl[(e, 11)] - 1) * 100
    mundo = (dxy[(e + 1, 11)] / dxy[(e, 11)] - 1) * 100
    rows.append((e, tot, mundo, tot - mundo))
    print(e, f"dólar {tot:+.1f} = mundo {mundo:+.1f} + real {tot - mundo:+.1f}")

BG, INK, MUTED, GRID = "#f4f6f3", "#1b2419", "#5f6b5c", "#dfe4dc"
UP, DOWN, BLUE = "#4a6741", "#b5523f", "#3b6ea8"
T_SOBE, T_CAI = "#e0eadc", "#f1e1dc"
plt.rcParams["font.family"] = "Liberation Sans" if any("Liberation Sans" in f.name for f in fm.fontManager.ttflist) else "DejaVu Sans"
rot = lambda v, p=1: f"{v:+.{p}f}%".replace(".", ",").replace("-", "−")

fig = plt.figure(figsize=(10, 6.6), dpi=200, facecolor=BG)
fig.text(.05, .935, "O dólar mexeu por causa do mundo ou do Brasil?", color=INK, fontsize=24, fontweight="bold")
fig.text(.05, .893, "Variação do dólar nos 12 meses após cada eleição, separada em duas partes", color=MUTED, fontsize=11.5)
# legenda simples
L = fig.add_axes([0, 0, 1, 1]); L.set_xlim(0, 1); L.set_ylim(0, 1); L.axis("off"); L.patch.set_alpha(0)
for x, cor, txt in ((.05, BLUE, "Dólar no mundo (DXY)"), (.30, DOWN, "Real mais fraco: empurra o dólar para cima"), (.65, UP, "Real mais forte: empurra o dólar para baixo")):
    L.add_patch(plt.Rectangle((x, .842), .018, .022, fc=cor, ec="none")); fig.text(x + .026, .853, txt, color=INK, fontsize=10, va="center")

ax = fig.add_axes([.05, .12, .90, .66], facecolor=BG)
ax.set_xlim(-.6, 5.6); ax.set_ylim(-28, 66)
for sp in ("top", "right", "left"): ax.spines[sp].set_visible(False)
ax.spines["bottom"].set_visible(False); ax.set_yticks([])
ax.axhline(0, color=INK, lw=1, zorder=1)
for v in (-20, 20, 40, 60): ax.axhline(v, color=GRID, lw=.8, zorder=0)
for i, (e, tot, mundo, real) in enumerate(rows):
    pos = neg = 0
    for v, cor in ((mundo, BLUE), (real, DOWN if real > 0 else UP)):
        if v >= 0: ax.bar(i, v, bottom=pos, width=.56, color=cor, zorder=3); mid = pos + v / 2; pos += v
        else: ax.bar(i, v, bottom=neg, width=.56, color=cor, zorder=3); mid = neg + v / 2; neg += v
        if abs(v) >= 2.2: ax.text(i, mid, rot(v, 1), ha="center", va="center", fontsize=10.5 if abs(v) >= 4 else 8.5, fontweight="bold", color="white", zorder=5)
    # total (dólar no Brasil) em destaque
    sobe = tot > 0
    ytop = (pos + 3.5) if tot >= 0 or pos > 0 else 3.5
    ax.text(i, ytop + 2, f"Dólar {rot(tot)}", ha="center", va="bottom", fontsize=12, fontweight="bold", color=INK,
            bbox=dict(boxstyle="round,pad=.35", fc=T_SOBE if sobe else T_CAI, ec="none"), zorder=6)
    ax.text(i, -26.5, f"{e} → {e+1}", ha="center", va="center", fontsize=11.5, fontweight="bold", color=INK)
ax.set_xticks([])
fig.text(.05, .045, "Dólar no Brasil = parte do mundo (DXY) + parte do real. Soma em pontos percentuais. Fonte: Investing (mensal). Base: fechamento de novembro do ano da eleição.", color=MUTED, fontsize=8.5)
fig.savefig("grafico_unico_mundo_ou_brasil.png", facecolor=BG); plt.close(fig)
