import streamlit as st
from simulator import run_simulation
from visualizer import plot_simulation
from summary import summarize_turns, summarize_total

st.set_page_config(page_title="Simulação Monte Carlo de Apostas", layout="wide")

st.title("🎲 Simulação Monte Carlo de Apostas")

aposta = st.number_input("Valor da Aposta", min_value=0.0, value=10.0, step=1.0)
retorno = st.number_input("Taxa de Retorno (multiplicador)", min_value=0.0, value=2.0, step=0.1)
turnos = st.slider("Quantidade de Turnos (Eixo X)", 1, 200, 50)
chance_perda = st.slider("Chance de Perder (%)", 0, 100, 50)
apostadores = st.number_input("Número de Apostadores (iterações)", min_value=1, value=1000, step=1)

if st.button("Iniciar Simulação"):
    resultados = run_simulation(aposta, retorno, turnos, chance_perda, apostadores)
    st.pyplot(plot_simulation(resultados))

    st.subheader("📊 Sumário por Turno")
    st.text(summarize_turns(resultados))

    st.subheader("📈 Sumário Total")
    st.text(summarize_total(resultados))
