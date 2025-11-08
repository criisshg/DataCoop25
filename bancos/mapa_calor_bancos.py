
import geopandas as gpd
import pandas as pd
import folium
from folium.plugins import HeatMap

# 1) Cargar GEOJSON de bancos
gdf_bancos = gpd.read_file(r"C:\Users\clara\Documentos\3º GED\bancos_espana.geojson")  # ruta a tu archivo

# 2) Normalizar geometrías: convertir LineString/Polygon a puntos (centroides o puntos representativos)
def geom_to_point(geom):
    if geom is None:
        return None
    geom_type = geom.geom_type
    if geom_type == "Point":
        return geom
    if geom_type in ("LineString", "MultiLineString", "Polygon", "MultiPolygon"):
        return geom.centroid
    # si hay GeometryCollection u otros, coger centroid por seguridad
    try:
        return geom.centroid
    except:
        return None

gdf_bancos["point_geom"] = gdf_bancos.geometry.apply(geom_to_point)
gdf_points = gdf_bancos.dropna(subset=["point_geom"]).copy()
gdf_points.set_geometry("point_geom", inplace=True)
gdf_points = gdf_points.to_crs(epsg=4326)  # asegurar lat/lon WGS84

# Extraer lista de [lat, lon] para HeatMap (nota: folium usa [lat, lon])
heat_data = [[pt.y, pt.x] for pt in gdf_points.geometry]

# 3) Crear el mapa base centrado en España
m = folium.Map(location=[40.4, -3.7], zoom_start=6, tiles="CartoDB positron")

# 4) Añadir HeatMap (ajusta radius, blur, max_zoom)
HeatMap(heat_data, radius=12, blur=15, max_zoom=11, min_opacity=0.3).add_to(m)

# 5) Guardar mapa
m.save(r"C:\Users\clara\Documentos\3º GED\mapa_heatmap_bancos.html")
print("Mapa guardado en: mapa_heatmap_bancos.html")
