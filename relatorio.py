import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf as pdf_backend
import numpy as np
import os
from datetime import datetime

LOAD_LEVELS = [10, 50, 100]
DIR = "resultados"
OUTPUT = os.path.join(DIR, "relatorio.pdf")

LABELS = {
    "POST /auth/login": "Login",
    "GET /carts/1": "Ver Carrinho",
    "POST /carts/add": "Add Carrinho",
    "GET /products": "Listar Produtos",
    "GET /products/[id]": "Prod. Específico",
    "GET /products/search?q=phone": "Buscar Produto",
}
CORES = ["#2ecc71", "#3498db", "#e74c3c"]


def ler_stats(nivel):
    df = pd.read_csv(os.path.join(DIR, f"carga_{nivel}_stats.csv"))
    df["Endpoint"] = df["Type"] + " " + df["Name"]
    df["Label"] = df["Endpoint"].map(LABELS).fillna(df["Name"])
    return df


def ler_historico(nivel):
    df = pd.read_csv(os.path.join(DIR, f"carga_{nivel}_stats_history.csv"))
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], unit="s")
    return df


def grafico_barras(stats, metrica, titulo, ylabel):
    endpoint_labels = list(LABELS.values())
    fig, ax = plt.subplots(figsize=(12, 5))
    x = np.arange(len(endpoint_labels))
    w = 0.25

    for i, (nivel, df) in enumerate(stats.items()):
        vals = []
        for lbl in endpoint_labels:
            row = df[(df["Label"] == lbl) & (df["Name"] != "Aggregated")]
            vals.append(float(row[metrica].values[0]) if len(row) > 0 else 0)
        ax.bar(x + i * w, vals, w, label=f"{nivel} usuários", color=CORES[i], alpha=0.85)

    ax.set_title(titulo, fontsize=13, fontweight="bold")
    ax.set_xticks(x + w)
    ax.set_xticklabels(endpoint_labels, rotation=20, ha="right")
    ax.set_ylabel(ylabel)
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    return fig


def grafico_historico(historicos):
    fig, ax = plt.subplots(figsize=(12, 5))
    for i, (nivel, df) in enumerate(historicos.items()):
        agg = df[df["Name"] == "Aggregated"].copy()
        if agg.empty:
            continue
        agg["t"] = (agg["Timestamp"] - agg["Timestamp"].iloc[0]).dt.total_seconds()
        ax.plot(agg["t"], agg["Requests/s"], label=f"{nivel} usuários", color=CORES[i], linewidth=2)

    ax.set_title("Evolução do Throughput ao Longo do Tempo", fontsize=13, fontweight="bold")
    ax.set_xlabel("Tempo (s)")
    ax.set_ylabel("Requisições/s")
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()
    return fig


def grafico_tabela(stats):
    fig, ax = plt.subplots(figsize=(12, 3))
    ax.axis("off")

    linhas = []
    for nivel, df in stats.items():
        agg = df[df["Name"] == "Aggregated"].iloc[0]
        linhas.append([
            f"{nivel} usuários",
            int(agg["Request Count"]),
            f"{agg['Requests/s']:.1f}",
            f"{agg['Average Response Time']:.0f} ms",
            f"{agg['90%']:.0f} ms",
            f"{agg['95%']:.0f} ms",
            int(agg["Failure Count"]),
        ])

    colunas = ["Carga", "Total Req.", "Throughput", "Média", "p90", "p95", "Falhas"]
    tabela = ax.table(cellText=linhas, colLabels=colunas, loc="center", cellLoc="center")
    tabela.auto_set_font_size(False)
    tabela.set_fontsize(11)
    tabela.scale(1, 2.5)

    for (row, col), cell in tabela.get_celld().items():
        if row == 0:
            cell.set_facecolor("#2c3e50")
            cell.set_text_props(color="white", fontweight="bold")
        elif row % 2 == 0:
            cell.set_facecolor("#ecf0f1")

    ax.set_title("Resumo Geral por Nível de Carga", fontsize=13, fontweight="bold", pad=30)
    fig.tight_layout()
    return fig


def pagina_capa():
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.axis("off")
    fig.patch.set_facecolor("#2c3e50")
    ax.text(0.5, 0.65, "Relatório de Testes de Performance", ha="center", va="center",
            fontsize=26, fontweight="bold", color="white", transform=ax.transAxes)
    ax.text(0.5, 0.52, "Sistema: DummyJSON API (dummyjson.com)", ha="center", va="center",
            fontsize=16, color="#ecf0f1", transform=ax.transAxes)
    ax.text(0.5, 0.42, "Ferramenta: Locust", ha="center", va="center",
            fontsize=14, color="#bdc3c7", transform=ax.transAxes)
    ax.text(0.5, 0.32, f"Gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M')}",
            ha="center", va="center", fontsize=12, color="#bdc3c7", transform=ax.transAxes)
    fig.tight_layout()
    return fig


def main():
    print("Carregando dados...")
    stats = {n: ler_stats(n) for n in LOAD_LEVELS}
    historicos = {n: ler_historico(n) for n in LOAD_LEVELS}

    print("Gerando gráficos...")
    with pdf_backend.PdfPages(OUTPUT) as pdf:
        figs = [
            pagina_capa(),
            grafico_tabela(stats),
            grafico_barras(stats, "Requests/s", "Throughput por Endpoint (req/s)", "req/s"),
            grafico_barras(stats, "90%", "Tempo de Resposta p90 por Endpoint (ms)", "ms"),
            grafico_barras(stats, "95%", "Tempo de Resposta p95 por Endpoint (ms)", "ms"),
            grafico_historico(historicos),
        ]
        for fig in figs:
            pdf.savefig(fig)
            plt.close(fig)

    print(f"\nRelatório gerado: {OUTPUT}")


if __name__ == "__main__":
    main()
