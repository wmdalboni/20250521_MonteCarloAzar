def summarize_turns(df):
    turnos = df.shape[1]
    sumario = ""
    for t in range(turnos):
        media = df.iloc[:, t].mean()
        std = df.iloc[:, t].std()
        sumario += f"Turno {t+1}: Média = {media:.2f}, Desvio Padrão = {std:.2f}\n"
    return sumario
