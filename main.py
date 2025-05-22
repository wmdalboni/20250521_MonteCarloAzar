import streamlit as st
from simulator import run_simulation
from visualizer import plot_simulation, plot_box_segmentado_unico


st.set_page_config(page_title="Simulabets!", layout="wide")

st.title("🎲 Simule antes de Jogar nas Bets!")

col1, col2 = st.columns(2)

with col1:
    aposta = st.number_input("Valor da Aposta", min_value=0.0, value=10.0, step=1.0, help="⚠️ Quanto dinheiro você vai apostar. Se não souber, deixe como está como exemplo.")
    retorno = st.number_input("Multiplicador (Taxa de Retorno)", min_value=0.0, value=2.0, step=0.1,help="⚠️ Quantas vezes você multiplicará sua aposta se você ganhar. Ex: Um valor 2 significa dobrar a aposta ao vencer. Se não souber, coloque uma média aproximada e arredondado para baixo.")
    chance_perda = st.number_input("Chance de Perder (%)", 0, 100, 95, help="⚠️ Qual sua chance de perder a cada aposta em \%. Ex: 95 siginifica 95\% de perder. Se não souber, prefira 95.")

with col2:
    turnos = st.number_input("Quantidade de Apostas", 1, 1000, 50, step=1, help="⚠️ O valor não pode ser negativo.")
    apostadores = st.number_input("Número de Apostadores", min_value=1, value=100, step=1, max_value=100, help="Ele simulará não só sua jogada mas vários outros como você. Mais pessoas jogando significa mais precisão. Se não souber, deixe como está.")

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

st.write("")
if valor_esperado < 0:
    mensagem = f"Com {turnos} apostas, você perderá R$ {abs(media_esperada):.2f} ao final!"
else:
    mensagem = f"Confira os dados inseridos porque, com o devido tempo, a Bet nunca perde!"

st.markdown(
    f"**ATENÇÃO**<br><span style='color:{cor}'> {mensagem} </span>",
    unsafe_allow_html=True
)


if st.button("Iniciar Simulação"):
    resultados = run_simulation(aposta, retorno, turnos, chance_perda, apostadores)
    with st.expander("**Não acredita nos dados?**", expanded=False):
        st.markdown("Em dúvida se os gráficos estão certos? \n Confira os dados da simulação. Cada linha representa um apostador e cada coluna representa um turno.")
        st.markdown("O saldo final de cada apostador é a última coluna.")
        st.dataframe(resultados)

    st.pyplot(plot_simulation(resultados))

    st.subheader("📊 Boxplot dos Saldos Finais por Faixa")
    st.pyplot(plot_box_segmentado_unico(resultados))
