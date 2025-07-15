import sqlite3
import pandas as pd
import os

processed_dota_path = os.path.join("data", "processed")

# Uses SQL structure to read and preprocess Dota player data
def preprocess_data(data_source='simulated'):
    db_path = os.path.join(processed_dota_path, "dota2_burnout.db")
    dota_db = sqlite3.connect(db_path)
    df = pd.read_sql_query("""
        SELECT ps.*, m.start_time, m.duration, m.radiant_win
        FROM performance_stats ps JOIN matches m ON ps.match_id = m.match_id
    """, dota_db)
    dota_db.close()

    if data_source == 'simulated':
        df['start_time'] = pd.to_datetime(df['start_time'])
        df['kda_ratio'] = (df['kills'] + df['assists']) / df['deaths'].replace(0, 1)
        df.sort_values(by=['player_id', 'start_time'], inplace=True)
    else:
        df['start_time'] = pd.to_datetime('2020-06-01')
        df['kda_ratio'] = df['kills'] / df['deaths'].replace(0, 1)
        df.sort_values(by=['match_id'], inplace=True)

    df.to_csv(os.path.join(processed_dota_path, "cleaned_performance.csv"), index=False)
    print("Preprocessed and cleaned data. The CSV has been saved.")
    return df
