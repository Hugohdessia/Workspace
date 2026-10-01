"""Versão limpa do infográfico 'O que impacta a alta do dólar no Brasil?' no padrão visual do projeto. Conceitual, sem dados."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Polygon
from matplotlib import font_manager as fm

BG, INK, MUTED = "#f4f6f3", "#1b2419", "#5f6b5c"
UP, DOWN = "#4a6741", "#b5523f"
T_SOBE, T_CAI, T_COL = "#e0eadc", "#f1e1dc", "#eaeee7"   # dólar sobe = verde, cai = vermelho
plt.rcParams["font.family"] = "Liberation Sans" if any("Liberation Sans" in f.name for f in fm.fontManager.ttflist) else "DejaVu Sans"

fig = plt.figure(figsize=(10, 8), dpi=200, facecolor=BG)
F = fig.add_axes([0, 0, 1, 1]); F.set_xlim(0, 1); F.set_ylim(0, 1); F.axis("off")

def seta(x, y0, y1, cor, lw=5, ms=22):
    F.add_patch(FancyArrowPatch((x, y0), (x, y1), arrowstyle="-|>", mutation_scale=ms, lw=lw, color=cor, shrinkA=0, shrinkB=0))

fig.text(.05, .93, "O que impacta a alta do dólar no Brasil?", color=INK, fontsize=25, fontweight="bold")
fig.text(.05, .888, "A cotação sobe quando a demanda por dólar é maior que a oferta", color=MUTED, fontsize=12)

colunas = [
    (.05, .33, "Cenário favorável ao real", UP, True,
     [("Juros altos no Brasil", "atraem capital estrangeiro"),
      ("Inflação baixa", "gera mais confiança e estabilidade"),
      ("Política e economia boas", "aumentam os investimentos no país")],
     "Aumenta a oferta de dólar no Brasil", "Dólar tende a cair", T_CAI, DOWN, False),
    (.62, .33, "Cenário desfavorável ao real", DOWN, False,
     [("Juros baixos no Brasil", "reduzem a atração de capital"),
      ("Inflação alta", "diminui a confiança na economia"),
      ("Política e economia ruins", "geram incerteza e saída de recursos")],
     "Cai a oferta e/ou sobe a demanda por dólar", "Dólar tende a subir", T_SOBE, UP, True),
]
for x0, w, titulo, cor, bem, itens, result, final, tint, fcor, fsobe in colunas:
    F.add_patch(FancyBboxPatch((x0, .10), w, .74, boxstyle="round,pad=0,rounding_size=.014", fc=T_COL, ec="none"))
    seta(x0 + .035, .80 if not bem else .745, .745 if not bem else .80, cor, lw=5)
    fig.text(x0 + .07, .7725, titulo, color=cor, fontsize=12.5, fontweight="bold", va="center")
    for i, (a, b) in enumerate(itens):
        y = .68 - i * .115
        F.scatter([x0 + .035], [y], s=45, color=cor, zorder=3)
        fig.text(x0 + .06, y + .012, a, color=INK, fontsize=12.5, fontweight="bold", va="center")
        fig.text(x0 + .06, y - .02, b, color=MUTED, fontsize=10.5, va="center")
    seta(x0 + w / 2, .345, .29, cor, lw=5, ms=22)
    fig.text(x0 + w / 2, .255, result, color=INK, fontsize=10.5, ha="center", va="center", style="italic")
    F.add_patch(FancyBboxPatch((x0 + .015, .11), w - .03, .095, boxstyle="round,pad=0,rounding_size=.012", fc=tint, ec="none"))
    seta(x0 + .06, .125 if fsobe else .19, .19 if fsobe else .125, fcor, lw=5)
    fig.text(x0 + .1, .1575, final, color=fcor, fontsize=15.5, fontweight="bold", va="center")

# centro: balança simples
cx = .5
F.plot([cx, cx], [.47, .70], color=MUTED, lw=3, solid_capstyle="round")
F.plot([cx - .045, cx + .045], [.47, .47], color=MUTED, lw=4, solid_capstyle="round")
F.plot([cx - .07, cx + .07], [.70, .70], color=MUTED, lw=3, solid_capstyle="round")
for sx, txt, cor in ((cx - .07, "Oferta\nde dólar", UP), (cx + .07, "Demanda\npor dólar", DOWN)):
    for d in (-.035, .035): F.plot([sx, sx + d], [.70, .625], color=MUTED, lw=1.4)
    F.add_patch(FancyBboxPatch((sx - .042, .605), .084, .02, boxstyle="round,pad=0,rounding_size=.008", fc=cor, ec="none"))
    fig.text(sx, .565, txt, color=cor, fontsize=10.5, fontweight="bold", ha="center", va="center", linespacing=1.15)
fig.text(cx, .74, "Em equilíbrio", color=MUTED, fontsize=10, ha="center")
F.add_patch(FancyBboxPatch((.385, .275), .23, .1, boxstyle="round,pad=0,rounding_size=.012", fc=T_COL, ec="none"))
fig.text(cx, .345, "Mais oferta", color=INK, fontsize=11, ha="center", va="center")
fig.text(cx, .318, "dólar mais barato", color=DOWN, fontsize=11, fontweight="bold", ha="center", va="center")
F.add_patch(FancyBboxPatch((.385, .15), .23, .1, boxstyle="round,pad=0,rounding_size=.012", fc=T_COL, ec="none"))
fig.text(cx, .22, "Mais demanda", color=INK, fontsize=11, ha="center", va="center")
fig.text(cx, .193, "dólar mais caro", color=UP, fontsize=11, fontweight="bold", ha="center", va="center")
fig.savefig("infografico_impacto_alta_dolar.png", facecolor=BG)
