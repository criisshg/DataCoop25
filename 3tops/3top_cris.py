import pandas as pd
from geopy.geocoders import Nominatim
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point

# Cargar el archivo CSV
file_path = r'C:\Users\emmah\OneDrive\Escritorio\UNI\TERCER\DataCoop25\3tops\municipios_priorizados_unicos.csv'  # Asegúrate de poner la ruta correcta
df = pd.read_csv(file_path)

# Ordenar por la columna 'score_total' para obtener los tres municipios más ponderados
df_top_3 = df.sort_values(by='score_total', ascending=False).head(3)

# Obtener las coordenadas de los municipios utilizando Geopy
geolocator = Nominatim(user_agent="municipios_geolocator")

municipios_nombres = [
    "Cieza, Murcia, Spain",
    "Totana, Murcia, Spain",
    "Villanueva de la Serena, Badajoz, Spain"
]

coordenadas = []
for nombre in municipios_nombres:
    location = geolocator.geocode(nombre)
    if location:
        coordenadas.append((nombre, location.latitude, location.longitude))

# Añadir las coordenadas a los datos
df_top_3['lat'] = [coord[1] for coord in coordenadas]
df_top_3['lon'] = [coord[2] for coord in coordenadas]

# Cargar el mapa de España desde un archivo GeoJSON
spain = gpd.read_file(r'C:\Users\emmah\OneDrive\Escritorio\UNI\TERCER\DataCoop25\bancos\export.geojson')  

# Crear un GeoDataFrame para los tres mejores municipios
geometry = [Point(lon, lat) for lon, lat in zip(df_top_3['lon'], df_top_3['lat'])]
gdf_municipios = gpd.GeoDataFrame(df_top_3, geometry=geometry)

# Crear el gráfico con el mapa de España
fig, ax = plt.subplots(figsize=(10, 10))

# Dibujar el mapa de España
spain.plot(ax=ax, color='lightgrey')

# Añadir los puntos de los tres mejores municipios
gdf_municipios.plot(ax=ax, color='orange', markersize=100)

# Añadir texto con la información de cada municipio
for _, municipio in gdf_municipios.iterrows():
    ax.text(municipio.geometry.x + 0.1, municipio.geometry.y, f"{municipio['NOMBRE']}\n{municipio['Poblacion']} hab\nScore: {municipio['score_total']:.3f}",
            fontsize=10, ha='left', color='black', fontweight='bold')

# Títulos y etiquetas
ax.set_title("Top 3 Municipios Prioritarios para Bancos en España", fontsize=16)
ax.set_xlabel("Longitud")
ax.set_ylabel("Latitud")

# Mostrar el gráfico
plt.show()
