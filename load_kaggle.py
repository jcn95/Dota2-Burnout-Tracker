import pandas as pd
import os
from datetime import datetime

# Paths set for Kaggle data
raw_dota_data = os.path.join("data", "Kaggle")
processed_dota_data = os.path.join("data", "processed")
os.makedirs(processed_dota_data, exist_ok=True)

def load_dota_matches():
    match_path = os.path.join(raw_dota_data, "match.csv")
    player_path = os.path.join(raw_dota_data, "players.csv")

    # The 2 CSV being focused from the Kaggle dataset is matches.csv and players.csv
    dota_match_df = pd.read_csv(match_path, usecols=["match_id", "start_time"])
    dota_player_df = pd.read_csv(player_path, usecols=[
        "match_id", "account_id", "kills", "deaths", "assists"
    ])

    # Clean and merge the player stats
    dota_cleaned = pd.merge(dota_player_df, dota_match_df, on="match_id")
    dota_cleaned.dropna(subset=["account_id"], inplace=True)
    dota_cleaned["player_id"] = dota_cleaned["account_id"].astype(int)
    dota_cleaned["start_time"] = pd.to_datetime(dota_cleaned["start_time"], unit="s")

    # Clean any missing values in the dataframe
    dota_cleaned["kills"] = dota_cleaned["kills"].fillna(0)
    dota_cleaned["assists"] = dota_cleaned["assists"].fillna(0)
    dota_cleaned["deaths"] = dota_cleaned["deaths"].replace(0, 1).fillna(1)

    # Calculate Kill to Death ratio and sort columns
    dota_cleaned["kda_ratio"] = (dota_cleaned["kills"] + dota_cleaned["assists"]) / dota_cleaned["deaths"]
    dota_cleaned = dota_cleaned[["match_id", "player_id", "start_time", "kills", "deaths", "assists", "kda_ratio"]]
    dota_cleaned.sort_values(by=["player_id", "start_time"], inplace=True)

    # Export the cleaned Kaggle dataset
    dota_cleaned.to_csv(os.path.join(processed_dota_data, "kaggle_cleaned.csv"), index=False)
    print(f"Loaded and processed {len(dota_match_df)} Dota 2 matches and {len(dota_player_df)} players from Kaggle match/player data.")
    return dota_cleaned