import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Crear el DataFrame con los datos proporcionados
data = pd.read_csv('./df_merged_output.csv', delimiter=',', encoding='utf-8')
df = pd.DataFrame(data)

# Aplicar la transformación logarítmica a los datos para los ejes y el tamaño de los puntos
df['renta_log'] = np.log(df['renta'] + 1)  # Logaritmo de la renta (sumamos 1 para evitar log(0))
df['poblacion_log'] = np.log(df['poblacion'] + 1)  # Logaritmo de la población (sumamos 1 para evitar log(0))

# Ajuste de tamaño de los puntos: si quieres que los puntos con pocos bancos sean más pequeños
df['size'] = np.log(df['num_bancos'] + 1) * 100  # Tamaño ajustado con logaritmo (sumamos 1 para evitar log(0))

# Crear el gráfico de dispersión
plt.figure(figsize=(10, 6))

# Ejes X: Renta logarítmica, Eje Y: Población logarítmica, Color: Número de bancos, Tamaño ajustado: Número de bancos
scatter = plt.scatter(df['renta_log'], df['poblacion_log'], 
                      c=df['num_bancos'],  # Color por número de bancos
                      s=df['size'],  # Tamaño ajustado por número de bancos logarítmico
                      cmap='viridis',  # Mapa de colores viridis para los puntos
                      alpha=0.7, edgecolors="w", linewidth=0.5)

# Títulos y etiquetas
plt.title('Relación entre Población, Renta y Número de Bancos (Logarítmico)', fontsize=14)
plt.xlabel('Renta (log)', fontsize=12)
plt.ylabel('Población (log)', fontsize=12)

# Barra de colores para el número de bancos
plt.colorbar(scatter, label='Número de Bancos')

# Mostrar gráfico
plt.tight_layout()
plt.show()
