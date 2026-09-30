"""Dívida bruta / PIB: Brasil x emergentes (2026). Dados em dados/divida_pib_2026.csv."""
import csv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

rows = [(r["grupo"], float(r["divida_bruta_pib_pct"])) for r in csv.DictReader(open("dados/divida_pib_2026.csv", encoding="utf-8"))]
D = dict(rows)
BG, INK, MUTED, GRID = "#f4f6f3", "#1b2419", "#5f6b5c", "#dfe4dc"
BRAS, BRAS2, BLUE, GREY = "#b5523f", "#d9a79b", "#3b6ea8", "#9fb2c7"
plt.rcParams["font.family"] = "Liberation Sans" if any("Liberation Sans" in f.name for f in fm.fontManager.ttflist) else "DejaVu Sans"
vb = lambda v: f"{v:.1f}".replace(".", ",") + "%"

ordem = ["Economias avançadas", "Brasil (FMI)", "Brasil (Banco Central)", "Mercados emergentes", "América Latina e Caribe"]
nomes = {"Economias avançadas": "Economias avançadas", "Brasil (FMI)": "Brasil (FMI)", "Mundo (média)": "Mundo (média)",
         "Brasil (Banco Central)": "Brasil (Banco Central, ago/26)", "Mercados emergentes": "Mercados emergentes", "América Latina e Caribe": "América Latina e Caribe"}
cores = {"Brasil (FMI)": BRAS, "Brasil (Banco Central)": BRAS2}

fig = plt.figure(figsize=(10, 6.2), dpi=200, facecolor=BG)
fig.text(.05, .925, "A dívida do Brasil frente aos emergentes", color=INK, fontsize=24, fontweight="bold")
fig.text(.05, .880, "Dívida bruta do governo em % do PIB, 2026", color=MUTED, fontsize=11.5)
ax = fig.add_axes([.30, .20, .62, .60], facecolor=BG)
ys = list(range(len(ordem)))[::-1]
for y, g in zip(ys, ordem):
    v = D[g]
    ax.barh(y, v, color=cores.get(g, GREY if g != "Mercados emergentes" else BLUE), height=.62, zorder=3)
    ax.text(v + 1.5, y, vb(v), va="center", fontsize=12.5, fontweight="bold", color=INK if "Brasil" not in g else BRAS)
    ax.text(-2, y, nomes[g], va="center", ha="right", fontsize=11.5, fontweight="bold" if "Brasil (FMI)" == g else "normal", color=INK)
for v in (50, 100): ax.axvline(v, color=GRID, lw=.8, zorder=0)
ax.set_xlim(0, 125); ax.set_ylim(-.6, len(ordem) - .4); ax.axis("off")
# diferença para os emergentes
d_em = D["Brasil (FMI)"] - D["Mercados emergentes"]; d_la = D["Brasil (FMI)"] - D["América Latina e Caribe"]
fig.text(.05, .125, "Pelo FMI, o Brasil fica " + f"{d_em:.1f}".replace(".", ",") + " pontos percentuais acima da média dos emergentes e " + f"{d_la:.1f}".replace(".", ",") + " acima da América Latina.", color=INK, fontsize=11, fontweight="bold")
fig.text(.05, .085, "Brasil (FMI) = projeção do Monitor Fiscal de abril/2026 (imprensa). Brasil (Banco Central) usa metodologia própria, mais baixa que a do FMI. Médias dos blocos: tabela informada.", color=MUTED, fontsize=8.3)
fig.text(.05, .055, "Fontes: FMI (via imprensa), Banco Central e tabela do usuário (fonte original não informada). Valores não checados diretamente nas bases originais.", color=MUTED, fontsize=8.3)
fig.savefig("grafico_divida_brasil_vs_emergentes.png", facecolor=BG); plt.close(fig)
