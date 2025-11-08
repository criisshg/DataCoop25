"""
Preprocess population data file to convert it to the right format.
"""
import pandas as pd

# Read the data - try different encodings
try:
    df = pd.read_csv('evolucion_poblacion.csv', sep=';', encoding='utf-8')
except UnicodeDecodeError:
    try:
        df = pd.read_csv('evolucion_poblacion.csv', sep=';', encoding='latin1')
    except UnicodeDecodeError:
        df = pd.read_csv('evolucion_poblacion.csv', sep=';', encoding='cp1252')

# Fix column name
df = df.rename(columns={'ÿMunicipios': 'Municipios'})

# Filter for total population (all sexes)
df = df[df['Sexo'] == 'Total']

# Extract municipality code and name
df['Codigo'] = df['Municipios'].str.split().str[0]
df['Municipio'] = df['Municipios'].str.split().str[1:].str.join(' ')

# Convert to numeric
df['Periodo'] = pd.to_numeric(df['Periodo'])
df['Total'] = pd.to_numeric(df['Total'], errors='coerce')

# Pivot the data
result = df.pivot_table(index=['Codigo', 'Municipio'], columns='Periodo', values='Total', aggfunc='first')
result = result.reset_index()

# Save to file
result.to_csv('evolucion_poblacion_wide.csv', sep=';', index=False)
print("Data transformed and saved to evolucion_poblacion_wide.csv")