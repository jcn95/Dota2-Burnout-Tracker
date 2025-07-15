import sqlite3
import json
import os

raw_dota_data = os.path.join("data", "raw")
processed_dota_data = os.path.join("data", "processed")
os.makedirs(processed_dota_data, exist_ok=True)

# In case the table has not been created already
dota_schema_sql = """
CREATE TABLE IF NOT EXISTS players (
    player_id INTEGER PRIMARY KEY,
    nickname TEXT,
    country TEXT
);

CREATE TABLE IF NOT EXISTS matches (
    match_id INTEGER PRIMARY KEY,
    start_time TEXT,
    duration INTEGER,
    radiant_win BOOLEAN
);

CREATE TABLE IF NOT EXISTS performance_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id INTEGER,
    player_id INTEGER,
    kills INTEGER,
    deaths INTEGER,
    assists INTEGER,
    win BOOLEAN,
    true_burnout BOOLEAN,
    FOREIGN KEY (match_id) REFERENCES matches (match_id),
    FOREIGN KEY (player_id) REFERENCES players (player_id)
);
"""

# Database that either creates simulated data source or pulls from kaggle
def dota2_database(data_source='simulated'):
    db_path = os.path.join(processed_dota_data, "dota2_burnout.db")
    dota_db = sqlite3.connect(db_path)
    dota_db.executescript(dota_schema_sql)

    if data_source == 'simulated':
        players = json.load(open(os.path.join(raw_dota_data, "players.json")))
        matches = json.load(open(os.path.join(raw_dota_data, "matches_simulated.json")))
        stats = json.load(open(os.path.join(raw_dota_data, "dotaplayer_log.json")))

        for dotaplayer in players:
            dota_db.execute("INSERT OR IGNORE INTO players VALUES (?, ?, ?)", (dotaplayer['player_id'], dotaplayer['nickname'], dotaplayer['country']))
        for dotamatch in matches:
            dota_db.execute("INSERT OR IGNORE INTO matches VALUES (?, ?, ?, ?)", (dotamatch['match_id'], dotamatch['start_time'], dotamatch['duration'], dotamatch['radiant_win']))
        for dotastat in stats:
            dota_db.execute("INSERT INTO performance_stats (match_id, player_id, kills, deaths, assists, win, true_burnout) VALUES (?, ?, ?, ?, ?, ?, ?)",
                         (dotastat['match_id'], dotastat['player_id'], dotastat['kills'], dotastat['deaths'], dotastat['assists'], dotastat['win'], dotastat['true_burnout']))

    elif data_source == 'real':
        matches = json.load(open(os.path.join(raw_dota_data, "matches.json")))
        for idx, dotamatch in enumerate(matches):
            dota_db.execute("INSERT OR IGNORE INTO matches VALUES (?, ?, ?, ?)",
                         (dotamatch['match_id'], "1970-01-01T00:00:00", dotamatch.get('duration', 1800), dotamatch.get('radiant_win', False)))
            dota_db.execute("INSERT INTO performance_stats (match_id, player_id, kills, deaths, assists, win, true_burnout) VALUES (?, ?, ?, ?, ?, ?, ?)",
                         (dotamatch['match_id'], dotamatch['radiant_team'], dotamatch.get('radiant_score', 0), dotamatch.get('dire_score', 0), 0, dotamatch.get('radiant_win', False), False))

    dota_db.commit()
    dota_db.close()
    print("Database setup has been completed")
