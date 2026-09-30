"""Dólar no Brasil x dólar no mundo (DXY) nos 12 meses após cada eleição, base 100 em novembro do ano eleitoral.

O espaço entre as linhas é o efeito do real: dólar no Brasil acima do DXY = real mais fraco; abaixo = real mais forte.
Fonte: Investing (USD/BRL mensal e DXY futuros mensal).
"""
import csv, datetime as dt, math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

def ler(a):
    s = {}
    for r in csv.DictReader(open(a, encoding="utf-8-sig")):
        d = dt.datetime.strptime(r["Data"], "%d.%m.%Y").date(); s[(d.year, d.month)] = float(r["Último"].replace(",", "."))
    return s
brl = ler("dados/usdbrl_mensal.csv"); dxy = ler("dados/dxy_futuros_mensal.csv")
ELE = [2002, 2006, 2010, 2014, 2018, 2022]
BG, INK, MUTED, GRID = "#f4f6f3", "#1b2419", "#5f6b5c", "#dfe4dc"
UP, DOWN, BLUE = "#4a6741", "#b5523f", "#3b6ea8"
plt.rcParams["font.family"] = "Liberation Sans" if any("Liberation Sans" in f.name for f in fm.fontManager.ttflist) else "DejaVu Sans"
rot = lambda v: f"{v:+.1f}%".replace(".", ",").replace("-", "−")

def serie(e):
    meses = [(e, 11), (e, 12)] + [(e + 1, m) for m in range(1, 12)] + [(e + 1, 11)]
    meses = [(e, 11), (e, 12)] + [(e + 1, m) for m in range(1, 12)]
    return meses

fig = plt.figure(figsize=(10, 7.6), dpi=200, facecolor=BG)
fig.text(.05, .945, "O dólar se moveu por causa do mundo ou do Brasil?", color=INK, fontsize=23, fontweight="bold")
fig.text(.05, .905, "Nos 12 meses após cada eleição: dólar no Brasil x dólar no mundo (DXY), os dois partindo de 100", color=MUTED, fontsize=11)
# legenda
L = fig.add_axes([0, 0, 1, 1]); L.set_xlim(0, 1); L.set_ylim(0, 1); L.axis("off"); L.patch.set_alpha(0)
L.plot([.05, .075], [.865, .865], color=INK, lw=3); fig.text(.082, .865, "Dólar no Brasil (USD/BRL)", color=INK, fontsize=9.5, va="center")
L.plot([.27, .295], [.865, .865], color=BLUE, lw=3); fig.text(.302, .865, "Dólar no mundo (DXY)", color=INK, fontsize=9.5, va="center")
L.add_patch(plt.Rectangle((.47, .857), .02, .016, fc=DOWN, alpha=.45, ec="none")); fig.text(.497, .865, "Real mais fraco (dólar no Brasil acima do DXY)", color=INK, fontsize=9.5, va="center")
L.add_patch(plt.Rectangle((.775, .857), .02, .016, fc=UP, alpha=.45, ec="none")); fig.text(.802, .865, "Real mais forte", color=INK, fontsize=9.5, va="center")

PW, PH = .285, .285
POS = [(.065, .525), (.375, .525), (.685, .525), (.065, .125), (.375, .125), (.685, .125)]
for (px, py), e in zip(POS, ELE):
    ms = [(e, 11), (e, 12)] + [(e + 1, m) for m in range(1, 11)] + [(e + 1, 11)]
    xs = list(range(len(ms)))
    b = [brl[m] / brl[ms[0]] * 100 for m in ms]; d = [dxy[m] / dxy[ms[0]] * 100 for m in ms]
    vb, vd = b[-1] - 100, d[-1] - 100
    tb, tw = math.log(b[-1] / 100), math.log(d[-1] / 100)
    share = tw / tb if tb else 0
    quem = "o mundo" if share >= .65 else ("o Brasil" if share <= .35 else "mundo e Brasil")
    ax = fig.add_axes([px, py, PW, PH], facecolor=BG)
    ax.set_xlim(0, len(ms) - 1 + 4.3); ax.set_ylim(70, 158)
    for s in ("top", "right", "left"): ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(GRID); ax.set_yticks([])
    ax.axhline(100, color=INK, lw=.8, alpha=.35, zorder=1)
    for v in (80, 120, 140): ax.axhline(v, color=GRID, lw=.7, zorder=0)
    ax.fill_between(xs, d, b, where=[bb >= dd for bb, dd in zip(b, d)], color=DOWN, alpha=.30, lw=0, interpolate=True, zorder=1)
    ax.fill_between(xs, d, b, where=[bb <= dd for bb, dd in zip(b, d)], color=UP, alpha=.30, lw=0, interpolate=True, zorder=1)
    ax.plot(xs, d, color=BLUE, lw=2.6, zorder=3); ax.plot(xs, b, color=INK, lw=2.6, zorder=4)
    ax.set_xticks([0, len(ms) - 1]); ax.set_xticklabels([f"Nov/{str(e)[2:]}", f"Nov/{str(e+1)[2:]}"], fontsize=8.5, color=MUTED)
    ax.tick_params(length=0, pad=4)
    # rótulos no fim das linhas (afastados se ficarem juntos)
    yb, yd = b[-1], d[-1]
    if abs(yb - yd) < 14:
        mid = (yb + yd) / 2; yb, yd = (mid + 7, mid - 7) if b[-1] >= d[-1] else (mid - 7, mid + 7)
    ax.text(len(ms) - 1 + .5, yb, rot(vb), color=INK, fontsize=11.5, fontweight="bold", va="center")
    ax.text(len(ms) - 1 + .5, yd, rot(vd), color=BLUE, fontsize=10.5, fontweight="bold", va="center")
    fig.text(px, py + PH + .022, f"{e} → {e+1}", color=INK, fontsize=12.5, fontweight="bold", va="center")
    real_fraco = b[-1] > d[-1]
    fig.text(px + PW, py + PH + .022, "Real mais fraco" if real_fraco else "Real mais forte", color=DOWN if real_fraco else UP, fontsize=10.5, fontweight="bold", va="center", ha="right")
    ax.text(0.2, 153, f"Quem pesa mais: {quem}", color=MUTED, fontsize=9.5, va="center", fontweight="bold")

fig.text(.05, .03, "Linha preta acima da azul = o dólar subiu mais no Brasil do que no mundo, ou seja, o real enfraqueceu. Fonte: Investing (mensal). Base: fechamento de novembro do ano da eleição.", color=MUTED, fontsize=8.2)
fig.savefig("grafico_dolar_vs_dxy_por_periodo.png", facecolor=BG); plt.close(fig)
