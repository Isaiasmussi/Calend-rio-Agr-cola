import streamlit as st
import geopandas as gpd

st.set_page_config(layout="wide")
st.title("🕵️‍♂️ Depurador de Dados do Mapa")

try:
    st.info("Tentando carregar os dados do mapa...")
    
    url = "https://raw.githubusercontent.com/fititnt/gis-dataset-brasil/master/uf/geojson/uf.json"
    gdf = gpd.read_file(url, encoding='latin-1')
    
    st.success("Dados carregados com sucesso! Abaixo estão as 5 primeiras linhas da tabela.")
    
    st.markdown("---")
    st.subheader("Nomes Exatos das Colunas:")
    st.write(gdf.columns.tolist())
    
    st.subheader("Visualização da Tabela:")
    st.dataframe(gdf.head())

except Exception as e:
    st.error(f"Ocorreu um erro ao tentar carregar ou exibir os dados: {e}")
