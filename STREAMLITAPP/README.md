# 🏦 Mapa Interactivo de Propensión 2026 - Caixa Enginyers

Aplicación Streamlit para análisis dinámico de municipios candidatos para apertura de nuevas oficinas bancarias cooperativas.

## 📊 Características

- **Ajuste dinámico de pesos**: Modifica en tiempo real la importancia de población, impacto social (renta baja), alquiler bajo y competencia
- **Visualización interactiva**: Mapa con puntos coloreados según puntuación dinámica (verde bajo → rojo alto)
- **Clustering inteligente**: Agrupación de puntos con suma de scores
- **Objetivos marcados**: 3 ubicaciones objetivo (Villanueva de la Serena, Torredonjimeno, Viator) destacadas con emoji 🏦
- **Top 10 ranking**: Tabla actualizada en tiempo real con los municipios mejor puntuados

## 🚀 Despliegue en Streamlit Community Cloud

### Paso 1: Preparar repositorio GitHub

1. Crea un nuevo repositorio público en GitHub
2. Sube estos archivos:
   ```
   PARTE 2/
   ├── app_weights_streamlit.py
   ├── municipios_priorizados_2026_con_coords.csv  ⬅️ IMPORTANTE: usar el CSV con coordenadas
   ├── requirements.txt
   └── .streamlit/
       └── config.toml
   ```

**⚠️ NO subas el shapefile** (demasiado pesado para GitHub). Usa el CSV con coordenadas generado.

### Paso 2: Desplegar en Streamlit Cloud

1. Ve a https://share.streamlit.io/
2. Inicia sesión con tu cuenta de GitHub
3. Click en **"New app"**
4. Configura:
   - **Repository**: tu-usuario/tu-repositorio
   - **Branch**: main
   - **Main file path**: `PARTE 2/app_weights_streamlit.py`
5. Click **"Deploy!"**
6. Espera 2-3 minutos mientras se construye

### Paso 3: Compartir

Tu app estará disponible en:
```
https://tu-usuario-nombre-repo.streamlit.app
```

Copia el link y compártelo con quien quieras. ¡Funciona desde cualquier dispositivo!

## 🎯 Cómo usar la app

1. **Ajusta los pesos** con los sliders en la barra lateral:
   - Población (0-1, default 0.25)
   - Impacto social / renta baja (0-1, default 0.45)
   - Alquiler bajo (0-1, default 0.25)
   - Oportunidad / competencia (0-1, default 0.05)

2. **Observa los cambios** en tiempo real:
   - Los colores de los puntos se actualizan
   - El Top 10 se recalcula
   - Los clusters muestran la suma de scores

3. **Explora el mapa**:
   - Haz zoom para ver municipios individuales
   - Click en un punto para ver desglose detallado
   - Activa/desactiva capas en el control superior derecho
   - Los 3 objetivos (🏦) están siempre visibles

## 📁 Archivos del proyecto

- `app_weights_streamlit.py`: Aplicación principal Streamlit
- `municipios_priorizados_2026_con_coords.csv`: Dataset con coordenadas (108 KB)
- `requirements.txt`: Dependencias Python
- `.streamlit/config.toml`: Configuración de servidor
- `generate_csv_with_coords.py`: Script para regenerar CSV con coordenadas (solo desarrollo local)

## 🛠️ Desarrollo local

```powershell
# Instalar dependencias
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

# Ejecutar app
streamlit run "PARTE 2/app_weights_streamlit.py"
```

La app estará disponible en:
- Local: http://localhost:8501
- Red: http://TU_IP:8501

## 📦 Dependencias

- streamlit
- streamlit-folium
- folium
- geopandas
- pandas
- numpy
- branca

## 🎨 Personalización

### Cambiar paleta de colores

En la barra lateral, selecciona entre:
- **Amarillos-rojos** (default): verde → amarillo → naranja → rojo
- **Azules**: claro → oscuro
- **Verdes**: claro → oscuro

### Modificar objetivos

Edita la lista `TARGET_NOMBRES` en `app_weights_streamlit.py` (línea ~236):
```python
TARGET_NOMBRES = ['Municipio1', 'Municipio2', 'Municipio3']
```

## 📊 Metodología

**Fórmula de puntuación:**
```
Score = (pop_norm × w_pop + 
         renta_score × w_social + 
         alquiler_score × w_rent + 
         competition × w_comp) × 1000
```

Donde:
- `pop_norm`: Población normalizada 0-1 (más alta = mejor)
- `renta_score`: 1 - renta normalizada (renta baja = más social = mejor)
- `alquiler_score`: 1 - alquiler normalizado (alquiler bajo = mejor)
- `competition`: 1 si no hay bancos, 0 si hay competencia

**Normalización:** Min-max por componente, usando mediana para valores faltantes.

**Colores:** Distribución por percentiles (p10-p90) para evitar concentración en extremos.

## 📞 Soporte

Para regenerar el CSV con coordenadas desde el shapefile:
```powershell
python generate_csv_with_coords.py
```

## 📄 Licencia

Proyecto para Hackathon Caixa Enginyers 2026
