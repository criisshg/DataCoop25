import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

# --- 1. Cargar CSV ---
df = pd.read_csv('poblacion_total_merged.csv', delimiter=',', encoding='utf-8')

# --- 2. Limpieza mínima ---
if 'CRECIMIENTO_NETO' in df.columns:
    df = df.drop(columns=['CRECIMIENTO_NETO'])
df = df.dropna()

# --- 3. Usar columna correcta de municipios ---
# El CSV tiene columnas PROVINCIA y NOMBRE
muni_col = 'NOMBRE'

# --- 4. Funciones auxiliares ---
def col_pob(year):
    yy = str(year)[-2:]
    return f'POB{yy}'

def check_cols(year):
    cp = col_pob(year)
    cr = str(year)
    if cp not in df.columns:
        raise ValueError(f"Falta columna {cp} para el año {year}.")
    if cr not in df.columns:
        raise ValueError(f"Falta columna de renta '{cr}' para el año {year}.")
    return cp, cr

# --- 5. Año base para entrenar ---
base_candidates = [2024, 2023, 2022, 2021, 2020, 2019, 2018]
base_year = None
for y in base_candidates:
    try:
        check_cols(y)
        base_year = y
        break
    except ValueError:
        continue
if base_year is None:
    raise ValueError("No hay columnas suficientes de población y renta para entrenar.")

pob_base, renta_base = check_cols(base_year)

# --- 6. Variables de entrenamiento ---
X = pd.DataFrame({
    'poblacion': pd.to_numeric(df[pob_base], errors='coerce'),
    'renta': pd.to_numeric(df[renta_base], errors='coerce')
})
y = pd.to_numeric(df['num_bancos'], errors='coerce')

mask = X.notna().all(axis=1) & y.notna()
X, y = X[mask], y[mask]

# 🔧 Mantener siempre NOMBRE después del filtrado
df_clean = df.copy().loc[mask]
df_clean[muni_col] = df_clean[muni_col].astype(str)

# --- 7. Entrenar modelo ---
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = XGBRegressor(
    n_estimators=400,
    learning_rate=0.05,
    max_depth=6,
    subsample=0.9,
    colsample_bytree=0.9,
    random_state=42
)
model.fit(X_train, y_train)
mae = mean_absolute_error(y_test, model.predict(X_test))
print(f"MAE (año base {base_year}): {mae:.2f}")

# --- 8. Predicción por horizontes ---
horizontes = [2026, 2028, 2030]
tops = {}

for year in horizontes:
    pob_col, renta_col = check_cols(year)
    X_pred = pd.DataFrame({
        'poblacion': pd.to_numeric(df_clean[pob_col], errors='coerce'),
        'renta': pd.to_numeric(df_clean[renta_col], errors='coerce')
    })
    preds = model.predict(X_pred).round(2)
    df_clean[f'prediccion_bancos_{year}'] = preds
    df_clean[f'diferencia_{year}'] = df_clean['num_bancos'] - df_clean[f'prediccion_bancos_{year}']

    top10 = df_clean.sort_values(by=f'diferencia_{year}', ascending=True).head(10)
    tops[year] = top10[[muni_col, 'num_bancos', f'prediccion_bancos_{year}', f'diferencia_{year}']]

    print(f"\n--- Top 10 déficit {year} ---")
    print(tops[year])

# --- 9. Gráfico comparativo ---
fig, axes = plt.subplots(1, 3, figsize=(20, 6), sharey=True)
pal = sns.color_palette('Reds_r', n_colors=len(horizontes))

for ax, (year, color) in zip(axes, zip(horizontes, pal)):
    df_top = df_clean.sort_values(by=f'diferencia_{year}', ascending=True).head(10)

    sns.barplot(
        x=muni_col,
        y=f'diferencia_{year}',
        data=df_top,
        color=color,
        ax=ax
    )

    ax.set_title(f"Déficit de Bancos {year}", fontsize=12)
    ax.set_xlabel('Municipio')
    ax.set_ylabel('Dif. (Reales - Predichos)' if year == horizontes[0] else '')
    ax.tick_params(axis='x', rotation=45, labelsize=9)

    # Etiquetas sobre las barras
    for p in ax.patches:
        value = p.get_height()
        ax.annotate(
            f'{value:.1f}',
            (p.get_x() + p.get_width() / 2., value),
            ha='center',
            va='bottom',
            fontsize=8,
            color='black',
            xytext=(0, 2),
            textcoords='offset points'
        )

# --- Leyenda ---
axes[0].legend(
    handles=[plt.Rectangle((0,0),1,1,color=pal[i]) for i in range(len(horizontes))],
    labels=[str(y) for y in horizontes],
    title='Horizonte',
    loc='upper right',
    fontsize=9,
    title_fontsize=10
)

plt.suptitle(f"Comparación de Déficit Bancario a 1, 3 y 5 años (base {base_year})", fontsize=14)
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.show()