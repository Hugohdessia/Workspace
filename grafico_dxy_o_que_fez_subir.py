"""O que fez o DXY subir: altas do índice (>= +10%), juros do Fed e contexto de cada alta.

DXY: Investing (futuros, fechamento mensal). Juros do Fed: FRED (FEDFUNDS, média mensal).
As altas são os trechos de baixa-para-alta do DXY com variação >= 10% (zigzag de 8%).
Os motivos de cada alta são contexto histórico, não são calculados nos dados.
"""
import csv, datetime as dt
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

fed = {}
for r in csv.DictReader(open("dados/fedfunds_mensal.csv")):
    d = dt.date.fromisoformat(r["observation_date"]); fed[(d.year, d.month)] = float(r["FEDFUNDS"])
dxy = {}
for r in csv.DictReader(open("dados/dxy_futuros_mensal.csv", encoding="utf-8-sig")):
    x = dt.datetime.strptime(r["Data"], "%d.%m.%Y").date(); dxy[(x.year, x.month)] = float(r["Último"].replace(",", "."))
ks = sorted(k for k in dxy if k in fed)
xm = lambda k: k[0] + k[1] / 12

# altas (trecho de baixa -> alta >= 10%), mesmas definidas na análise (pivôs do zigzag de 8%)
ALTAS = [((2004, 12), (2005, 11), "Fed sobe juros e a economia americana se recupera"),
         ((2008, 3), (2009, 2), "Crise financeira global: corrida ao dólar como porto seguro"),
         ((2009, 11), (2010, 5), "Crise da dívida na Europa enfraquece o euro"),
         ((2011, 4), (2016, 12), "Fed sai do estímulo e sobe juros, enquanto BCE e Japão seguem afrouxando"),
         ((2018, 1), (2020, 3), "Guerra comercial e, em mar/2020, corrida ao dólar na pandemia"),
         ((2020, 12), (2022, 9), "Fed sobe juros mais rápido que os outros e guerra na Ucrânia")]

BG, INK, MUTED, GRID = "#f4f6f3", "#1b2419", "#5f6b5c", "#dfe4dc"
BLUE, GLINE, FEDC = "#2f5f99", "#b9c4d0", "#8a6d3b"
plt.rcParams["font.family"] = "Liberation Sans" if any("Liberation Sans" in f.name for f in fm.fontManager.ttflist) else "DejaVu Sans"
rot = lambda v: f"{v:+.1f}%".replace(".", ",").replace("-", "−")
tint = lambda c, a: matplotlib.colors.to_rgba(c, a)

fig = plt.figure(figsize=(10, 7.6), dpi=200, facecolor=BG)
fig.text(.05, .935, "O que fez o dólar no mundo (DXY) subir", color=INK, fontsize=24, fontweight="bold")
fig.text(.05, .895, "As 6 grandes altas do DXY desde 2001 (≥ +10%), com os juros do Fed embaixo", color=MUTED, fontsize=11)

ax = fig.add_axes([.07, .54, .89, .31], facecolor=BG)
ax2 = fig.add_axes([.07, .37, .89, .13], facecolor=BG, sharex=ax)
xs = [xm(k) for k in ks]
ax.plot(xs, [dxy[k] for k in ks], color=GLINE, lw=2.2, zorder=2)
ax2.plot(xs, [fed[k] for k in ks], color=FEDC, lw=2.2, zorder=2)
ax.set_xlim(2001, 2027); ax.set_ylim(66, 128); ax2.set_ylim(-.3, 6.9)
for a in (ax, ax2):
    a.set_yticks([]); a.tick_params(length=0)
    for sp in a.spines.values(): sp.set_visible(False)
for v in (80, 100): ax.axhline(v, color=GRID, lw=.8, zorder=0); ax.text(2000.9, v, str(v), ha="right", va="center", fontsize=8.5, color=MUTED)
for v in (0, 2, 4, 6): ax2.axhline(v, color=GRID, lw=.8, zorder=0); ax2.text(2000.9, v, f"{v}%", ha="right", va="center", fontsize=8.5, color=MUTED)
ax.text(2001.2, 126, "DXY", color=BLUE, fontsize=11, fontweight="bold", va="top")
ax2.text(2022.6, 6.7, "Juros do Fed", color=FEDC, fontsize=11, fontweight="bold", va="top")
plt.setp(ax.get_xticklabels(), visible=False)
ax2.set_xticks(range(2002, 2027, 2)); ax2.set_xticklabels([str(y) for y in range(2002, 2027, 2)], fontsize=8.5, color=MUTED)
ax2.tick_params(axis="x", pad=6)

rows = []
for i, (a, b, motivo) in enumerate(ALTAS, 1):
    v = 100 * (dxy[b] / dxy[a] - 1); df = fed[b] - fed[a]
    estado = "subindo" if df > .5 else ("cortando" if df < -.5 else "perto de zero / estável")
    for a_ in (ax, ax2): a_.axvspan(xm(a), xm(b), color=tint(BLUE, .13), lw=0, zorder=0)
    ks_ = [k for k in ks if a <= k <= b]
    ax.plot([xm(k) for k in ks_], [dxy[k] for k in ks_], color=BLUE, lw=4.2, solid_capstyle="round", zorder=4)
    ax2.plot([xm(k) for k in ks_], [fed[k] for k in ks_], color=FEDC, lw=4.2, solid_capstyle="round", zorder=4)
    mid = (xm(a) + xm(b)) / 2
    ax.text(mid, 126, str(i), ha="center", va="top", fontsize=12, fontweight="bold", color="white",
            bbox=dict(boxstyle="circle,pad=.35", fc=BLUE, ec="none"))
    rows.append((i, motivo, v, fed[a], fed[b], estado))

# lista embaixo: o que puxou cada alta
fig.text(.05, .325, "O que puxou cada alta", color=INK, fontsize=13, fontweight="bold")
y = .285
for i, motivo, v, fa, fb, estado in rows:
    fig.text(.05, y, str(i), color="white", fontsize=9, fontweight="bold", ha="center", va="center",
             bbox=dict(boxstyle="circle,pad=.3", fc=BLUE, ec="none"))
    fig.text(.075, y, rot(v), color=BLUE, fontsize=10.5, fontweight="bold", va="center")
    fig.text(.155, y, f"{motivo}", color=INK, fontsize=9.5, va="center")
    fig.text(.95, y, f"Fed {estado} ({fa:.1f}% → {fb:.1f}%)".replace(".", ","), color=FEDC, fontsize=9, va="center", ha="right", fontweight="bold")
    y -= .038
fig.text(.05, .04, "Só 2 das 6 altas do DXY coincidiram com o Fed subindo juros. Motivos: contexto histórico (não calculado nos dados).", color=MUTED, fontsize=8.5)
fig.text(.95, .014, "Fonte: Investing (DXY futuros, mensal) e FRED (Fed Funds, média mensal)", color=MUTED, fontsize=8, ha="right")
fig.savefig("grafico_dxy_o_que_fez_subir.png", facecolor=BG); plt.close(fig)
for r in rows: print(r)
