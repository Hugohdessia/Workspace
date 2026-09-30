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
rs = lambda v: "R\\$ " + f"{v:.2f}".replace(".", ",")

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

# ---- série mensal contínua (fechamento do mês) para os gráficos 1 e 2
xm = lambda k: k[0] + k[1] / 12          # fim do mês k
serie = sorted(k for k in brl if k >= (2002, 6))
SX = [xm(k) for k in serie]; SY = [brl[k] for k in serie]
tint = lambda c, a=.13: matplotlib.colors.to_rgba(c, a)

def base_mensal(titulo, sub, ymax=7.0):
    fig = plt.figure(figsize=(10, 5.6), dpi=200, facecolor=BG)
    fig.text(.05, .86, titulo, color=INK, fontsize=24, fontweight="bold")
    fig.text(.05, .795, sub, color=MUTED, fontsize=11)
    ax = fig.add_axes([.07, .14, .89, .58], facecolor=BG)
    ax.set_xlim(2002.3, 2027.2); ax.set_ylim(1.2, ymax)
    for v in (2, 3, 4, 5, 6):
        ax.axhline(v, color=GRID, lw=.8, zorder=0)
        ax.text(2002.2, v, f"R\\$ {v}", ha="right", va="center", fontsize=8.5, color=MUTED)
    ax.set_yticks([])
    for sp in ax.spines.values(): sp.set_visible(False)
    yrs = list(range(2003, 2027)); el = {e + 11 / 12 for e in ELEICOES}
    anos_t = [y for y in range(2002, 2027) if y in ELEICOES or (y - 2002) % 4 == 2 or y == 2026]
    ax.set_xticks([y + 11 / 12 for y in anos_t])
    ax.set_xticklabels([f"Nov/{y}" if y in ELEICOES else str(y) for y in anos_t], fontsize=8, color=MUTED, rotation=0)
    for lab, y in zip(ax.get_xticklabels(), anos_t):
        if y in ELEICOES: lab.set_color(INK); lab.set_fontweight("bold"); lab.set_fontsize(9.5)
    ax.tick_params(axis="x", length=0, pad=8)
    fig.text(.95, .04, FONTE, color=MUTED, fontsize=8, ha="right")
    return fig, ax

def janela_pts(a, b):
    ks = [k for k in serie if a <= k <= b]
    return [xm(k) for k in ks], [brl[k] for k in ks]

# ---- 1) 1 ano depois: linha mensal + 6 janelas destacadas
fig, ax = base_mensal("O dólar no 1º ano de cada governo", "Linha mensal do dólar. Em destaque: de novembro da eleição a novembro do ano seguinte")
ax.plot(SX, SY, color="#c3cbbf", lw=2, zorder=1)
for e in ELEICOES:
    a, b = um[e]; v = var(brl, a, b); c = cor(v)
    ax.axvspan(xm(a), xm(b), color=tint(c), zorder=0)
    x, y = janela_pts(a, b)
    ax.plot(x, y, color=c, lw=4.5, solid_capstyle="round", zorder=3)
    ax.scatter([x[0]], [y[0]], s=70, color=BG, edgecolor=c, lw=2.2, zorder=4)
    ax.scatter([x[-1]], [y[-1]], s=70, color=c, zorder=4)
    top = max(y) + .3
    xc = (x[0] + x[-1]) / 2 + (.9 if e == 2002 else 0)
    ax.text(xc, top + .28, rot(v), ha="center", va="bottom", fontsize=16, fontweight="bold", color=c)
    ax.text(xc, top, f"{rs(brl[a])} → {rs(brl[b])}", ha="center", va="bottom", fontsize=8.5, color=MUTED)
fig.savefig("grafico_1_ano_nov_a_nov.png", facecolor=BG); plt.close(fig)

# ---- 2) ciclos de 4 anos: mesmo estilo do gráfico 1, valores no eixo
fig, ax = base_mensal("Ciclos de 4 anos: o dólar subiu nos 3 últimos fechados",
                      "De novembro de uma eleição a novembro da seguinte. O ciclo de 2022 é parcial (até set/2026)", ymax=7.6)
GREY = "#8f978c"
for e in ELEICOES:
    a, b = ciclo[e]; v = var(brl, a, b); parcial = e == 2022
    c = GREY if parcial else cor(v)
    x, y = janela_pts(a, b)
    ax.axvspan(xm(a), xm(b), color=tint(c, .13), ec=BG, lw=2, zorder=0)
    ax.plot(x, y, color=c, lw=3.6, solid_capstyle="round", zorder=3)
    ax.scatter([x[0]], [y[0]], s=75, color=BG, edgecolor=c, lw=2.2, zorder=4)
    ax.scatter([x[-1]], [y[-1]], s=75, color=c, zorder=4)
    m = (x[0] + x[-1]) / 2
    ax.text(m, 7.5, rot(v) + (" *" if parcial else ""), ha="center", va="top", fontsize=18, fontweight="bold", color=c)
    ax.text(m, 6.9, f"{rs(brl[a])} → {rs(brl[b])}", ha="center", va="top", fontsize=9, color=MUTED)
fig.text(.07, .075, "* ciclo em andamento: Nov/2022 a Set/2026", color=MUTED, fontsize=8)
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
ax.axhline(100, color=GRID, lw=1, zorder=0)
ax.text(xs[-1] + .15, brl[HOJE] / b0 * 100, f"Dólar\n{rot(var(brl, (2002, 11), HOJE), 0)}\ndesde nov/2002", color=UP, fontsize=9.5, fontweight="bold", va="center")
ax.text(xs[-1] + .15, dxy[HOJE] / d0 * 100, f"DXY\n{rot(var(dxy, (2002, 11), HOJE), 0)}", color=BLUE, fontsize=9.5, fontweight="bold", va="center")
ax.set_xlim(2001.6, 2030.2)
xt(ax, [xn((e, 11)) for e in ELEICOES], [f"Nov/{e}" for e in ELEICOES])
fig.savefig("grafico_usdbrl_vs_dxy_nov_a_nov.png", facecolor=BG); plt.close(fig)

# ---- 4) só o DXY (limpo): ciclos em faixas + 1º ano em destaque
dsk = [k for k in sorted(dxy) if k >= (2002, 6)]
dvar = lambda a, b: var(dxy, a, b)
DB, GLINE, INKG = "#2f5f99", "#b9c4d0", "#3d4a3a"
fig = plt.figure(figsize=(10, 5.6), dpi=200, facecolor=BG)
fig.text(.05, .86, "O dólar no mundo (DXY) nos ciclos de eleição", color=INK, fontsize=24, fontweight="bold")
fig.text(.05, .795, "Em cima: variação do ciclo de 4 anos (nov a nov). Em azul: o 1º ano de cada ciclo", color=MUTED, fontsize=11)
ax = fig.add_axes([.07, .14, .89, .58], facecolor=BG)
ax.set_xlim(2002.3, 2029.4); ax.set_ylim(66, 124)
for v in (80, 100):
    ax.axhline(v, color=GRID, lw=.8, zorder=0); ax.text(2002.2, v, str(v), ha="right", va="center", fontsize=8.5, color=MUTED)
ax.set_yticks([])
for sp in ax.spines.values(): sp.set_visible(False)
ax.set_xticks([e + 11 / 12 for e in ELEICOES] + [xm(HOJE)])
ax.set_xticklabels([f"Nov/{e}" for e in ELEICOES] + ["Set/2026"], fontsize=9.5, color=INK, fontweight="bold")
ax.tick_params(axis="x", length=0, pad=8)
ax.plot([xm(k) for k in dsk], [dxy[k] for k in dsk], color=GLINE, lw=2.2, zorder=2)
for i, e in enumerate(ELEICOES):
    a, b = ciclo[e]; v = dvar(a, b); u1 = um[e]; v1 = dvar(*u1)
    if i % 2 == 0: ax.axvspan(xm(a), xm(b), color=tint(DB, .06), lw=0, zorder=0)
    k1 = [k for k in dsk if u1[0] <= k <= u1[1]]
    x1 = [xm(k) for k in k1]; y1 = [dxy[k] for k in k1]
    ax.plot(x1, y1, color=DB, lw=5, solid_capstyle="round", zorder=4)
    ax.text((x1[0] + x1[-1]) / 2 + (.9 if e == 2022 else 0), max(y1) + 3, rot(v1), ha="center", va="bottom", fontsize=13, fontweight="bold", color=DB)
    ax.text((xm(a) + xm(b)) / 2, 122.5, rot(v) + (" *" if e == 2022 else ""), ha="center", va="top", fontsize=17, fontweight="bold", color=INKG)
ax.text(xm(HOJE) + .4, dxy[HOJE], f"DXY\n{dxy[HOJE]:.1f}".replace(".", ","), ha="left", va="center", fontsize=11, fontweight="bold", color=DB, linespacing=1.3)
fig.text(.07, .075, "* ciclo em andamento: Nov/2022 a Set/2026", color=MUTED, fontsize=8)
fig.text(.95, .04, "Fonte: Investing (DXY futuros, fechamento mensal). Base: fechamento de novembro do ano da eleição", color=MUTED, fontsize=8, ha="right")
fig.savefig("grafico_dxy_nov_a_nov.png", facecolor=BG); plt.close(fig)
