import json
import csv

# Cargar el archivo GeoJSON
with open('DataCoop25\export.geojson', 'r', encoding='utf-8') as geojson_file:
    data = json.load(geojson_file)

# Abrir un archivo CSV para escribir los datos
with open('output.csv', 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=["id", "amenity", "atm", "brand", "name", "coordinates"])
    writer.writeheader()

    # Iterar sobre cada feature del GeoJSON
    for feature in data['features']:
        properties = feature['properties']
        geometry = feature['geometry']
        
        # Extraer las coordenadas
        if geometry['type'] == 'Point':
            coordinates = geometry['coordinates']
        elif geometry['type'] == 'LineString':
            coordinates = geometry['coordinates']
        else:
            coordinates = None

        # Crear un diccionario con la información que deseamos exportar
        row = {
            "id": feature['id'],
            "amenity": properties.get('amenity', ''),
            "atm": properties.get('atm', ''),
            "brand": properties.get('brand', ''),
            "name": properties.get('name', ''),
            "coordinates": coordinates
        }
        
        # Escribir la fila en el CSV
        writer.writerow(row)

print("Archivo CSV generado exitosamente.")
