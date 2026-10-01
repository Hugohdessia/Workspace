"""Variação 2: duas faixas horizontais (causa -> efeito -> resultado), sem balança. Conceitual, sem dados."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib import font_manager as fm
from PIL import Image

BG, INK, MUTED = "#f4f6f3", "#1b2419", "#5f6b5c"
UP, DOWN = "#4a6741", "#b5523f"
T_SOBE, T_CAI, T_COL = "#e0eadc", "#f1e1dc", "#eaeee7"
plt.rcParams["font.family"] = "Liberation Sans" if any("Liberation Sans" in f.name for f in fm.fontManager.ttflist) else "DejaVu Sans"
FLAG = Image.open("imagens/bandeira_brasil.webp").convert("RGB")
W_, H_ = 10, 7.2
fig = plt.figure(figsize=(W_, H_), dpi=200, facecolor=BG)
F = fig.add_axes([0, 0, 1, 1]); F.set_xlim(0, 1); F.set_ylim(0, 1); F.axis("off")

def seta(p0, p1, cor, lw=5, ms=22):
    F.add_patch(FancyArrowPatch(p0, p1, arrowstyle="-|>", mutation_scale=ms, lw=lw, color=cor, shrinkA=0, shrinkB=0))

fig.text(.05, .925, "O que impacta a alta do dólar no Brasil?", color=INK, fontsize=25, fontweight="bold")
fig.text(.05, .88, "A cotação sobe quando a demanda por dólar é maior que a oferta", color=MUTED, fontsize=12)

faixas = [
    (.50, "Brasil em boa fase", "Cenário favorável ao real", UP, True,
     [("Juros altos", "atraem capital estrangeiro"), ("Inflação baixa", "gera confiança e estabilidade"), ("Política e economia boas", "aumentam os investimentos")],
     "Entra mais dólar\nno país", "Mais oferta de dólar", "Dólar tende a cair", T_CAI, DOWN, False),
    (.13, "Brasil em dúvida", "Cenário desfavorável ao real", DOWN, False,
     [("Juros baixos", "reduzem a atração de capital"), ("Inflação alta", "diminui a confiança"), ("Política e economia ruins", "geram incerteza e saída de recursos")],
     "Sai dólar do país\nou procura aumenta", "Menos oferta e/ou mais demanda", "Dólar tende a subir", T_SOBE, UP, True),
]
for y0, nome, sub, cor, bem, itens, meio, regra, final, tint, fcor, fsobe in faixas:
    h = .31
    F.add_patch(FancyBboxPatch((.04, y0), .92, h, boxstyle="round,pad=0,rounding_size=.014", fc=T_COL, ec="none"))
    fh = .08 * (W_ / H_) * FLAG.size[1] / FLAG.size[0]
    a = fig.add_axes([.06, y0 + h / 2 - fh / 2, .08, fh]); a.imshow(FLAG); a.axis("off")
    seta((.17, y0 + h / 2 - .045 if not bem else y0 + h / 2 - .045), (.17, y0 + h / 2 + .045 if bem else y0 + h / 2 + .045), cor, lw=5) if bem else seta((.17, y0 + h / 2 + .045), (.17, y0 + h / 2 - .045), cor, lw=5)
    fig.text(.2, y0 + h / 2 + .022, nome, color=cor, fontsize=13.5, fontweight="bold", va="center")
    fig.text(.2, y0 + h / 2 - .022, sub, color=MUTED, fontsize=10, va="center")
    for i, (t, d) in enumerate(itens):
        y = y0 + h - .085 - i * .085
        F.scatter([.41], [y], s=40, color=cor, zorder=3)
        fig.text(.43, y, t, color=INK, fontsize=11.5, fontweight="bold", va="center")
        fig.text(.43, y - .027, d, color=MUTED, fontsize=9.5, va="center")
    seta((.67, y0 + h / 2), (.715, y0 + h / 2), cor, lw=4, ms=20)
    F.add_patch(FancyBboxPatch((.73, y0 + .035), .205, h - .07, boxstyle="round,pad=0,rounding_size=.012", fc=tint, ec="none"))
    fig.text(.8325, y0 + h - .075, regra, color=MUTED, fontsize=9.5, ha="center", va="center")
    fig.text(.8325, y0 + h / 2 - .02, final, color=fcor, fontsize=14.5, fontweight="bold", ha="center", va="center")
    seta((.8325, y0 + .045 if fsobe else y0 + .1), (.8325, y0 + .1 if fsobe else y0 + .045), fcor, lw=4, ms=16)
fig.text(.5, .075, "Mais oferta = dólar mais barato   |   Mais demanda = dólar mais caro", color=INK, fontsize=12, ha="center", va="center")
fig.savefig("infografico_impacto_alta_dolar_v2.png", facecolor=BG)
