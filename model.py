# model.py

from sklearn.ensemble import RandomForestClassifier
import numpy as np

def entrenar_modelo(data):
    """Entrena un modelo Random Forest"""
    features = ['RSI', 'MACD', 'SMA_20', 'SMA_50']
    X = data[features]
    y = np.where(data['close'].shift(-1) > data['close'], 1, 0)
    X = X[:-1]
    y = y[:-1]

    modelo = RandomForestClassifier(n_estimators=100)
    modelo.fit(X, y)

    return modelo, X.iloc[-1].values.reshape(1, -1)