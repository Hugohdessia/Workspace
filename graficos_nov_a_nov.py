"""Dólar (USD/BRL) e DXY de novembro a novembro após cada eleição presidencial.

Base: fechamento de novembro do ano da eleição. Compara com novembro do ano seguinte
(1 ano) e com novembro da eleição seguinte (ciclo de 4 anos). O ciclo de 2022 ainda não
terminou: usa o último dado disponível (29/09/2026).
Fontes: Investing (USD/BRL mensal; DXY futuros mensal). Dados em dados/.
"""
import csv, datetime as dt
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

def ler(arq):
    s = {}
    for r in csv.DictReader(open(arq, encoding="utf-8-sig")):
        d = dt.datetime.strptime(r["Data"], "%d.%m.%Y").date()
        s[(d.year, d.month)] = float(r["Último"].replace(",", "."))
    return s

brl = ler("dados/usdbrl_mensal.csv"); dxy = ler("dados/dxy_futuros_mensal.csv")
# último dado (29/09/2026): fechamento diário do USD/BRL; DXY = mensal (futuro) de set/2026
HOJE = (2026, 9); brl[HOJE] = 5.2097
ELEICOES = [2002, 2006, 2010, 2014, 2018, 2022]

def var(s, a, b): return (s[b] / s[a] - 1) * 100
um = {e: ((e, 11), (e + 1, 11)) for e in ELEICOES}
ciclo = {e: ((e, 11), (e + 4, 11) if e + 4 <= 2025 else HOJE) for e in ELEICOES}

# ---- CSV resumo
with open("resumo_nov_a_nov.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["janela", "eleicao", "inicio", "fim", "usdbrl_inicio", "usdbrl_fim", "usdbrl_var_pct", "dxy_inicio", "dxy_fim", "dxy_var_pct"])
    for nome, jan in (("1 ano", um), ("ciclo 4 anos", ciclo)):
        for e, (a, b) in jan.items():
            w.writerow([nome, e, f"{a[0]}-{a[1]:02d}", f"{b[0]}-{b[1]:02d}", brl[a], brl[b], round(var(brl, a, b), 1),
                        dxy[a], dxy[b], round(var(dxy, a, b), 1)])
with open("serie_mensal_usdbrl_dxy.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["mes", "usdbrl", "dxy_futuro"])
    for k in sorted(set(brl) & set(dxy)): w.writerow([f"{k[0]}-{k[1]:02d}", brl[k], dxy[k]])
for nome, jan in (("1 ano", um), ("4 anos", ciclo)):
    for e, (a, b) in jan.items():
        print(nome, e, f"USD/BRL {var(brl,a,b):+.1f}%  DXY {var(dxy,a,b):+.1f}%  ({brl[a]:.2f}->{brl[b]:.2f})")

# ---- estilo
BG, INK, MUTED, GRID = "#f4f6f3", "#1b2419", "#5f6b5c", "#dfe4dc"
UP, DOWN, BLUE = "#4a6741", "#b5523f", "#3b6ea8"
plt.rcParams["font.family"] = "Liberation Sans" if any("Liberation Sans" in f.name for f in fm.fontManager.ttflist) else "DejaVu Sans"
rot = lambda v, d=1: f"{v:+.{d}f}%".replace(".", ",").replace("-", "−")
cor = lambda v: UP if v > 0 else DOWN
rs = lambda v: "R$ " + f"{v:.2f}".replace(".", ",")

def base(titulo, sub, xmax, ymax, fonte):
    fig = plt.figure(figsize=(10, 5.6), dpi=200, facecolor=BG)
    fig.text(.05, .86, titulo, color=INK, fontsize=24, fontweight="bold")
    fig.text(.05, .795, sub, color=MUTED, fontsize=11)
    ax = fig.add_axes([.05, .14, .90, .58], facecolor=BG)
    ax.set_xlim(2001, xmax); ax.set_ylim(0.6, ymax)
    ax.set_yticks([]); ax.tick_params(length=0, pad=10)
    for sp in ax.spines.values(): sp.set_visible(False)
    fig.text(.95, .04, fonte, color=MUTED, fontsize=8, ha="right")
    return fig, ax

FONTE = "Fonte: Investing (fechamento mensal). Base: fechamento de novembro do ano da eleição"
xt = lambda ax, pos, labs: (ax.set_xticks(pos), ax.set_xticklabels(labs, color=INK, fontsize=11, fontweight="bold"))

# ---- 1) 1 ano depois
fig, ax = base("O dólar no 1º ano de cada governo", "Variação de novembro do ano da eleição a novembro do ano seguinte", 2026.8, 6.6, FONTE)
seq = [x for e in ELEICOES if e < 2022 or True for x in ((e, brl[(e, 11)]), (e + 1, brl[(e + 1, 11)]))]
ax.plot([p[0] for p in seq], [p[1] for p in seq], color="#cfd5cb", lw=3, zorder=0)
for e in ELEICOES:
    a, b = um[e]; v = var(brl, a, b); c = cor(v)
    ax.plot([e, e + 1], [brl[a], brl[b]], color=c, lw=5, solid_capstyle="round")
    ax.scatter([e, e + 1], [brl[a], brl[b]], s=45, color=c, zorder=3)
    for x, dx, ha, k in ((e, -.22, "right", a), (e + 1, .22, "left", b)):
        ax.text(x + dx, brl[k], rs(brl[k]), ha=ha, va="center", fontsize=9.5, color=MUTED)
    y = max(brl[a], brl[b]) + .3
    ax.text(e + .5, y + .32, rot(v), ha="center", va="bottom", fontsize=16, fontweight="bold", color=c)
    ax.text(e + .5, y, f"DXY {rot(var(dxy, a, b))}", ha="center", va="bottom", fontsize=10, fontweight="bold", color=BLUE)
xt(ax, ELEICOES, [f"Nov/{e}" for e in ELEICOES])
fig.savefig("grafico_1_ano_nov_a_nov.png", facecolor=BG); plt.close(fig)

# ---- 2) ciclo de 4 anos
fig, ax = base("Ciclos de 4 anos: o dólar subiu nos 3 últimos",
               "Variação de novembro de uma eleição a novembro da seguinte. O ciclo de 2022 é parcial (até set/2026)", 2027.6, 7.0, FONTE)
pts = ELEICOES
for i, e in enumerate(pts[:-1]):
    a, b = ciclo[e]; v = var(brl, a, b); c = cor(v); n = pts[i + 1]
    ax.plot([e, n], [brl[a], brl[b]], color=c, lw=5, solid_capstyle="round")
    ym = (brl[a] + brl[b]) / 2
    ax.text((e + n) / 2 - .35, ym + .78, rot(v), ha="center", va="bottom", fontsize=16, fontweight="bold", color=c)
    ax.text((e + n) / 2 - .35, ym + .48, f"DXY {rot(var(dxy, a, b))}", ha="center", va="bottom", fontsize=10, fontweight="bold", color=BLUE)
a, b = ciclo[2022]; v = var(brl, a, b)
ax.plot([2022, 2026.75], [brl[a], brl[b]], color="#a5aca2", lw=5, ls=(0, (1, 1.6)), solid_capstyle="round")
ax.scatter([2026.75], [brl[b]], s=40, color="#a5aca2", zorder=3)
ax.text(2026.2, brl[b] - .5, f"até set/2026\n{rot(v)}\nDXY {rot(var(dxy, a, b))}", ha="center", va="top", fontsize=10, color=MUTED, fontweight="bold", linespacing=1.35)
ax.scatter(pts, [brl[(e, 11)] for e in pts], s=110, color=BG, edgecolor=INK, lw=2.2, zorder=3)
for e in pts: ax.text(e, brl[(e, 11)] - .28, rs(brl[(e, 11)]), ha="center", va="top", fontsize=10.5, color=INK)
xt(ax, pts + [2026.75], [f"Nov/{e}" for e in pts] + ["Set/2026"])
fig.savefig("grafico_ciclo_4_anos_nov_a_nov.png", facecolor=BG); plt.close(fig)

# ---- 3) USD/BRL x DXY, série mensal contínua, base 100 em nov/2002
fig, ax = base("Dólar no Brasil x dólar no mundo",
               "USD/BRL contra o DXY, base 100 em nov/2002. Faixas = ciclos de novembro a novembro", 2027.6, 6.6, FONTE)
ax.set_ylim(15, 225)
ks = sorted(k for k in brl if k >= (2002, 11) and k in dxy)
xs = [k[0] + (k[1] - 1) / 12 + (1 / 12) for k in ks]
b0, d0 = brl[(2002, 11)], dxy[(2002, 11)]
ax.plot(xs, [brl[k] / b0 * 100 for k in ks], color=UP, lw=2.6)
ax.plot(xs, [dxy[k] / d0 * 100 for k in ks], color=BLUE, lw=2.6)
xn = lambda k: k[0] + (k[1] - 1) / 12 + 1 / 12
for i, e in enumerate(ELEICOES):
    a, b = ciclo[e]; x0, x1 = xn(a), xn(b)
    if i % 2 == 0: ax.axvspan(x0, x1, color="#eaeee7", zorder=0)
    m = (x0 + x1) / 2
    ax.text(m, 216, f"Dólar {rot(var(brl, a, b))}", color=UP, fontsize=10.5, fontweight="bold", ha="center", va="top")
    ax.text(m, 202, f"DXY {rot(var(dxy, a, b))}", color=BLUE, fontsize=10.5, fontweight="bold", ha="center", va="top")
ax.axhline(100, color=GRID, lw=1, zorder=0)
ax.text(xs[-1] + .15, brl[HOJE] / b0 * 100, f"Dólar\n{rot(var(brl, (2002, 11), HOJE), 0)} desde nov/2002", color=UP, fontsize=9.5, fontweight="bold", va="center")
ax.text(xs[-1] + .15, dxy[HOJE] / d0 * 100, f"DXY\n{rot(var(dxy, (2002, 11), HOJE), 0)}", color=BLUE, fontsize=9.5, fontweight="bold", va="center")
ax.set_xlim(2002.5, 2029.3)
xt(ax, [xn((e, 11)) for e in ELEICOES], [f"Nov/{e}" for e in ELEICOES])
fig.savefig("grafico_usdbrl_vs_dxy_nov_a_nov.png", facecolor=BG); plt.close(fig)
