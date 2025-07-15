import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error, precision_score, recall_score, f1_score
from scipy.stats import zscore

# Applies burnout flags based on z-score and uses linear regression model

def run_dota_model(df):
    df['kda_zscore'] = df.groupby('player_id')['kda_ratio'].transform(zscore)
    df['burnout_flag'] = df['kda_zscore'] < -0.5
    df['timestamp'] = df['start_time'].astype(int) // 10**9
    lr_model = LinearRegression().fit(df[['timestamp']], df['kda_ratio'])
    prediction = lr_model.predict(df[['timestamp']])
    print("R2:", r2_score(df['kda_ratio'], prediction), "MAE:", mean_absolute_error(df['kda_ratio'], prediction))

# Determines if prediction is actually true and if there is an actual burnout
    if 'true_burnout' in df.columns:
        y_true = df['true_burnout']
        y_prediction = df['burnout_flag']
        print("Precision:", precision_score(y_true, y_prediction, zero_division=0)) # In case there is a ratio with 0, zero_division will just return 0 instead of error
        print("Recall:", recall_score(y_true, y_prediction, zero_division=0))
        print("F1:", f1_score(y_true, y_prediction, zero_division=0)) 
        print("Burnout flags:", y_prediction.sum(), "out of", len(df))
    else:
        print("No ground truth")

    return df