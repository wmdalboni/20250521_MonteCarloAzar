import matplotlib.pyplot as plt
import seaborn as sns

def plot_simulation(df):
    plt.style.use("default")
    fig, ax = plt.subplots(figsize=(12, 6), facecolor="#f2f2f2")  # Fundo externo cinza claro

    # Fundo da área verde (acima de 0)
    ax.axhspan(0, df.max().max(), facecolor="#e6f4ea")  # Verde muito claro
    # Fundo da área vermelha (abaixo de 0)
    ax.axhspan(df.min().min(), 0, facecolor="#fce8e6")  # Vermelho muito claro

    # Linha horizontal na altura do zero
    ax.axhline(0, color="#333333", linewidth=1.2, linestyle="--", label="Ponto de Equilíbrio")

    # Plotar até 100 linhas aleatórias para performance
    for i in range(min(100, df.shape[0])):
        ax.plot(df.columns, df.iloc[i], color="gray", alpha=0.05)

    # Linha da média
    media = df.mean()
    ax.plot(df.columns, media, color="#1a5d1a", linewidth=2.5, label="Média")

    # Maior vencedor
    idx_max = df.iloc[:, -1].idxmax()
    ax.plot(df.columns, df.loc[idx_max], color="#0b3d0b", linewidth=2, linestyle="-", label="Maior Vencedor")

    # Maior perdedor
    idx_min = df.iloc[:, -1].idxmin()
    ax.plot(df.columns, df.loc[idx_min], color="#800000", linewidth=2, linestyle="-", label="Maior Perdedor")

    # Legenda e labels
    ax.set_xlabel("Turno", fontsize=12)
    ax.set_ylabel("Saldo Acumulado", fontsize=12)
    ax.set_title("Evolução dos Saldos dos Apostadores", fontsize=14, weight='bold')

    ax.legend(frameon=False)
    ax.grid(True, linestyle="--", alpha=0.3)
    ax.set_facecolor("#ffffff")  # Dentro do gráfico: branco

    return fig
