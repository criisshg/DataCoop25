import folium
from folium.plugins import HeatMap
import pandas as pd

# Cargar el archivo CSV
df_2026 = pd.read_csv(r"C:\Users\emmah\OneDrive\Escritorio\UNI\TERCER\DataCoop25\parte_2\predecir2026\municipios_priorizados_2026.csv")

# Filtrar los municipios con coordenadas (eliminamos los NaN si existen)
df_2026 = df_2026.dropna(subset=['lat', 'lon'])

# Crear un mapa base centrado en España
m = folium.Map(location=[40.4637, -3.7492], zoom_start=6)  # Coordenadas aproximadas de España

# Crear un HeatMap de los municipios
heat_data = [[row['lat'], row['lon'], row['score_total']] for index, row in df_2026.iterrows()]
HeatMap(heat_data).add_to(m)

# Guardar el mapa en un archivo HTML
m.save('heatmap_espana.html')
