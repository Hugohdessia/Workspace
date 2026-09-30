"""Por que o dólar subiu ou caiu depois de cada eleição: dólar no mundo (DXY) x real (Brasil).

Base: fechamento de novembro do ano da eleição a novembro do ano seguinte (USD/BRL mensal e DXY futuros mensal, Investing).
Efeito do real = (1 + USD/BRL) / (1 + DXY) - 1 : negativo = real mais forte que a cesta; positivo = real mais fraco.
"""
import csv, datetime as dt, math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib import font_manager as fm
from PIL import Image

def ler(a):
    s = {}
    for r in csv.DictReader(open(a, encoding="utf-8-sig")):
        d = dt.datetime.strptime(r["Data"], "%d.%m.%Y").date(); s[(d.year, d.month)] = float(r["Último"].replace(",", "."))
    return s
brl = ler("dados/usdbrl_mensal.csv"); dxy = ler("dados/dxy_futuros_mensal.csv")
ELE = [2002, 2006, 2010, 2014, 2018, 2022]
dados = []
for e in ELE:
    vb = brl[(e + 1, 11)] / brl[(e, 11)]; vd = dxy[(e + 1, 11)] / dxy[(e, 11)]
    tb, tw = math.log(vb) * 100, math.log(vd) * 100
    share = tw / tb if tb else 0     # fatia do movimento explicada pelo mundo
    if share >= .65: veredito = "Mais mundo"
    elif share <= .35: veredito = "Mais Brasil"
    else: veredito = "Mundo e Brasil"
    dados.append(dict(e=e, dolar=(vb - 1) * 100, mundo=(vd - 1) * 100, real=(vb / vd - 1) * 100, veredito=veredito, share=share))
    print(e, f"dólar {(vb-1)*100:+.1f}% mundo {(vd-1)*100:+.1f}% real {(vb/vd-1)*100:+.1f}% share_mundo {share:+.0%} -> {veredito}")

BG, INK, MUTED, GRID = "#f4f6f3", "#1b2419", "#5f6b5c", "#dfe4dc"
UP, DOWN, BLUE = "#4a6741", "#b5523f", "#3b6ea8"
T_SOBE, T_CAI = "#e0eadc", "#f1e1dc"
plt.rcParams["font.family"] = "Liberation Sans" if any("Liberation Sans" in f.name for f in fm.fontManager.ttflist) else "DejaVu Sans"
FLAG = Image.open("imagens/bandeira_brasil.webp").convert("RGB"); USD = Image.open("imagens/dolar_nota.jpg").convert("RGB"); BRL = Image.open("imagens/real_nota.jpg").convert("RGB")
rot = lambda v: f"{v:+.1f}%".replace(".", ",").replace("-", "−")

W_, H_ = 10, 7.0
fig = plt.figure(figsize=(W_, H_), dpi=200, facecolor=BG)
F = fig.add_axes([0, 0, 1, 1]); F.set_xlim(0, 1); F.set_ylim(0, 1); F.axis("off"); F.patch.set_alpha(0)
def icone(img, cx, cy, w):
    h = w * img.size[1] / img.size[0] * (W_ / H_)
    a = fig.add_axes([cx - w / 2, cy - h / 2, w, h]); a.imshow(img); a.axis("off")
def seta(cx, cy, sent, cor, L=.055, lw=6):
    F.add_patch(FancyArrowPatch((cx, cy - sent * L), (cx, cy + sent * L), arrowstyle="-|>", mutation_scale=22, lw=lw, color=cor, shrinkA=0, shrinkB=0))

fig.text(.05, .945, "Por que o dólar subiu ou caiu depois de cada eleição?", color=INK, fontsize=22, fontweight="bold")
fig.text(.05, .905, "O dólar no Brasil depende de duas coisas: o dólar no mundo (DXY) e o real (o que acontece no Brasil)", color=MUTED, fontsize=11)

X0, CW = .255, .118
ROWS = [(.735, "Dólar no Brasil", "USD → R$"), (.56, "Dólar no mundo", "DXY"), (.385, "Real", "Brasil"), (.215, "O que explica", "")]
for y, nome, sub in ROWS[:3]:
    F.add_patch(FancyBboxPatch((.05, y - .07), .9, .14, boxstyle="round,pad=0,rounding_size=.01", fc="white", ec="none", alpha=.0))
# ícones e rótulos das linhas
icone(USD, .075, .755, .055); icone(BRL, .13, .755, .055)
fig.text(.05, .695, "Dólar no Brasil", color=INK, fontsize=11.5, fontweight="bold", va="center")
icone(USD, .10, .585, .07)
fig.text(.05, .525, "Dólar no mundo (DXY)", color=INK, fontsize=11.5, fontweight="bold", va="center")
icone(FLAG, .10, .415, .06)
fig.text(.05, .355, "Real (Brasil)", color=INK, fontsize=11.5, fontweight="bold", va="center")
fig.text(.05, .215, "O que explica", color=INK, fontsize=11.5, fontweight="bold", va="center")
for y in (.64, .47, .30):
    F.add_artist(plt.Line2D([.05, .96], [y, y], color=GRID, lw=1))

for i, d in enumerate(dados):
    cx = X0 + i * CW + CW / 2
    fig.text(cx, .865, f"{d['e']}→{d['e']+1}", color=INK, fontsize=12, fontweight="bold", ha="center", va="center")
    # dólar no Brasil
    sobe = d["dolar"] > 0
    F.add_patch(FancyBboxPatch((cx - CW / 2 + .006, .665), CW - .012, .145, boxstyle="round,pad=0,rounding_size=.01", fc=T_SOBE if sobe else T_CAI, ec="none"))
    seta(cx - .028, .745, 1 if sobe else -1, UP if sobe else DOWN)
    fig.text(cx + .012, .765, rot(d["dolar"]), color=INK, fontsize=13, fontweight="bold", va="center")
    fig.text(cx + .012, .728, "sobe" if sobe else "cai", color=MUTED, fontsize=10, va="center")
    # dólar no mundo
    forte = d["mundo"] > 0
    seta(cx - .028, .56, 1 if forte else -1, BLUE)
    fig.text(cx + .012, .58, rot(d["mundo"]), color=BLUE, fontsize=12, fontweight="bold", va="center")
    fig.text(cx + .012, .543, "mais forte" if forte else "mais fraco", color=MUTED, fontsize=9.5, va="center")
    # real
    real_forte = d["real"] < 0
    seta(cx - .028, .385, 1 if real_forte else -1, UP if real_forte else DOWN)
    fig.text(cx + .012, .40, "real mais", color=MUTED, fontsize=9.5, va="center")
    fig.text(cx + .012, .368, "forte" if real_forte else "fraco", color=UP if real_forte else DOWN, fontsize=11.5, fontweight="bold", va="center")
    # veredito
    cor = BLUE if d["veredito"] == "Mais mundo" else (INK if d["veredito"] == "Mundo e Brasil" else MUTED)
    F.add_patch(FancyBboxPatch((cx - CW / 2 + .008, .185), CW - .016, .06, boxstyle="round,pad=0,rounding_size=.012", fc="white", ec=GRID, lw=1.2))
    fig.text(cx, .215, d["veredito"], color=cor, fontsize=10.5, fontweight="bold", ha="center", va="center")

fig.text(.05, .105, "Como ler: se o dólar sobe no mundo (DXY) e o real enfraquece, os dois empurram o dólar para cima. Se um puxa para cada lado, vence o que pesa mais.", color=INK, fontsize=9.5)
fig.text(.05, .07, "Real mais forte/fraco = variação do dólar no Brasil descontada a do DXY. 'O que explica' = quem pesa mais no movimento do dólar.", color=MUTED, fontsize=8.5)
fig.text(.05, .04, "Fonte: Investing (USD/BRL mensal e DXY futuros mensal). Base: fechamento de novembro do ano da eleição a novembro do ano seguinte.", color=MUTED, fontsize=8)
fig.savefig("grafico_por_que_dolar_mudou.png", facecolor=BG); plt.close(fig)
