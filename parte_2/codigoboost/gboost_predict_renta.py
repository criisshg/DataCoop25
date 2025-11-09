import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

# Cargar el CSV
df = pd.read_csv('renta_provincias_2015_2023.csv')

# Años históricos
years = np.array([2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]).reshape(-1, 1)

# Años a predecir
future_years = [2026, 2028, 2030]
future_years_array = np.array(future_years).reshape(-1, 1)

# Crear nuevo DataFrame para resultados
results = df[['Provincias']].copy()

# Predecir para cada provincia
for index, row in df.iterrows():
    values = row[1:].values.astype(float)

    # Verificar si hay NaN
    if np.isnan(values).any():
        print(f"Saltando provincia con datos faltantes: {row['Provincias']}")
        continue

    model = LinearRegression()
    model.fit(years, values)
    predictions = model.predict(future_years_array)

    for year, pred in zip(future_years, predictions):
        results.loc[index, str(year)] = round(pred, 3)  # Redondeo a 3 decimales

# Combinar y guardar
final_df = pd.merge(df, results.drop(columns=['Provincias']), left_index=True, right_index=True)
final_df.to_csv('prediccion_renta.csv', index=False)
