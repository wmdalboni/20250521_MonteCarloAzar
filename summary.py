def summarize_turns(df):
    turnos = df.shape[1]
    sumario = ""
    for t in range(turnos):
        media = df.iloc[:, t].mean()
        std = df.iloc[:, t].std()
        sumario += f"Turno {t+1}: Média = {media:.2f}, Desvio Padrão = {std:.2f}\n"
    return sumario

def summarize_total(df):
    finais = df.iloc[:, -1]
    media_total = finais.mean()
    std_total = finais.std()
    return (
        f"Média final dos saldos: {media_total:.2f}\n"
        f"Desvio padrão final: {std_total:.2f}\n"
        f"Min: {finais.min():.2f}, Max: {finais.max():.2f}"
    )
