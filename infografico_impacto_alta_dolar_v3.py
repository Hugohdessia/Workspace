"""Variação 3: duas colunas + balança inclinada com notas de dólar, ícones nos itens. Conceitual, sem dados."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Polygon
from matplotlib import font_manager as fm
from PIL import Image

BG, INK, MUTED = "#f4f6f3", "#1b2419", "#5f6b5c"
UP, DOWN = "#4a6741", "#b5523f"
T_SOBE, T_CAI, T_COL = "#e0eadc", "#f1e1dc", "#eaeee7"
plt.rcParams["font.family"] = "Liberation Sans" if any("Liberation Sans" in f.name for f in fm.fontManager.ttflist) else "DejaVu Sans"
FLAG = Image.open("imagens/bandeira_brasil.webp").convert("RGB")
USD = Image.open("imagens/dolar_nota.jpg").convert("RGB")
W_, H_ = 10, 8
fig = plt.figure(figsize=(W_, H_), dpi=200, facecolor=BG)
F = fig.add_axes([0, 0, 1, 1]); F.set_xlim(0, 1); F.set_ylim(0, 1); F.axis("off")

def seta(p0, p1, cor, lw=5, ms=22):
    F.add_patch(FancyArrowPatch(p0, p1, arrowstyle="-|>", mutation_scale=ms, lw=lw, color=cor, shrinkA=0, shrinkB=0, zorder=5))

def icone(img, cx, cy, w, rot=0, z=3):
    h = w * img.size[1] / img.size[0] * (W_ / H_)
    a = fig.add_axes([cx - w / 2, cy - h / 2, w, h], zorder=z)
    a.imshow(img.convert('RGBA').rotate(rot, expand=True, resample=Image.BICUBIC) if rot else img); a.axis("off")

fig.text(.05, .94, "O que impacta a alta do dólar no Brasil?", color=INK, fontsize=25, fontweight="bold")
fig.text(.05, .90, "A cotação sobe quando a demanda por dólar é maior que a oferta", color=MUTED, fontsize=12)

def badge(x, y, cor, tipo, bem):
    F.add_patch(plt.Circle((x, y), .021, color="white", ec=cor, lw=1.6, transform=F.transData)) if False else F.scatter([x], [y], s=520, facecolor="white", edgecolor=cor, linewidth=1.6, zorder=3)
    if tipo == "juros":
        fig.text(x, y, "%", color=cor, fontsize=13, fontweight="bold", ha="center", va="center", zorder=4)
    elif tipo == "inflacao":
        seta((x, y + .014 if not bem else y - .014), (x, y - .014 if not bem else y + .014), cor, lw=2.6, ms=11) if False else None
        fig.text(x, y, "IPC", color=cor, fontsize=8.5, fontweight="bold", ha="center", va="center", zorder=4)
        seta((x + .0, y - .011) if bem else (x, y + .011), (x, y - .021) if bem else (x, y + .021), cor, lw=0, ms=0) if False else None
    else:
        icone(FLAG, x, y, .026, z=4)

cols = [
    (.04, "Cenário favorável ao real", UP, True,
     [("juros", "Juros altos no Brasil", "atraem capital estrangeiro"), ("inflacao", "Inflação baixa", "gera confiança e estabilidade"), ("pol", "Política e economia boas", "aumentam investimentos no país")],
     "Aumenta a oferta de dólar no Brasil", "Dólar tende a cair", T_CAI, DOWN, False),
    (.66, "Cenário desfavorável ao real", DOWN, False,
     [("juros", "Juros baixos no Brasil", "reduzem a atração de capital"), ("inflacao", "Inflação alta", "diminui a confiança"), ("pol", "Política e economia ruins", "geram incerteza e saída de capital")],
     "Cai a oferta e/ou sobe a demanda", "Dólar tende a subir", T_SOBE, UP, True),
]
w = .30
for x0, titulo, cor, bem, itens, result, final, tint, fcor, fsobe in cols:
    F.add_patch(FancyBboxPatch((x0, .08), w, .76, boxstyle="round,pad=0,rounding_size=.014", fc=T_COL, ec="none"))
    seta((x0 + .035, .765 if bem else .82), (x0 + .035, .82 if bem else .765), cor, lw=5)
    fig.text(x0 + .065, .79, titulo, color=cor, fontsize=11.5, fontweight="bold", va="center")
    for i, (tp, a, b) in enumerate(itens):
        y = .70 - i * .115
        badge(x0 + .04, y, cor, tp, bem)
        fig.text(x0 + .075, y + .013, a, color=INK, fontsize=12, fontweight="bold", va="center")
        fig.text(x0 + .075, y - .02, b, color=MUTED, fontsize=10, va="center")
    seta((x0 + w / 2, .35), (x0 + w / 2, .30), cor, lw=5, ms=22)
    fig.text(x0 + w / 2, .265, result, color=INK, fontsize=10.5, ha="center", va="center", style="italic")
    F.add_patch(FancyBboxPatch((x0 + .015, .095), w - .03, .12, boxstyle="round,pad=0,rounding_size=.012", fc=tint, ec="none"))
    seta((x0 + .055, .115 if fsobe else .195), (x0 + .055, .195 if fsobe else .115), fcor, lw=5)
    fig.text(x0 + .095, .155, final, color=fcor, fontsize=13.5, fontweight="bold", va="center")

# balança central (inclinada: demanda pesa mais)
cx, py = .5, .66
F.plot([cx, cx], [.30, py], color=MUTED, lw=4, solid_capstyle="round", zorder=1)
F.plot([cx - .05, cx + .05], [.30, .30], color=MUTED, lw=5, solid_capstyle="round")
F.add_patch(Polygon([[cx - .03, .30], [cx + .03, .30], [cx, .35]], color=MUTED, zorder=1))
F.scatter([cx], [py], s=90, color=INK, zorder=4)
L, R = (cx - .085, py + .022), (cx + .085, py - .022)
F.plot([L[0], R[0]], [L[1], R[1]], color=INK, lw=4, solid_capstyle="round", zorder=3)
for (px, py2), cor, nome, n in ((L, UP, "Oferta de dólar", 2), (R, DOWN, "Demanda por dólar", 5)):
    by = py2 - .11
    for d in (-.035, .035): F.plot([px, px + d], [py2, by + .012], color=MUTED, lw=1.3, zorder=2)
    F.add_patch(FancyBboxPatch((px - .042, by - .008), .084, .022, boxstyle="round,pad=0,rounding_size=.009", fc=cor, ec="none", zorder=3))
    for k in range(n):
        icone(USD, px + (k % 2 - .5) * .01, by + .026 + k * .011, .065, rot=(-4 if k % 2 else 3), z=3 + k // 2)
    fig.text(px, by - .05, nome.replace(" de ", "\nde ").replace(" por ", "\npor "), color=cor, fontsize=10, fontweight="bold", ha="center", va="center", linespacing=1.1)
fig.text(cx, .79, "Quem pesa mais\ndefine o preço", color=MUTED, fontsize=10.5, ha="center", va="center", linespacing=1.2)
fig.text(cx, .225, "Mais oferta", color=INK, fontsize=10.5, ha="center", va="center")
fig.text(cx, .20, "dólar mais barato", color=DOWN, fontsize=10.5, fontweight="bold", ha="center", va="center")
fig.text(cx, .155, "Mais demanda", color=INK, fontsize=10.5, ha="center", va="center")
fig.text(cx, .13, "dólar mais caro", color=UP, fontsize=10.5, fontweight="bold", ha="center", va="center")
fig.savefig("infografico_impacto_alta_dolar_v3.png", facecolor=BG)
