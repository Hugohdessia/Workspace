"""Variação do dólar (PTAX venda, fim de ano) após eleições presidenciais."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# PTAX de venda no último dia útil do ano (R$/US$)
# 2002 e 2003 conferidos em fonte externa; demais de memória (não verificados online)
fim_ano = {2002: 3.5325, 2003: 2.8884, 2006: 2.1380, 2007: 1.7713, 2010: 1.6662,
           2011: 1.8758, 2014: 2.6562, 2015: 3.9048, 2018: 3.8748, 2019: 4.0307,
           2022: 5.2177, 2023: 4.8413}
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
               "Variação do fim de uma eleição ao fim da seguinte")
for k, a in enumerate(anos[:-1]):
    b = anos[k + 1]; v = quatro[a]; c = cor(v)
    ax.plot([a, b], [fim_ano[a], fim_ano[b]], color=c, lw=5, solid_capstyle="round")
    ym = (fim_ano[a] + fim_ano[b]) / 2
    ax.text((a + b) / 2 + .1, ym + .35, rot(v), ha="center", va="bottom", fontsize=16, fontweight="bold", color=c)
ax.plot([2022, 2023], [fim_ano[2022], fim_ano[2023]], color="#a5aca2", lw=5, ls=(0, (1, 1.6)), solid_capstyle="round")
ax.text(2023, fim_ano[2023] - .35, "2023: R$ 4,84\n(em curso)", ha="center", va="top", fontsize=10.5, color=MUTED, fontweight="bold", linespacing=1.3)
ax.scatter(anos, [fim_ano[a] for a in anos], s=110, color=BG, edgecolor=INK, lw=2.2, zorder=3)
for a in anos:
    ax.text(a, fim_ano[a] - .28, "R$ " + f"{fim_ano[a]:.2f}".replace(".", ","), ha="center", va="top",
            fontsize=10.5, color=INK)
ax.set_xticks(anos + [2023]); ax.set_xticklabels([str(a) for a in anos] + [""], color=INK, fontsize=12, fontweight="bold")
fig.savefig("dolar_ciclo_4_anos.png", facecolor=BG); plt.close(fig)
