"""Quando o DXY subiu: as 6 grandes altas (>= +10%) desde 2001, só o índice.

DXY: Investing (futuros, fechamento mensal). Motivos: contexto histórico (não calculado).
"""
import csv, datetime as dt
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

dxy = {}
for r in csv.DictReader(open("dados/dxy_futuros_mensal.csv", encoding="utf-8-sig")):
    x = dt.datetime.strptime(r["Data"], "%d.%m.%Y").date(); dxy[(x.year, x.month)] = float(r["Último"].replace(",", "."))
ks = sorted(dxy); xm = lambda k: k[0] + k[1] / 12
MES = ["", "jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]

ALTAS = [((2004, 12), (2005, 11), "Fed sobe juros e a economia americana se recupera"),
         ((2008, 3), (2009, 2), "Crise financeira global: corrida ao dólar como porto seguro"),
         ((2009, 11), (2010, 5), "Crise da dívida na Europa enfraquece o euro"),
         ((2011, 4), (2016, 12), "Fed sai do estímulo e sobe juros, enquanto BCE e Japão seguem afrouxando"),
         ((2018, 1), (2020, 3), "Guerra comercial e, em mar/2020, corrida ao dólar na pandemia"),
         ((2020, 12), (2022, 9), "Fed sobe juros mais rápido que os outros e guerra na Ucrânia")]

BG, INK, MUTED, GRID = "#f4f6f3", "#1b2419", "#5f6b5c", "#dfe4dc"
BLUE, GLINE = "#2f5f99", "#b9c4d0"
plt.rcParams["font.family"] = "Liberation Sans" if any("Liberation Sans" in f.name for f in fm.fontManager.ttflist) else "DejaVu Sans"
rot = lambda v: f"{v:+.1f}%".replace(".", ",")
tint = lambda c, a: matplotlib.colors.to_rgba(c, a)

CURTO = {1: "Fed sobe juros", 2: "Crise financeira", 3: "Crise do euro", 4: "Fed x BCE e Japão",
         5: "Guerra comercial e Covid", 6: "Fed e Ucrânia"}
ALTURA = {1: 134, 2: 134, 3: 120, 4: 134, 5: 120, 6: 134}
fig = plt.figure(figsize=(10, 5.8), dpi=200, facecolor=BG)
fig.text(.05, .89, "Quando o dólar no mundo (DXY) subiu", color=INK, fontsize=24, fontweight="bold")
fig.text(.05, .825, "As 6 grandes altas do DXY desde 2001 (subidas de pelo menos +10%) e o que estava por trás", color=MUTED, fontsize=11)
ax = fig.add_axes([.07, .12, .89, .64], facecolor=BG)
xs = [xm(k) for k in ks]
ax.plot(xs, [dxy[k] for k in ks], color=GLINE, lw=2.4, zorder=2)
ax.set_xlim(2001, 2027); ax.set_ylim(66, 136)
ax.set_yticks([])
for sp in ax.spines.values(): sp.set_visible(False)
for v in (80, 100): ax.axhline(v, color=GRID, lw=.8, zorder=0); ax.text(2000.9, v, str(v), ha="right", va="center", fontsize=8.5, color=MUTED)
ax.set_xticks(range(2002, 2027, 2)); ax.set_xticklabels([str(y) for y in range(2002, 2027, 2)], fontsize=8.5, color=MUTED)
ax.tick_params(length=0, pad=6)
for i, (a, b, motivo) in enumerate(ALTAS, 1):
    v = 100 * (dxy[b] / dxy[a] - 1)
    ax.axvspan(xm(a), xm(b), color=tint(BLUE, .13), lw=0, zorder=0)
    kk = [k for k in ks if a <= k <= b]
    ax.plot([xm(k) for k in kk], [dxy[k] for k in kk], color=BLUE, lw=4.4, solid_capstyle="round", zorder=4)
    m = (xm(a) + xm(b)) / 2; yt = ALTURA[i]
    ax.text(m, yt, rot(v), ha="center", va="top", fontsize=15, fontweight="bold", color=BLUE)
    ax.text(m, yt - 6.3, CURTO[i], ha="center", va="top", fontsize=9, color=INK)
fig.text(.05, .035, "Motivos: contexto histórico (não calculado nos dados).", color=MUTED, fontsize=8.5)
fig.text(.95, .035, "Fonte: Investing (DXY futuros, fechamento mensal)", color=MUTED, fontsize=8, ha="right")
fig.savefig("grafico_dxy_altas.png", facecolor=BG); plt.close(fig)
