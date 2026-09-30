"""O que é o DXY: composição da cesta, como ler e a série desde 2001.

Composição (pesos oficiais do índice, ICE): EUR 57,6% JPY 13,6% GBP 11,9% CAD 9,1% SEK 4,2% CHF 3,6%.
Série: Investing (DXY futuros, fechamento mensal), dados/dxy_futuros_mensal.csv.
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
BG, INK, MUTED, GRID = "#f4f6f3", "#1b2419", "#5f6b5c", "#dfe4dc"
BLUE, BLUE2, GLINE = "#2f5f99", "#7ea1cc", "#b9c4d0"
UPC, DOWNC = "#4a6741", "#b5523f"
plt.rcParams["font.family"] = "Liberation Sans" if any("Liberation Sans" in f.name for f in fm.fontManager.ttflist) else "DejaVu Sans"
vb = lambda v: f"{v:.1f}".replace(".", ",")

CESTA = [("Euro", "EUR", 57.6), ("Iene japonês", "JPY", 13.6), ("Libra esterlina", "GBP", 11.9),
         ("Dólar canadense", "CAD", 9.1), ("Coroa sueca", "SEK", 4.2), ("Franco suíço", "CHF", 3.6)]

fig = plt.figure(figsize=(10, 7.4), dpi=200, facecolor=BG)
fig.text(.05, .925, "O que é o DXY", color=INK, fontsize=26, fontweight="bold")
fig.text(.05, .88, "O índice que mede a força do dólar americano contra uma cesta de 6 moedas", color=MUTED, fontsize=11.5)

# --- cesta
fig.text(.05, .815, "A cesta", color=INK, fontsize=13, fontweight="bold")
ax = fig.add_axes([.17, .50, .33, .28], facecolor=BG)
ys = list(range(len(CESTA)))[::-1]
for y, (nome, cod, p) in zip(ys, CESTA):
    ax.barh(y, p, color=BLUE if p > 50 else BLUE2, height=.62)
    ax.text(p + 1.2, y, f"{vb(p)}%", va="center", fontsize=11, fontweight="bold", color=INK)
    ax.text(-1.5, y, nome, va="center", ha="right", fontsize=10.5, color=INK)
ax.set_xlim(0, 70); ax.set_ylim(-.6, 5.6); ax.axis("off")

# --- como ler
fig.text(.58, .815, "Como ler", color=INK, fontsize=13, fontweight="bold")
cards = [("▲", UPC, "DXY sobe", "dólar mais forte frente à cesta"),
         ("▼", DOWNC, "DXY cai", "dólar mais fraco frente à cesta"),
         ("100", BLUE, "Base", "100 é o nível do dólar em março de 1973"),
         ("R$", MUTED, "Real fora da cesta", "o índice não inclui o real")]
y = .765
for sym, c, t, d in cards:
    fig.text(.605, y, sym, color="white", fontsize=11 if len(sym) > 1 else 13, fontweight="bold", ha="center", va="center",
             bbox=dict(boxstyle="circle,pad=.45", fc=c, ec="none"))
    fig.text(.65, y + .012, t, color=INK, fontsize=11.5, fontweight="bold", va="center")
    fig.text(.65, y - .016, d, color=MUTED, fontsize=9.5, va="center")
    y -= .068

# --- série
fig.text(.05, .415, "O DXY desde 2001", color=INK, fontsize=13, fontweight="bold")
ax2 = fig.add_axes([.07, .09, .89, .26], facecolor=BG)
xs = [xm(k) for k in ks]; ys_ = [dxy[k] for k in ks]
ax2.plot(xs, ys_, color=BLUE, lw=2.6)
ax2.axhline(100, color=GRID, lw=1, zorder=0); ax2.text(2000.9, 100, "100", ha="right", va="center", fontsize=8.5, color=MUTED)
kmax = max(ks, key=lambda k: dxy[k]); kmin = min(ks, key=lambda k: dxy[k]); khoje = ks[-1]
pts = [(kmin, "mín.", "top", -8), (kmax, "máx.", "bottom", 5), (khoje, "hoje", "bottom", 5)]
for k, lab, va, off in pts:
    ax2.scatter([xm(k)], [dxy[k]], s=55, color=BG, edgecolor=BLUE, lw=2.2, zorder=4)
    ax2.text(xm(k), dxy[k] + off, f"{lab} {vb(dxy[k])}", ha="center", va=va, fontsize=9.5, fontweight="bold", color=BLUE)
ax2.set_xlim(2001, 2027.4); ax2.set_ylim(56, 128); ax2.set_yticks([])
ax2.set_xticks(range(2002, 2027, 4)); ax2.set_xticklabels([str(y) for y in range(2002, 2027, 4)], fontsize=8.5, color=MUTED)
ax2.tick_params(length=0, pad=6)
for sp in ax2.spines.values(): sp.set_visible(False)
fig.text(.05, .03, "Composição: pesos do índice (ICE). Série: Investing (DXY futuros, fechamento mensal; mín./máx. desde 2001).", color=MUTED, fontsize=8)
fig.savefig("grafico_o_que_e_dxy.png", facecolor=BG); plt.close(fig)
print(kmin, dxy[kmin], kmax, dxy[kmax], khoje, dxy[khoje])
