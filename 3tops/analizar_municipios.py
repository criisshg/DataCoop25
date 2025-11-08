import pandas as pd
import geopandas as gpd
import numpy as np

print("Cargando datos...")

# 1. Cargar datos de bancos por municipio
try:
    bancos_municipio = pd.read_csv('bancos_por_municipio.csv')
    print(f"Datos de bancos cargados: {len(bancos_municipio)} municipios")
    
    # Asegurar formato correcto de códigos
    bancos_municipio['CPRO'] = bancos_municipio['CPRO'].astype(str).str.zfill(2)
    bancos_municipio['CMUN'] = bancos_municipio['CMUN'].astype(str).str.zfill(3)
except Exception as e:
    print(f"Error al cargar bancos_por_municipio.csv: {e}")
    bancos_municipio = pd.DataFrame()

# 2. Cargar datos de población por municipio
try:
    # Leer el Excel y normalizar la estructura (skiprows=1 para quitar el título largo)
    poblacion = pd.read_excel('POBLACIONPORMUNICIPIO.xlsx', skiprows=1)

    # Renombrar columnas según la estructura observada
    poblacion.columns = ['CPRO', 'PROVINCIA', 'CMUN', 'NOMBRE', 'POB24', 'HOMBRES', 'MUJERES']

    # Eliminar filas no válidas (fila de cabecera que aparece como dato)
    poblacion = poblacion[poblacion['CPRO'].astype(str).str.strip() != 'CPRO']

    # Convertir tipos y rellenar ceros en códigos
    poblacion['CPRO'] = poblacion['CPRO'].astype(str).str.zfill(2)
    poblacion['CMUN'] = poblacion['CMUN'].astype(str).str.zfill(3)
    poblacion['POB24'] = pd.to_numeric(poblacion['POB24'], errors='coerce').fillna(0).astype(int)

    print(f"\nDatos de población cargados: {len(poblacion)} registros")
    print("\nPrimeras filas procesadas:")
    print(poblacion.head())
except Exception as e:
    print(f"Error al cargar POBLACIONPORMUNICIPIO.xlsx: {e}")
    poblacion = pd.DataFrame()

# 3. Cargar datos de renta por municipio (o usar datos provinciales como proxy si es necesario)
try:
    renta = pd.read_csv('renta media.csv', sep=';', encoding='latin1')
    print(f"Datos de renta cargados: {len(renta)} registros")

    # Reutilizamos el proceso para extraer código CPRO desde el nombre de provincia
    def extract_cpro_from_name(name):
        provincia_codes = {
            'Álava': '01', 'Albacete': '02', 'Alicante': '03', 'Almería': '04',
            'Ávila': '05', 'Badajoz': '06', 'Baleares': '07', 'Barcelona': '08',
            'Burgos': '09', 'Cáceres': '10', 'Cádiz': '11', 'Castellón': '12',
            'Ciudad Real': '13', 'Córdoba': '14', 'Coruña, A': '15', 'Cuenca': '16',
            'Girona': '17', 'Granada': '18', 'Guadalajara': '19', 'Guipúzcoa': '20',
            'Huelva': '21', 'Huesca': '22', 'Jaén': '23', 'León': '24',
            'Lleida': '25', 'Rioja, La': '26', 'Lugo': '27', 'Madrid': '28',
            'Málaga': '29', 'Murcia': '30', 'Navarra': '31', 'Ourense': '32',
            'Asturias': '33', 'Palencia': '34', 'Palmas, Las': '35', 'Pontevedra': '36',
            'Salamanca': '37', 'Santa Cruz de Tenerife': '38', 'Cantabria': '39',
            'Segovia': '40', 'Sevilla': '41', 'Soria': '42', 'Tarragona': '43',
            'Teruel': '44', 'Toledo': '45', 'Valencia': '46', 'Valladolid': '47',
            'Vizcaya': '48', 'Zamora': '49', 'Zaragoza': '50', 'Ceuta': '51',
            'Melilla': '52'
        }
        if pd.isna(name):
            return None
        for prov, code in provincia_codes.items():
            if prov.lower() in str(name).lower():
                return code
        return None

    renta = renta[renta['Provincias'].notna()]
    renta['CPRO'] = renta['Provincias'].apply(extract_cpro_from_name)
    renta['renta_media'] = pd.to_numeric(renta['Total'].astype(str).str.replace(',', '.'), errors='coerce')
    renta = renta[renta['CPRO'].notna() & renta['renta_media'].notna()]
    print(f"Datos de renta procesados: {len(renta)} provincias con datos válidos")
except Exception as e:
    print(f"Error al cargar renta media.csv: {e}")
    renta = pd.DataFrame()

# 4. Preparar análisis
print("\nPreparando análisis...")

# Crear DataFrame base con todos los municipios de población
if not poblacion.empty:
    # Usar POB24 como población total
    municipios = poblacion[['CPRO', 'CMUN', 'NOMBRE', 'POB24', 'PROVINCIA']].copy()
    municipios = municipios.rename(columns={'POB24': 'Poblacion'})
    
    # Añadir información de bancos (0 si no hay datos)
    municipios = municipios.merge(
        bancos_municipio[['CPRO', 'CMUN', 'num_bancos']], 
        on=['CPRO', 'CMUN'], 
        how='left'
    )
    municipios['num_bancos'] = municipios['num_bancos'].fillna(0)
    
    # Filtrar municipios con más de 6000 habitantes y sin bancos
    municipios_candidatos = municipios[
        (municipios['Poblacion'] > 6000) & 
        (municipios['num_bancos'] == 0)
    ]

    # --- Mapear precio de alquiler por provincia (alquiler_municipio.csv) ---
    try:
        alquiler = pd.read_csv('alquiler_municipio.csv', sep=',', encoding='utf-8', engine='python', header=None)
        alquiler.columns = ['Localizacion', 'Precio_m2', 'V1', 'V2', 'V3', 'V4', 'V5']

        # Normalizar texto helper
        import unicodedata
        def norm(s):
            if pd.isna(s):
                return ''
            s = str(s)
            s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode('ascii')
            return s.lower()

        alquiler['loc_norm'] = alquiler['Localizacion'].apply(norm)

        # Extraer numeric price from Precio_m2
        import re
        def extract_price(s):
            if pd.isna(s):
                return np.nan
            s = str(s)
            m = re.search(r'([0-9]+[\.,]?[0-9]*)\s*\u20AC', s)
            if m:
                return float(m.group(1).replace(',', '.'))
            m2 = re.search(r'([0-9]+[\.,]?[0-9]*)\s*€/m2', s)
            if m2:
                return float(m2.group(1).replace(',', '.'))
            # fallback: digits only
            m3 = re.search(r'([0-9]+[\.,]?[0-9]*)', s)
            if m3:
                return float(m3.group(1).replace(',', '.'))
            return np.nan

        alquiler['precio'] = alquiler['Precio_m2'].apply(extract_price)

        # Keep province-level entries: those containing 'provincia' or matching known provinces
        provincias_unique = municipios['PROVINCIA'].dropna().unique().tolist()
        provincias_norm = [norm(p) for p in provincias_unique]

        # Build map: try exact matches first, then 'provincia' entries
        rent_map = {}
        for _, r in alquiler.iterrows():
            ln = r['loc_norm']
            price = r['precio']
            if pd.isna(price):
                continue
            if 'provincia' in ln:
                # key = text before ' provincia'
                key = ln.replace(' provincia', '').strip()
                rent_map[key] = price
            else:
                rent_map[ln] = price

        # Function to find price for a given municipio province string
        def find_rent_for_prov(prov):
            key = norm(prov)
            # direct match
            if key in rent_map:
                return rent_map[key]
            # try substring match
            for k, v in rent_map.items():
                if k in key or key in k:
                    return v
            return np.nan

        municipios_candidatos['alquiler_m2'] = municipios_candidatos['PROVINCIA'].apply(find_rent_for_prov)
    except Exception as e:
        print(f"Error cargando alquiler_municipio.csv: {e}")
        municipios_candidatos['alquiler_m2'] = np.nan

    # Mapear renta (ingresos) por provincia usando renta (CPRO)
    if not renta.empty:
        renta_map = renta.set_index('CPRO')['renta_media'].to_dict()
        municipios_candidatos['renta_media'] = municipios_candidatos['CPRO'].map(renta_map)
    else:
        municipios_candidatos['renta_media'] = np.nan

    # 5. Scoring: queremos priorizar impacto social (renta baja), poblacion alta y alquiler bajo
    def normalize(series):
        s = series.copy().astype(float)
        if s.isna().all():
            return pd.Series(0, index=s.index)
        s = s.fillna(s.median())
        mn = s.min()
        mx = s.max()
        if mx == mn:
            return pd.Series(1.0, index=s.index)
        return (s - mn) / (mx - mn)

    # Prepare variables
    municipios_candidatos['pop_score'] = normalize(municipios_candidatos['Poblacion'])
    # For social impact prefer lower renta -> invert normalized renta
    municipios_candidatos['renta_norm'] = normalize(municipios_candidatos['renta_media'])
    municipios_candidatos['renta_score'] = 1 - municipios_candidatos['renta_norm']
    # Prefer lower alquiler -> invert
    municipios_candidatos['alquiler_norm'] = normalize(municipios_candidatos['alquiler_m2'])
    municipios_candidatos['alquiler_score'] = 1 - municipios_candidatos['alquiler_norm']

    # Competition score: since all have 0 bancos, keep 1; in general could use distance to nearest bank
    municipios_candidatos['competition_score'] = 1.0

    # Weights reflecting Caixa Enginyers cooperative mission (tunable)
    w_pop = 0.25
    w_social = 0.45  # low renta prioritized for social impact
    w_rent = 0.25
    w_comp = 0.05

    municipios_candidatos['score_total'] = (
        municipios_candidatos['pop_score'] * w_pop +
        municipios_candidatos['renta_score'] * w_social +
        municipios_candidatos['alquiler_score'] * w_rent +
        municipios_candidatos['competition_score'] * w_comp
    )

    mejores = municipios_candidatos.sort_values('score_total', ascending=False).reset_index(drop=True)

    print("\nTop 10 municipios candidatos según criterios cooperativos:")
    for i, r in mejores.head(10).iterrows():
        print(f"\n{i+1}. {r['NOMBRE']} ({r['PROVINCIA']})")
        print(f"   Población: {int(r['Poblacion']):,}")
        print(f"   Renta media provincial: {r['renta_media'] if not pd.isna(r['renta_media']) else 'N/D'}")
        print(f"   Alquiler €/m2 (prov.): {r['alquiler_m2'] if not pd.isna(r['alquiler_m2']) else 'N/D'}")
        print(f"   Score total: {r['score_total']:.3f}")

    mejores[['CPRO','CMUN','NOMBRE','PROVINCIA','Poblacion','num_bancos','renta_media','alquiler_m2','score_total']].to_csv('municipios_priorizados.csv', index=False)
    print("\nResultados completos guardados en 'municipios_priorizados.csv'")
    
    # Ordenar por población descendente
    municipios_candidatos = municipios_candidatos.sort_values('Poblacion', ascending=False)
    
    # Mostrar resultados
    print("\nMunicipios candidatos (>1000 habitantes, sin bancos):")
    print(f"Total encontrados: {len(municipios_candidatos)}")
    print("\nTop 10 municipios por población:")
    
    for idx, row in municipios_candidatos.head(10).iterrows():
        print(f"\nMunicipio: {row['NOMBRE']}")
        print(f"Provincia: {row['PROVINCIA']}")
        print(f"Población: {row['Poblacion']:,.0f}")
        print(f"Número de bancos: {row['num_bancos']:.0f}")
        
        # Mostrar renta media de la provincia si está disponible
        if not renta.empty:
            renta_prov = renta[renta['CPRO'] == row['CPRO']]['renta_media'].iloc[0] if len(renta[renta['CPRO'] == row['CPRO']]) > 0 else None
            if renta_prov:
                print(f"Renta media provincial: {renta_prov:,.2f}€")
    
    # Guardar resultados
    municipios_candidatos.to_csv('municipios_sin_bancos.csv', index=False)
    print("\nResultados completos guardados en 'municipios_sin_bancos.csv'")

    # --------------------------------------------------
    # 6. Calcular distancia al banco más cercano para cada municipio candidato
    # --------------------------------------------------
    try:
        print("\nCalculando distancia al banco más cercano para cada municipio candidato...")
        # Cargar geometrías de municipios (shapefile)
        muni_gdf = gpd.read_file('cartografia_censo2011_nacional/')

        # Normalizar códigos en el gdf de municipios si existen
        if 'CPRO' in muni_gdf.columns:
            muni_gdf['CPRO'] = muni_gdf['CPRO'].astype(str).str.zfill(2)
        if 'CMUN' in muni_gdf.columns:
            muni_gdf['CMUN'] = muni_gdf['CMUN'].astype(str).str.zfill(3)

        # Merge geometries with our candidatos by CPRO+CMUN to get geometry for each candidate
        candidatos_geo = municipios_candidatos.merge(
            muni_gdf[['CPRO','CMUN','geometry']],
            on=['CPRO','CMUN'],
            how='left'
        )

        # Some candidates may not have matched geometry; drop those without geometry
        candidatos_geo = candidatos_geo[~candidatos_geo['geometry'].isna()].copy()

        # Representative point (guaranteed dentro del polígono)
        # Ensure geometry column is a GeoSeries before using representative_point
        geom_series = gpd.GeoSeries(candidatos_geo['geometry'], crs=muni_gdf.crs)
        candidatos_geo['rep_point'] = geom_series.representative_point().values
        candidatos_pts = gpd.GeoDataFrame(candidatos_geo.drop(columns=['geometry']).copy(), geometry='rep_point', crs=muni_gdf.crs)

        # Cargar bancos/ATMs
        bancos_gdf = gpd.read_file('export.geojson')

        # Ensure both are in the same metric CRS (use EPSG:25830 if available, else use municipios CRS)
        metric_crs = 'EPSG:25830'
        try:
            candidatos_pts = candidatos_pts.to_crs(metric_crs)
            bancos_gdf = bancos_gdf.to_crs(metric_crs)
        except Exception:
            # fallback: reproject both to municipios CRS
            target = municipios_crs = muni_gdf.crs
            candidatos_pts = candidatos_pts.to_crs(target)
            bancos_gdf = bancos_gdf.to_crs(target)

        # Run nearest join (requires geopandas >=0.10)
        joined = gpd.sjoin_nearest(candidatos_pts, bancos_gdf[['geometry']], how='left', distance_col='dist_m')

        # dist_m may be NaN for empty banks_gdf
        joined['dist_m'] = joined['dist_m'].fillna(99999999)
        joined['dist_km'] = joined['dist_m'] / 1000.0

        # Compute distance score with exponential decay
        decay_km = 10.0
        joined['dist_score'] = np.exp(- joined['dist_km'] / decay_km)
        joined.loc[joined['dist_km'] > 50, 'dist_score'] = 0.0

        # Merge dist back into municipios_priorizados (mejores)
        merged_scores = mejores.merge(
            joined[['CPRO','CMUN','dist_m','dist_km','dist_score']],
            on=['CPRO','CMUN'],
            how='left'
        )

        # Fill missing dist_score with 0 (no nearby banks known)
        merged_scores['dist_score'] = merged_scores['dist_score'].fillna(0.0)

        # Integrate into final score: normalize all weights so they sum to 1
        # Original weights (tunable) defined earlier: w_pop, w_social, w_rent, w_comp
        w_dist = 0.12
        total_w = w_pop + w_social + w_rent + w_comp + w_dist
        # Avoid division by zero
        if total_w == 0:
            # fallback: equal weights
            w_pop_n = w_social_n = w_rent_n = w_comp_n = w_dist_n = 1.0 / 5.0
        else:
            w_pop_n = w_pop / total_w
            w_social_n = w_social / total_w
            w_rent_n = w_rent / total_w
            w_comp_n = w_comp / total_w
            w_dist_n = w_dist / total_w

        print(f"\nPesos normalizados (suman 1): pop={w_pop_n:.3f}, social={w_social_n:.3f}, rent={w_rent_n:.3f}, comp={w_comp_n:.3f}, dist={w_dist_n:.3f}")

        # Use individual component scores present in 'merged_scores' to compute final weighted score
        # Ensure component columns exist; if not, fall back to score_total and dist_score blending
        required_cols = {'pop_score','renta_score','alquiler_score','competition_score','dist_score'}
        if required_cols.issubset(set(merged_scores.columns)):
            merged_scores['score_with_distance'] = (
                merged_scores['pop_score'] * w_pop_n +
                merged_scores['renta_score'] * w_social_n +
                merged_scores['alquiler_score'] * w_rent_n +
                merged_scores['competition_score'] * w_comp_n +
                merged_scores['dist_score'] * w_dist_n
            )
        else:
            # fallback (shouldn't normally happen): keep previous blending behavior
            merged_scores['score_with_distance'] = merged_scores['score_total'] * (1 - w_dist) + merged_scores['dist_score'] * w_dist

        # Save results
        merged_scores.to_csv('municipios_con_distancia.csv', index=False)
        merged_scores.sort_values('score_with_distance', ascending=False).to_csv('municipios_priorizados_con_distancia.csv', index=False)

        print("\nDistancias calculadas y resultados guardados en 'municipios_con_distancia.csv' y 'municipios_priorizados_con_distancia.csv'")
        print("\nTop 5 según score con distancia:")
        for i, r in merged_scores.sort_values('score_with_distance', ascending=False).head(5).iterrows():
            print(f"\n{i+1}. {r['NOMBRE']} ({r['PROVINCIA']})")
            print(f"   Población: {int(r['Poblacion']):,}")
            print(f"   Distancia al banco más cercano: {r['dist_km']:.2f} km")
            print(f"   Score previo: {r['score_total']:.3f}, Score con distancia: {r['score_with_distance']:.3f}")

    except Exception as e:
        print(f"Error calculando distancias: {e}")
        import traceback
        traceback.print_exc()
