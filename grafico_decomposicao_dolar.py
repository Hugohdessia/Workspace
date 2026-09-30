"""De onde veio cada movimento do dólar: parte do mundo (DXY) x parte do Brasil.

USD/BRL mensal (Investing) e DXY futuros mensal (Investing). Períodos = ciclos de alta/queda do USD/BRL (>= 15%).
Decomposição em log: ln(USD/BRL) = ln(DXY) + ln(USD/BRL ÷ DXY). 'Brasil' = o que sobra depois de tirar o DXY.
Último ponto: USD/BRL de 29/09/2026 (R$ 5,2097) e DXY de set/2026.
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
brl = ler("dados/usdbrl_mensal.csv"); dxy = ler("dados/dxy_futuros_mensal.csv"); brl[(2026, 9)] = 5.2097
ks = sorted(k for k in brl if k >= (2002, 1) and k in dxy)
xm = lambda k: k[0] + k[1] / 12

TH = .15   # vira período quando o USD/BRL reverte >= 15% desde o extremo
piv = [ks[0]]; direction = 0; ext = ks[0]
for k in ks[1:]:
    if direction == 0:
        r = brl[k] / brl[piv[0]] - 1
        if abs(r) > TH: direction = 1 if r > 0 else -1; ext = k
        continue
    if direction == 1:
        if brl[k] > brl[ext]: ext = k
        elif brl[k] / brl[ext] - 1 < -TH: piv.append(ext); direction = -1; ext = k
    else:
        if brl[k] < brl[ext]: ext = k
        elif brl[k] / brl[ext] - 1 > TH: piv.append(ext); direction = 1; ext = k
piv.append(ext)

periodos = []
for a, b in zip(piv, piv[1:]):
    tb = math.log(brl[b] / brl[a]) * 100; tw = math.log(dxy[b] / dxy[a]) * 100; tr = tb - tw
    pct = (brl[b] / brl[a] - 1) * 100
    if abs(tr) > 2.5 * abs(tw) or (tw * tr < 0 and abs(tr) > abs(tw)): tag = "Brasil"
    elif abs(tw) > 2.5 * abs(tr): tag = "Mundo"
    else: tag = "Mundo + Brasil"
    periodos.append(dict(a=a, b=b, pct=pct, tb=tb, tw=tw, tr=tr, tag=tag))
    print(a, b, f"{pct:+.0f}%", f"mundo {tw:+.0f}", f"Brasil {tr:+.0f}", tag)

BG, INK, MUTED, GRID = "#f4f6f3", "#1b2419", "#5f6b5c", "#dfe4dc"
UP, DOWN, BLUE = "#4a6741", "#b5523f", "#3b6ea8"
T_SOBE, T_CAI = "#e0eadc", "#f1e1dc"    # dólar sobe = verde, cai = vermelho (vídeo sobre dolarizar)
plt.rcParams["font.family"] = "Liberation Sans" if any("Liberation Sans" in f.name for f in fm.fontManager.ttflist) else "DejaVu Sans"
rot = lambda v, d=0: f"{v:+.{d}f}".replace("-", "−")

fig = plt.figure(figsize=(10, 7.4), dpi=200, facecolor=BG)
fig.text(.05, .945, "De onde veio cada movimento do dólar", color=INK, fontsize=24, fontweight="bold")
fig.text(.05, .905, "O dólar contra o real separado em duas partes: o que veio do mundo (DXY) e o que veio do Brasil", color=MUTED, fontsize=11.5)
ax = fig.add_axes([.06, .47, .90, .39], facecolor=BG)
ax2 = fig.add_axes([.06, .10, .90, .29], facecolor=BG, sharex=ax)
xs = [xm(k) for k in ks]
ax.plot(xs, [brl[k] for k in ks], color=INK, lw=2.2, zorder=3)
ax.set_xlim(2001.8, 2027.0); ax.set_ylim(1.0, 7.9)
for a_ in (ax, ax2):
    a_.set_yticks([]); a_.tick_params(length=0)
    for sp in a_.spines.values(): sp.set_visible(False)
for v in (2, 4, 6): ax.axhline(v, color=GRID, lw=.8, zorder=0); ax.text(2001.7, v, f"R\\$ {v}", ha="right", va="center", fontsize=8.5, color=MUTED)
ax2.set_ylim(-110, 110)
for v in (-100, -50, 50, 100): ax2.axhline(v, color=GRID, lw=.8, zorder=0)
ax2.axhline(0, color=INK, lw=.9, zorder=1)
ax2.text(2001.7, 0, "0", ha="right", va="center", fontsize=8.5, color=MUTED)
plt.setp(ax.get_xticklabels(), visible=False)
ax2.set_xticks(range(2002, 2027, 2)); ax2.set_xticklabels([str(y) for y in range(2002, 2027, 2)], fontsize=8.5, color=MUTED); ax2.tick_params(axis="x", pad=6)

for p in periodos:
    x0, x1 = xm(p["a"]), xm(p["b"]); m = (x0 + x1) / 2; w = (x1 - x0) * .78
    tint = T_SOBE if p["pct"] > 0 else T_CAI
    ax.axvspan(x0, x1, color=tint, lw=0, zorder=0); ax2.axvspan(x0, x1, color=tint, lw=0, zorder=0)
    ax.text(m, 7.75, rot(p["pct"]) + "%", ha="center", va="top", fontsize=13 if (x1 - x0) > 1.2 else 10.5, fontweight="bold", color=INK)
    ax.text(m, 7.05 if (x1 - x0) > 1 else 6.25, p["tag"].replace(" + ", "\n+ ") if (x1 - x0) < 1.7 else p["tag"], ha="center", va="top", fontsize=9 if (x1 - x0) > 1 else 8, fontweight="bold",
            color=(BLUE if p["tag"] == "Mundo" else (INK if "+" in p["tag"] else MUTED)), linespacing=1.15)
    # barras empilhadas: mundo (azul) e Brasil (vermelho = empurrou o dólar para cima, verde = empurrou para baixo)
    pos = neg = 0
    for nome, v, cor in (("mundo", p["tw"], BLUE), ("brasil", p["tr"], DOWN if p["tr"] > 0 else UP)):
        if v >= 0: ax2.bar(m, v, bottom=pos, width=w, color=cor, zorder=3); mid = pos + v / 2; pos += v
        else: ax2.bar(m, v, bottom=neg, width=w, color=cor, zorder=3); mid = neg + v / 2; neg += v
        if abs(v) >= 9: ax2.text(m, mid, rot(v), ha="center", va="center", fontsize=8.5 if w > .5 else 7.5, fontweight="bold", color="white", zorder=5)
    ax2.scatter([m], [p["tb"]], marker="D", s=20, color=INK, edgecolor=BG, lw=.8, zorder=6)

# contexto nos picos (contexto histórico, não calculado)
CTX = [((2002, 9), "Eleição de 2002", 3.76, .28), ((2009, 2), "Crise global", 2.39, .32), ((2016, 2), "Crise fiscal e recessão", 4.02, .3),
       ((2020, 10), "Pandemia", 5.74, .3), ((2024, 12), "Dúvida fiscal", 6.18, -.0)]
for k, t, y, off in CTX:
    if t == "Dúvida fiscal":
        ax.text(xm(k) - .25, y, t, ha="right", va="center", fontsize=8, color=INK, fontstyle="italic")
    else:
        ax.annotate(t, (xm(k), y), xytext=(xm(k), y + off), ha="center", va="bottom", fontsize=8, color=INK, fontstyle="italic")
    ax.scatter([xm(k)], [y], s=26, color=INK, zorder=5)

# legenda
fig.text(.06, .055, "■", color=BLUE, fontsize=11, va="center"); fig.text(.078, .055, "Parte do mundo (DXY)", color=INK, fontsize=9, va="center")
fig.text(.23, .055, "■", color=DOWN, fontsize=11, va="center"); fig.text(.248, .055, "Brasil piorou: empurrou o dólar para cima", color=INK, fontsize=9, va="center")
fig.text(.50, .055, "■", color=UP, fontsize=11, va="center"); fig.text(.518, .055, "Brasil melhorou: empurrou o dólar para baixo", color=INK, fontsize=9, va="center")
fig.text(.795, .055, "◆", color=INK, fontsize=9, va="center", family="DejaVu Sans"); fig.text(.812, .055, "Dólar total", color=INK, fontsize=9, va="center")
fig.text(.06, .40, "De onde veio cada movimento (em pontos percentuais)", color=INK, fontsize=10, fontweight="bold", va="center")
fig.text(.06, .022, "Barras em pontos percentuais (log). Brasil = USD/BRL ÷ DXY. Contexto nos picos é histórico, não calculado. Fonte: Investing (mensal).", color=MUTED, fontsize=8)
fig.savefig("grafico_decomposicao_dolar.png", facecolor=BG); plt.close(fig)
