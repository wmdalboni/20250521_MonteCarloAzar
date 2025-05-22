import numpy as np
import pandas as pd

def run_simulation(aposta, retorno, turnos, chance_perda, apostadores):
    # Primeiro, calculo a chance de vitória a partir da chance de perda informada (convertendo % para probabilidade decimal).
    chance_vitoria = 1 - (chance_perda / 100)

    # Crio uma matriz zero para armazenar o saldo de cada apostador em cada turno.
    # Linhas = número de apostadores, colunas = número de turnos (apostas).
    historico = np.zeros((apostadores, turnos))

    # Agora faço a simulação para cada apostador.
    for i in range(apostadores):
        saldo = 0  # Inicializo o saldo de cada apostador como zero.
        # Para cada turno (aposta), vou determinar se ele ganhou ou perdeu.
        for t in range(turnos):
            # Simulo a aposta usando uma distribuição uniforme [0,1).
            # Se o número gerado for menor que a chance de vitória, o apostador venceu.
            venceu = np.random.rand() < chance_vitoria

            # Calculo o lucro da aposta: se ganhou, o retorno menos a aposta original.
            lucro = (aposta * retorno) - aposta

            # Atualizo o saldo somando o lucro se venceu, ou subtraindo a aposta se perdeu.
            saldo += lucro if venceu else -aposta

            # Armazeno o saldo atualizado na matriz histórica, na linha do apostador e coluna do turno.
            historico[i, t] = saldo

    # No final, converto a matriz numpy em um DataFrame do pandas para facilitar análise e visualização.
    return pd.DataFrame(historico)
