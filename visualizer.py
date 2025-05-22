# visualizer.py
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from collections import Counter
import seaborn as sns
import numpy as np

def _adicionar_marca_dagua_e_disclaimer(ax, texto_linkedin, texto_disclaimer):
    """
    Aqui eu criei essa função para adicionar uma marca d'água sutil e um disclaimer no rodapé do gráfico.
    Quis deixar a marca d'água grande, no centro, mas com transparência bem baixa para não atrapalhar a leitura.
    O disclaimer fica no canto inferior direito, menor e também transparente, pra não poluir visualmente.
    Uso transform=ax.transAxes para posicionar baseado no eixo (0 a 1).
    """
    ax.text(0.5, 0.5, texto_linkedin, fontsize=40, color='gray', alpha=0.1,
            ha='center', va='center', rotation=30, transform=ax.transAxes, zorder=0)

    ax.text(1.0, -0.07, texto_disclaimer, fontsize=8, color='gray', alpha=0.4,
            ha='right', va='top', transform=ax.transAxes)

def plot_simulation(df):
    """
    Essa função é a principal para plotar a simulação dos saldos acumulados dos apostadores.
    Começo definindo uma função interna para ajustar a posição dos textos, evitando que fiquem muito próximos.
    """

    def ajustar_posicao_texto_espaco_minimo(valores, espacamento_min=15):
        """
        Aqui eu garanto que os valores dos textos finais no gráfico não fiquem colados,
        adicionando um espaçamento mínimo entre eles.
        Faço isso ordenando os valores, aplicando deslocamento quando necessário,
        e depois realocando para manter a ordem original.
        """
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

    # Começo criando o plot com um fundo claro cinza para suavizar a visualização.
    plt.style.use("default")
    fig, ax = plt.subplots(figsize=(14, 7), facecolor="#f2f2f2", constrained_layout=True)

    # Faço duas áreas de fundo coloridas para facilitar a leitura dos valores positivos e negativos.
    ax.axhspan(0, df.max().max(), facecolor="#e6f4ea")  # Verde claro para positivos
    ax.axhspan(df.min().min(), 0, facecolor="#fce8e6")  # Vermelho claro para negativos

    # Marco o ponto de equilíbrio (zero) com uma linha tracejada escura.
    ax.axhline(0, color="#333333", linewidth=1.2, linestyle="--", label="Ponto de Equilíbrio")

    # Para mostrar o comportamento individual de até 100 linhas, ploto cada uma com muita transparência.
    for i in range(min(100, df.shape[0])):
        ax.plot(df.columns, df.iloc[i], color="gray", alpha=0.05)

    # Separo os vencedores e perdedores para calcular médias e identificar valores finais.
    finais = df.iloc[:, -1]
    vencedores = df[finais >= 0]
    perdedores = df[finais < 0]

    media_geral = df.mean()
    val_final_geral = media_geral.iloc[-1]

    # Se tiver vencedores, calculo a média deles, senão pego o melhor resultado diretamente.
    if not vencedores.empty:
        media_vencedores = vencedores.mean()
        val_final_venc = media_vencedores.iloc[-1]
        linha_venc = media_vencedores
        label_venc = "Média dos Vencedores"
        texto_venc = f" R$ {val_final_venc:,.2f}"
    else:
        idx_max = finais.idxmax()
        linha_venc = df.loc[idx_max]
        val_final_venc = linha_venc.iloc[-1]
        label_venc = "Melhor Resultado"
        texto_venc = f" Melhor resultado: \n R$ {val_final_venc:,.2f}"

    # Faço o mesmo para os perdedores, calculando média ou pegando o pior resultado.
    if not perdedores.empty:
        media_perdedores = perdedores.mean()
        val_final_perd = media_perdedores.iloc[-1]
        linha_perd = media_perdedores
        label_perd = "Média dos Perdedores"
        texto_perd = f" R$ {val_final_perd:,.2f}"
    else:
        idx_min = finais.idxmin()
        linha_perd = df.loc[idx_min]
        val_final_perd = linha_perd.iloc[-1]
        label_perd = "Pior Resultado"
        texto_perd = f" Pior resultado: R$ {val_final_perd:,.2f}"

    # Para os textos finais, preparo uma pequena lógica para evitar sobreposição.
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
        # Aqui eu aplico o deslocamento calculado para evitar que as linhas e textos fiquem sobrepostos.
        return linha + jitter_map.get(valor_final, 0)

    # Ajusto a posição dos textos no eixo Y para evitar sobreposição.
    posicoes_texto = ajustar_posicao_texto_espaco_minimo(
        [val + jitter_map.get(val, 0) for val in valores_finais],
        espacamento_min=espacamento_min * 1.1
    )

    # Ploto a linha dos vencedores (ou melhor resultado) com destaque em verde.
    linha_venc = aplicar_jitter(linha_venc, val_final_venc)
    ax.plot(df.columns, linha_venc, color="#2e7d32", linewidth=2.5, label=label_venc)
    ax.text(df.columns[-1], posicoes_texto[valores_finais.index(val_final_venc)], texto_venc,
            color="#2e7d32", fontsize=10, va='center', ha='left', weight='bold')

    # Ploto a linha dos perdedores (ou pior resultado) em vermelho.
    linha_perd = aplicar_jitter(linha_perd, val_final_perd)
    ax.plot(df.columns, linha_perd, color="#c62828", linewidth=2.5, label=label_perd)
    ax.text(df.columns[-1], posicoes_texto[valores_finais.index(val_final_perd)], texto_perd,
            color="#c62828", fontsize=10, va='center', ha='left', weight='bold')

    # Ploto a média geral com linha tracejada preta.
    linha_geral = aplicar_jitter(media_geral, val_final_geral)
    ax.plot(df.columns, linha_geral, color="#060606", linewidth=2.5, linestyle='--', label="Média Geral")
    ax.text(df.columns[-1], posicoes_texto[valores_finais.index(val_final_geral)],
            f" R$ {val_final_geral:,.2f}", color="#060606", fontsize=10, va='center', ha='left', weight='bold')

    # Formato o eixo Y para moeda brasileira.
    ax.yaxis.set_major_formatter(mtick.StrMethodFormatter(' R$ {x:,.0f}'))
    ax.set_xlabel("Turno", fontsize=12)
    ax.set_ylabel("Saldo Acumulado (R$)", fontsize=12)
    ax.legend(frameon=False)
    ax.grid(True, linestyle="--", alpha=0.3)
    ax.set_facecolor("#ffffff")

    # Removo as bordas do gráfico para um visual mais limpo.
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Agora adiciono a marca d'água e o disclaimer, para garantir a autoria e informar que os dados são simulados.
    _adicionar_marca_dagua_e_disclaimer(ax,
                                        texto_linkedin="linkedin.com/in/seunome",
                                        texto_disclaimer="© 2025 /in/willian-dalboni-50126637 - Dados simulados para fins educacionais")

    return fig

def plot_box_segmentado_unico(df):
    """
    Aqui eu faço um boxplot do saldo final da simulação, segmentando visualmente os valores positivos e negativos.
    Quero mostrar claramente quem ganhou e quem perdeu, e dar uma descrição resumida com números no gráfico.
    """

    finais = df.iloc[:, -1].values
    fig, ax = plt.subplots(figsize=(12, 5), facecolor="#f9f9f9")

    min_val = finais.min()
    max_val = finais.max()

    # Adiciono cor de fundo para partes negativas e positivas.
    if min_val < 0:
        ax.axvspan(min_val, 0, facecolor="#fce8e6")
    if max_val > 0:
        ax.axvspan(0, max_val, facecolor="#e6f4ea")

    # Linha do ponto de equilíbrio no eixo X.
    ax.axvline(0, color="#333333", linewidth=1.2, linestyle="--", label="Ponto de Equilíbrio")

    # Faço o boxplot horizontal do saldo final.
    sns.boxplot(x=finais, orient='h', ax=ax,
                boxprops=dict(facecolor=(1,1,1,0.2), edgecolor='black'),
                whiskerprops=dict(color='black'),
                capprops=dict(color='black'),
                medianprops=dict(color='black'),
                flierprops=dict(marker='o', markersize=5, linestyle='none', markerfacecolor='gray', alpha=0.3),
                width=0.3)

    # Removo ticks verticais, pois só o eixo X importa aqui.
    ax.set_yticks([])
    ax.set_xlabel("Saldo Final (R$)", fontsize=12)
    ax.grid(True, axis='x', linestyle='--', alpha=0.3)
    ax.set_facecolor((1, 1, 1, 0.5))

    total = len(finais)
    vencedores = finais[finais >= 0]
    perdedores = finais[finais < 0]
    y_text = 0.3  # Posição vertical dos textos

    # Texto resumo para vencedores.
    if len(vencedores) > 0:
        pct_vencedores = len(vencedores) / total * 100
        texto_vencedores = (
            f"{len(vencedores)} vencedores! ({pct_vencedores:.1f}%)\n"
            f"Máx: R$ {vencedores.max():,.2f}\n"
            f"Médio: R$ {vencedores.mean():,.2f}\n"
            f"Mín: R$ {vencedores.min():,.2f}"
        )
    else:
        texto_vencedores = "Não há vencedores.\n Veja os perdedores."

    # Texto resumo para perdedores.
    if len(perdedores) > 0:
        pct_perdedores = len(perdedores) / total * 100
        texto_perdedores = (
            f"{len(perdedores)} perdedores! ({pct_perdedores:.1f}%)\n"
            f"Máx: R$ {perdedores.max():,.2f}\n"
            f"Médio: R$ {perdedores.mean():,.2f}\n"
            f"Mín: R$ {perdedores.min():,.2f}"
        )
    else:
        texto_perdedores = "Não há perdedores.\n Os dados estão errados."

    xlim = ax.get_xlim()

    # Texto à direita para vencedores
    ax.text(max(0, xlim[0]*0.1 + xlim[1]*0.9), y_text, texto_vencedores,
            ha='left', va='top', fontsize=10, color='#2e7d32')

    # Texto à esquerda para perdedores
    ax.text(min(0, xlim[0]*0.9 + xlim[1]*0.1), -y_text, texto_perdedores,
            ha='right', va='bottom', fontsize=10, color='#c62828')

    for spine in ax.spines.values():
        spine.set_visible(False)

    # Também adiciono a marca d'água e disclaimer aqui para manter a consistência.
    _adicionar_marca_dagua_e_disclaimer(ax,
                                        texto_linkedin="linkedin.com/in/seunome",
                                        texto_disclaimer="© 2025 /in/willian-dalboni-50126637 - Dados simulados para fins educacionais")

    plt.tight_layout()
    return fig
