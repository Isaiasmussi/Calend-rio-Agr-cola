import streamlit as st
import pandas as pd

# --- Configuração da Página ---
st.set_page_config(
    page_title="Calendário Agrícola 2.0 Beta",
    page_icon="🌱",
    layout="wide"
)

# --- Dados do Calendário ---
# Usando um dicionário para facilitar a manutenção
# Adicionei Milho 1ª e 2ª Safra como culturas separadas para clareza
calendar_data = {
    'Soja': [
        {'Estado': 'Mato Grosso (MT)', 'Plantio': '16/Set - 03/Dez', 'Colheita': 'Janeiro - Março'},
        {'Estado': 'Paraná (PR)', 'Plantio': '11/Set - 30/Dez', 'Colheita': 'Janeiro - Março'},
        {'Estado': 'Rio Grande do Sul (RS)', 'Plantio': '01/Out - 18/Fev', 'Colheita': 'Março - Maio'},
        {'Estado': 'Goiás (GO)', 'Plantio': '25/Set - 02/Jan', 'Colheita': 'Janeiro - Março'},
        {'Estado': 'Mato Grosso do Sul (MS)', 'Plantio': '16/Set - 31/Dez', 'Colheita': 'Janeiro - Março'},
    ],
    'Milho 1ª Safra': [
        {'Estado': 'Mato Grosso (MT)', 'Plantio': 'Agosto - Novembro', 'Colheita': 'Janeiro - Abril'},
        {'Estado': 'Paraná (PR)', 'Plantio': 'Agosto - Dezembro', 'Colheita': 'Janeiro - Abril'},
        {'Estado': 'Goiás (GO)', 'Plantio': 'Setembro - Dezembro', 'Colheita': 'Janeiro - Maio'},
        {'Estado': 'Mato Grosso do Sul (MS)', 'Plantio': 'Agosto - Novembro', 'Colheita': 'Janeiro - Abril'},
        {'Estado': 'Minas Gerais (MG)', 'Plantio': 'Setembro - Dezembro', 'Colheita': 'Fevereiro - Maio'},
    ],
    'Milho 2ª Safra (Safrinha)': [
        {'Estado': 'Mato Grosso (MT)', 'Plantio': 'Janeiro - Março', 'Colheita': 'Junho - Agosto'},
        {'Estado': 'Paraná (PR)', 'Plantio': 'Janeiro - Março', 'Colheita': 'Junho - Agosto'},
        {'Estado': 'Goiás (GO)', 'Plantio': 'Janeiro - Março', 'Colheita': 'Junho - Setembro'},
        {'Estado': 'Mato Grosso do Sul (MS)', 'Plantio': 'Janeiro - Março', 'Colheita': 'Junho - Agosto'},
        {'Estado': 'Minas Gerais (MG)', 'Plantio': 'Janeiro - Março', 'Colheita': 'Julho - Setembro'},
    ],
    'Algodão': [
        {'Estado': 'Mato Grosso (MT)', 'Plantio': 'Dezembro - Janeiro', 'Colheita': 'Junho - Agosto'},
        {'Estado': 'Bahia (BA)', 'Plantio': 'Dezembro - Janeiro', 'Colheita': 'Julho - Setembro'},
        {'Estado': 'Goiás (GO)', 'Plantio': 'Dezembro - Fevereiro', 'Colheita': 'Julho - Setembro'},
        {'Estado': 'Mato Grosso do Sul (MS)', 'Plantio': 'Novembro - Dezembro', 'Colheita': 'Maio - Julho'},
    ]
}

# --- Interface do Usuário (UI) ---
st.title("🗓️ Calendário Agrícola 2.0 (Beta)")
st.markdown("Uma visão interativa sobre as janelas de plantio e colheita no Brasil.")

# --- Filtro na Barra Lateral ---
st.sidebar.header("Filtros")
selected_culture = st.sidebar.selectbox(
    "Selecione a Cultura:",
    options=list(calendar_data.keys())
)

# --- Exibição dos Dados ---
st.header(f"🌱 {selected_culture}")
st.markdown(f"**Principais estados produtores e suas janelas de atividade:**")

# Criar DataFrame com os dados da cultura selecionada
df = pd.DataFrame(calendar_data[selected_culture])

# Exibir a tabela
st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

st.info("Fonte dos dados: Conab e Embrapa. As datas são janelas de referência e podem variar.")
