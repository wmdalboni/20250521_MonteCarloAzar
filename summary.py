def summarize_turns(df):
    # Primeiro, pego o número de turnos (colunas) do DataFrame.
    turnos = df.shape[1]

    # Inicializo uma string vazia para armazenar o resumo.
    sumario = ""

    # Percorro cada turno para calcular estatísticas.
    for t in range(turnos):
        # Para o turno atual, calculo a média dos saldos de todos os apostadores.
        media = df.iloc[:, t].mean()

        # Também calculo o desvio padrão, para entender a dispersão dos saldos.
        std = df.iloc[:, t].std()

        # Concateno esses valores formatados na string resumo, organizando por turno.
        sumario += f"Turno {t+1}: Média = {media:.2f}, Desvio Padrão = {std:.2f}\n"

    # No final, retorno a string com o resumo completo de todos os turnos.
    return sumario
