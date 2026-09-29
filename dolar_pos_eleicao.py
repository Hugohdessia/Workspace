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

def grafico(dados, titulo, sub, arq, rot):
    fig, ax = plt.subplots(figsize=(9, 5.2), dpi=150)
    xs = [str(a) for a in dados]
    vals = list(dados.values())
    cores = ["#c0392b" if v > 0 else "#2e7d5b" for v in vals]
    bars = ax.bar(xs, vals, color=cores, width=.6)
    for b, v in zip(bars, vals):
        ax.annotate(f"{v:+.1f}%".replace(".", ","), (b.get_x() + b.get_width() / 2, v),
                    ha="center", va="bottom" if v > 0 else "top", fontsize=11,
                    xytext=(0, 4 if v > 0 else -4), textcoords="offset points")
    ax.axhline(0, color="#444", lw=.8)
    ax.set_title(titulo, loc="left", fontsize=14, fontweight="bold")
    ax.text(0, 1.02, sub, transform=ax.transAxes, fontsize=9, color="#555")
    ax.set_xlabel("Ano da eleição"); ax.set_ylabel(rot)
    ax.margins(y=.15)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    fig.text(.01, .01, "Vermelho = dólar subiu | Verde = dólar caiu. PTAX venda, fim de ano.",
             fontsize=8, color="#666")
    fig.tight_layout(rect=(0, .03, 1, 1)); fig.savefig(arq); plt.close(fig)

grafico(um_ano, "Dólar 1 ano após a eleição", "Variação do fim do ano eleitoral ao fim do ano seguinte",
        "dolar_1_ano_pos_eleicao.png", "Variação do dólar (%)")
grafico(quatro, "Dólar em ciclos de 4 anos", "Variação do fim do ano eleitoral ao fim do ano da eleição seguinte (2022 ainda em curso)",
        "dolar_ciclo_4_anos.png", "Variação do dólar (%)")
