import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
import json
from streamlit_folium import st_folium

# --- 1. Configuração da Página ---
st.set_page_config(
    page_title="Calendário Agrícola Estratégico",
    layout="wide"
)

# --- 2. DADOS COMPLETOS DO MAPA (EMBUTIDOS DIRETAMENTE NO CÓDIGO) ---
GEOJSON_DATA = """
{
"type": "FeatureCollection",
"features": [
{"type": "Feature", "properties": {"name": "Acre"}, "geometry": {"type": "Polygon", "coordinates": [[[-73.792, -7.072], [-73.654, -7.536], [-73.498, -7.83], [-73.18, -7.33], [-72.585, -7.422], [-72.432, -7.994], [-71.09, -7.341], [-71.127, -8.349], [-70.528, -8.781], [-70.64, -11.05], [-71.07, -10.95], [-73.66, -10.02], [-73.792, -7.072]]]}},
{"type": "Feature", "properties": {"name": "Alagoas"}, "geometry": {"type": "Polygon", "coordinates": [[[-35.46, -8.82], [-35.1, -9.69], [-35.8, -9.8], [-36.2, -9.62], [-36.03, -9.23], [-36.63, -9.3], [-37.2, -9.22], [-37.3, -9.49], [-38.2, -9.73], [-37.8, -10.49], [-37.25, -10.3], [-36.39, -10.27], [-35.98, -9.95], [-35.46, -8.82]]]}},
{"type": "Feature", "properties": {"name": "Amapá"}, "geometry": {"type": "Polygon", "coordinates": [[[-51.85, 4.38], [-50.35, 3.44], [-50.93, 2.22], [-50.3, 1.44], [-50.9, 0.58], [-50.2, 0.08], [-51.1, -0.16], [-52.3, -0.3], [-53.1, -0.1], [-54.7, 0.92], [-51.6, 2.05], [-51.85, 4.38]]]}},
{"type": "Feature", "properties": {"name": "Amazonas"}, "geometry": {"type": "Polygon", "coordinates": [[[-68.8, 2.2], [-67.3, 2.2], [-67.1, 4.2], [-66.1, 4.2], [-65.5, 3.1], [-65.3, 2.4], [-64.5, 2.1], [-63.6, 2.6], [-62.8, 2.5], [-62.2, 3.2], [-60.6, 2.8], [-59.9, 1.9], [-59.6, 2.2], [-58.5, 1.5], [-58.4, 0.7], [-59.1, 0.2], [-59.1, -0.4], [-58.2, -1.1], [-58.6, -1.9], [-57.6, -2.4], [-56.9, -2.8], [-57.1, -3.2], [-56.5, -4.3], [-58.3, -4.3], [-59.6, -5.2], [-60.3, -4.7], [-60.4, -6.1], [-61.2, -6.1], [-61.3, -6.9], [-62.1, -7.3], [-62.8, -7.1], [-63.2, -7.5], [-63.2, -8.0], [-64.2, -8.7], [-65.3, -8.5], [-65.8, -9.1], [-66.8, -9.1], [-67.0, -8.8], [-68.0, -9.7], [-68.8, -9.4], [-69.6, -10.0], [-70.0, -9.4], [-69.6, -8.6], [-69.9, -8.4], [-70.6, -7.5], [-71.2, -7.8], [-71.8, -7.4], [-71.3, -6.4], [-71.6, -6.2], [-71.1, -5.3], [-71.8, -5.0], [-72.1, -4.4], [-72.9, -4.6], [-73.5, -4.3], [-73.2, -3.0], [-73.6, -2.7], [-73.8, -1.9], [-73.1, -1.2], [-72.6, -0.1], [-71.7, 0.3], [-70.8, -0.2], [-69.9, -0.8], [-70.0, -1.5], [-69.3, -2.1], [-69.8, -2.8], [-69.2, -4.1], [-68.6, -4.2], [-67.9, -3.2], [-67.5, -2.0], [-68.0, -1.1], [-68.8, -0.2], [-68.9, 0.5], [-69.8, 1.2], [-69.3, 2.0], [-68.8, 2.2]]]}},
{"type": "Feature", "properties": {"name": "Bahia"}, "geometry": {"type": "Polygon", "coordinates": [[[-38.6, -8.5], [-37.8, -9.7], [-38.2, -9.7], [-37.3, -9.5], [-37.2, -9.2], [-36.6, -9.3], [-36.0, -9.2], [-35.8, -9.6], [-35.1, -9.7], [-35.5, -10.4], [-35.7, -11.0], [-36.0, -11.3], [-36.4, -12.3], [-37.4, -13.0], [-38.3, -13.0], [-38.5, -13.9], [-38.8, -14.8], [-38.7, -15.6], [-39.1, -16.2], [-39.1, -17.0], [-39.5, -17.4], [-39.2, -18.0], [-40.0, -17.8], [-40.3, -17.1], [-41.1, -17.2], [-41.5, -16.4], [-41.1, -16.0], [-41.5, -15.4], [-41.8, -14.9], [-42.4, -14.9], [-42.8, -14.3], [-42.3, -13.6], [-42.7, -13.2], [-42.2, -12.6], [-42.9, -12.4], [-43.0, -12.0], [-44.0, -12.1], [-44.3, -11.6], [-44.9, -11.9], [-45.7, -11.5], [-46.3, -10.9], [-45.9, -10.2], [-44.8, -9.9], [-44.2, -9.2], [-43.4, -9.3], [-42.7, -8.7], [-41.8, -8.6], [-40.9, -8.9], [-40.1, -8.8], [-39.4, -8.6], [-38.6, -8.5]]]}},
{"type": "Feature", "properties": {"name": "Ceará"}, "geometry": {"type": "Polygon", "coordinates": [[[-38.6, -2.8], [-37.2, -3.8], [-37.4, -4.5], [-37.2, -5.2], [-37.7, -5.7], [-37.8, -6.3], [-38.5, -7.0], [-39.0, -7.2], [-39.2, -6.8], [-39.8, -6.8], [-40.4, -7.2], [-41.1, -6.6], [-41.2, -5.4], [-40.7, -5.0], [-40.9, -4.2], [-40.3, -3.5], [-40.0, -2.8], [-39.2, -2.6], [-38.6, -2.8]]]}},
{"type": "Feature", "properties": {"name": "Distrito Federal"}, "geometry": {"type": "Polygon", "coordinates": [[[-47.5, -15.5], [-47.4, -15.7], [-47.6, -16.0], [-48.0, -16.0], [-48.3, -15.8], [-48.0, -15.5], [-47.5, -15.5]]]}},
{"type": "Feature", "properties": {"name": "Espírito Santo"}, "geometry": {"type": "Polygon", "coordinates": [[[-40.0, -17.8], [-39.2, -18.0], [-39.5, -17.4], [-39.1, -17.0], [-39.1, -16.2], [-38.7, -15.6], [-38.8, -14.8], [-38.3, -13.0], [-39.7, -18.3], [-40.7, -18.3], [-41.2, -18.9], [-41.8, -19.6], [-41.3, -20.4], [-41.8, -20.6], [-41.2, -21.2], [-40.9, -21.2], [-40.9, -20.8], [-40.6, -20.8], [-40.0, -20.4], [-40.0, -19.7], [-39.7, -19.2], [-40.0, -17.8]]]}},
{"type": "Feature", "properties": {"name": "Goiás"}, "geometry": {"type": "Polygon", "coordinates": [[[-48.3, -12.5], [-47.8, -12.8], [-47.1, -12.8], [-46.4, -13.4], [-46.4, -14.2], [-47.2, -14.8], [-47.2, -15.3], [-47.6, -16.0], [-47.4, -15.7], [-47.5, -15.5], [-48.0, -15.5], [-48.3, -15.8], [-48.0, -16.0], [-48.8, -16.5], [-49.3, -16.2], [-49.6, -16.8], [-49.2, -17.3], [-49.8, -17.5], [-49.8, -18.2], [-50.3, -19.1], [-50.0, -19.5], [-51.0, -18.8], [-51.8, -19.1], [-52.6, -18.5], [-53.1, -17.6], [-52.4, -16.9], [-53.0, -16.4], [-52.4, -15.9], [-51.3, -16.4], [-51.2, -15.8], [-51.8, -15.2], [-51.2, -14.4], [-50.7, -14.5], [-50.8, -13.8], [-50.2, -13.2], [-49.5, -13.5], [-49.0, -12.8], [-48.3, -12.5]]]}},
{"type": "Feature", "properties": {"name": "Maranhão"}, "geometry": {"type": "Polygon", "coordinates": [[[-43.0, -1.0], [-42.4, -2.1], [-41.8, -3.1], [-41.8, -3.9], [-41.3, -4.6], [-40.9, -4.2], [-40.7, -5.0], [-41.2, -5.4], [-41.1, -6.6], [-40.4, -7.2], [-39.8, -6.8], [-39.2, -6.8], [-39.0, -7.2], [-39.1, -7.6], [-40.0, -8.3], [-41.2, -8.3], [-42.0, -8.0], [-42.7, -8.7], [-43.4, -9.3], [-44.2, -9.2], [-44.8, -9.9], [-45.9, -10.2], [-46.3, -10.9], [-46.8, -9.8], [-47.1, -9.1], [-47.3, -8.3], [-47.0, -7.5], [-47.5, -6.8], [-47.3, -6.1], [-47.8, -5.4], [-48.5, -4.8], [-48.2, -3.9], [-47.7, -3.4], [-47.2, -2.8], [-46.4, -2.7], [-45.7, -2.5], [-45.0, -2.9], [-44.4, -2.7], [-44.1, -1.8], [-43.5, -1.5], [-43.0, -1.0]]]}},
{"type": "Feature", "properties": {"name": "Mato Grosso"}, "geometry": {"type": "Polygon", "coordinates": [[[-58.2, -7.2], [-56.5, -8.0], [-55.3, -7.7], [-54.6, -8.4], [-53.8, -8.4], [-53.2, -9.1], [-51.8, -9.9], [-51.2, -10.9], [-50.6, -11.5], [-50.8, -12.3], [-50.2, -13.2], [-50.8, -13.8], [-50.7, -14.5], [-51.2, -14.4], [-51.8, -15.2], [-51.2, -15.8], [-51.3, -16.4], [-52.4, -15.9], [-53.0, -16.4], [-52.4, -16.9], [-53.1, -17.6], [-52.6, -18.5], [-53.4, -18.4], [-54.2, -17.4], [-54.8, -17.4], [-55.6, -17.0], [-56.3, -17.5], [-57.0, -16.8], [-57.4, -16.2], [-57.9, -16.4], [-58.4, -15.2], [-58.1, -14.5], [-58.9, -14.3], [-59.4, -14.9], [-60.2, -14.3], [-60.1, -13.7], [-61.0, -13.2], [-60.8, -12.2], [-61.5, -11.5], [-61.3, -10.6], [-60.7, -9.9], [-60.2, -9.3], [-59.3, -9.1], [-58.6, -8.3], [-58.2, -7.2]]]}},
{"type": "Feature", "properties": {"name": "Mato Grosso do Sul"}, "geometry": {"type": "Polygon", "coordinates": [[[-53.4, -18.4], [-52.6, -18.5], [-51.8, -19.1], [-51.0, -18.8], [-51.7, -20.0], [-51.2, -21.0], [-52.1, -21.5], [-52.1, -22.4], [-52.8, -22.3], [-53.5, -22.9], [-54.0, -22.5], [-54.6, -22.8], [-55.3, -22.3], [-56.0, -22.6], [-56.5, -22.2], [-57.2, -22.3], [-57.8, -21.9], [-57.6, -21.2], [-58.1, -20.2], [-57.4, -19.7], [-56.8, -19.9], [-56.1, -19.4], [-55.7, -19.7], [-55.6, -19.1], [-54.8, -18.8], [-54.8, -17.4], [-54.2, -17.4], [-53.4, -18.4]]]}},
{"type": "Feature", "properties": {"name": "Minas Gerais"}, "geometry": {"type": "Polygon", "coordinates": [[[-44.2, -14.3], [-43.0, -14.9], [-42.8, -14.3], [-42.4, -14.9], [-41.8, -14.9], [-41.5, -15.4], [-41.1, -16.0], [-41.5, -16.4], [-41.1, -17.2], [-40.3, -17.1], [-40.0, -17.8], [-39.7, -19.2], [-40.0, -19.7], [-40.0, -20.4], [-40.6, -20.8], [-40.9, -20.8], [-40.9, -21.2], [-41.2, -21.2], [-41.8, -20.6], [-41.3, -20.4], [-41.8, -19.6], [-42.3, -20.2], [-42.6, -20.8], [-42.2, -21.5], [-42.9, -21.8], [-43.4, -21.5], [-43.8, -22.1], [-44.5, -21.8], [-44.8, -22.6], [-45.1, -22.2], [-45.6, -22.8], [-46.2, -22.3], [-46.7, -21.7], [-46.4, -21.2], [-47.3, -20.5], [-47.3, -20.0], [-47.9, -20.1], [-48.3, -19.6], [-49.0, -20.0], [-50.0, -19.5], [-50.3, -19.1], [-49.8, -18.2], [-49.8, -17.5], [-49.2, -17.3], [-49.6, -16.8], [-49.3, -16.2], [-48.8, -16.5], [-48.0, -16.0], [-47.2, -15.3], [-47.2, -14.8], [-46.4, -14.2], [-45.1, -14.5], [-44.2, -14.3]]]}},
{"type": "Feature", "properties": {"name": "Pará"}, "geometry": {"type": "Polygon", "coordinates": [[[-54.7, 0.9], [-53.1, -0.1], [-52.3, -0.3], [-51.1, -0.2], [-50.2, 0.1], [-49.5, 0.0], [-48.7, -0.1], [-48.1, -0.8], [-47.5, -0.6], [-46.9, -1.0], [-46.0, -1.0], [-45.4, -1.4], [-45.6, -2.1], [-45.0, -2.9], [-45.7, -2.5], [-46.4, -2.7], [-47.2, -2.8], [-47.7, -3.4], [-48.2, -3.9], [-48.5, -4.8], [-47.8, -5.4], [-47.3, -6.1], [-47.5, -6.8], [-47.0, -7.5], [-47.3, -8.3], [-47.1, -9.1], [-46.8, -9.8], [-48.0, -9.5], [-48.8, -8.6], [-49.2, -9.2], [-49.8, -8.8], [-50.6, -8.2], [-51.0, -8.1], [-51.4, -7.2], [-51.1, -6.5], [-51.8, -5.9], [-52.3, -5.3], [-52.3, -4.6], [-53.1, -4.6], [-53.4, -5.4], [-54.0, -5.3], [-54.4, -6.1], [-55.0, -5.8], [-55.3, -6.5], [-55.0, -7.5], [-55.3, -7.7], [-56.5, -8.0], [-58.2, -7.2], [-58.6, -8.3], [-59.3, -9.1], [-58.8, -6.3], [-58.0, -5.5], [-57.3, -4.8], [-57.0, -4.0], [-56.5, -4.3], [-57.1, -3.2], [-56.9, -2.8], [-57.6, -2.4], [-58.6, -1.9], [-58.2, -1.1], [-59.1, -0.4], [-59.1, 0.2], [-58.4, 0.7], [-58.5, 1.5], [-57.8, 1.7], [-56.5, 1.7], [-55.9, 2.0], [-55.3, 1.1], [-54.8, 1.5], [-54.7, 0.9]]]}},
{"type": "Feature", "properties": {"name": "Paraíba"}, "geometry": {"type": "Polygon", "coordinates": [[[-37.2, -6.0], [-36.9, -6.6], [-36.5, -6.6], [-36.2, -7.0], [-35.5, -7.0], [-35.0, -6.8], [-34.8, -7.2], [-35.2, -7.4], [-34.9, -7.9], [-35.3, -8.2], [-36.0, -8.4], [-36.7, -8.3], [-37.2, -8.4], [-38.0, -8.1], [-38.2, -7.6], [-38.8, -7.5], [-38.5, -7.0], [-37.8, -6.3], [-37.7, -5.7], [-37.2, -6.0]]]}},
{"type": "Feature", "properties": {"name": "Paraná"}, "geometry": {"type": "Polygon", "coordinates": [[[-51.7, -22.5], [-51.2, -22.9], [-50.3, -22.8], [-49.5, -23.3], [-48.8, -22.8], [-48.3, -23.2], [-48.1, -23.9], [-48.3, -24.4], [-48.1, -25.2], [-48.6, -25.5], [-48.3, -25.9], [-49.0, -25.8], [-49.5, -26.3], [-49.9, -26.0], [-50.3, -26.4], [-50.9, -25.8], [-51.5, -26.2], [-52.0, -25.7], [-52.4, -26.0], [-52.9, -25.5], [-53.6, -25.8], [-54.1, -25.5], [-54.5, -25.8], [-54.3, -25.2], [-54.0, -25.0], [-53.3, -24.8], [-52.9, -24.4], [-52.1, -24.4], [-51.7, -23.8], [-52.1, -23.4], [-52.8, -23.6], [-53.5, -22.9], [-54.0, -22.5], [-53.5, -22.9], [-52.8, -22.3], [-52.1, -22.4], [-51.7, -22.5]]]}},
{"type": "Feature", "properties": {"name": "Pernambuco"}, "geometry": {"type": "Polygon", "coordinates": [[[-35.4, -7.3], [-34.9, -7.9], [-35.2, -7.4], [-34.8, -7.2], [-35.0, -6.8], [-35.5, -7.0], [-36.2, -7.0], [-36.5, -6.6], [-36.9, -6.6], [-37.2, -6.0], [-38.3, -7.1], [-39.0, -7.5], [-39.6, -7.4], [-40.3, -8.1], [-40.0, -8.3], [-39.1, -7.6], [-39.0, -7.2], [-38.5, -7.0], [-37.8, -6.3], [-38.8, -7.5], [-38.2, -7.6], [-38.0, -8.1], [-37.2, -8.4], [-36.7, -8.3], [-36.0, -8.4], [-35.3, -8.2], [-35.4, -7.3]]]}},
{"type": "Feature", "properties": {"name": "Piauí"}, "geometry": {"type": "Polygon", "coordinates": [[[-41.8, -2.8], [-41.3, -3.4], [-40.9, -4.2], [-41.3, -4.6], [-41.8, -3.9], [-41.8, -3.1], [-42.4, -2.1], [-43.0, -2.8], [-43.8, -3.5], [-44.4, -4.2], [-45.1, -4.5], [-45.5, -5.4], [-45.1, -6.3], [-45.5, -7.2], [-45.0, -8.1], [-44.6, -8.9], [-43.9, -9.6], [-42.7, -10.0], [-42.0, -10.5], [-41.2, -10.2], [-40.6, -9.5], [-40.0, -8.8], [-40.1, -8.3], [-41.2, -8.3], [-42.0, -8.0], [-42.7, -8.7], [-41.8, -8.6], [-40.9, -8.9], [-40.6, -9.5], [-41.2, -8.3], [-40.4, -7.2], [-41.1, -6.6], [-41.2, -5.4], [-40.7, -5.0], [-41.3, -4.6], [-40.9, -4.2], [-41.8, -2.8]]]}},
{"type": "Feature", "properties": {"name": "Rio de Janeiro"}, "geometry": {"type": "Polygon", "coordinates": [[[-42.2, -21.5], [-42.6, -20.8], [-42.3, -20.2], [-41.8, -19.6], [-41.0, -21.0], [-40.9, -21.2], [-41.2, -21.2], [-41.8, -20.6], [-41.3, -20.4], [-42.0, -21.8], [-42.5, -22.2], [-42.0, -22.8], [-42.5, -23.0], [-43.1, -22.8], [-43.7, -23.2], [-44.3, -22.8], [-44.7, -23.0], [-44.5, -22.5], [-44.8, -22.6], [-44.5, -21.8], [-43.8, -22.1], [-43.4, -21.5], [-42.9, -21.8], [-42.2, -21.5]]]}},
{"type": "Feature", "properties": {"name": "Rio Grande do Norte"}, "geometry": {"type": "Polygon", "coordinates": [[[-36.2, -4.8], [-35.2, -5.2], [-35.0, -6.0], [-35.5, -6.4], [-36.2, -6.5], [-36.5, -6.6], [-36.9, -6.6], [-37.2, -6.0], [-37.7, -5.7], [-38.2, -5.7], [-38.0, -5.2], [-37.4, -5.1], [-36.8, -5.3], [-36.2, -4.8]]]}},
{"type": "Feature", "properties": {"name": "Rio Grande do Sul"}, "geometry": {"type": "Polygon", "coordinates": [[[-53.4, -27.2], [-52.4, -27.2], [-51.5, -27.6], [-51.2, -28.3], [-50.7, -28.5], [-50.1, -29.0], [-49.7, -29.2], [-50.2, -29.8], [-50.9, -29.5], [-51.3, -30.0], [-50.9, -30.5], [-51.2, -31.0], [-51.7, -31.5], [-52.2, -31.8], [-52.5, -32.2], [-53.2, -32.5], [-53.1, -33.2], [-53.7, -33.6], [-54.9, -32.1], [-55.6, -31.7], [-56.2, -30.9], [-57.1, -30.5], [-56.9, -29.8], [-57.6, -29.3], [-57.1, -28.6], [-56.2, -28.5], [-55.3, -28.1], [-54.4, -28.3], [-53.8, -27.8], [-53.4, -27.2]]]}},
{"type": "Feature", "properties": {"name": "Rondônia"}, "geometry": {"type": "Polygon", "coordinates": [[[-62.8, -7.9], [-62.1, -7.3], [-61.3, -6.9], [-61.2, -6.1], [-60.4, -6.1], [-60.3, -4.7], [-59.6, -5.2], [-58.3, -4.3], [-56.5, -4.3], [-57.0, -4.0], [-57.3, -4.8], [-58.0, -5.5], [-58.8, -6.3], [-59.3, -9.1], [-60.2, -9.3], [-60.7, -9.9], [-61.3, -10.6], [-61.5, -11.5], [-60.8, -12.2], [-61.0, -13.2], [-60.1, -13.7], [-60.2, -14.3], [-61.4, -13.8], [-62.2, -13.4], [-62.9, -13.3], [-63.6, -12.8], [-64.0, -12.3], [-64.6, -11.6], [-65.1, -11.0], [-65.3, -10.0], [-65.0, -9.3], [-65.3, -8.5], [-64.2, -8.7], [-63.2, -8.0], [-63.2, -7.5], [-62.8, -7.9]]]}},
{"type": "Feature", "properties": {"name": "Roraima"}, "geometry": {"type": "Polygon", "coordinates": [[[-62.2, 3.2], [-61.3, 4.3], [-60.3, 5.1], [-59.8, 4.5], [-59.5, 3.5], [-59.9, 2.7], [-60.6, 2.8], [-62.2, 3.2]]]}},
{"type": "Feature", "properties": {"name": "Santa Catarina"}, "geometry": {"type": "Polygon", "coordinates": [[[-51.2, -25.9], [-50.9, -25.8], [-50.3, -26.4], [-49.9, -26.0], [-49.5, -26.3], [-49.0, -25.8], [-48.3, -25.9], [-48.6, -25.5], [-48.4, -26.2], [-48.6, -26.8], [-48.3, -27.3], [-48.8, -27.7], [-48.5, -28.2], [-49.2, -28.4], [-49.2, -29.1], [-49.7, -29.2], [-50.1, -29.0], [-50.7, -28.5], [-51.2, -28.3], [-51.5, -27.6], [-52.4, -27.2], [-53.4, -27.2], [-53.8, -27.8], [-53.2, -26.7], [-52.5, -26.5], [-51.8, -26.9], [-51.2, -25.9]]]}},
{"type": "Feature", "properties": {"name": "São Paulo"}, "geometry": {"type": "Polygon", "coordinates": [[[-48.1, -20.2], [-47.3, -20.0], [-47.3, -20.5], [-46.4, -21.2], [-46.7, -21.7], [-46.2, -22.3], [-45.6, -22.8], [-45.1, -22.2], [-44.8, -22.6], [-44.5, -22.5], [-44.7, -23.0], [-44.3, -22.8], [-43.7, -23.2], [-45.1, -23.9], [-45.8, -23.9], [-46.4, -24.4], [-47.2, -24.7], [-47.7, -25.2], [-48.1, -25.2], [-48.3, -24.4], [-49.0, -25.0], [-50.0, -24.7], [-50.6, -24.0], [-51.2, -23.2], [-51.6, -22.7], [-51.7, -22.5], [-52.1, -22.4], [-52.1, -21.5], [-51.2, -21.0], [-51.7, -20.0], [-51.0, -19.8], [-50.0, -20.3], [-49.0, -20.0], [-48.3, -19.6], [-47.9, -20.1], [-48.1, -20.2]]]}},
{"type": "Feature", "properties": {"name": "Sergipe"}, "geometry": {"type": "Polygon", "coordinates": [[[-37.2, -9.5], [-36.8, -9.8], [-36.4, -9.6], [-36.4, -10.2], [-37.2, -10.3], [-37.8, -10.5], [-38.0, -10.9], [-37.5, -11.2], [-37.0, -11.0], [-36.8, -10.5], [-37.2, -9.5]]]}},
{"type": "Feature", "properties": {"name": "Tocantins"}, "geometry": {"type": "Polygon", "coordinates": [[[-48.0, -5.2], [-47.5, -5.4], [-47.0, -6.0], [-47.3, -6.1], [-47.5, -6.8], [-47.0, -7.5], [-47.3, -8.3], [-47.1, -9.1], [-46.8, -9.8], [-46.3, -10.9], [-45.9, -10.2], [-44.8, -9.9], [-44.2, -9.2], [-43.4, -9.3], [-42.7, -10.0], [-43.9, -9.6], [-44.6, -8.9], [-45.0, -8.1], [-45.5, -7.2], [-45.1, -6.3], [-45.5, -5.4], [-46.6, -5.2], [-48.0, -5.2]]]}}
]
}
"""

# --- 3. Carregamento e Processamento dos Dados ---
# Carrega o GeoDataFrame a partir do nosso objeto JSON interno
gdf_states = gpd.GeoDataFrame.from_features(json.loads(GEOJSON_DATA)["features"])
gdf_states.crs = "EPSG:4326"

# Estrutura de dados com categorias SAMAS
management_data = {
    'Soja': {
        'states': ['Mato Grosso', 'Paraná', 'Rio Grande do Sul', 'Goiás', 'Mato Grosso do Sul'],
        'timeline': {
            'Adubos': {
                'Preparo do solo e Adubação': ['Agosto', 'Setembro', 'Outubro']
            },
            'Sementes': {
                'Aquisição e Tratamento de Sementes': ['Agosto', 'Setembro', 'Outubro']
            },
            'Agroquímicos': {
                'Herbicidas (Dessecantes e Pré-plantio)': ['Agosto', 'Setembro', 'Outubro'],
                'Controle de Ervas Daninhas (Pós-emergência)': ['Outubro', 'Novembro', 'Dezembro'],
                'Controle de Pragas Iniciais': ['Outubro', 'Novembro', 'Dezembro'],
                'Controle de Doenças': ['Dezembro', 'Janeiro']
            }
        },
        'details': """
        - **Pragas em Foco:** Lagarta da Soja, Lagarta do Cartucho, Elasmo e Falsa Medideira. Atenção também para a Mosca Branca.
        - **Doenças Principais:** Mofo Branco, Antracnose e Ferrugem Asiática.
        """
    },
    'Milho Safra': {
        'states': ['Mato Grosso', 'Paraná', 'Goiás', 'Mato Grosso do Sul', 'Minas Gerais'],
        'timeline': {
            'Adubos': {
                'Adubação de Cobertura (Nitrogenada)': ['Novembro', 'Dezembro', 'Janeiro']
            },
            'Sementes': {
                'Plantio e Tratamento de Sementes': ['Outubro', 'Novembro']
            },
            'Agroquímicos': {
                'Preparo de Solo e Herbicidas': ['Setembro', 'Outubro', 'Novembro'],
                'Controle de Pragas': ['Outubro', 'Novembro', 'Dezembro', 'Janeiro']
            },
            'Serviços': {
                'Aquisição de Financiamento/Custeio': ['Agosto', 'Setembro']
            }
        },
        'details': """
        - **Pragas em Foco:** Corós, lagarta rosca, elasmo (iniciais). Na fase de desenvolvimento, atenção especial à **Cigarrinha**, lagarta do cartucho e percevejo barriga verde.
        - **Doenças:** Ocorrência geralmente mais tardia, com exceção de nematóides.
        """
    },
    'Algodão': {
        'states': ['Mato Grosso', 'Bahia', 'Goiás', 'Mato Grosso do Sul'],
        'timeline': {
            'Adubos': {
                'Adubação de Plantio e Cobertura': ['Dezembro', 'Janeiro']
            },
            'Sementes': {
                'Plantio e Tratamento de Sementes': ['Dezembro', 'Janeiro']
            },
            'Agroquímicos': {
                'Controle de Pragas': ['Dezembro', 'Janeiro'],
                'Controle de Doenças': ['Janeiro']
            },
            'Serviços': {
                'Financiamento e Preparo do Solo': ['Outubro', 'Novembro', 'Dezembro']
            }
        },
        'details': """
        - **Pragas em Foco (Atenção Máxima):** Bicudo, ácaros, pulgões, curuquerê, lagarta rosada, Helicoverpa e percevejos.
        - **Estratégia de Plantio:** Comum em sucessão a uma soja super precoce (MT e BA).
        """
    }
}


# --- 4. Funções de Geração do Dashboard ---
def create_map(relevant_states, selected_states=None):
    """Cria um mapa Folium destacando os estados relevantes e uma lista de estados selecionados."""
    
    # O mapa sempre terá a mesma visão geral do Brasil
    location = [-15.788497, -47.879873]
    zoom_start = 4

    # Cria o mapa com o tile layer escuro e remove a marca d'água
    m = folium.Map(location=location, zoom_start=zoom_start, tiles="CartoDB dark_matter", attributionControl=False)

    def style_function(feature):
        state_name = feature['properties']['name']
        # Lógica de estilo:
        # 1. Se o estado está na lista de selecionados, pinta de amarelo com borda preta grossa.
        # 2. Senão, se é um estado relevante para a cultura, pinta de verde.
        # 3. Senão, pinta de cinza escuro.
        if selected_states and state_name in selected_states:
            return {'fillColor': '#0cc95e', 'color': 'black', 'weight': 2.5, 'fillOpacity': 1.0}
        elif state_name in relevant_states:
            return {'fillColor': '#0a381e', 'color': 'white', 'weight': 1, 'fillOpacity': 1.0}
        else:
            return {'fillColor': 'black', 'color': '#333333', 'weight': 1, 'fillOpacity': 1.0}

    # Adiciona os polígonos dos estados com o estilo definido
    folium.GeoJson(
        data=json.loads(GEOJSON_DATA),
        style_function=style_function,
        tooltip=folium.GeoJsonTooltip(fields=['name'], aliases=['Estado:'])
    ).add_to(m)

    return m

def create_styled_timeline(timeline_data, months):
    """Cria e estiliza um DataFrame do cronograma com categorias SAMAS."""
    
    records = []
    for samas_cat, sub_cats in timeline_data.items():
        for sub_cat, active_months in sub_cats.items():
            row = {'SAMAS': samas_cat, 'Atividade': sub_cat}
            for month in months:
                row[month] = 'X' if month in active_months else ''
            records.append(row)
    
    if not records:
        return pd.DataFrame()

    df = pd.DataFrame(records).set_index(['SAMAS', 'Atividade'])
    
    def style_active(val):
        color = '#27332D' 
        font_color = '#FFFFFF'
        is_active = val == 'X'
        
        return f'background-color: {color if is_active else "transparent"}; color: {font_color if is_active else "transparent"}; text-align: center; border: 1px solid #444;'
        
    header_props = [
        ('background-color', '#121212'),
        ('color', 'white'),
        ('font-weight', 'bold')
    ]
    
    styles = [
        dict(selector="th", props=header_props),
        dict(selector="th.row_heading", props=header_props),
        dict(selector="th.col_heading", props=header_props),
        dict(selector="td", props=[('border', '1px solid #444')]),
    ]

    # Remove o fundo branco da tabela
    st.markdown("""
    <style>
        .stDataFrame {
            background-color: transparent;
        }
    </style>
    """, unsafe_allow_html=True)

    styled_df = df.style.apply(lambda s: s.map(style_active)).set_table_styles(styles)
    return styled_df


# --- 5. Interface Principal ---
st.title("Calendário Agrícola Estratégico")

months_of_interest = ['Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro', 'Janeiro']

tab_labels = ["Soja", "Milho Safra", "Algodão"]
tabs = st.tabs(tab_labels)

for tab, culture_name in zip(tabs, tab_labels):
    with tab:
        culture_data = management_data[culture_name]
        
        # Layout principal com painel de filtros à direita
        main_content, filter_panel = st.columns([2.5, 1])

        with filter_panel:
            st.subheader("Filtros e Controles")
            
            # Filtro multiselect agora está aqui
            selected_states = st.multiselect(
                'Destaque um ou mais estados no mapa:',
                options=sorted(culture_data['states']),
                key=f'multiselect_{culture_name}' # Chave única para cada multiselect
            )

        with main_content:
            st.header(f"Análise da Cultura: {culture_name}")
            
            st.subheader("Mapa Interativo dos Estados Produtores")
            folium_map = create_map(culture_data['states'], selected_states=selected_states)
            st_folium(folium_map, use_container_width=True, height=400)

            st.subheader("Cronograma de Atividades (SAMAS)")
            styled_timeline = create_styled_timeline(culture_data['timeline'], months_of_interest)
            st.dataframe(styled_timeline, use_container_width=True)
            with st.expander("Ver Detalhes e Pontos de Atenção"):
                st.markdown(culture_data['details'])
