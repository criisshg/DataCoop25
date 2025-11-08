import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

# Cargar el CSV original
df = pd.read_csv(r"C:\Users\clara\Documentos\3º GED\poblacion_municipios_2015_2023.csv")
df.fillna(df.mean(numeric_only=True), inplace=True)


# Años históricos
years = np.array([2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]).reshape(-1, 1)

# Años a predecir
future_years = [2026, 2028, 2030]
future_years_array = np.array(future_years).reshape(-1, 1)

# Crear nuevo DataFrame para resultados
results = df[['Municipios']].copy()

# Predecir para cada municipio
for index, row in df.iterrows():
    values = row[1:].values.astype(float)
    model = LinearRegression()
    model.fit(years, values)
    predictions = model.predict(future_years_array)
    for year, pred in zip(future_years, predictions):
        results.loc[index, str(year)] = round(pred)

# Combinar con datos originales
final_df = pd.merge(df, results.drop(columns=['Municipios']), left_index=True, right_index=True)

# Guardar en nuevo CSV
final_df.to_csv('municipios_predicciones.csv', index=False)
