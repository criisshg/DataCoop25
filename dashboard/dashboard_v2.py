import pandas as pd
import plotly.express as px
import streamlit as st

# Leer el archivo CSV
df = pd.read_csv('/alquiler/alquiler_municipio.csv', encoding='utf-8')

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

# Configuración de Streamlit con fondo oscuro
st.set_page_config(page_title='Análisis de Precios', layout='wide', initial_sidebar_state='collapsed')

# Establecer un fondo oscuro
st.markdown("""
    <style>
        body {
            background-color: #1e1e1e;
            color: white;
        }
        .css-1q8dd3m {
            background-color: #2b2b2b;
        }
        .streamlit-expanderHeader {
            color: white;
        }
        .css-13qz1un {
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# Título de la página
st.title("UAB THE HACK! - Repte de Caixa d'Enginyers - Dashboard fet per DataCoop - 2025")
st.header('Análisis de Precios por Metro Cuadrado')

# Crear columnas para organizar los gráficos y tablas en horizontal
col1, col2 = st.columns(2)

# Gráfico Top 10 más baratos
with col1:
    st.subheader('Top 10 Ubicaciones Más Baratas')
    fig1 = px.bar(df_top_10_baratos, 
                  x='Localización', 
                  y='Precio_m2', 
                  title=' ',
                  #title='Top 10 Ubicaciones Más Baratas por Metro Cuadrado',
                  labels={'Precio_m2': 'Precio/m²', 'Localización': 'Localización'},
                  color='Precio_m2', 
                  color_continuous_scale='Blues',
                  text='Precio_m2')  # Mostrar los valores encima de las barras

    fig1.update_traces(texttemplate='%{text:.2f} €', textposition='outside', marker=dict(line=dict(color='black', width=1)))
    fig1.update_layout(title_font_size=20, xaxis_tickangle=-45, xaxis_title_font_size=14, yaxis_title_font_size=14)

    # Mostrar el gráfico interactivo
    st.plotly_chart(fig1, use_container_width=True)

    # Mostrar la tabla debajo del gráfico
    st.subheader('Datos de las 10 Ubicaciones')
    st.write(df_top_10_baratos[['Localización', 'Precio_m2']])

# Gráfico Top 10 más caros
with col2:
    st.subheader('Top 10 Ubicaciones Más Caras')
    fig2 = px.bar(df_top_10_caros, 
                  x='Localización', 
                  y='Precio_m2',
                  title=' ',
                  #title='Top 10 Ubicaciones Más Caras por Metro Cuadrado',
                  labels={'Precio_m2': 'Precio/m²', 'Localización': 'Localización'},
                  color='Precio_m2', 
                  color_continuous_scale='Blues',
                  text='Precio_m2')  # Mostrar los valores encima de las barras

    fig2.update_traces(texttemplate='%{text:.2f} €', textposition='outside', marker=dict(line=dict(color='black', width=1)))
    fig2.update_layout(title_font_size=20, xaxis_tickangle=-45, xaxis_title_font_size=14, yaxis_title_font_size=14)

    # Mostrar el gráfico interactivo
    st.plotly_chart(fig2, use_container_width=True)

    # Mostrar la tabla debajo del gráfico
    st.subheader('Datos de las 10 Ubicaciones')
    st.write(df_top_10_caros[['Localización', 'Precio_m2']])
