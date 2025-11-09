import pandas as pd
import folium
from folium.plugins import HeatMap
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from tqdm import tqdm

# Ruta al archivo CSV
csv_path = r"C:\Users\clara\Documentos\3º GED\predicciones\municipios_priorizados_2030.csv"

# Cargar datos
df = pd.read_csv(csv_path)
df = df[df['score_total'].notnull()]

# Geolocalización
geolocator = Nominatim(user_agent="mapa_municipios")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

latitudes = []
longitudes = []

print("Geolocalizando municipios...")
for _, row in tqdm(df.iterrows(), total=len(df)):
    location = geocode(f"{row['NOMBRE']}, {row['PROVINCIA']}, España")
    if location:
        latitudes.append(location.latitude)
        longitudes.append(location.longitude)
    else:
        latitudes.append(None)
        longitudes.append(None)

df['lat'] = latitudes
df['lon'] = longitudes
df = df.dropna(subset=['lat', 'lon'])

# Crear mapa
mapa = folium.Map(location=[40.4168, -3.7038], zoom_start=6)

# Añadir círculos con popups
for _, row in df.iterrows():
    popup_text = f"""
    <b>{row['NOMBRE']}</b><br>
    Provincia: {row['PROVINCIA']}<br>
    Score: {row['score_total']:.3f}<br>
    Renta: {row['renta_2030'] if pd.notnull(row['renta_2030']) else 'N/D'}<br>
    Población: {int(row['Poblacion_2030']) if pd.notnull(row['Poblacion_2030']) else 'N/D'}
    """
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=5 + row['score_total'] * 10,
        color='blue',
        fill=True,
        fill_color='blue',
        fill_opacity=0.6,
        popup=folium.Popup(popup_text, max_width=250)
    ).add_to(mapa)

# Añadir capa de calor
heat_data = [[row['lat'], row['lon'], row['score_total']] for _, row in df.iterrows()]
HeatMap(heat_data, radius=10, blur=15, max_zoom=1).add_to(mapa)

# Guardar mapa
mapa.save("mapa_interactivo_municipios_2030.html")
print("Mapa guardado como mapa_interactivo_municipios_2030.html")
