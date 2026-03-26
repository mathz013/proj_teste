import streamlit as st
import gspread
from datetime import datetime

# --- CONFIGURAÇÃO DO GOOGLE SHEETS --- #
try:
    gc = gspread.service_account(filename='gm-automacao-84e171073079.json')
    planilha = gc.open("proj_teste").get_worksheet(0)
except Exception as e:
    st.error(f"Erro ao conectar com o Google Sheets: {e}")

# --- INTERFACE VISUAL --- #
st.title("🚀 GM Automação - Controle de Produção")
st.subheader("Registro de Lote Industrial")

with st.form("registro_producao"):
    maquina = st.text_input("Identificação da Máquina")
    operador = st.text_input("Nome do Operador")
    pecas_boas = st.number_input("Peças Boas", min_value=0, step=1)
    defeitos = st.number_input("Defeitos", min_value=0, step=1)
    peso = st.number_input("Peso Total (kg)", min_value=0.0)
    
    # Nova pergunta de Status usando um rádio ou selectbox
    status_maquina = st.radio("A máquina está rodando?", ("Sim", "Não"))
    
    # Converter o Sim/Não para o texto que você quer na planilha
    status_texto = "RODANDO" if status_maquina == "Sim" else "PARADA"

    enviar = st.form_submit_button("Salvar na Planilha")

if enviar:
    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    # 1. VALORES: Agora com 7 itens para bater com as 7 colunas (A até G)
    valores = [data_hora, maquina, operador, pecas_boas, defeitos, peso, status_texto]
    
    # 2. NOMES: Para a sua lógica de índice funcionar em todos os campos
    nomes = ["Data/Hora", "Máquina", "Operador", "Peças Boas", "Defeitos", "Peso", "Status"]

    erro_encontrado = False
    
    # Valida de Máquina (índice 1) até Status (índice 6)
    for i in range(1, len(valores)):
        # Nota: Defeitos e Peso podem ser 0, então cuidado se quiser obrigar valor > 0
        if not valores[i] and nomes[i] not in ["Defeitos", "Peso"]:
            st.error(f"⚠️ O campo '{nomes[i]}' é obrigatório!")
            erro_encontrado = True
            break

    if not erro_encontrado:
        # O value_input_option='USER_ENTERED' garante que números virem números no Sheets
        planilha.append_row(valores, value_input_option='USER_ENTERED')
        st.success(f"✅ Registro de {status_texto} enviado com sucesso!")