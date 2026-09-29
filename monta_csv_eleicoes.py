"""Monta os CSVs diários USD/BRL + DXY após cada ano eleitoral (1 ano e ciclo de 4 anos).

Lê os CSVs exportados do Investing (colunas Data, Último, ...; vírgula decimal; datas dd.mm.aaaa)
e junta todos os arquivos USD_BRL* e *ndice_Do_lar* da pasta de uploads.
"""
import csv, glob, datetime as dt, sys

PASTA = "/root/.claude/uploads/b50f19c7-d106-5321-9056-642adc8cbe34/"
ELEICOES = [2002, 2006, 2010, 2014, 2018, 2022]

def ler(padrao):
    s = {}
    for f in glob.glob(PASTA + padrao):
        for r in csv.DictReader(open(f, encoding="utf-8-sig")):
            d = dt.datetime.strptime(r["Data"], "%d.%m.%Y").date()
            s[d] = float(r["Último"].replace(",", "."))
    return dict(sorted(s.items()))

brl = ler("*USD_BRL*.csv"); dxy = ler("*ndice_Do_lar*.csv")
for nome, s in (("USD/BRL", brl), ("DXY", dxy)):
    print(f"{nome}: {min(s)} -> {max(s)} ({len(s)} dias)")

def ate(s, d):  # último fechamento em/antes de d
    return s[max(x for x in s if x <= d)]

def cobre(s, ini, fim):
    """True se há dados contínuos (sem buracos > 10 dias) de ini a fim."""
    ds = [min(x for x in s if x >= ini - dt.timedelta(days=10))] if min(s) <= ini else []
    if not ds: return False
    pts = [x for x in s if ini - dt.timedelta(days=10) <= x <= fim]
    if not pts or max(pts) < fim - dt.timedelta(days=10): return False
    return all((b - a).days <= 10 for a, b in zip(pts, pts[1:]))

def janela(ano_ini, ano_fim, arq):
    linhas, faltas = [], []
    for e in ELEICOES:
        ini, fim = dt.date(e, 12, 31), dt.date(e + ano_fim, 12, 31)
        fim = min(fim, min(max(brl), max(dxy)))
        if not (cobre(brl, ini, fim) and cobre(dxy, ini, fim)):
            faltas.append(e); continue
        base_b, base_d = ate(brl, ini), ate(dxy, ini)
        datas = sorted(x for x in set(brl) | set(dxy) if ini <= x <= fim)
        for d in datas:
            b, x = ate(brl, d), ate(dxy, d)
            linhas.append([e, d.isoformat(), b, x, round((b / base_b - 1) * 100, 2), round((x / base_d - 1) * 100, 2)])
    if linhas:
        with open(arq, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["eleicao", "data", "usdbrl", "dxy", "usdbrl_pct_desde_fim_do_ano_eleitoral", "dxy_pct_desde_fim_do_ano_eleitoral"])
            w.writerows(linhas)
    print(arq, "->", len(linhas), "linhas;", "sem cobertura de dados p/ eleições:", faltas or "nenhuma")

janela(0, 1, "dados_1_ano_pos_eleicao.csv")
janela(0, 4, "dados_ciclo_4_anos.csv")
