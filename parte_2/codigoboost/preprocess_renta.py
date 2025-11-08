"""
Preprocess renta data file to convert it to the right format.
"""
import pandas as pd

# Read the data
df = pd.read_csv('evolucion_renta.csv', sep=';')

# Filter for "Renta neta media por persona"
df = df[df['Indicadores de renta media'] == 'Renta neta media por persona']

# Keep only province level data (remove national and autonomous community levels)
df = df[df['Comunidades y Ciudades Autónomas'].notna() & 
        df['Provincias'].notna() & 
        df['Islas'].isna()]

# Extract province and year data
df['Periodo'] = pd.to_numeric(df['Periodo'])
df['Total'] = pd.to_numeric(df['Total'], errors='coerce')

# Pivot the data
result = df.pivot_table(index='Provincias', columns='Periodo', values='Total', aggfunc='first')

# Save to file
result.to_csv('evolucion_renta_wide.csv', sep=';')
print("Data transformed and saved to evolucion_renta_wide.csv")