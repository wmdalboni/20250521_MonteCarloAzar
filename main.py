import streamlit as st
from simulator import run_simulation
from visualizer import plot_simulation, plot_box_segmentado_unico


st.set_page_config(page_title="Simulação Monte Carlo de Apostas", layout="wide")

st.title("🎲 Simulação Monte Carlo de Apostas")

col1, col2 = st.columns(2)

with col1:
    aposta = st.number_input("Valor da Aposta", min_value=0.0, value=10.0, step=1.0)
    retorno = st.number_input("Taxa de Retorno (multiplicador)", min_value=0.0, value=2.0, step=0.1)
    chance_perda = st.number_input("Chance de Perder (%)", 0, 100, 50)

with col2:
    turnos = st.number_input("Quantidade de Turnos (Eixo X)", 1, 1000, 50)
    apostadores = st.number_input("Número de Apostadores (iterações)", min_value=1, value=1000, step=1)

    col3, col4, col5, col6 = st.columns(4)

    with col3:
        st.write("")
        lucro_liquido = (retorno - 1) * aposta
        st.markdown(f"**Se Ganhar:**<br>R$ {lucro_liquido:.2f}", unsafe_allow_html=True)

    with col4:
        st.write("")
        perda_unitaria = -aposta
        st.markdown(f"**Se Perder:**<br>R$ {perda_unitaria:.2f}", unsafe_allow_html=True)

    with col5:
        st.write("")
        prob_perda = chance_perda / 100
        prob_ganho = 1 - prob_perda

        valor_esperado = (prob_ganho * lucro_liquido) + (prob_perda * perda_unitaria)

        cor = "green" if valor_esperado > 0 else "red" if valor_esperado < 0 else "black"

        st.markdown(
            f"**Unitário Esperado:**<br><span style='color:{cor}'>R$ {valor_esperado:.2f} </span>",
            unsafe_allow_html=True
        )

    with col6:
        st.write("")
        media_esperada = valor_esperado * turnos

        st.markdown(
            f"**Total Esperada:**<br><span style='color:{cor}'>R$ {media_esperada:.2f} </span>",
            unsafe_allow_html=True
        )

if st.button("Iniciar Simulação"):
    resultados = run_simulation(aposta, retorno, turnos, chance_perda, apostadores)

    st.dataframe(resultados)

    st.pyplot(plot_simulation(resultados))

    st.subheader("📊 Boxplot dos Saldos Finais por Faixa")
    st.pyplot(plot_box_segmentado_unico(resultados))
