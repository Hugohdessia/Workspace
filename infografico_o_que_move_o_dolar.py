"""Infográfico didático: o que faz o dólar (contra o real) subir ou cair. Sem dados, só conceito."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib import font_manager as fm

BG, INK, MUTED, GRID = "#f4f6f3", "#1b2419", "#5f6b5c", "#dfe4dc"
UP, DOWN, BLUE = "#4a6741", "#b5523f", "#3b6ea8"
plt.rcParams["font.family"] = "Liberation Sans" if any("Liberation Sans" in f.name for f in fm.fontManager.ttflist) else "DejaVu Sans"

SOBE = {"FORA DO BRASIL": [("Medo no mundo", "investidores correm para a segurança do dólar"),
                           ("Juros sobem nos EUA", "deixar dinheiro lá passa a render mais"),
                           ("Commodities em queda", "o Brasil recebe menos dólares das exportações")],
        "DENTRO DO BRASIL": [("Dúvida com as contas públicas", "menos confiança na economia"),
                             ("Juros caem no Brasil", "investir aqui compensa menos"),
                             ("Incerteza política", "investidores esperam ou tiram o dinheiro")]}
CAI = {"FORA DO BRASIL": [("Mais apetite por risco", "dinheiro vai buscar retorno em outros países"),
                          ("Juros caem nos EUA", "deixar dinheiro lá passa a render menos"),
                          ("Commodities em alta", "entram mais dólares das exportações")],
       "DENTRO DO BRASIL": [("Confiança nas contas públicas", "mais segurança para investir"),
                            ("Juros altos no Brasil", "atraem investidores de fora"),
                            ("Política e economia previsíveis", "o dinheiro estrangeiro fica")]}

fig = plt.figure(figsize=(10, 7.8), dpi=200, facecolor=BG)
fig.text(.05, .945, "O que faz o dólar subir ou cair", color=INK, fontsize=26, fontweight="bold")
fig.text(.05, .905, "O dólar é um preço: sobe quando mais gente quer comprar, e cai quando entra mais dólar no país", color=MUTED, fontsize=11.5)

def painel(x0, titulo, cor, sinal, blocos):
    W, H, y0 = .43, .665, .205
    fig.add_artist(FancyBboxPatch((x0, y0), W, H, boxstyle="round,pad=0,rounding_size=.012", transform=fig.transFigure, fc="white", ec=GRID, lw=1.2))
    fig.add_artist(FancyBboxPatch((x0, y0 + H - .07), W, .07, boxstyle="round,pad=0,rounding_size=.012", transform=fig.transFigure, fc=cor, ec="none"))
    fig.text(x0 + .02, y0 + H - .035, f"{sinal}  {titulo}", color="white", fontsize=17, fontweight="bold", va="center")
    y = y0 + H - .115
    for bloco, itens in blocos.items():
        fig.text(x0 + .02, y, bloco, color=cor, fontsize=9.5, fontweight="bold", va="center")
        fig.add_artist(plt.Line2D([x0 + .02, x0 + W - .02], [y - .014, y - .014], color=GRID, lw=1))
        y -= .05
        for t, d in itens:
            fig.text(x0 + .028, y, "●", color=cor, fontsize=8, va="center")
            fig.text(x0 + .05, y + .009, t, color=INK, fontsize=11.5, fontweight="bold", va="center")
            fig.text(x0 + .05, y - .016, d, color=MUTED, fontsize=9, va="center")
            y -= .07
        y -= .012

painel(.05, "Dólar SOBE quando...", UP, "▲", SOBE)
painel(.52, "Dólar CAI quando...", DOWN, "▼", CAI)

fig.add_artist(FancyBboxPatch((.05, .045), .90, .11, boxstyle="round,pad=0,rounding_size=.012", transform=fig.transFigure, fc=BLUE, ec="none"))
fig.text(.5, .115, "Na prática, várias forças agem ao mesmo tempo.", color="white", fontsize=13, fontweight="bold", va="center", ha="center")
fig.text(.5, .080, "O DXY mostra o que vem de fora; o que sobra é o efeito do Brasil.", color="white", fontsize=11.5, va="center", ha="center")
fig.savefig("infografico_o_que_move_o_dolar.png", facecolor=BG); plt.close(fig)
