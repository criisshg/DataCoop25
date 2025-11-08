import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Leer CSV
df = pd.read_csv('bancos_por_municipio.csv')  # reemplaza con tu ruta

# Seleccionar top 15 municipios con más bancos
top_10 = df.sort_values('num_bancos', ascending=False).head(15)

# Configuración estética de Seaborn
sns.set(style="whitegrid")

# ------------------- Top 10 -------------------
plt.figure(figsize=(12,6))
top_plot = sns.barplot(
    x='NMUN', y='num_bancos', data=top_10, palette='viridis'
)
plt.title('Top 15 municipis amb més bancs')
plt.xlabel('Municipi')
plt.ylabel('Número de bancs')
plt.xticks(rotation=45)

# Añadir etiquetas encima de cada barra
for index, row in top_10.iterrows():
    top_plot.text(index, row['num_bancos'] + 0.1, row['num_bancos'], color='black', ha="center")

plt.tight_layout()
plt.show()

