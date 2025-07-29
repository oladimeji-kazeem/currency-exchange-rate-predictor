from fredapi import Fred
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor

def fetch_currency_data(pair_code, fred_api_key):
    fred = Fred(api_key=fred_api_key)
    eur_usd = fred.get_series(pair_code)
    interest_rate = fred.get_series('FEDFUNDS')
    cpi = fred.get_series('CPIAUCSL')

    df = pd.concat([eur_usd, interest_rate, cpi], axis=1)
    df.columns = ['rate', 'interest_rate', 'cpi']
    df.index = pd.to_datetime(df.index)
    df.dropna(inplace=True)

    for i in range(1, 4):
        df[f'rate_lag{i}'] = df['rate'].shift(i)
    df.dropna(inplace=True)
    
    return df

def train_mlp_model(df):
    X = df[['rate_lag1', 'rate_lag2', 'rate_lag3', 'interest_rate', 'cpi']]
    y = df['rate'].values.reshape(-1, 1)

    x_scaler = StandardScaler()
    y_scaler = StandardScaler()
    X_scaled = x_scaler.fit_transform(X)
    y_scaled = y_scaler.fit_transform(y).flatten()

    split = int(len(df) * 0.8)
    X_train, X_test = X_scaled[:split], X_scaled[split:]
    y_train, y_test = y_scaled[:split], y_scaled[split:]

    mlp = MLPRegressor(hidden_layer_sizes=(64, 64), max_iter=1000, random_state=42, early_stopping=True)
    mlp.fit(X_train, y_train)
    
    y_pred_scaled = mlp.predict(X_test)
    y_pred = y_scaler.inverse_transform(y_pred_scaled.reshape(-1, 1)).flatten()
    y_test_actual = y_scaler.inverse_transform(y_test.reshape(-1, 1)).flatten()
    
    return df.index[split:], y_test_actual, y_pred