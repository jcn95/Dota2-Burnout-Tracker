import os
import json
import random
import numpy as np
from datetime import datetime, timedelta

# Create folder for the raw simulated data
raw_dota_data = os.path.join("data", "raw")
os.makedirs(raw_dota_data, exist_ok=True)

def dota2_simulate_logs(num_players=10, num_matches=75):
    players = []
    matches = []
    dotaplayer_log = []

    # Set the base time for the simulated player logs
    base_time = datetime(2022, 6, 1)

    # Create simulated Dota 2 player profiles
    for dotaplayer_num in range(1, num_players + 1):
        dotaplayer_id = 1000 + dotaplayer_num
        players.append({
            "player_id": dotaplayer_id,
            "nickname": f"Player{dotaplayer_num}",
            "country": random.choice(["USA", "Canada", "Europe", "Brazil", "Asia"])
        })

    # Assign 5 matches for simulated burnout
        burnout_matches = random.sample(range(10, num_matches), 5) 

        for dotagame_index in range(1, num_matches + 1):
            match_id = dotaplayer_id * 100 + dotagame_index
            start_time = base_time + timedelta(days=dotagame_index)
            duration = random.randint(1500, 3600)
            radiant_win = random.choice([True, False])

            matches.append({
                "match_id": match_id,
                "start_time": start_time.isoformat(),
                "duration": duration,
                "radiant_win": radiant_win
            })

            #Simulated raw stats
            kills = random.randint(0, 15)
            deaths = random.randint(1, 10)
            assists = random.randint(0, 20)

            #Simulate burnout from the random poor kill scalings
            if dotagame_index in burnout_matches:
                kill_scaling = random.choice([0.3, 0.4, 0.5])
                dota_kills = int(kills * kill_scaling)
                assists = int(assists * random.uniform(0.2, 0.5))
                true_burnout = True
            else:
                true_burnout = False

            dotaplayer_log.append({
                "match_id": match_id,
                "player_id": dotaplayer_id,
                "kills": kills,
                "deaths": deaths,
                "assists": assists,
                "win": radiant_win,
                "true_burnout": true_burnout
            })

    # JSON files for the simulated data
    with open(os.path.join(raw_dota_data, "players.json"), "w") as f:
        json.dump(players, f)
    with open(os.path.join(raw_dota_data, "matches_simulated.json"), "w") as f:
        json.dump(matches, f)
    with open(os.path.join(raw_dota_data, "dotaplayer_log.json"), "w") as f:
        json.dump(dotaplayer_log, f)

    print("Finished simulating Dota 2 match data for all players. Let's analyze now.")
