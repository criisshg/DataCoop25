"""
Predict trends using GradientBoostingRegressor with engineered features.
Generates CSV files with forecasts for target years (2026/2028/2030).
Uses cross-validation and feature importance analysis.
"""
import os
import sys
import math
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import r2_score, mean_absolute_percentage_error
import warnings
warnings.filterwarnings('ignore')

WORKDIR = os.path.dirname(__file__)
CURRENT_YEAR = 2025
TARGET_YEARS = [CURRENT_YEAR + 1, CURRENT_YEAR + 3, CURRENT_YEAR + 5]

def create_features(years, values):
    """Create time series features from year/value pairs."""
    df = pd.DataFrame({'year': years, 'value': values})
    df = df.sort_values('year')
    
    # Basic features
    df['year_norm'] = (df['year'] - df['year'].min()) / (df['year'].max() - df['year'].min())
    
    # Lag features (t-1, t-2)
    df['value_lag1'] = df['value'].shift(1)
    df['value_lag2'] = df['value'].shift(2)
    
    # Growth rates
    df['growth_1y'] = df['value'].pct_change()
    df['growth_2y'] = df['value'].pct_change(periods=2)
    
    # Rolling statistics
    df['roll_mean_2y'] = df['value'].rolling(window=2, min_periods=1).mean()
    df['roll_std_2y'] = df['value'].rolling(window=2, min_periods=1).std()
    
    # Exponential weighted features
    df['ewm_mean'] = df['value'].ewm(span=2, adjust=False).mean()
    
    # Fill NaN with 0 for initial periods
    df = df.fillna(0)
    
    return df

def train_and_predict(years, values, target_years):
    """Train GBoost model and predict target years."""
    if len(years) < 3:
        return {t: np.nan for t in target_years}, np.nan, None
    
    # Create features
    df = create_features(years, values)
    
    # Prepare X/y
    feature_cols = ['year_norm', 'value_lag1', 'value_lag2', 'growth_1y', 
                   'growth_2y', 'roll_mean_2y', 'roll_std_2y', 'ewm_mean']
    X = df[feature_cols].values
    y = df['value'].values
    
    # Configure model
    model = GradientBoostingRegressor(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=3,
        random_state=42
    )
    
    # Time series CV
    tscv = TimeSeriesSplit(n_splits=3)
    cv_scores = []
    
    for train_idx, val_idx in tscv.split(X):
        X_train, X_val = X[train_idx], X[val_idx]
        y_train, y_val = y[train_idx], y[val_idx]
        model.fit(X_train, y_train)
        y_pred = model.predict(X_val)
        score = r2_score(y_val, y_pred)
        cv_scores.append(score)
    
    # Fit on all data
    model.fit(X, y)
    
    # Prepare features for future years
    future_years = pd.DataFrame({'year': target_years})
    future_years['year_norm'] = (future_years['year'] - df['year'].min()) / (df['year'].max() - df['year'].min())
    
    # Use last known values for lags
    last_value = df['value'].iloc[-1]
    last_growth = df['growth_1y'].iloc[-1]
    
    predictions = {}
    for year in target_years:
        idx = future_years['year'] == year
        X_future = np.zeros((1, len(feature_cols)))
        X_future[0, 0] = future_years.loc[idx, 'year_norm'].iloc[0]  # year_norm
        X_future[0, 1] = last_value  # value_lag1
        X_future[0, 2] = df['value'].iloc[-2] if len(df) > 2 else last_value  # value_lag2
        X_future[0, 3] = last_growth  # growth_1y
        X_future[0, 4] = df['growth_2y'].iloc[-1]  # growth_2y
        X_future[0, 5] = df['roll_mean_2y'].iloc[-1]  # roll_mean_2y
        X_future[0, 6] = df['roll_std_2y'].iloc[-1]  # roll_std_2y
        X_future[0, 7] = df['ewm_mean'].iloc[-1]  # ewm_mean
        
        pred = model.predict(X_future)[0]
        predictions[year] = float(pred)
        # Update for next year
        last_value = pred
        last_growth = (pred - last_value) / last_value if last_value != 0 else 0
    
    cv_score = np.mean(cv_scores)
    feature_importance = dict(zip(feature_cols, model.feature_importances_))
    
    return predictions, cv_score, feature_importance

def forecast_alquiler(path):
    """Forecast rent prices using GBoost."""
    df = pd.read_csv(path, sep=';', encoding='utf-8')
    years = []
    for c in df.columns:
        if c.lower().startswith('precio_'):
            try:
                y = int(c.split('_')[1])
                years.append(y)
            except:
                pass
    years = sorted(years)
    
    out_rows = []
    importances = []
    
    for _, row in df.iterrows():
        loc = row['Localización']
        vals = [row.get(f'Precio_{y}', np.nan) for y in years]
        preds, r2, feat_imp = train_and_predict(years, vals, TARGET_YEARS)
        
        out = {'Localizacion': loc, 'last_year': max(years)}
        for y in years:
            out[f'val_{y}'] = row.get(f'Precio_{y}', np.nan)
        for t in TARGET_YEARS:
            out[f'pred_{t}'] = preds[t]
        out['r2'] = r2
        out_rows.append(out)
        
        if feat_imp:
            imp = {'Localizacion': loc}
            imp.update(feat_imp)
            importances.append(imp)
    
    out_df = pd.DataFrame(out_rows)
    out_df.to_csv(os.path.join(WORKDIR, 'alquiler_predictions_gboost.csv'), index=False)
    
    # Save feature importances
    if importances:
        imp_df = pd.DataFrame(importances)
        imp_df.to_csv(os.path.join(WORKDIR, 'alquiler_feature_importance.csv'), index=False)
    
    print('Saved alquiler_predictions_gboost.csv and alquiler_feature_importance.csv')
    return out_df

def forecast_renta(path):
    """Forecast income using GBoost."""
    df = pd.read_csv(path, sep=';', encoding='utf-8', engine='python')
    df = df.rename(columns=lambda s: s.strip())
    dfp = df[df['Provincias'].notna()].copy()
    dfp['Total_num'] = pd.to_numeric(dfp['Total'].astype(str).str.replace(',', '.'), errors='coerce')
    dfp['Periodo'] = pd.to_numeric(dfp['Periodo'], errors='coerce')
    
    groups = dfp.groupby('Provincias')
    out_rows = []
    importances = []
    
    for prov, g in groups:
        g_sorted = g.sort_values('Periodo')
        years = g_sorted['Periodo'].astype(int).tolist()
        vals = g_sorted['Total_num'].tolist()
        
        preds, r2, feat_imp = train_and_predict(years, vals, TARGET_YEARS)
        
        out = {'Provincia': prov, 'last_year': int(max(years))}
        for y, v in zip(years, vals):
            out[f'val_{y}'] = v
        for t in TARGET_YEARS:
            out[f'pred_{t}'] = preds[t]
        out['r2'] = r2
        out_rows.append(out)
        
        if feat_imp:
            imp = {'Provincia': prov}
            imp.update(feat_imp)
            importances.append(imp)
    
    out_df = pd.DataFrame(out_rows)
    out_df.to_csv(os.path.join(WORKDIR, 'renta_predictions_gboost.csv'), index=False)
    
    if importances:
        imp_df = pd.DataFrame(importances)
        imp_df.to_csv(os.path.join(WORKDIR, 'renta_feature_importance.csv'), index=False)
    
    print('Saved renta_predictions_gboost.csv and renta_feature_importance.csv')
    return out_df

def forecast_population(path):
    """Forecast population using GBoost (province level)."""
    df = pd.read_csv(path, sep=';', encoding='utf-8', engine='python')
    df.columns = [c.strip('\ufeff').strip() for c in df.columns]
    
    def prov_code(m):
        if pd.isna(m):
            return None
        s = str(m).strip()
        parts = s.split()
        code = parts[0]
        if len(code) >= 2:
            return code[:2]
        return None
    
    df['PROV'] = df[df.columns[0]].apply(prov_code)
    df['Periodo'] = pd.to_numeric(df['Periodo'], errors='coerce')
    df['Total_num'] = pd.to_numeric(df['Total'].astype(str).str.replace('.', '').replace('', np.nan), errors='coerce')
    
    # Keep years >= 2000 and aggregate by province
    df2 = df[(df['Periodo'] >= 2000) & (df['Periodo'] <= CURRENT_YEAR) & (df['Sexo'] == 'Total')]
    groups = df2.groupby(['PROV','Periodo'])['Total_num'].sum().reset_index()
    
    provs = groups['PROV'].unique()
    out_rows = []
    importances = []
    
    for prov in provs:
        g = groups[groups['PROV'] == prov].sort_values('Periodo')
        years = g['Periodo'].astype(int).tolist()
        vals = g['Total_num'].tolist()
        
        preds, r2, feat_imp = train_and_predict(years, vals, TARGET_YEARS)
        
        out = {'PROV': prov, 'last_year': int(max(years))}
        for y, v in zip(years, vals):
            out[f'val_{y}'] = v
        for t in TARGET_YEARS:
            out[f'pred_{t}'] = preds[t]
        out['r2'] = r2
        out_rows.append(out)
        
        if feat_imp:
            imp = {'PROV': prov}
            imp.update(feat_imp)
            importances.append(imp)
    
    out_df = pd.DataFrame(out_rows)
    out_df.to_csv(os.path.join(WORKDIR, 'poblacion_predictions_prov_gboost.csv'), index=False)
    
    if importances:
        imp_df = pd.DataFrame(importances)
        imp_df.to_csv(os.path.join(WORKDIR, 'poblacion_feature_importance.csv'), index=False)
    
    print('Saved poblacion_predictions_prov_gboost.csv and poblacion_feature_importance.csv')
    return out_df

def merge_predictions(alq_df, renta_df, pop_df):
    """Merge predictions from different models."""
    renta_keys = renta_df['Provincia'].tolist()
    renta_map = {k.lower(): k for k in renta_keys}
    
    merged_rows = []
    for _, row in alq_df.iterrows():
        loc = str(row['Localizacion'])
        key = None
        lk = loc.lower()
        
        if lk in renta_map:
            key = renta_map[lk]
        else:
            for prov in renta_keys:
                if prov.lower() in lk or lk in prov.lower():
                    key = prov
                    break
        
        renta_row = renta_df[renta_df['Provincia'] == key] if key is not None else pd.DataFrame()
        
        out = {
            'Localizacion': loc,
            'pred_rent_2026': row.get('pred_2026'),
            'pred_rent_2028': row.get('pred_2028'),
            'pred_rent_2030': row.get('pred_2030'),
            'alq_r2': row.get('r2')
        }
        
        if not renta_row.empty:
            out['pred_renta_2026'] = float(renta_row['pred_2026'].iloc[0])
            out['pred_renta_2028'] = float(renta_row['pred_2028'].iloc[0])
            out['pred_renta_2030'] = float(renta_row['pred_2030'].iloc[0])
            out['renta_r2'] = float(renta_row['r2'].iloc[0])
        else:
            out['pred_renta_2026'] = out['pred_renta_2028'] = out['pred_renta_2030'] = np.nan
            out['renta_r2'] = np.nan
        
        merged_rows.append(out)
    
    merged_df = pd.DataFrame(merged_rows)
    merged_df.to_csv(os.path.join(WORKDIR, 'combined_predictions_prov_gboost.csv'), index=False)
    print('Saved combined_predictions_prov_gboost.csv')
    return merged_df

if __name__ == '__main__':
    base = WORKDIR
    alquiler_path = os.path.join(base, 'alquiler_precios_unido_imputed.csv')
    renta_path = os.path.join(base, 'evolucion_renta.csv')
    poblacion_path = os.path.join(base, 'evolucion_poblacion.csv')
    
    if os.path.exists(alquiler_path):
        alq = forecast_alquiler(alquiler_path)
    else:
        print('alquiler file not found:', alquiler_path)
        alq = pd.DataFrame()
    
    if os.path.exists(renta_path):
        ren = forecast_renta(renta_path)
    else:
        print('renta file not found:', renta_path)
        ren = pd.DataFrame()
    
    if os.path.exists(poblacion_path):
        pop = forecast_population(poblacion_path)
    else:
        print('poblacion file not found:', poblacion_path)
        pop = pd.DataFrame()
    
    if not alq.empty and not ren.empty:
        merge_predictions(alq, ren, pop)
    
    print('Done')
