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

# Usar session_state para controlar o valor da hora
if 'hora_chegada_str' not in st.session_state:
    st.session_state.hora_chegada_str = ""

# Entrada da hora de chegada
col1, col2 = st.columns([2, 1])
with col1:
    hora_chegada_str = st.text_input("Digite a hora de chegada (HH:MM):", placeholder="Ex: 08:30", value=st.session_state.hora_chegada_str)
with col2:
    if st.button("Usar horário atual"):
        # Preencher o campo de hora com a hora atual
        st.session_state.hora_chegada_str = datetime.now().astimezone(br_tz).strftime("%H:%M")

# Opção de alerta de 5 minutos
ativar_alerta = st.checkbox("🔔 Ativar alerta de 5 minutos antes")

if hora_chegada_str:
    try:
        # Converter entrada para datetime no fuso de Brasília corretamente
        chegada_dt = br_tz.localize(datetime.strptime(hora_chegada_str, "%H:%M"))
        
        # Calcular horário de saída
        hora_saida = chegada_dt + jornada
        
        # Calcular tolerância (5 minutos antes e depois)
        hora_saida_antes = hora_saida - timedelta(minutes=5)
        hora_saida_depois = hora_saida + timedelta(minutes=5)

        # Calcular contagem regressiva
        agora = datetime.now().astimezone(br_tz)
        tempo_restante = hora_saida - agora
        horas, minutos = divmod(int(tempo_restante.total_seconds()) // 60, 60)

        # Exibir resultado
        st.success(f"🔔 Você deve sair às **{hora_saida.strftime('%H:%M')}**")
        st.info(f"⏳ Tolerância: **{hora_saida_antes.strftime('%H:%M')}** até **{hora_saida_depois.strftime('%H:%M')}**")
        
        if tempo_restante.total_seconds() > 0:
            st.warning(f"⏳ Tempo restante: **{horas}h {minutos}min**")
            
            # Alerta de 5 minutos antes
            if ativar_alerta and tempo_restante.total_seconds() <= 300:  # 5 minutos = 300 segundos
                st.error("🚨 Atenção! Faltam apenas 5 minutos para o fim do expediente!")
        else:
            st.error("⏰ Seu expediente já terminou!")
    
    except ValueError:
        st.error("⚠️ Formato inválido! Digite no formato HH:MM, ex: 08:30")

# Rodapé com Foto, Assinatura e LinkedIn
st.markdown("---")
col1, col2 = st.columns([1, 3])
with col1:
    st.image("eu.png", width=100)  # Substitua pelo caminho da sua foto
with col2:
    st.markdown("🖊️ **Desenvolvido por Matheus Miranda Lopes**")
    st.markdown("[🔗 Meu LinkedIn](https://www.linkedin.com/in/matheus-miranda-31275b174/)", unsafe_allow_html=True)

   
