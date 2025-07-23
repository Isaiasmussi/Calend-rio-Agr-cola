import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import st_folium

# --- 1. Configuração da Página e Tema ---
st.set_page_config(
    page_title="Calendário Agrícola Estratégico",
    page_icon="🗺️",
    layout="wide"
)

# --- 2. Extração e Estrutura dos Dados do Documento ---
# Dados extraídos e estruturados a partir do arquivo ANÁLISE DAS PRINCIPAIS CULTURAS DE VERÃO.docx
# [cite_start]O período de análise considerado é de Agosto/25 a Janeiro/26 [cite: 6]
management_data = {
    'Soja': {
        'states': ['Mato Grosso', 'Paraná', 'Rio Grande do Sul', 'Goiás', 'Mato Grosso do Sul'],
        'timeline': {
            # [cite_start]Assuntos recorrentes de Agosto a Outubro/25 [cite: 9]
            'Preparo do solo e Adubação': ['Agosto', 'Setembro', 'Outubro'],
            'Aquisição e Tratamento de Sementes': ['Agosto', 'Setembro', 'Outubro'],
            'Herbicidas (Dessecantes e Pré-plantio)': ['Agosto', 'Setembro', 'Outubro'],
            # [cite_start]Controle de ervas em pós emergência de Outubro a Dezembro [cite: 10]
            'Controle de Ervas Daninhas (Pós-emergência)': ['Outubro', 'Novembro', 'Dezembro'],
            # [cite_start]Controle de pragas na fase inicial [cite: 11]
            'Controle de Pragas Iniciais': ['Outubro', 'Novembro', 'Dezembro'],
            # [cite_start]Controle de doenças no final do ciclo [cite: 13]
            'Controle de Doenças': ['Dezembro', 'Janeiro']
        },
        'details': """
        - [cite_start]**Pragas em Foco:** Lagarta da Soja, Lagarta do Cartucho, Elasmo e Falsa Medideira[cite: 12]. [cite_start]Atenção também para a Mosca Branca[cite: 11].
        - [cite_start]**Doenças Principais:** Mofo Branco, Antracnose e Ferrugem Asiática, que exigem monitoramento constante pois os danos são severos[cite: 13].
        """
    },
    'Milho Safra': {
        'states': ['Mato Grosso', 'Paraná', 'Goiás', 'Mato Grosso do Sul', 'Minas Gerais'],
        'timeline': {
            [cite_start]'Aquisição de Financiamento/Custeio': ['Agosto', 'Setembro'], # [cite: 15]
            [cite_start]'Preparo de Solo e Herbicidas': ['Setembro', 'Outubro', 'Novembro'], # [cite: 16]
            [cite_start]'Plantio (Sementes e Adubos)': ['Outubro', 'Novembro'], # [cite: 16]
            [cite_start]'Adubação de Cobertura (Nitrogenada)': ['Novembro', 'Dezembro', 'Janeiro'], # [cite: 17]
            [cite_start]'Controle de Pragas': ['Outubro', 'Novembro', 'Dezembro', 'Janeiro'] # [cite: 18]
        },
        'details': """
        - [cite_start]**Pragas em Foco:** Corós, lagarta rosca, lagarta elasmo, larva alfinete (iniciais). Na fase de desenvolvimento, atenção especial à **Cigarrinha**, além da lagarta do cartucho e percevejo barriga verde[cite: 18].
        - [cite_start]**Doenças:** Ocorrência geralmente mais tardia, com exceção de nematóides[cite: 19].
        - [cite_start]**Particularidade:** A adubação nitrogenada em cobertura é uma etapa chave que se estende por um período mais longo[cite: 17].
        """
    },
    'Algodão': {
        'states': ['Mato Grosso', 'Bahia', 'Goiás', 'Mato Grosso do Sul'],
        'timeline': {
            # [cite_start]Dinâmica semelhante ao milho [cite: 25]
            'Financiamento e Preparo do Solo': ['Outubro', 'Novembro', 'Dezembro'],
            'Plantio e Adubação de Plantio': ['Dezembro', 'Janeiro'],
            'Adubação de Cobertura': ['Janeiro'],
            # [cite_start]Grande preocupação desde o plantio [cite: 26]
            'Controle de Pragas': ['Dezembro', 'Janeiro'],
            # [cite_start]Preocupação maior a partir de Janeiro [cite: 27]
            'Controle de Doenças': ['Janeiro']
        },
        'details': """
        - [cite_start]**Pragas em Foco (Atenção Máxima):** A cultura exige controle intenso desde o início, com foco em Bicudo, ácaros, pulgões, curuquerê, lagarta rosada, lagarta das maçãs, Helicoverpa e percevejos[cite: 26].
        - [cite_start]**Estratégia de Plantio:** É comum em regiões do MT e BA o plantio do algodão em sucessão a uma soja super precoce[cite: 22, 23].
        - [cite_start]**Comportamento:** O ciclo é semelhante ao milho, porém mais tardio[cite: 21].
        """
    }
}

# --- 3. Carregamento dos Dados Geográficos ---
@st.cache_data
def load_geodata():
    # URL para um arquivo GeoJSON de alta qualidade dos estados do Brasil
    url = "https://raw.githubusercontent.com/fititnt/gis-dataset-brasil/master/uf/geojson/uf.json"
    return gpd.read_file(url)

gdf_states = load_geodata()


# --- 4. Funções de Geração do Dashboard ---
def create_choropleth_map(relevant_states):
    """Cria um mapa Folium destacando os estados relevantes."""
    m = folium.Map(location=[-15.788497, -47.879873], zoom_start=4, tiles='CartoDB dark_matter')

    # Filtrar o GeoDataFrame para incluir apenas os estados relevantes
    gdf_filtered = gdf_states[gdf_states['NOME'].isin(relevant_states)]

    # Adicionar os estados relevantes com destaque
    folium.GeoJson(
        gdf_filtered,
        style_function=lambda feature: {
            'fillColor': '#2E8B57', # Cor primária do tema
            'color': '#FFFFFF',
            'weight': 1,
            'fillOpacity': 0.7,
        },
        tooltip=folium.GeoJsonTooltip(fields=['NOME'], aliases=['Estado:'])
    ).add_to(m)

    return m

def create_timeline_df(timeline_data, months):
    """Cria um DataFrame visual para o cronograma de atividades."""
    df = pd.DataFrame(index=timeline_data.keys(), columns=months)
    for activity, active_months in timeline_data.items():
        for month in active_months:
            if month in df.columns:
                df.loc[activity, month] = '✅'
    return df.fillna('')


# --- 5. Interface Principal com Abas ---
st.title("🗺️ Calendário Agrícola Estratégico")
st.markdown("""
[cite_start]Análise das atividades de campo para as principais culturas de verão, focada no período de **Agosto/25 a Janeiro/26**[cite: 6].
[cite_start]O objetivo é alinhar a comunicação e campanhas publicitárias do Portal Agrolink com os acontecimentos do campo[cite: 3, 4, 5].
""")

# Meses para o nosso cronograma
months_of_interest = ['Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro', 'Janeiro']

# Criação do menu superior com abas
tab_soja, tab_milho, tab_algodao = st.tabs(["🌱 Soja", "🌽 Milho Safra", "⚪ Algodão"])

# --- Aba de Soja ---
with tab_soja:
    culture_data = management_data['Soja']
    st.header("Soja: Mapa e Cronograma de Atividades")

    map_col, timeline_col = st.columns([1, 2])

    with map_col:
        st.subheader("Principais Estados Produtores")
        folium_map = create_choropleth_map(culture_data['states'])
        st_folium(folium_map, use_container_width=True, height=400)

    with timeline_col:
        st.subheader("Cronograma de Atividades no Campo")
        timeline_df = create_timeline_df(culture_data['timeline'], months_of_interest)
        st.dataframe(timeline_df, use_container_width=True)
        with st.expander("Ver Detalhes e Pontos de Atenção"):
            st.markdown(culture_data['details'])


# --- Aba de Milho Safra ---
with tab_milho:
    culture_data = management_data['Milho Safra']
    st.header("Milho Safra: Mapa e Cronograma de Atividades")

    map_col, timeline_col = st.columns([1, 2])

    with map_col:
        st.subheader("Principais Estados Produtores")
        folium_map = create_choropleth_map(culture_data['states'])
        st_folium(folium_map, use_container_width=True, height=400)

    with timeline_col:
        st.subheader("Cronograma de Atividades no Campo")
        timeline_df = create_timeline_df(culture_data['timeline'], months_of_interest)
        st.dataframe(timeline_df, use_container_width=True)
        with st.expander("Ver Detalhes e Pontos de Atenção"):
            st.markdown(culture_data['details'])


# --- Aba de Algodão ---
with tab_algodao:
    culture_data = management_data['Algodão']
    st.header("Algodão: Mapa e Cronograma de Atividades")

    map_col, timeline_col = st.columns([1, 2])

    with map_col:
        st.subheader("Principais Estados Produtores")
        folium_map = create_choropleth_map(culture_data['states'])
        st_folium(folium_map, use_container_width=True, height=400)

    with timeline_col:
        st.subheader("Cronograma de Atividades no Campo")
        timeline_df = create_timeline_df(culture_data['timeline'], months_of_interest)
        st.dataframe(timeline_df, use_container_width=True)
        with st.expander("Ver Detalhes e Pontos de Atenção"):
            st.markdown(culture_data['details'])
