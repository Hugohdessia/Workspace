"""Infográfico em setas: forças internas (Brasil) e externas (mundo) puxando o dólar. Conceitual, sem dados."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib import font_manager as fm
from PIL import Image

BG, INK, MUTED, GRID = "#f4f6f3", "#1b2419", "#5f6b5c", "#dfe4dc"
UP, DOWN, NEUTRO = "#4a6741", "#b5523f", "#8f978c"
BLUE = "#3b6ea8"
plt.rcParams["font.family"] = "Liberation Sans" if any("Liberation Sans" in f.name for f in fm.fontManager.ttflist) else "DejaVu Sans"
FLAG = Image.open("imagens/bandeira_brasil.webp").convert("RGB")
USD = Image.open("imagens/dolar_nota.jpg").convert("RGB")
BRL = Image.open("imagens/real_nota.jpg").convert("RGB")

fig = plt.figure(figsize=(10, 8.2), dpi=200, facecolor=BG)
F = fig.add_axes([0, 0, 1, 1]); F.set_xlim(0, 1); F.set_ylim(0, 1); F.axis("off"); F.patch.set_alpha(0)
fig.text(.05, .945, "Como as forças puxam o dólar", color=INK, fontsize=26, fontweight="bold")
fig.text(.05, .905, "Brasil: seta para cima = bem, para baixo = em dúvida. Mundo: dólar forte sobe, dólar fraco desce. O resultado é o dólar no Brasil", color=MUTED, fontsize=11)
# US$ -> R$ no canto
for im, x in ((USD, .80), (BRL, .90)):
    a = fig.add_axes([x, .935, .075, .04]); a.imshow(im); a.axis("off")
F.annotate("", xy=(.895, .955), xytext=(.878, .955), arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.4))

def icone(img, cx, y, w, rot=None):
    h = w * img.size[1] / img.size[0] * (10 / 8.2)
    a = fig.add_axes([cx - w / 2, y - h / 2, w, h]); a.imshow(img); a.axis("off")
    return a

def seta(cx, y0, dy, cor):
    F.add_patch(FancyArrowPatch((cx, y0), (cx, y0 + dy), arrowstyle="-|>", mutation_scale=26, lw=6, color=cor, shrinkA=0, shrinkB=0))

def card(x0, y0, titulo, brasil, mundo, resultado, exemplo):
    W, H = .43, .385
    F.add_patch(FancyBboxPatch((x0, y0), W, H, boxstyle="round,pad=0,rounding_size=.012", fc="white", ec=GRID, lw=1.2))
    fig.text(x0 + .02, y0 + H - .03, titulo, color=INK, fontsize=11.5, fontweight="bold", va="center")
    base = y0 + .115
    xs = [x0 + .065, x0 + .185, x0 + .32]
    for cx, sym in ((x0 + .125, "+"), (x0 + .25, "=")):
        fig.text(cx, base + .075, sym, color=MUTED, fontsize=22, ha="center", va="center", fontweight="bold")
    # Brasil
    icone(FLAG, xs[0], base, .075)
    fig.text(xs[0], base - .047, brasil[0], color=INK, fontsize=9.5, ha="center", va="center", fontweight="bold")
    # Mundo
    icone(USD, xs[1], base, .095)
    fig.text(xs[1], base - .047, mundo[0], color=INK, fontsize=9.5, ha="center", va="center", fontweight="bold")
    # Resultado
    icone(USD, xs[2], base, .095)
    fig.text(xs[2], base - .047, "Dólar no Brasil", color=INK, fontsize=9.5, ha="center", va="center", fontweight="bold")
    bem = "bem" in brasil[0]
    cor_brasil = UP if bem else DOWN      # verde = Brasil bem (seta para cima), vermelho = Brasil em dúvida (para baixo)
    brasil = (brasil[0], (1 if bem else -1, brasil[1][1]))
    for cx, (sent, L), cor in zip(xs[:2], (brasil[1], mundo[1]), (cor_brasil, BLUE)):
        seta(cx, base + .035 if sent > 0 else base + .035 + L, sent * L, cor)
    sent, L = resultado[1]
    if sent == 0:
        F.add_patch(FancyArrowPatch((xs[2], base + .035), (xs[2], base + .035 + .1), arrowstyle="<|-|>", mutation_scale=22, lw=5, color=NEUTRO))
    else:
        seta(xs[2], base + .035 if sent > 0 else base + .035 + L, sent * L, INK)
    fig.text(x0 + W - .02, y0 + H - .07, resultado[0], color=(NEUTRO if sent == 0 else INK), fontsize=11.5, fontweight="bold", va="center", ha="right")
    fig.text(x0 + .02, y0 + .022, exemplo, color=MUTED, fontsize=9, va="center")

card(.05, .485, "1  Brasil em dúvida + dólar forte no mundo", ("Brasil em dúvida", (1, .085)), ("Dólar forte", (1, .085)), ("Dólar tende a subir", (1, .13)), "Ex.: 2014→15")
card(.52, .485, "2  Brasil em dúvida + dólar fraco no mundo", ("Brasil em dúvida", (1, .085)), ("Dólar fraco", (-1, .085)), ("Depende de qual pesa mais", (0, 0)), "Ex.: 2010→11 (o dólar subiu)")
card(.05, .075, "3  Brasil bem + dólar forte no mundo", ("Brasil bem", (-1, .085)), ("Dólar forte", (1, .085)), ("Depende de qual pesa mais", (0, 0)), "As forças se compensam parcialmente")
card(.52, .075, "4  Brasil bem + dólar fraco no mundo", ("Brasil bem", (-1, .085)), ("Dólar fraco", (-1, .085)), ("Dólar tende a cair", (-1, .13)), "Ex.: 2002→03 e 2006→07")
fig.text(.05, .052, "Cores das setas:", color=MUTED, fontsize=9, va="center")
fig.text(.165, .052, "Brasil bem", color=UP, fontsize=9, fontweight="bold", va="center")
fig.text(.245, .052, "Brasil em dúvida", color=DOWN, fontsize=9, fontweight="bold", va="center")
fig.text(.375, .052, "Mundo", color=BLUE, fontsize=9, fontweight="bold", va="center")
fig.text(.440, .052, "Resultado", color=INK, fontsize=9, fontweight="bold", va="center")
fig.text(.05, .03, "O preço do dólar em reais é a soma das duas forças: o que vem de fora e o que vem do Brasil. Conceitual, não calculado.", color=MUTED, fontsize=8.5)
fig.savefig("infografico_forcas_dolar.png", facecolor=BG); plt.close(fig)
