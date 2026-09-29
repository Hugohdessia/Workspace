"""Variação do dólar (PTAX venda, fim de ano) após eleições presidenciais."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# PTAX de venda no último dia útil do ano (R$/US$)
# 2002 e 2003 conferidos em fonte externa; demais de memória (não verificados online)
fim_ano = {2002: 3.5325, 2003: 2.8884, 2006: 2.1380, 2007: 1.7713, 2010: 1.6662,
           2011: 1.8758, 2014: 2.6562, 2015: 3.9048, 2018: 3.8748, 2019: 4.0307,
           2022: 5.2177, 2023: 4.8413}
# Anos após 2022 (ciclo em curso): PTAX fim de 2024 e 2025; 2026 = cotação de meados de set/2026 (aprox.)
curso = {2023: 4.8413, 2024: 6.1923, 2025: 5.5018, 2026: 5.15}
tabela = {2002: -18.2, 2006: -17.2, 2010: 12.6, 2014: 47.0, 2018: 4.0, 2022: -7.2}
tabela4 = {2002: -39.5, 2006: -22.1, 2010: 59.4, 2014: 45.9, 2018: 34.7}

anos = [2002, 2006, 2010, 2014, 2018, 2022]
um_ano = {a: (fim_ano[a + 1] / fim_ano[a] - 1) * 100 for a in anos}
quatro = {a: (fim_ano[b] / fim_ano[a] - 1) * 100 for a, b in zip(anos[:-1], anos[1:])}

print("Eleição | 1 ano calc (tabela) | 4 anos calc (tabela)")
for a in anos:
    print(a, f"{um_ano[a]:+.1f} ({tabela[a]:+.1f})",
          f"{quatro[a]:+.1f} ({tabela4[a]:+.1f})" if a in quatro else "-")

from matplotlib import font_manager as fm

BG, INK, MUTED, GRID = "#f4f6f3", "#1b2419", "#5f6b5c", "#dfe4dc"
UP, DOWN, DEST = "#4a6741", "#b5523f", "#25331f"
fam = "Liberation Sans" if any("Liberation Sans" in f.name for f in fm.fontManager.ttflist) else "DejaVu Sans"
plt.rcParams["font.family"] = fam

def base(titulo, sub):
    fig = plt.figure(figsize=(10, 5.6), dpi=200, facecolor=BG)
    fig.text(.05, .86, titulo, color=INK, fontsize=25, fontweight="bold")
    fig.text(.05, .795, sub, color=MUTED, fontsize=11.5)
    ax = fig.add_axes([.05, .14, .90, .58], facecolor=BG)
    ax.set_xlim(2001, 2024); ax.set_ylim(0.6, 6.0)
    ax.set_yticks([]); ax.tick_params(length=0, pad=10)
    for sp in ax.spines.values(): sp.set_visible(False)
    ax.set_xticks(anos)
    ax.set_xticklabels([str(a) for a in anos], color=INK, fontsize=12, fontweight="bold")
    fig.text(.95, .04, "Fonte: Banco Central (PTAX, fim de ano)", color=MUTED, fontsize=8, ha="right")
    return fig, ax

def rot(v): return f"{v:+.1f}%".replace(".", ",").replace("-", "\u2212")
def cor(v): return UP if v > 0 else DOWN

# ---- 1) 1 ano depois de cada eleição
fig, ax = base("O dólar no 1º ano depois da eleição",
               "Variação do fim do ano eleitoral ao fim do ano seguinte")
seq = [x for a in anos for x in (a, a + 1)]
ax.plot(seq, [fim_ano[x] for x in seq], color="#cfd5cb", lw=3, zorder=0)
for a in anos:
    v = um_ano[a]; c = cor(v)
    ax.plot([a, a + 1], [fim_ano[a], fim_ano[a + 1]], color=c, lw=5, solid_capstyle="round")
    ax.scatter([a, a + 1], [fim_ano[a], fim_ano[a + 1]], s=45, color=c, zorder=3)
    for x, dx, ha in ((a, -.22, "right"), (a + 1, .22, "left")):
        ax.text(x + dx, fim_ano[x], "R$ " + f"{fim_ano[x]:.2f}".replace(".", ","), ha=ha, va="center",
                fontsize=9.5, color=MUTED)
    ax.text(a + .5, max(fim_ano[a], fim_ano[a + 1]) + .3, rot(v), ha="center", va="bottom",
            fontsize=16, fontweight="bold", color=c)
fig.savefig("dolar_1_ano_pos_eleicao.png", facecolor=BG); plt.close(fig)

# ---- 2) ciclos de 4 anos
fig, ax = base("Ciclos de 4 anos: o dólar subiu nos 3 últimos",
               "Variação do fim de uma eleição ao fim da seguinte. O ciclo de 2022 termina em outubro de 2026 (dado parcial)")
for k, a in enumerate(anos[:-1]):
    b = anos[k + 1]; v = quatro[a]; c = cor(v)
    ax.plot([a, b], [fim_ano[a], fim_ano[b]], color=c, lw=5, solid_capstyle="round")
    ym = (fim_ano[a] + fim_ano[b]) / 2
    ax.text((a + b) / 2 + .1, ym + .35, rot(v), ha="center", va="bottom", fontsize=16, fontweight="bold", color=c)
cx = [2022, 2023, 2024, 2025, 2026]; cy = [fim_ano[2022]] + [curso[y] for y in cx[1:]]
ax.plot(cx, cy, color="#a5aca2", lw=5, ls=(0, (1, 1.6)), solid_capstyle="round")
ax.scatter(cx[1:], cy[1:], s=40, color="#a5aca2", zorder=3)
ax.text(2026, curso[2026] - .35, "set/2026: R$ 5,15\n" + rot((curso[2026] / fim_ano[2022] - 1) * 100) + " até agora", ha="center", va="top", fontsize=10.5, color=MUTED, fontweight="bold", linespacing=1.3)
ax.text(2024, curso[2024] + .2, "R$ 6,19", ha="center", va="bottom", fontsize=9.5, color=MUTED)
ax.scatter(anos, [fim_ano[a] for a in anos], s=110, color=BG, edgecolor=INK, lw=2.2, zorder=3)
for a in anos:
    ax.text(a, fim_ano[a] - .28, "R$ " + f"{fim_ano[a]:.2f}".replace(".", ","), ha="center", va="top",
            fontsize=10.5, color=INK)
ax.set_xlim(2001, 2027.3); ax.set_ylim(0.6, 6.9)
ax.set_xticks(anos + [2026]); ax.set_xticklabels([str(a) for a in anos] + ["2026"], color=INK, fontsize=12, fontweight="bold")
fig.savefig("dolar_ciclo_4_anos.png", facecolor=BG); plt.close(fig)

# ---- 3) USD/BRL x DXY por ciclo
# DXY fim de ano: 2014 em diante conferido por variações anuais publicadas; 2002-2010 de memória (não verificado)
dxy = {2002: 101.7, 2006: 83.7, 2010: 79.0, 2014: 90.3, 2018: 96.2, 2022: 103.5}
BLUE = "#3b6ea8"
fig, ax = base("Dólar no Brasil x dólar no mundo",
               "Base 100 no fim de 2002. USD/BRL contra o DXY (índice do dólar frente às principais moedas)")
ax.set_ylim(20, 165)
brl = [fim_ano[a] / fim_ano[2002] * 100 for a in anos]
dx = [dxy[a] / dxy[2002] * 100 for a in anos]
ax.axhline(100, color=GRID, lw=1.2, zorder=0)
ax.plot(anos, brl, color=UP, lw=5, solid_capstyle="round")
ax.plot(anos, dx, color=BLUE, lw=5, solid_capstyle="round")
ax.scatter(anos, brl, s=90, color=BG, edgecolor=UP, lw=2.4, zorder=3)
ax.scatter(anos, dx, s=90, color=BG, edgecolor=BLUE, lw=2.4, zorder=3)
ax.text(2022.35, brl[-1], f"Dólar (USD/BRL)\n{brl[-1]-100:+.0f}% desde 2002".replace("-", "−"), color=UP,
        fontsize=10.5, fontweight="bold", va="center")
ax.text(2022.35, dx[-1] - 6, f"DXY\n{dx[-1]-100:+.0f}% desde 2002".replace("-", "−"), color=BLUE,
        fontsize=10.5, fontweight="bold", va="center")
ax.set_xlim(2001, 2026.2)
for k, a in enumerate(anos[:-1]):
    b = anos[k + 1]; m = (a + b) / 2
    vb = (fim_ano[b] / fim_ano[a] - 1) * 100; vd = (dxy[b] / dxy[a] - 1) * 100
    ax.text(m, 27, f"Dólar {rot(vb)}", color=UP, fontsize=10.5, fontweight="bold", ha="center")
    ax.text(m, 21, f"DXY {rot(vd)}", color=BLUE, fontsize=10.5, fontweight="bold", ha="center")
fig.text(.05, .04, "DXY 2002–2010 estimado, sem conferência em fonte.", color=MUTED, fontsize=8)
fig.savefig("dolar_vs_dxy.png", facecolor=BG); plt.close(fig)
