"""Infográfico em matriz: situação do Brasil x dólar no mundo -> efeito sobre o dólar no Brasil. Conceitual, sem dados."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib import font_manager as fm
from PIL import Image

BG, INK, MUTED = "#f4f6f3", "#1b2419", "#5f6b5c"
UP, DOWN, BLUE, NEUTRO = "#4a6741", "#b5523f", "#3b6ea8", "#8f978c"
T_SOBE, T_CAI, T_MIX = "#f1e1dc", "#e0eadc", "#e9ece6"
plt.rcParams["font.family"] = "Liberation Sans" if any("Liberation Sans" in f.name for f in fm.fontManager.ttflist) else "DejaVu Sans"
FLAG = Image.open("imagens/bandeira_brasil.webp").convert("RGB")
USD = Image.open("imagens/dolar_nota.jpg").convert("RGB")
BRL = Image.open("imagens/real_nota.jpg").convert("RGB")

W_, H_ = 10, 7.4
fig = plt.figure(figsize=(W_, H_), dpi=200, facecolor=BG)
F = fig.add_axes([0, 0, 1, 1]); F.set_xlim(0, 1); F.set_ylim(0, 1); F.axis("off"); F.patch.set_alpha(0)

def icone(img, cx, cy, w):
    h = w * img.size[1] / img.size[0] * (W_ / H_)
    a = fig.add_axes([cx - w / 2, cy - h / 2, w, h]); a.imshow(img); a.axis("off")

def seta(cx, y0, y1, cor, lw=6, dupla=False):
    F.add_patch(FancyArrowPatch((cx, y0), (cx, y1), arrowstyle="<|-|>" if dupla else "-|>", mutation_scale=24, lw=lw, color=cor, shrinkA=0, shrinkB=0))

fig.text(.05, .935, "Como as forças puxam o dólar", color=INK, fontsize=26, fontweight="bold")
fig.text(.05, .893, "A situação do Brasil e a força do dólar no mundo, juntas, empurram o dólar no Brasil", color=MUTED, fontsize=11.5)
icone(USD, .845, .94, .075); icone(BRL, .925, .94, .075)
F.annotate("", xy=(.885, .94), xytext=(.878, .94), arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.4))

COLX = [.29, .635]; CW = .325
ROWY = [.405, .10]; RH = .275

# cabeçalho das colunas: mundo
fig.text(.29, .84, "NO MUNDO", color=MUTED, fontsize=9.5, fontweight="bold", va="center")
for x0, nome, sent in ((COLX[0], "Dólar forte", 1), (COLX[1], "Dólar fraco", -1)):
    icone(USD, x0 + .07, .775, .085)
    y0, y1 = (.75, .80) if sent > 0 else (.80, .75)
    seta(x0 + .135, y0, y1, BLUE, lw=5)
    fig.text(x0 + .155, .775, nome, color=INK, fontsize=13, fontweight="bold", va="center")
# cabeçalho das linhas: brasil
fig.text(.05, .84, "NO BRASIL", color=MUTED, fontsize=9.5, fontweight="bold", va="center")
for y0, nome, bem in ((ROWY[0], "Brasil em dúvida", False), (ROWY[1], "Brasil bem", True)):
    cy = y0 + RH / 2
    icone(FLAG, .105, cy + .03, .095)
    cor = UP if bem else DOWN
    seta(.205, (cy - .005) if bem else (cy + .065), (cy + .065) if bem else (cy - .005), cor, lw=6)
    fig.text(.05, cy - .06, nome, color=INK, fontsize=13.5, fontweight="bold", va="center")

CEL = {(0, 0): ("Dólar tende a subir", 1, T_SOBE, "Ex.: 2014→15"),
       (0, 1): ("Depende de\nqual pesa mais", 0, T_MIX, "Ex.: 2010→11 (o dólar subiu)"),
       (1, 0): ("Depende de\nqual pesa mais", 0, T_MIX, ""),
       (1, 1): ("Dólar tende a cair", -1, T_CAI, "Ex.: 2002→03 e 2006→07")}
for (r, c), (txt, sent, tint, ex) in CEL.items():
    x0, y0 = COLX[c], ROWY[r]
    F.add_patch(FancyBboxPatch((x0, y0), CW, RH, boxstyle="round,pad=0,rounding_size=.014", fc=tint, ec="none"))
    cx, cy = x0 + .075, y0 + RH / 2
    if sent == 0:
        seta(cx, cy - .07, cy + .07, NEUTRO, lw=5, dupla=True)
    else:
        seta(cx, cy - .07 if sent > 0 else cy + .07, cy + .07 if sent > 0 else cy - .07, INK, lw=6)
    fig.text(x0 + .135, cy + (.012 if ex else 0), txt, color=INK if sent else MUTED, fontsize=13.5, fontweight="bold", va="center", linespacing=1.25)
    if ex: fig.text(x0 + .135, cy - .032, ex, color=MUTED, fontsize=9.5, va="center")

fig.text(.05, .035, "Setas: Brasil (verde = bem, vermelho = em dúvida), mundo (azul) e resultado sobre o dólar no Brasil (preto). Conceitual, não calculado.", color=MUTED, fontsize=8.5)
fig.savefig("infografico_forcas_dolar.png", facecolor=BG); plt.close(fig)
