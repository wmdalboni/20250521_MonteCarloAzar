import streamlit as st
from simulator import run_simulation
from visualizer import plot_simulation, plot_box_segmentado_unico
import os

# Recupero a chave Pix
pix_key = st.secrets.get("PIX_KEY", None)

# Aqui eu configuro a página do Streamlit, dando um título para a aba e definindo o layout como 'wide' para usar mais espaço horizontal.
st.set_page_config(page_title="Simulabets!", layout="wide")
st.info("Este site está em construção e funcionará melhor em telas grandes. Se você está vendo isso, é porque você é especial! Obrigado por testar!")

# Defino o título principal que vai aparecer no topo da aplicação.
st.title("🎲 SimulaBet 🎲")
st.markdown("## Simule suas apostas!")

# Crio duas colunas para organizar os inputs do usuário lado a lado, assim fica mais limpo e intuitivo.
col1, col2 = st.columns(2)

# Na primeira coluna, peço para o usuário informar o valor da aposta, o multiplicador do ganho e a chance de perder.
with col1:
    # Valor da aposta: uso number_input para garantir que o usuário insira um número positivo.
    aposta = st.number_input(
        "Valor da Aposta (R$)", min_value=0.0, value=10.0, step=1.0,
        help="⚠️ Quanto dinheiro você vai apostar. Se não souber, deixe como está como exemplo."
    )
    # Multiplicador de retorno: quantas vezes a aposta será multiplicada se ganhar.
    retorno = st.number_input(
        "Multiplicador ao ganhar (Taxa de Retorno)", min_value=0.0, value=5.0, step=0.1,
        help="⚠️ Quantas vezes você multiplicará sua aposta se você ganhar. Ex: Um valor 2 significa dobrar a aposta ao vencer. Se não souber, coloque um valor aproximado e arredondado para baixo."
    )
    # Chance de perder em porcentagem.
    chance_perda = st.number_input(
        "Chance de Perder (%)", 0, 100, 85,
        help="⚠️ Qual sua chance de perder a cada aposta em %. Ex: 95 significa 95% de perder. Se não souber, deixe como está."
    )

# Na segunda coluna, peço quantidade de apostas e número de apostadores (simulação múltipla para precisão).
with col2:
    # Número de apostas que serão simuladas.
    turnos = st.number_input(
        "Quantidade de Apostas", 1, 1000, 100, step=1,
        help="⚠️ O valor não pode ser negativo."
    )
    # Número de apostadores simulados (para gerar uma média mais confiável).
    apostadores = st.number_input(
        "Número de Apostadores", min_value=1, value=300, step=1, max_value=300,
        help="Ele simulará não só sua jogada mas vários outros como você. Mais pessoas jogando significa mais precisão. Se não souber, deixe como está."
    )

    # Dentro da segunda coluna, crio 4 sub-colunas para mostrar cálculos rápidos lado a lado: lucro, perda, valor esperado e valor esperado total.
    col3, col4, col5, col6 = st.columns(4)

    # Calculo o lucro líquido em caso de vitória (multiplicador menos o valor apostado).
    with col3:
        st.write("")
        lucro_liquido = (retorno - 1) * aposta
        st.markdown(f"**Se Ganhar:**<br>R$ {lucro_liquido:.2f}", unsafe_allow_html=True)

    # Calculo a perda unitária (que é o valor da aposta negativo).
    with col4:
        st.write("")
        perda_unitaria = -aposta
        st.markdown(f"**Se Perder:**<br>R$ {perda_unitaria:.2f}", unsafe_allow_html=True)

    # Calculo o valor esperado para uma aposta: chance de ganhar vezes lucro + chance de perder vezes perda.
    with col5:
        st.write("")
        prob_perda = chance_perda / 100
        prob_ganho = 1 - prob_perda
        valor_esperado = (prob_ganho * lucro_liquido) + (prob_perda * perda_unitaria)
        # Defino a cor do texto: verde se positivo, vermelho se negativo, preto se zero.
        cor = "green" if valor_esperado > 0 else "red" if valor_esperado < 0 else "black"
        # Mostro o valor esperado para 1 aposta com a cor definida.
        st.markdown(
            f"**01 Aposta:**<br><span style='color:{cor}'>R$ {valor_esperado:.2f}</span>",
            unsafe_allow_html=True
        )

    # Multiplico o valor esperado pelo número de apostas para mostrar o valor esperado total.
    with col6:
        st.write("")
        media_esperada = valor_esperado * turnos
        st.markdown(
            f"**{turnos:.0f} Apostas:**<br><span style='color:{cor}'>R$ {media_esperada:.2f}</span>",
            unsafe_allow_html=True
        )

# Quando o botão "Iniciar Simulação" for clicado, chamo a função de simulação e mostro os resultados.
if st.button("Iniciar Simulação"):
    # Executo a simulação com os parâmetros fornecidos.
    resultados = run_simulation(aposta, retorno, turnos, chance_perda, apostadores)

    st.write("")

    # Exibo uma mensagem de alerta personalizada baseada no valor esperado.
    if valor_esperado < 0:
        mensagem = f"Com {turnos} apostas, você perderá R$ {abs(media_esperada):.2f}* ao final!"
        cor_msg = "red"
        icone = " 🚨 "
        titulo = "VOCÊ VAI SE LASCAR!"
    else:
        mensagem = "Os dados inseridos estão subestimando* a ganância da Bet!"
        cor_msg = "orange"
        icone = " ⚠️ "
        titulo = "CUIDADO!"

    # Exibo o banner de alerta com estilo inline CSS, destacando o aviso para o usuário.
    st.markdown(f"""
    <div style="background-color:#{'ffcccc' if cor_msg=='red' else 'fff3cd'};padding:20px;border-radius:10px;border:2px solid {cor_msg};">
        <h1 style="color:{cor_msg};">{icone} {titulo}</h1>
        <h2 style="color:{cor_msg};">{mensagem}</h2>
        <em style="color:{cor_msg};">*Mais provável.</em>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f"")
                
    # Mostro o gráfico da simulação usando matplotlib integrado ao Streamlit.
    st.subheader("📊 Quanto dinheiro eu vou perder?")
    st.pyplot(plot_simulation(resultados))

    # Mostro o boxplot dos saldos finais segmentados.
    st.subheader("📊 Qual a chance de eu perder dinheiro?")
    st.pyplot(plot_box_segmentado_unico(resultados))

    # Permito ao usuário expandir e conferir os dados brutos da simulação em uma tabela.
    with st.expander("**Quer conferir os dados? Clique aqui!**", expanded=False):
        st.markdown(
            "Em dúvida se os gráficos estão certos?\n"
            "Confira os dados da simulação. Cada linha representa um apostador e cada coluna representa um turno.\n"
            "O saldo final de cada apostador é a última coluna."
        )
        st.dataframe(resultados)


# -------------------------------------------------------
# DISCLAIMER EM COLUNAS
# -------------------------------------------------------
col1, col2 = st.columns([3, 1])  # Coluna 1 maior, coluna 2 menor

with col1:
    disclaimer_html = f"""
    ---
    <div style="font-size:12px;color:gray;margin-top:20px;">
    <b>Disclaimer:</b> Espero que esta ferramenta ajude a salvar alguém importante para você da ludomania, do mesmo jeito que ela ajudou quem era importante para mim.  
    Esta ferramenta é oferecida com carinho, para fins educacionais e de simulação apenas.  
    Os resultados aqui apresentados não garantem ganhos ou perdas reais. Use por sua conta e risco.<br><br>

    Você pode usar, modificar e distribuir este código, desde que mantenha o devido crédito ao autor original:  
    <b>Willian Dalboni, Analista de Dados e BI</b> (<a href="https://www.linkedin.com/in/willian-dalboni-50126637/" target="_blank">LinkedIn</a>).<br><br>
    Se este projeto fez a diferença para você, considere apoiar com uma doação simbólica via Pix na Imagem ao lado. 
    <br>Muito obrigado pelo seu apoio e confiança!  
    </div>
    """
    st.markdown(disclaimer_html, unsafe_allow_html=True)

with col2:
    st.markdown("---")
    # Adicione a imagem do seu QR Code do Pix aqui
    st.image("img/pix.png", caption="Apoie via Pix", width=200)


