"""
Este archivo crea una aplicación interactiva con Streamlit para visualizar mapas de calor basados en la densidad de población de
municipios en diferentes años (2026, 2028, 2030). Utiliza **Folium** para generar los mapas de calor y **Nominatim (OpenStreetMap)**
para obtener las coordenadas geográficas de los municipios. Los usuarios pueden seleccionar el año mediante un slider interactivo, 
y el mapa se actualiza dinámicamente según su elección. La aplicación permite explorar la distribución geográfica de la población a
través de un mapa interactivo, facilitando análisis territoriales de manera visual e intuitiva.

""" 


import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap
from geopy.geocoders import Nominatim

# Crear una instancia de geolocalizador usando Nominatim (OpenStreetMap)
geolocator = Nominatim(user_agent="municipios_geolocator")

# Cargar los archivos CSV para los diferentes años
df_2026 = pd.read_csv(r"C:\Users\emmah\OneDrive\Escritorio\UNI\TERCER\DataCoop25\parte_2\predecir2026\municipios_priorizados_2026.csv")
df_2028 = pd.read_csv(r"C:\Users\emmah\OneDrive\Escritorio\UNI\TERCER\DataCoop25\parte_2\predecir2026\municipios_priorizados_2028.csv")
df_2030 = pd.read_csv(r"C:\Users\emmah\OneDrive\Escritorio\UNI\TERCER\DataCoop25\parte_2\predecir2026\municipios_priorizados_2030.csv")

# Función para obtener coordenadas de los municipios usando Nominatim (OpenStreetMap)
def obtener_coordenadas(df):
    coordenadas = []
    for index, row in df.iterrows():
        nombre_completo = f"{row['NOMBRE']}, {row['PROVINCIA']}, España"  # Crear el nombre completo
        location = geolocator.geocode(nombre_completo)
        if location:
            coordenadas.append((row['NOMBRE'], location.latitude, location.longitude))
        else:
            coordenadas.append((row['NOMBRE'], None, None))  # Si no encuentra coordenadas, se asigna None
    df['lat'] = [coord[1] for coord in coordenadas]
    df['lon'] = [coord[2] for coord in coordenadas]
    return df

# Obtener las coordenadas de cada uno de los DataFrames
df_2026 = obtener_coordenadas(df_2026)
df_2028 = obtener_coordenadas(df_2028)
df_2030 = obtener_coordenadas(df_2030)

# Función para crear el mapa de calor con un año seleccionado
def crear_mapa_heatmap(year):
    # Seleccionar el DataFrame según el año
    if year == 2026:
        df = df_2026
    elif year == 2028:
        df = df_2028
    elif year == 2030:
        df = df_2030

    # Eliminar filas sin coordenadas (sin lat y lon)
    df = df.dropna(subset=['lat', 'lon'])

    # Crear el mapa base centrado en España
    mapa = folium.Map(location=[40.4637, -3.7492], zoom_start=6)

    # Preparar los datos para el mapa de calor (usando población como valor para el mapa)
    heat_data = [[row['lat'], row['lon'], row['Poblacion_2026']] for index, row in df.iterrows()]

    # Crear la capa de mapa de calor
    HeatMap(heat_data).add_to(mapa)

    # Guardar el mapa en un archivo HTML temporal para Streamlit
    return mapa

# Interfaz Streamlit
st.title("Mapa de Calor de Municipios Prioritarios")

# Slider para seleccionar el año
year = st.slider("Selecciona el año", 2026, 2030, 2026, step=2)

# Crear el mapa con el año seleccionado
mapa = crear_mapa_heatmap(year)

# Mostrar el mapa en Streamlit
st.subheader(f"Mapa de Calor para el año {year}")
st.markdown("Visualización de la densidad de población en función del municipio.")

# Convertir el mapa de Folium en HTML para ser visualizado en Streamlit
from io import BytesIO
from IPython.display import IFrame

# Guardar el mapa como HTML en un buffer
map_html = 'temp_map.html'
mapa.save(map_html)

# Mostrar el mapa en Streamlit (incrustar el HTML)
with open(map_html, 'r') as file:
    map_html_content = file.read()
st.components.v1.html(map_html_content, height=600)
