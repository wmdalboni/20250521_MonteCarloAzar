import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from collections import Counter
from matplotlib.collections import PolyCollection
import numpy as np
import seaborn as sns
import pandas as pd

def plot_simulation(df):
    def ajustar_posicao_texto_espaco_minimo(valores, espacamento_min=15):
        valores_ordenados = sorted(valores)
        posicoes = [valores_ordenados[0]]
        for v in valores_ordenados[1:]:
            pos_ant = posicoes[-1]
            if v - pos_ant < espacamento_min:
                posicoes.append(pos_ant + espacamento_min)
            else:
                posicoes.append(v)
        count_orig = Counter()
        resultado = []
        for v in valores:
            count_orig[v] += 1
            occ = count_orig[v]
            c = 0
            idx = -1
            for i, val_ord in enumerate(valores_ordenados):
                if val_ord == v:
                    c += 1
                if val_ord == v and c == occ:
                    idx = i
                    break
            resultado.append(posicoes[idx])
        return resultado

    plt.style.use("default")
    fig, ax = plt.subplots(figsize=(12, 6), facecolor="#f2f2f2")

    ax.axhspan(0, df.max().max(), facecolor="#e6f4ea")
    ax.axhspan(df.min().min(), 0, facecolor="#fce8e6")
    ax.axhline(0, color="#333333", linewidth=1.2, linestyle="--", label="Ponto de Equilíbrio")

    for i in range(min(100, df.shape[0])):
        ax.plot(df.columns, df.iloc[i], color="gray", alpha=0.05)

    finais = df.iloc[:, -1]
    vencedores = df[finais > 0]
    perdedores = df[finais < 0]

    media_geral = df.mean()
    val_final_geral = media_geral.iloc[-1]

    if not vencedores.empty:
        media_vencedores = vencedores.mean()
        val_final_venc = media_vencedores.iloc[-1]
        linha_venc = media_vencedores
        label_venc = "Média dos Vencedores"
        texto_venc = f"R$ {val_final_venc:,.2f}"
    else:
        idx_max = finais.idxmax()
        linha_venc = df.loc[idx_max]
        val_final_venc = linha_venc.iloc[-1]
        label_venc = "Melhor Resultado"
        texto_venc = f"Melhor resultado: R$ {val_final_venc:,.2f}"

    if not perdedores.empty:
        media_perdedores = perdedores.mean()
        val_final_perd = media_perdedores.iloc[-1]
        linha_perd = media_perdedores
        label_perd = "Média dos Perdedores"
        texto_perd = f"R$ {val_final_perd:,.2f}"
    else:
        idx_min = finais.idxmin()
        linha_perd = df.loc[idx_min]
        val_final_perd = linha_perd.iloc[-1]
        label_perd = "Pior Resultado"
        texto_perd = f"Pior resultado: R$ {val_final_perd:,.2f}"

    valores_finais = [val_final_perd, val_final_venc, val_final_geral]
    range_y = df.max().max() - df.min().min()
    espacamento_min = 0.02 * range_y
    valores_ordenados = sorted(valores_finais)
    jitter_valores = [0, 0, 0]
    for i in range(1, len(valores_ordenados)):
        diff = valores_ordenados[i] - valores_ordenados[i-1]
        if diff < espacamento_min:
            desloc = espacamento_min - diff
            jitter_valores[i] = jitter_valores[i-1] + desloc
    jitter_map = dict(zip(valores_ordenados, jitter_valores))

    def aplicar_jitter(linha, valor_final):
        return linha + jitter_map.get(valor_final, 0)

    posicoes_texto = ajustar_posicao_texto_espaco_minimo(
        [val + jitter_map.get(val, 0) for val in valores_finais],
        espacamento_min=espacamento_min * 1.1
    )

    linha_venc = aplicar_jitter(linha_venc, val_final_venc)
    ax.plot(df.columns, linha_venc, color="#2e7d32", linewidth=2.5, label=label_venc)
    ax.text(df.columns[-1], posicoes_texto[valores_finais.index(val_final_venc)], texto_venc,
            color="#2e7d32", fontsize=10, va='center', ha='left', weight='bold')

    linha_perd = aplicar_jitter(linha_perd, val_final_perd)
    ax.plot(df.columns, linha_perd, color="#c62828", linewidth=2.5, label=label_perd)
    ax.text(df.columns[-1], posicoes_texto[valores_finais.index(val_final_perd)], texto_perd,
            color="#c62828", fontsize=10, va='center', ha='left', weight='bold')

    linha_geral = aplicar_jitter(media_geral, val_final_geral)
    ax.plot(df.columns, linha_geral, color="#1a5d1a", linewidth=2.5, linestyle='--', label="Média Geral")
    ax.text(df.columns[-1], posicoes_texto[valores_finais.index(val_final_geral)],
            f"R$ {val_final_geral:,.2f}", color="#1a5d1a", fontsize=10, va='center', ha='left', weight='bold')

    ax.yaxis.set_major_formatter(mtick.StrMethodFormatter('R$ {x:,.0f}'))
    ax.set_xlabel("Turno", fontsize=12)
    ax.set_ylabel("Saldo Acumulado (R$)", fontsize=12)
    ax.set_title("Evolução dos Saldos dos Apostadores", fontsize=14, weight='bold')
    ax.legend(frameon=False)
    ax.grid(True, linestyle="--", alpha=0.3)
    ax.set_facecolor("#ffffff")

    for spine in ax.spines.values():
        spine.set_visible(False)

    return fig

def plot_summary_histogram(df, bins=8):
    finais = df.iloc[:, -1]
    bin_series = pd.qcut(finais, q=bins, duplicates='drop')

    bin_labels = []
    for interval in bin_series.cat.categories:
        low = interval.left
        high = interval.right
        label = f"R${low:,.2f} → R${high:,.2f}"
        bin_labels.append(label)

    bin_series = bin_series.cat.rename_categories(bin_labels)
    df_plot = pd.DataFrame({"Saldo Final": finais, "Faixa": bin_series})

    plt.style.use("default")
    fig, ax = plt.subplots(figsize=(10, 6), facecolor="#f9f9f9")

    palette = sns.color_palette("husl", len(df_plot["Faixa"].unique()))
    for i, faixa in enumerate(df_plot["Faixa"].unique()):
        subset = df_plot[df_plot["Faixa"] == faixa]["Saldo Final"]
        ax.hist(subset, bins=30, alpha=0.6, label=faixa, color=palette[i])

    media = finais.mean()
    ax.axvline(media, color='black', linestyle='--', linewidth=2, label=f"Média: R$ {media:,.2f}")

    ax.set_title("Histograma Empilhado dos Saldos Finais por Faixa", fontsize=14, weight='bold')
    ax.set_xlabel("Saldo Final (R$)", fontsize=12)
    ax.set_ylabel("Frequência", fontsize=12)
    ax.legend(title="Faixa", bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(True, linestyle="--", alpha=0.3)
    plt.tight_layout()

    return fig


def plot_histogram_kde(df):
    finais = df.iloc[:, -1]
    perc_perdedores = (finais < 0).mean() * 100

    plt.style.use("default")
    fig, ax = plt.subplots(figsize=(10, 6), facecolor="#f9f9f9")

    sns.histplot(finais, bins=30, kde=True, color="gray", edgecolor="black", ax=ax, stat='density')

    media = finais.mean()
    ax.axvline(media, color='black', linestyle='--', linewidth=2, label=f"Média: R$ {media:,.2f}")

    ax.set_title("Histograma com Densidade dos Saldos Finais", fontsize=14, weight='bold')
    ax.set_xlabel("Saldo Final (R$)", fontsize=12)
    ax.set_ylabel("Densidade", fontsize=12)

    ax.text(0.95, 0.95, f"{perc_perdedores:.1f}% de chance de ser um perdedor",
            transform=ax.transAxes, ha='right', va='top',
            fontsize=12, bbox=dict(facecolor='white', edgecolor='gray', boxstyle='round'))

    ax.grid(True, linestyle="--", alpha=0.3)
    plt.tight_layout()

    return fig

def plot_violin_segmentado_unico(df):
    finais = df.iloc[:, -1].values

    fig, ax = plt.subplots(figsize=(12, 3), facecolor="#f9f9f9")

    # Seaborn violinplot para obter a forma, mas não desenhar nada
    sns.violinplot(x=finais, orient='h', ax=ax, color='gray', alpha=0.0, linewidth=0)

    # Recupera o Path do violin gerado
    for coll in ax.collections:
        if isinstance(coll, PolyCollection):
            verts = coll.get_paths()[0].vertices
            break
    else:
        raise RuntimeError("Não foi possível obter os vértices do violin.")

    x = verts[:, 0]
    y = verts[:, 1]

    # Separar onde x < 0 e x >= 0
    idx_neg = x < 0
    idx_pos = x >= 0

    def criar_poly(x, y):
        coords = np.column_stack([x, y])
        coords = np.vstack([coords, [x[-1], 0], [x[0], 0], coords[0]])
        return coords

    # Parte negativa
    if np.any(idx_neg):
        x_neg = x[idx_neg]
        y_neg = y[idx_neg]
        poly_neg = criar_poly(x_neg, y_neg)
        pc_neg = PolyCollection([poly_neg], facecolor="#c62828", alpha=0.3)
        ax.add_collection(pc_neg)

    # Parte positiva
    if np.any(idx_pos):
        x_pos = x[idx_pos]
        y_pos = y[idx_pos]
        poly_pos = criar_poly(x_pos, y_pos)
        pc_pos = PolyCollection([poly_pos], facecolor="#2e7d32", alpha=0.3)
        ax.add_collection(pc_pos)

    ax.set_ylim(-0.5, 0.5)
    ax.set_yticks([])
    ax.set_xlabel("Saldo Final (R$)", fontsize=12)
    ax.set_title("Violin Plot Segmentado (Horizontal)", fontsize=14, weight='bold')
    ax.grid(True, axis='x', linestyle='--', alpha=0.3)

    for spine in ax.spines.values():
        spine.set_visible(False)

    total = len(finais)
    vencedores = finais[finais >= 0]
    perdedores = finais[finais < 0]

    y_text = 0.3  # deslocamento vertical

    if len(vencedores) > 0:
        pct_vencedores = len(vencedores) / total * 100
        texto_vencedores = (
            f"Vencedores: {len(vencedores)} ({pct_vencedores:.1f}%)\n"
            f"Máximo: R\$ {vencedores.max():,.2f}\n"
            f"Médio: R\$ {vencedores.mean():,.2f}\n"
            f"Mínimo: R\$ {vencedores.min():,.2f}"
        )
    else:
        texto_vencedores = "Não há vencedores.\nVeja perdedores."

    if len(perdedores) > 0:
        pct_perdedores = len(perdedores) / total * 100
        texto_perdedores = (
            f"Perdedores: {len(perdedores)} ({pct_perdedores:.1f}%)\n"
            f"Máximo: R\$ {perdedores.max():,.2f}\n"
            f"Médio: R\$ {perdedores.mean():,.2f}\n"
            f"Mínimo: R\$ {perdedores.min():,.2f}"
        )
    else:
        texto_perdedores = "Não há perdedores.\nVeja vencedores."

    # Coloca texto dos vencedores à direita do zero
    xlim = ax.get_xlim()
    x_meio = (xlim[0] + xlim[1]) / 2
    ax.text(max(0, xlim[0]*0.1 + xlim[1]*0.9), y_text, texto_vencedores,
            ha='left', va='top', fontsize=10, color='#2e7d32')

    # Coloca texto dos perdedores à esquerda do zero
    ax.text(min(0, xlim[0]*0.9 + xlim[1]*0.1), -y_text, texto_perdedores,
            ha='right', va='bottom', fontsize=10, color='#c62828')

    plt.tight_layout()
    return fig
