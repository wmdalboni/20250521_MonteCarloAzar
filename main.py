import streamlit as st
from simulator import run_simulation
from visualizer import plot_simulation,  plot_violin_segmentado_unico
# from summary import summarize_turns

st.set_page_config(page_title="Simulação Monte Carlo de Apostas", layout="wide")

st.title("🎲 Simulação Monte Carlo de Apostas")

aposta = st.number_input("Valor da Aposta", min_value=0.0, value=10.0, step=1.0)
retorno = st.number_input("Taxa de Retorno (multiplicador)", min_value=0.0, value=2.0, step=0.1)
turnos = st.number_input("Quantidade de Turnos (Eixo X)", 1, 1000, 50)
chance_perda = st.number_input("Chance de Perder (%)", 0, 100, 50)
apostadores = st.number_input("Número de Apostadores (iterações)", min_value=1, value=1000, step=1)
# bins = st.slider("Quantidade de Faixas (bins)", min_value=2, max_value=20, value=8)

if st.button("Iniciar Simulação"):
    resultados = run_simulation(aposta, retorno, turnos, chance_perda, apostadores)

    st.pyplot(plot_simulation(resultados))

    st.subheader("📊 Violin Plot dos Saldos Finais por Faixa")
    st.pyplot(plot_violin_segmentado_unico(resultados))
