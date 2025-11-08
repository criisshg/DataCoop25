import pandas as pd
import matplotlib.pyplot as plt

# Cargar el CSV
df = pd.read_csv("DataCoop25/RentaMedia_limpio.csv", sep=',', encoding='utf-8')

print(df.columns)
# Ordenar los datos de manera descendente por la columna 'Total' y seleccionar los primeros 10
df_top10 = df.sort_values(by='Total', ascending=False).head(10)

# Ordenar los datos de manera ascendente por la columna 'Total' para obtener los 10 municipios con menor renta neta media
df_bottom10 = df.sort_values(by='Total', ascending=True).head(10)

# Graficar los 10 municipios con mayor renta neta media
plt.figure(figsize=(10, 6))
plt.barh(df_top10['Municipios'], df_top10['Total'], color='skyblue')
plt.xlabel('Renta neta media por hogar')
plt.ylabel('Municipios')
plt.title('Top 10 Municipios con Mayor Renta Neta Media por Hogar en 2023')

# Invertir el eje Y para mostrar el mayor en la parte superior
plt.gca().invert_yaxis()
plt.show()

# Graficar los 10 municipios con menor renta neta media
plt.figure(figsize=(10, 6))
plt.barh(df_bottom10['Municipios'], df_bottom10['Total'], color='skyblue')
plt.xlabel('Renta neta media por hogar')
plt.ylabel('Municipios')
plt.title('Top 10 Municipios con Menor Renta Neta Media por Hogar en 2023')

# Invertir el eje Y para mostrar el mayor en la parte superior
plt.gca().invert_yaxis()
plt.show()
