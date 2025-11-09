import pandas as pd
import plotly.express as px
import streamlit as st

# Leer el archivo CSV
df = pd.read_csv(r'C:\Users\emmah\OneDrive\Escritorio\UNI\TERCER\DataCoop25\alquiler\alquiler_municipio.csv', encoding='utf-8')

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
st.set_page_config(page_title='DataCoop', layout='wide', initial_sidebar_state='collapsed')

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

# ----------------------- GRAFICAS ALQUILER -----------------------
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


# ----------------------- GRAFICAS RENTA -----------------------

# Leer el archivo CSV de renta
df_renta = pd.read_csv(r"C:\Users\emmah\OneDrive\Escritorio\UNI\TERCER\DataCoop25\10RENTAS\RentaMedia_limpio.csv", sep=',', encoding='utf-8')

# Ordenar los datos de manera descendente por la columna 'Total' y seleccionar los primeros 10
df_renta_top10 = df_renta.sort_values(by='Total', ascending=False).head(10)

# Ordenar los datos de manera ascendente por la columna 'Total' para obtener los 10 municipios con menor renta neta media
df_renta_bottom10 = df_renta.sort_values(by='Total', ascending=True).head(10)

# Título del apartado
st.header('Análisis de Renta Neta Media por Municipio')

# Crear columnas para organizar los gráficos y tablas en horizontal
col1, col2 = st.columns(2)

# Gráfico de Barras Horizontales de los Top 10 Municipios con Mayor Renta Neta
with col1:
    st.subheader('Top 10 Municipios con Mayor Renta Neta Media')

    # Gráfico de barras horizontales
    fig_renta_top = px.bar(df_renta_top10,
                           x='Total',
                           y='Municipios',
                           title='Top 10 Municipios con Mayor Renta Neta Media',
                           labels={'Total': 'Renta Neta Media', 'Municipios': 'Municipios'},
                           color='Total',
                           color_continuous_scale='Blues')

    # Mostrar el gráfico interactivo
    st.plotly_chart(fig_renta_top, use_container_width=True)

    # Mostrar la tabla debajo del gráfico
    st.subheader('Datos de los Municipios con Mayor Renta')
    st.write(df_renta_top10[['Municipios', 'Total']])


# Gráfico de Barras Horizontales de los Top 10 Municipios con Menor Renta Neta
with col2:
    st.subheader('Top 10 Municipios con Menor Renta Neta Media')

    # Gráfico de barras horizontales
    fig_renta_bottom = px.bar(df_renta_bottom10,
                              x='Total',
                              y='Municipios',
                              title='Top 10 Municipios con Menor Renta Neta Media',
                              labels={'Total': 'Renta Neta Media', 'Municipios': 'Municipios'},
                              color='Total',
                              color_continuous_scale='Blues')

    # Mostrar el gráfico interactivo
    st.plotly_chart(fig_renta_bottom, use_container_width=True)

    # Mostrar la tabla debajo del gráfico
    st.subheader('Datos de los Municipios con Menor Renta')
    st.write(df_renta_bottom10[['Municipios', 'Total']])

# ----------------------- MAPA INTERACTIVO BANCOS -----------------------
# Ruta del archivo HTML
html_file_path = r"C:\Users\emmah\OneDrive\Escritorio\UNI\TERCER\DataCoop25\bancos\mapa_heatmap_bancos.html"  # Cambia esto por la ruta correcta

# Leer el contenido del archivo HTML
with open(html_file_path, "r", encoding="utf-8") as file:
    html_content = file.read()

# Título del apartado
st.header('Análisis de Red de presencia de Sucursales Bancarias en España')

# Subtítulo o introducción sobre el mapa
st.subheader("""
    El mapa resalta las zonas con mayor densidad de cobertura bancaria.
    Las áreas más calientes indican una mayor concentración de sucursales, distinguiendo la cobertura bancaria en diferentes regiones del país.
""")
# Mostrar el contenido HTML en Streamlit
st.components.v1.html(html_content, height=600) 
# Mostrar el contenido del archivo HTML en Streamlit
#st.markdown(html_content, unsafe_allow_html=True)

# ----------------------- MAPA INTERACTIVO municipios prioriczados -----------------------

# Ruta del archivo HTML
html_file_path_density = r"C:\Users\emmah\OneDrive\Escritorio\UNI\TERCER\DataCoop25\3tops\map_choropleth_simple.html"  # Cambia esto por la ruta correcta

# Leer el contenido del archivo HTML
with open(html_file_path_density, "r", encoding="utf-8") as file:
    html_file_path_density = file.read()

# Título del apartado
    st.header('Densidad de Población en España')
# Subtítulo de introducción
    st.subheader("Análisis de Municipios Sin Cobertura Bancaria en España")


# Crear columnas para organizar los gráficos y tablas en horizontal
col1, col2 = st.columns(2)

with col1:
    # Descripción visual con Markdown enriquecido
    st.markdown("""

        El **mapa interactivo** a continuación muestra los **municipios de España sin cobertura bancaria**, 
        destacando las zonas con mayor necesidad de **expansión de sucursales bancarias**. Este análisis se basa en varios criterios:

        ### Criterios de Selección:

        1. **Población**: 
            - Municipios con **más de 6,000 habitantes**.
            - Zonas suficientemente grandes para justificar una sucursal bancaria.

        2. **Renta Media**:
            - Se priorizaron municipios con **renta neta media baja**.
            - La presencia bancaria tiene un mayor **impacto social** en estas áreas.

        3. **Precio de Alquiler**:
            - Municipios con **precios de alquiler bajos**.
            - Minimizar el coste de establecimiento, garantizando una **inversión rentable**.

        4. **Municipios Sin Bancos**:
            - Se seleccionaron **municipios sin ninguna sucursal bancaria**.
            -  Identificando áreas con **mayor potencial** para la expansión de la red bancaria.
    """)

with col2:
    # Mostrar el contenido HTML en Streamlit
    st.components.v1.html(html_file_path_density, height=600) 

# statement de cierre
# Usar Markdown con estilo CSS personalizado
st.markdown("""
    <style>
        .custom-box {
            background-color: #1E3A8A;  /* Azul oscuro */
            color: white;
            padding: 15px;
            border-radius: 15px;
            font-size: 19px;
            font-weight: bold;
            margin-bottom: 20px;
            text-align: center;  /* Centra el texto dentro del recuadro */
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100px;  /* Ajusta la altura del recuadro */
        }

        .custom-box-container {
            display: flex;
            justify-content: center;  /* Centra el recuadro en la página */
            align-items: center;
            height: 100%;  /* Ajusta la altura de la pantalla */
        }
    </style>

    <div class="custom-box-container">
        <div class="custom-box">
            Zonas más calientes = Densidad de potencial para la expansión de sucursales.
        </div>
    </div>
""", unsafe_allow_html=True)


# ----------------------- 3 OFICINAS -----------------------

#st.header('Top 3 Municipios Prioritarios para Nuevas Sucursales Bancarias en España')


        # Aquí gráfico que represente los 3 municipios prioritarios + COL2 TABLA NOMBRES, POBLACION, SCORE TOTAL



# ----------------------- parte 2 -----------------------
import plotly.graph_objects as go

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
fig1 = go.Figure()

for municipio in nombres:
    fila = df_poblacion[df_poblacion["Municipios"] == municipio]
    if not fila.empty:
        fig1.add_trace(go.Scatter(
            x=anios,
            y=fila.iloc[0][anios],
            mode='lines+markers',
            name=municipio
        ))

fig1.update_layout(
    title="Evolución de la población (2015–2030)",
    xaxis_title="Años",
    yaxis_title="Habitantes",
    template="plotly_dark"
)

# Gráfica de renta
fig2 = go.Figure()

for provincia in provincias:
    fila = df_renta[df_renta["Provincias"] == provincia]
    if not fila.empty:
        fig2.add_trace(go.Scatter(
            x=anios,
            y=fila.iloc[0][anios],
            mode='lines+markers',
            name=provincia
        ))

fig2.update_layout(
    title="Evolución de la renta por provincia (2015-2030)",
    xaxis_title="Años",
    yaxis_title="Renta (€)",
    template="plotly_dark"
)

# Mostrar en Streamlit
st.header('Evolución de Población y Renta en Municipios Prioritarios (2015-2030)')
st.subheader("""Análisis de la evolución de la población y la renta en los municipios priorizados para la expansión bancaria. Se presentan gráficas que muestran las tendencias desde 2015 hasta 2030, destacando los municipios con mayor potencial.""")

# Mostrar las gráficas en Streamlit
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig1)  # Muestra la gráfica de población
with col2:
    st.plotly_chart(fig2)  # Muestra la gráfica de renta


"""
# ----------------------- HEATMAPS -----------------------
# Cargar los archivos CSV para los diferentes años
df_2026 = pd.read_csv(r"C:\Users\emmah\OneDrive\Escritorio\UNI\TERCER\DataCoop25\parte_2\predecir2026\municipios_priorizados_2026.csv")
df_2028 = pd.read_csv(r"C:\Users\emmah\OneDrive\Escritorio\UNI\TERCER\DataCoop25\parte_2\predecir2028\municipios_priorizados_2028.csv")
df_2030 = pd.read_csv(r"C:\Users\emmah\OneDrive\Escritorio\UNI\TERCER\DataCoop25\parte_2\predecir2030\municipios_priorizados_2030.csv")

# plots de heatmaps

st.header('Mapas de Calor de Municipios Prioritarios por Año (26-28-30)')

col1, col2, col3 = st.columns(3)
with col1:
    st.subheader('Año 2026')
    st.components.v1.html(open("heatmap2026.html", "r").read(), height=600)
with col2:
    st.subheader('Año 2028')
    html_file_path_2028 = r"C:\Users\emmah\OneDrive\Escritorio\UNI\TERCER\DataCoop25\parte_2\predecir2028\mapa_heatmap_2028.html"
    with open(html_file_path_2028, "r", encoding="utf-8") as file:
        html_content_2028 = file.read()
    st.components.v1.html(html_content_2028, height=500)
with col3:
    st.subheader('Año 2030')
    html_file_path_2030 = r"C:\Users\emmah\OneDrive\Escritorio\UNI\TERCER\DataCoop25\parte_2\predecir2030\mapa_heatmap_2030.html"
    with open(html_file_path_2030, "r", encoding="utf-8") as file:
        html_content_2030 = file.read()
    st.components.v1.html(html_content_2030, height=500)
"""