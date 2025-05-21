import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from collections import Counter
import numpy as np

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

    # Fundo colorido
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

    # Substituições
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

    # Espaçamento
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

    # Linhas principais
    linha_venc = aplicar_jitter(linha_venc, val_final_venc)
    ax.plot(df.columns, linha_venc, color="#2e7d32", linewidth=2.5, label=label_venc)
    ax.text(df.columns[-1], posicoes_texto[valores_finais.index(val_final_venc)],
            texto_venc,
            color="#2e7d32", fontsize=10, va='center', ha='left', weight='bold')

    linha_perd = aplicar_jitter(linha_perd, val_final_perd)
    ax.plot(df.columns, linha_perd, color="#c62828", linewidth=2.5, label=label_perd)
    ax.text(df.columns[-1], posicoes_texto[valores_finais.index(val_final_perd)],
            texto_perd,
            color="#c62828", fontsize=10, va='center', ha='left', weight='bold')

    linha_geral = aplicar_jitter(media_geral, val_final_geral)
    ax.plot(df.columns, linha_geral, color="#1a5d1a", linewidth=2.5, linestyle='--', label="Média Geral")
    ax.text(df.columns[-1], posicoes_texto[valores_finais.index(val_final_geral)],
            f"R$ {val_final_geral:,.2f}",
            color="#1a5d1a", fontsize=10, va='center', ha='left', weight='bold')

    # Ajustes finais
    ax.yaxis.set_major_formatter(mtick.StrMethodFormatter('R$ {x:,.0f}'))
    ax.set_xlabel("Turno", fontsize=12)
    ax.set_ylabel("Saldo Acumulado (R$)", fontsize=12)
    ax.set_title("Evolução dos Saldos dos Apostadores", fontsize=14, weight='bold')
    ax.legend(frameon=False)
    ax.grid(True, linestyle="--", alpha=0.3)
    ax.set_facecolor("#ffffff")

    # Remove bordas pretas
    for spine in ax.spines.values():
        spine.set_visible(False)

    return fig
