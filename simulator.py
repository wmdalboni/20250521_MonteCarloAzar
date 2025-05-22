import numpy as np
import pandas as pd

def run_simulation(aposta, retorno, turnos, chance_perda, apostadores):
    chance_vitoria = 1 - (chance_perda / 100)
    historico = np.zeros((apostadores, turnos))

    for i in range(apostadores):
        saldo = 0
        for t in range(turnos):
            venceu = np.random.rand() < chance_vitoria
            lucro = (aposta * retorno) - aposta
            saldo += lucro if venceu else -aposta
            historico[i, t] = saldo

    return pd.DataFrame(historico)

