import streamlit as st
from datetime import datetime, timedelta
import pytz

# Configuração da página
st.set_page_config(page_title="Calculadora de Jornada", page_icon="⏳", layout="centered")

# Definir fuso horário de Brasília
br_tz = pytz.timezone("America/Sao_Paulo")

# Estilos personalizados
st.markdown(
    """
    <style>
        .stButton > button {
            background-color: #4CAF50;
            color: white;
            font-size: 16px;
        }
        .stSuccess {
            font-size: 20px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Título principal
st.title("📅 Calculadora de Jornada de Trabalho")

# Opção para selecionar a duração da jornada
jornada_horas = st.selectbox("Selecione sua jornada:", ["8h", "9h48min", "12h", "6h"], index=1)

# Converter jornada para timedelta
jornada_mapa = {"8h": timedelta(hours=8), "9h48min": timedelta(hours=9, minutes=48), "12h": timedelta(hours=12), "6h": timedelta(hours=6)}
jornada = jornada_mapa[jornada_horas]

# Criar uma variável no session_state para armazenar o horário de chegada
if "hora_chegada" not in st.session_state:
    st.session_state.hora_chegada = ""

# Função para validar a hora
def validar_hora(hora_str):
    try:
        hora, minuto = map(int, hora_str.split(":"))
        if 0 <= hora < 24 and 0 <= minuto < 60:
            return True
    except ValueError:
        return False
    return False

# Entrada da hora de chegada
col1, col2 = st.columns([2, 1])
with col1:
    hora_chegada_str = st.text_input("Digite a hora de chegada (HH:MM):", placeholder="Ex: 08:30", value=st.session_state.hora_chegada)
with col2:
    if st.button("Usar horário atual"):
        st.session_state.hora_chegada = datetime.now().astimezone(br_tz).strftime("%H:%M")
        hora_chegada_str = st.session_state.hora_chegada  # Atualiza a variável local para cálculo
        st.rerun()  # Atualiza a interface corretamente

# Processamento da hora de saída
if hora_chegada_str:
    if validar_hora(hora_chegada_str):
        agora = datetime.now().astimezone(br_tz)
        hora, minuto = map(int, hora_chegada_str.split(":"))
        chegada_dt = agora.replace(hour=hora, minute=minuto, second=0, microsecond=0)

        # Se a hora de chegada for maior que a hora atual, significa que começou no dia anterior
        if chegada_dt > agora:
            chegada_dt -= timedelta(days=1)

        # Calcular horário de saída e tolerância
        hora_saida = chegada_dt + jornada
        hora_saida_antes = hora_saida - timedelta(minutes=5)
        hora_saida_depois = hora_saida + timedelta(minutes=5)

        # Exibir horários fixos
        st.success(f"🔔 Você deve sair às **{hora_saida.strftime('%H:%M')}**")
        st.info(f"⏳ Tolerância: **{hora_saida_antes.strftime('%H:%M')}** até **{hora_saida_depois.strftime('%H:%M')}**")
    else:
        st.error("⚠️ Formato inválido! Digite no formato HH:MM, ex: 08:30")

# Rodapé com Foto, Assinatura e LinkedIn
st.markdown("---")
col1, col2 = st.columns([1, 3])
with col1:
    st.image("tech_lopes.png", width=100)  # Substitua pelo caminho da sua foto
with col2:
    st.markdown("🖊️ **Desenvolvido por Matheus Miranda Lopes**")
    st.markdown("[🔗 Meu LinkedIn](https://www.linkedin.com/in/matheus-miranda-31275b174/)", unsafe_allow_html=True)

   
