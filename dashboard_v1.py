import pandas as pd
import plotly.express as px
import streamlit as st

# Leer el archivo CSV
df = pd.read_csv('alquiler_municipio.csv', encoding='utf-8')

# Renombrar las columnas para facilitar el manejo
columns = ['Localización', 'Precio_m2', 'Variacion_mensual', 'Variacion_trimestral', 
           'Variacion_anual', 'Maximo_historico', 'Variacion_maximo']
df.columns = columns

# Filtrar solo las filas que contienen 'provincia' en la columna 'Localización'
df = df[df['Localización'].str.contains('provincia', case=False, na=False)]

# Eliminar el símbolo de € y convertir a valor numérico
df['Precio_m2'] = df['Precio_m2'].str.replace(' €/m2', '').astype(float)

# Eliminar la palabra 'provincia' de los nombres de las localizaciones
df['Localización'] = df['Localización'].str.replace(' provincia', '', case=False)

# Ordenar los valores por precio por metro cuadrado
df_sorted = df.sort_values('Precio_m2')

# Top 10 más baratos
df_top_10_baratos = df_sorted.head(10)

# Top 10 más caros
df_top_10_caros = df_sorted.tail(10)

# Configuración de Streamlit
st.title('Análisis de Precios por Metro Cuadrado')

# Visualización del gráfico para los 10 más baratos
st.subheader('Top 10 Ubicaciones Más Baratas por Metro Cuadrado')
fig1 = px.bar(df_top_10_baratos, 
              x='Localización', 
              y='Precio_m2', 
              title='Top 10 Ubicaciones Más Baratas por Metro Cuadrado',
              labels={'Precio_m2': 'Precio/m²', 'Localización': 'Localización'},
              color='Precio_m2', 
              color_continuous_scale='viridis',
              text='Precio_m2')  # Mostrar los valores encima de las barras

fig1.update_traces(texttemplate='%{text:.2f} €', textposition='outside', marker=dict(line=dict(color='black', width=1)))
fig1.update_layout(title_font_size=20, xaxis_tickangle=-45, xaxis_title_font_size=14, yaxis_title_font_size=14)

# Mostrar el gráfico interactivo
st.plotly_chart(fig1)

# Visualización del gráfico para los 10 más caros
st.subheader('Top 10 Ubicaciones Más Caras por Metro Cuadrado')
fig2 = px.bar(df_top_10_caros, 
              x='Localización', 
              y='Precio_m2', 
              title='Top 10 Ubicaciones Más Caras por Metro Cuadrado',
              labels={'Precio_m2': 'Precio/m²', 'Localización': 'Localización'},
              color='Precio_m2', 
              color_continuous_scale='viridis',
              text='Precio_m2')  # Mostrar los valores encima de las barras

fig2.update_traces(texttemplate='%{text:.2f} €', textposition='outside', marker=dict(line=dict(color='black', width=1)))
fig2.update_layout(title_font_size=20, xaxis_tickangle=-45, xaxis_title_font_size=14, yaxis_title_font_size=14)

# Mostrar el gráfico interactivo
st.plotly_chart(fig2)

# Imprimir los 10 más baratos y los 10 más caros en formato tabla
st.subheader('Datos de las 10 Ubicaciones Más Baratas')
st.write(df_top_10_baratos[['Localización', 'Precio_m2']])

st.subheader('Datos de las 10 Ubicaciones Más Caras')
st.write(df_top_10_caros[['Localización', 'Precio_m2']])
