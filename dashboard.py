import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
import json
from streamlit_folium import st_folium

# --- 1. Configuração da Página ---
st.set_page_config(
    page_title="Calendário Agrícola Estratégico",
    page_icon="🗺️",
    layout="wide"
)

# --- 2. Dados do Mapa (Embutidos no Código) ---
# Fonte: https://github.com/tbrugz/geodata-br/blob/master/geojson/geojs-27-mun.json (Adaptado para UFs)
# A estrutura de dados agora é conhecida e garantida. O nome da coluna dos estados é 'nome'.
brazil_states_geojson = {
  "type": "FeatureCollection",
  "features": [
    {"type": "Feature", "id": "AC", "properties": {"nome": "Acre"}, "geometry": None},
    {"type": "Feature", "id": "AL", "properties": {"nome": "Alagoas"}, "geometry": None},
    {"type": "Feature", "id": "AP", "properties": {"nome": "Amapá"}, "geometry": None},
    {"type": "Feature", "id": "AM", "properties": {"nome": "Amazonas"}, "geometry": None},
    {"type": "Feature", "id": "BA", "properties": {"nome": "Bahia"}, "geometry": None},
    {"type": "Feature", "id": "CE", "properties": {"nome": "Ceará"}, "geometry": None},
    {"type": "Feature", "id": "DF", "properties": {"nome": "Distrito Federal"}, "geometry": None},
    {"type": "Feature", "id": "ES", "properties": {"nome": "Espírito Santo"}, "geometry": None},
    {"type": "Feature", "id": "GO", "properties": {"nome": "Goiás"}, "geometry": None},
    {"type": "Feature", "id": "MA", "properties": {"nome": "Maranhão"}, "geometry": None},
    {"type": "Feature", "id": "MT", "properties": {"nome": "Mato Grosso"}, "geometry": None},
    {"type": "Feature", "id": "MS", "properties": {"nome": "Mato Grosso do Sul"}, "geometry": None},
    {"type": "Feature", "id": "MG", "properties": {"nome": "Minas Gerais"}, "geometry": None},
    {"type": "Feature", "id": "PA", "properties": {"nome": "Pará"}, "geometry": None},
    {"type": "Feature", "id": "PB", "properties": {"nome": "Paraíba"}, "geometry": None},
    {"type": "Feature", "id": "PR", "properties": {"nome": "Paraná"}, "geometry": None},
    {"type": "Feature", "id": "PE", "properties": {"nome": "Pernambuco"}, "geometry": None},
    {"type": "Feature", "id": "PI", "properties": {"nome": "Piauí"}, "geometry": None},
    {"type": "Feature", "id": "RJ", "properties": {"nome": "Rio de Janeiro"}, "geometry": None},
    {"type": "Feature", "id": "RN", "properties": {"nome": "Rio Grande do Norte"}, "geometry": None},
    {"type": "Feature", "id": "RS", "properties": {"nome": "Rio Grande do Sul"}, "geometry": None},
    {"type": "Feature", "id": "RO", "properties": {"nome": "Rondônia"}, "geometry": None},
    {"type": "Feature", "id": "RR", "properties": {"nome": "Roraima"}, "geometry": None},
    {"type": "Feature", "id": "SC", "properties": {"nome": "Santa Catarina"}, "geometry": None},
    {"type": "Feature", "id": "SP", "properties": {"nome": "São Paulo"}, "geometry": None},
    {"type": "Feature", "id": "SE", "properties": {"nome": "Sergipe"}, "geometry": None},
    {"type": "Feature", "id": "TO", "properties": {"nome": "Tocantins"}, "geometry": None}
  ]
}
# As geometrias foram omitidas aqui para simplificar, mas o Folium fará a busca pelo ID
# Carregamos o GeoDataFrame a partir do nosso objeto JSON interno
gdf_states = gpd.GeoDataFrame.from_features(brazil_states_geojson["features"])


# --- 3. Dados Estratégicos (do seu Documento) ---
management_data = {
    'Soja': {
        'states': ['Mato Grosso', 'Paraná', 'Rio Grande do Sul', 'Goiás', 'Mato Grosso do Sul'],
        'timeline': {
            'Preparo do solo e Adubação': ['Agosto', 'Setembro', 'Outubro'],
            'Aquisição e Tratamento de Sementes': ['Agosto', 'Setembro', 'Outubro'],
            'Controle de Ervas Daninhas (Pós-emergência)': ['Outubro', 'Novembro', 'Dezembro'],
        },
        'details': """
        - **Pragas em Foco:** Lagarta da Soja, Elasmo, Falsa Medideira, Mosca Branca.
        - **Doenças Principais:** Mofo Branco, Antracnose, Ferrugem Asiática.
        """
    },
    'Milho Safra': {
        'states': ['Mato Grosso', 'Paraná', 'Goiás', 'Mato Grosso do Sul', 'Minas Gerais'],
        'timeline': {
            'Aquisição de Financiamento/Custeio': ['Agosto', 'Setembro'],
            'Preparo de Solo e Herbicidas': ['Setembro', 'Outubro', 'Novembro'],
            'Adubação de Cobertura (Nitrogenada)': ['Novembro', 'Dezembro', 'Janeiro'],
        },
        'details': """
        - **Pragas em Foco:** Cigarrinha, lagarta do cartucho, percevejo barriga verde.
        - **Doenças:** Ocorrência geralmente mais tardia.
        """
    },
    'Algodão': {
        'states': ['Mato Grosso', 'Bahia', 'Goiás', 'Mato Grosso do Sul'],
        'timeline': {
            'Financiamento e Preparo do Solo': ['Outubro', 'Novembro', 'Dezembro'],
            'Plantio e Adubação de Plantio': ['Dezembro', 'Janeiro'],
            'Controle de Pragas': ['Dezembro', 'Janeiro'],
        },
        'details': """
        - **Pragas em Foco:** Bicudo, ácaros, pulgões, curuquerê, lagarta rosada, Helicoverpa.
        - **Estratégia de Plantio:** Comum em sucessão a uma soja super precoce.
        """
    }
}


# --- 4. Funções de Geração do Dashboard ---
def create_choropleth_map(relevant_states):
    """Cria um mapa Folium destacando os estados relevantes. Esta versão usa um Choropleth que é mais robusto."""
    
    # Criamos um dataframe simples para o mapa: Estado | Status
    map_df = pd.DataFrame(brazil_states_geojson['features'])
    map_df['nome'] = map_df['properties'].apply(lambda x: x['nome'])
    map_df['status'] = map_df['nome'].apply(lambda x: 1 if x in relevant_states else 0)
    map_df['id'] = map_df['nome'] # Chave para o join

    # URL de um GeoJSON público e de alta performance para as fronteiras
    geojson_url = "https://raw.githubusercontent.com/luizpedone/municipal-brazilian-geodata/master/data/UF.json"

    m = folium.Map(location=[-15.788497, -47.879873], zoom_start=4, tiles='CartoDB dark_matter')

    folium.Choropleth(
        geo_data=geojson_url,
        data=map_df,
        columns=['id', 'status'],
        key_on='feature.properties.NM_UF', # O nome da propriedade de estado neste arquivo é 'NM_UF'
        fill_color='YlGn', # Esquema de cores Verde
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Status',
        highlight=True
    ).add_to(m)

    return m

def create_timeline_df(timeline_data, months):
    """Cria um DataFrame visual para o cronograma de atividades."""
    df = pd.DataFrame(index=timeline_data.keys(), columns=months)
    df.index.name = "Atividade / Mês"
    for activity, active_months in timeline_data.items():
        for month in active_months:
            if month in df.columns:
                df.loc[activity, month] = '✅'
    return df.fillna('')


# --- 5. Interface Principal ---
st.title("🗺️ Calendário Agrícola Estratégico")

months_of_interest = ['Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro', 'Janeiro']
tab_soja, tab_milho, tab_algodao = st.tabs(["🌱 Soja", "🌽 Milho Safra", "⚪ Algodão"])

for tab, culture_name in zip([tab_soja, tab_milho, tab_algodao], ['Soja', 'Milho Safra', 'Algodão']):
    with tab:
        culture_data = management_data[culture_name]
        st.header(f"{tab.label}: Mapa e Cronograma")

        map_col, timeline_col = st.columns([1, 2])

        with map_col:
            st.subheader("Principais Estados Produtores")
            folium_map = create_choropleth_map(culture_data['states'])
            st_folium(folium_map, use_container_width=True, height=400)

        with timeline_col:
            st.subheader("Cronograma de Atividades")
            timeline_df = create_timeline_df(culture_data['timeline'], months_of_interest)
            st.dataframe(timeline_df, use_container_width=True)
            with st.expander("**Pontos de Atenção**"):
                st.markdown(culture_data['details'])
