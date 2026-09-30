"""Bloco 1: (a) comentário de cada período (12 meses após a eleição) e (b) dólar aqui x dólar no mundo.

Dados: USD/BRL mensal e DXY futuros mensal (Investing), base = fechamento de novembro do ano da eleição.
Comentários: contexto histórico (não calculado nos dados).
"""
import csv, datetime as dt
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
vb = {e: (brl[(e + 1, 11)] / brl[(e, 11)] - 1) * 100 for e in ELE}
vd = {e: (dxy[(e + 1, 11)] / dxy[(e, 11)] - 1) * 100 for e in ELE}
vr = {e: ((1 + vb[e] / 100) / (1 + vd[e] / 100) - 1) * 100 for e in ELE}   # efeito do real

BG, INK, MUTED, GRID = "#f4f6f3", "#1b2419", "#5f6b5c", "#dfe4dc"
UP, DOWN, BLUE = "#4a6741", "#b5523f", "#3b6ea8"
plt.rcParams["font.family"] = "Liberation Sans" if any("Liberation Sans" in f.name for f in fm.fontManager.ttflist) else "DejaVu Sans"
rot = lambda v: f"{v:+.1f}%".replace(".", ",").replace("-", "−")
cor = lambda v: UP if v > 0 else DOWN

# ------------------------------------------------------------------ (a) comentários (cartões curtos)
from matplotlib.patches import FancyBboxPatch
TAGS = {2002: ("Confiança volta após a eleição", "Dólar fraco, mais apetite por risco"),
        2006: ("Inflação baixa e juros em queda", "Boom de commodities"),
        2010: ("Alta concentrada em set/2011", "Crise do euro"),
        2014: ("Crise fiscal e recessão", "Fim do estímulo do Fed"),
        2018: ("Ruído político pós-eleição", "Guerra comercial EUA-China"),
        2022: ("Dúvida fiscal, depois arcabouço", "Dólar perde força após o pico")}
fig = plt.figure(figsize=(10, 6.2), dpi=200, facecolor=BG)
fig.text(.05, .92, "O que estava por trás de cada período", color=INK, fontsize=23, fontweight="bold")
fig.text(.05, .875, "12 meses após cada eleição, de novembro a novembro", color=MUTED, fontsize=11)
W, H, GX, GY = .285, .355, .0325, .045
for i, e in enumerate(ELE):
    col, row = i % 3, i // 3
    x0 = .05 + col * (W + GX); y0 = .47 - row * (H + GY)
    fig.add_artist(FancyBboxPatch((x0, y0), W, H, boxstyle="round,pad=0,rounding_size=.012", transform=fig.transFigure,
                                  fc="white", ec=GRID, lw=1.2))
    fig.text(x0 + .02, y0 + H - .04, f"{e} → {e+1}", color=MUTED, fontsize=10.5, fontweight="bold", va="center")
    fig.text(x0 + .02, y0 + H - .10, rot(vb[e]), color=cor(vb[e]), fontsize=24, fontweight="bold", va="center")
    fig.text(x0 + .02, y0 + H - .152, f"DXY {rot(vd[e])}", color=BLUE, fontsize=10.5, fontweight="bold", va="center")
    fig.add_artist(plt.Line2D([x0 + .02, x0 + W - .02], [y0 + .135, y0 + .135], color=GRID, lw=1))
    br, mu = TAGS[e]
    fig.text(x0 + .02, y0 + .105, "BRASIL", color=MUTED, fontsize=7.5, fontweight="bold", va="center")
    fig.text(x0 + .02, y0 + .083, br, color=INK, fontsize=9.3, va="center")
    fig.text(x0 + .02, y0 + .052, "MUNDO", color=MUTED, fontsize=7.5, fontweight="bold", va="center")
    fig.text(x0 + .02, y0 + .030, mu, color=INK, fontsize=9.3, va="center")
fig.text(.05, .028, "Dólar = USD/BRL. Motivos: contexto histórico, não calculado nos dados. Fonte: Investing (fechamento mensal).", color=MUTED, fontsize=8)
fig.savefig("bloco1_comentarios_periodos.png", facecolor=BG); plt.close(fig)

# ------------------------------------------------------------------ (b) aqui x mundo
TAG = {2002: "Caíram juntos", 2006: "Caíram juntos, o real mais", 2010: "Subiu aqui, caiu no mundo",
       2014: "Subiram juntos, o real muito mais", 2018: "Mundo parado, subiu aqui", 2022: "Caíram juntos"}
fig = plt.figure(figsize=(10, 6.4), dpi=200, facecolor=BG)
fig.text(.05, .92, "O dólar subiu só aqui ou no mundo todo?", color=INK, fontsize=23, fontweight="bold")
fig.text(.05, .875, "Variação em 12 meses após cada eleição: dólar contra o real x DXY (dólar contra as moedas do mundo)", color=MUTED, fontsize=11)
ax = fig.add_axes([.20, .20, .48, .58], facecolor=BG)
ax.set_xlim(-28, 66); ax.set_ylim(-.6, 5.6); ax.set_yticks([])
for sp in ax.spines.values(): sp.set_visible(False)
ax.axvline(0, color=INK, lw=.8, alpha=.45, zorder=1)
for v in (-20, 20, 40): ax.axvline(v, color=GRID, lw=.8, zorder=0)
ax.set_xticks([-20, 0, 20, 40]); ax.set_xticklabels(["−20%", "0", "+20%", "+40%"], fontsize=9, color=MUTED); ax.tick_params(length=0, pad=6)
for i, e in enumerate(ELE):
    yy = 5 - i
    ax.plot([vd[e], vb[e]], [yy, yy], color="#bfc7bb", lw=5, solid_capstyle="round", zorder=2)
    ax.scatter([vd[e]], [yy], s=110, color=BLUE, zorder=4)
    ax.scatter([vb[e]], [yy], s=170, color=cor(vb[e]), zorder=5)
    lo, hi = sorted([vd[e], vb[e]])
    ax.text(vd[e] + (-2.4 if vd[e] <= vb[e] else 2.4), yy + .02, rot(vd[e]), ha="right" if vd[e] <= vb[e] else "left", va="center", fontsize=9, color=BLUE, fontweight="bold")
    ax.text(vb[e] + (2.6 if vb[e] >= vd[e] else -2.6), yy + .02, rot(vb[e]), ha="left" if vb[e] >= vd[e] else "right", va="center", fontsize=10.5, color=cor(vb[e]), fontweight="bold")
    fig.text(.05, .20 + .58 * (yy + .6) / 6.2, f"{e} → {e+1}", color=INK, fontsize=10.5, fontweight="bold", va="center")
    fig.text(.74, .20 + .58 * (yy + .6) / 6.2, TAG[e], color=INK, fontsize=10, va="center")
    fig.text(.74, .20 + .58 * (yy + .6) / 6.2 - .03, f"efeito do real: {rot(vr[e])}", color=MUTED, fontsize=8.5, va="center")
fig.text(.20, .815, "●", color=BLUE, fontsize=12, va="center"); fig.text(.22, .815, "DXY (mundo)", color=INK, fontsize=9.5, va="center")
fig.text(.35, .815, "●", color=UP, fontsize=14, va="center"); fig.text(.372, .815, "Dólar contra o real", color=INK, fontsize=9.5, va="center")
fig.text(.05, .095, "Quando o dólar sobe aqui bem mais do que o DXY, os fatores brasileiros ganham peso. Quando os dois andam juntos, há força do dólar no mundo.", color=INK, fontsize=9.5)
fig.text(.05, .06, "Efeito do real = variação do USD/BRL em relação à do DXY (1 + USD/BRL) ÷ (1 + DXY) − 1.", color=MUTED, fontsize=8.5)
fig.text(.05, .028, "Fonte: Investing (USD/BRL mensal e DXY futuros mensal). Base: fechamento de novembro do ano da eleição.", color=MUTED, fontsize=8)
fig.savefig("bloco1_dolar_aqui_x_mundo.png", facecolor=BG); plt.close(fig)
