# analisis_bancarias.py
# Cristina Huanca  15:25 2025-11-08

# Importar bibliotecas necesarias
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from geopy.distance import geodesic
import folium
import geopandas as gpd
from sklearn.cluster import KMeans
import joblib  # Para guardar el modelo entrenado

# Función para cargar datos
def cargar_datos():
    """
    Cargar todos los datasets de entrada.
    """
    # Ajusta los paths de los archivos CSV de tus datasets
    df_poblacion = pd.read_csv('poblacion_municipio.csv', delimiter=';')
    df_cajeros = pd.read_csv('cajeros.csv')
    df_alquileres = pd.read_csv('alquiler_municipio.csv')
    df_renta = pd.read_csv('renta.csv')

    return df_poblacion, df_cajeros, df_alquileres, df_hipotecas

# Función de limpieza y transformación de datos
def limpiar_datos(df):
    """
    Limpiar y transformar datos: eliminar valores nulos, transformar tipos, normalizar datos.
    """
    # Ejemplo: Eliminar valores nulos o imputarlos
    df = df.dropna()  # O puedes imputar con valores de la media
    # Ejemplo: Asegurarse de que las columnas que se usan para la geolocalización sean correctas
    df['lat'] = pd.to_numeric(df['lat'], errors='coerce')
    df['lon'] = pd.to_numeric(df['lon'], errors='coerce')
    return df

# Función de análisis exploratorio de datos (EDA)
def analisis_eda(df):
    """
    Realizar análisis exploratorio de los datos (EDA), análisis de correlaciones y visualización.
    """
    # Muestra estadísticas descriptivas
    print(df.describe())
    
    # Visualizar correlaciones entre variables
    correlation_matrix = df.corr()
    plt.figure(figsize=(10, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm")
    plt.title("Correlaciones entre variables")
    plt.show()

    # Visualización geoespacial de los datos (ejemplo: distribución de cajeros automáticos)
    mapa = folium.Map(location=[df['lat'].mean(), df['lon'].mean()], zoom_start=6)
    for i, row in df.iterrows():
        folium.Marker(location=[row['lat'], row['lon']], popup=row['name']).add_to(mapa)
    mapa.save("mapa_cajeros.html")

# Función de preparación para el modelo predictivo
def preparar_modelo(df_poblacion, df_cajeros, df_alquileres):
    """
    Preparar los datos para el modelo predictivo.
    """
    # Unir todos los datos relevantes
    df = pd.merge(df_poblacion, df_cajeros, on='municipio', how='left')
    df = pd.merge(df, df_alquileres, on='municipio', how='left')

    # Crear las características (features) y la variable objetivo (target)
    X = df[['densidad_poblacional', 'precio_alquiler', 'numero_cajeros']]  # Ejemplo de características
    y = df['apertura_exitosa']  # Variable objetivo (esto es un ejemplo)

    return X, y

# Función de modelado predictivo
def entrenar_modelo(X, y):
    """
    Entrenar un modelo de predicción con Random Forest.
    """
    # Dividir los datos en entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Inicializar y entrenar el modelo
    modelo = RandomForestClassifier(n_estimators=100, random_state=42)
    modelo.fit(X_train, y_train)

    # Evaluar el modelo
    y_pred = modelo.predict(X_test)
    print(classification_report(y_test, y_pred))
    print(f"Accuracy: {accuracy_score(y_test, y_pred)}")

    # Guardar el modelo entrenado
    joblib.dump(modelo, 'modelo_entrenado.pkl')

    return modelo

# Función para hacer predicciones y obtener las mejores ubicaciones
def obtener_mejores_ubicaciones(df, modelo):
    """
    Obtener las ubicaciones con mejor puntuación para abrir nuevas oficinas bancarias.
    """
    # Hacer predicciones en el dataset de ubicaciones
    X = df[['densidad_poblacional', 'precio_alquiler', 'numero_cajeros']]
    df['probabilidad'] = modelo.predict_proba(X)[:, 1]  # Obtener probabilidad de éxito

    # Seleccionar las top 3 ubicaciones con mayor probabilidad
    mejores_ubicaciones = df.nlargest(3, 'probabilidad')
    return mejores_ubicaciones

# Función para generar una ruta para la entidad móvil
def generar_ruta(mejores_ubicaciones):
    """
    Generar una ruta optimizada para la entidad móvil a partir de las mejores ubicaciones.
    """
    # Asumimos que cada ubicación tiene coordenadas lat/lon
    ubicaciones = mejores_ubicaciones[['lat', 'lon']].values

    # Calcular la ruta más corta entre las ubicaciones usando geodesic para distancias
    ruta = [ubicaciones[0]]
    for i in range(1, len(ubicaciones)):
        # Calcular la distancia entre ubicaciones
        distancias = [geodesic(ruta[-1], ubicacion).km for ubicacion in ubicaciones[i:]]
        proxima_ubicacion = ubicaciones[i + distancias.index(min(distancias))]
        ruta.append(proxima_ubicacion)
    
    print("Ruta de la entidad móvil:", ruta)
    return ruta

# Main: Ejecutar las funciones
if __name__ == "__main__":
    # Cargar los datos
    df_poblacion, df_cajeros, df_alquileres, df_hipotecas = cargar_datos()

    # Limpiar los datos
    df_poblacion = limpiar_datos(df_poblacion)
    df_cajeros = limpiar_datos(df_cajeros)
    df_alquileres = limpiar_datos(df_alquileres)

    # Realizar el análisis exploratorio
    analisis_eda(df_poblacion)

    # Preparar los datos para el modelo
    X, y = preparar_modelo(df_poblacion, df_cajeros, df_alquileres)

    # Entrenar el modelo
    modelo = entrenar_modelo(X, y)

    # Obtener las mejores ubicaciones
    mejores_ubicaciones = obtener_mejores_ubicaciones(df_poblacion, modelo)
    print("Mejores ubicaciones para abrir oficinas:", mejores_ubicaciones)

    # Generar la ruta para la entidad móvil
    ruta = generar_ruta(mejores_ubicaciones)
