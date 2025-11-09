import pandas as pd
import matplotlib.pyplot as plt

# Cargar los archivos CSV
df_2026 = pd.read_csv(r"C:\Users\emmah\OneDrive\Escritorio\UNI\TERCER\DataCoop25\parte_2\predecir2026\municipios_priorizados_2026.csv")
df_poblacion = pd.read_csv(r"C:\Users\emmah\OneDrive\Escritorio\UNI\TERCER\DataCoop25\parte_2\datosfuturos\municipios_predicciones.csv")
df_renta = pd.read_csv(r"C:\Users\emmah\OneDrive\Escritorio\UNI\TERCER\DataCoop25\parte_2\datosfuturos\prediccion_renta.csv")

# Seleccionar los 10 municipios con mayor score en 2026
top_municipios = df_2026.sort_values(by="score_total", ascending=False).head(10)
nombres = top_municipios["NOMBRE"].tolist()
provincias = top_municipios["PROVINCIA"].tolist()
anios = [str(a) for a in [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2026, 2028, 2030]]

# Gráfica de población
plt.figure(figsize=(12, 6))
for municipio in nombres:
    fila = df_poblacion[df_poblacion["Municipios"] == municipio]
    if not fila.empty:
        plt.plot(anios, fila.iloc[0][anios], label=municipio)
plt.title("Evolución de la población (2015–2030)")
plt.ylabel("Habitantes")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Gráfica de renta
plt.figure(figsize=(12, 6))
for provincia in provincias:
    fila = df_renta[df_renta["Provincias"] == provincia]
    if not fila.empty:
        plt.plot(anios, fila.iloc[0][anios], label=provincia)
plt.title("Evolución de la renta por provincia (2015–2030)")
plt.ylabel("Renta (€)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
