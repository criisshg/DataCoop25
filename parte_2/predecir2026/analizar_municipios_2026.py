import pandas as pd
import numpy as np

print("Cargando datos...")

# 1. Cargar datos originales de municipios con códigos
try:
    municipios_info = pd.read_csv('municipios_sin_bancos.csv')
    print(f"Información de municipios cargada: {len(municipios_info)} municipios")
    
    # Asegurar formato correcto de códigos
    municipios_info['CPRO'] = municipios_info['CPRO'].astype(str).str.zfill(2)
    municipios_info['CMUN'] = municipios_info['CMUN'].astype(str).str.zfill(3)
    
    # 2. Cargar predicciones de población
    poblacion_pred = pd.read_csv('municipios_predicciones.csv', encoding='latin1')
    print(f"Predicciones de población cargadas: {len(poblacion_pred)} municipios")
    
    # Unir datos
    poblacion = pd.merge(
        municipios_info[['CPRO', 'CMUN', 'NOMBRE', 'PROVINCIA', 'num_bancos']],
        poblacion_pred[['Municipios', '2026']],
        left_on='NOMBRE',
        right_on='Municipios',
        how='inner'
    )
except Exception as e:
    print(f"Error al cargar municipios_predicciones.csv: {e}")
    poblacion = pd.DataFrame()

# 2. Cargar predicciones de renta
try:
    renta = pd.read_csv('prediccion_renta.csv', sep=',', encoding='latin1')
    print(f"Predicciones de renta cargadas: {len(renta)} provincias")

    # Mapeo de nombres de provincia a códigos
    provincia_codes = {
        'Álava': '01', 'Albacete': '02', 'Alicante/Alacant': '03', 'Almería': '04',
        'Ávila': '05', 'Badajoz': '06', 'Balears, Illes': '07', 'Barcelona': '08',
        'Burgos': '09', 'Cáceres': '10', 'Cádiz': '11', 'Castellón/Castelló': '12',
        'Ciudad Real': '13', 'Córdoba': '14', 'Coruña, A': '15', 'Cuenca': '16',
        'Girona': '17', 'Granada': '18', 'Guadalajara': '19', 'Gipuzkoa': '20',
        'Huelva': '21', 'Huesca': '22', 'Jaén': '23', 'León': '24',
        'Lleida': '25', 'Rioja, La': '26', 'Lugo': '27', 'Madrid': '28',
        'Málaga': '29', 'Murcia': '30', 'Navarra': '31', 'Ourense': '32',
        'Asturias': '33', 'Palencia': '34', 'Palmas, Las': '35', 'Pontevedra': '36',
        'Salamanca': '37', 'Santa Cruz de Tenerife': '38', 'Cantabria': '39',
        'Segovia': '40', 'Sevilla': '41', 'Soria': '42', 'Tarragona': '43',
        'Teruel': '44', 'Toledo': '45', 'Valencia/València': '46', 'Valladolid': '47',
        'Bizkaia': '48', 'Zamora': '49', 'Zaragoza': '50', 'Ceuta': '51',
        'Melilla': '52'
    }

    # Crear mapa de códigos a predicciones de renta 2026
    renta['CPRO'] = renta['Provincias'].map(provincia_codes)
    renta_2026_map = renta.set_index('CPRO')['2026'].to_dict()
    
except Exception as e:
    print(f"Error al cargar prediccion_renta.csv: {e}")
    renta = pd.DataFrame()

# Crear DataFrame base con municipios y predicciones
if not poblacion.empty:
    # Usar predicción 2026 como población
    municipios = poblacion[['CPRO', 'CMUN', 'NOMBRE', 'PROVINCIA', '2026', 'num_bancos']].copy()
    municipios = municipios.rename(columns={'2026': 'Poblacion_2026'})
    
    # Convertir población a numérico
    municipios['Poblacion_2026'] = pd.to_numeric(municipios['Poblacion_2026'], errors='coerce')
    
    # Añadir predicciones de renta por provincia
    municipios['renta_2026'] = municipios['CPRO'].map(renta_2026_map)
    
    # Filtrar municipios con más de 6000 habitantes predichos y sin bancos actuales
    municipios_candidatos = municipios[
        (municipios['Poblacion_2026'] > 6000) & 
        (municipios['num_bancos'] == 0)
    ]

    # Normalización de variables
    def normalize(series):
        s = series.copy().astype(float)
        if s.isna().all():
            return pd.Series(0, index=s.index)
        s = s.fillna(s.median())
        mn = s.min()
        mx = s.max()
        if mx == mn:
            return pd.Series(1, index=s.index)
        return (s - mn) / (mx - mn)

    # Preparar scores
    municipios_candidatos['pop_score'] = normalize(municipios_candidatos['Poblacion_2026'])
    # Para impacto social preferimos renta más baja -> invertir normalización
    municipios_candidatos['renta_norm'] = normalize(municipios_candidatos['renta_2026'])
    municipios_candidatos['renta_score'] = 1 - municipios_candidatos['renta_norm']

    # Score de competencia (todos tienen 0 bancos actualmente)
    municipios_candidatos['competition_score'] = 1.0

    # Pesos reflejando la misión cooperativa
    w_pop = 0.35  # Aumentado porque es predicción futura
    w_social = 0.45  # Renta baja priorizada para impacto social
    w_comp = 0.20  # Aumentado por oportunidad de mercado

    # Calcular score total
    municipios_candidatos['score_total'] = (
        municipios_candidatos['pop_score'] * w_pop +
        municipios_candidatos['renta_score'] * w_social +
        municipios_candidatos['competition_score'] * w_comp
    )

    # Ordenar por score total
    mejores = municipios_candidatos.sort_values('score_total', ascending=False).reset_index(drop=True)

    print("\nTop 20 municipios candidatos para 2026:")
    for i, r in mejores.head(20).iterrows():
        print(f"\n{i+1}. {r['NOMBRE']} ({r['PROVINCIA']})")
        print(f"   Población 2026: {int(r['Poblacion_2026']):,}")
        print(f"   Renta media 2026: {r['renta_2026']:,.2f}€")
        print(f"   Score total: {r['score_total']:.3f}")

    # Guardar resultados
    mejores[['CPRO', 'CMUN', 'NOMBRE', 'PROVINCIA', 'Poblacion_2026', 'renta_2026', 'score_total']].to_csv(
        'municipios_priorizados_2026.csv', 
        index=False
    )
    print("\nResultados completos guardados en 'municipios_priorizados_2026.csv'")