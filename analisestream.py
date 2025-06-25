import streamlit as st
import urllib.request
import numpy as np
import cv2

# Configura layout largo
st.set_page_config(page_title="Monitoramento com Câmera", layout="wide")

# Oculta menu e rodapé para visual mais limpo
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# URL da câmera do celular (IP da câmera)
CAMERA_URL = "http://192.168.0.100:8080/shot.jpg"  # ajuste se necessário

# Dados simulados dos sensores
sensores = [
    {"nome": "Sensor 1", "pressao": 145, "outlier": True},
    {"nome": "Sensor 2", "pressao": 110, "outlier": False},
    {"nome": "Sensor 3", "pressao": 130, "outlier": True},
]

st.title("🩺 Painel de Sensores e Câmera IP")

# Variável de controle
camera_ativa = False

# Mostra sensores na parte de cima
for sensor in sensores:
    col1, col2, col3, col4 = st.columns([1.5, 2, 2, 2])

    with col1:
        st.markdown(f"**{sensor['nome']}**")

    with col2:
        st.markdown(f"**Pressão:** {sensor['pressao']} mmHg")

    with col3:
        st.markdown(f"**Outlier:** {'🔴 Sim' if sensor['outlier'] else '🟢 Não'}**")

    with col4:
        if st.button(f"Ver Câmera {sensor['nome']}", key=sensor['nome']):
            camera_ativa = True

    st.markdown("---")

# Parte inferior: imagem grande da câmera
if camera_ativa:
    st.subheader("📷 Imagem da Câmera IP")
    try:
        img_resp = urllib.request.urlopen(CAMERA_URL, timeout=5)
        img_np = np.array(bytearray(img_resp.read()), dtype=np.uint8)
        frame = cv2.imdecode(img_np, -1)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        st.image(frame, caption="Imagem capturada da câmera", use_container_width=True)
    except Exception as e:
        st.error(f"❌ Erro ao capturar imagem: {e}")
