# Dota2-Burnout-Tracker
Dota 2 model that pulls in real data from Dota players using Kaggle dataset and also simulates player data. This project will showcase a model that analyzes patterns in performance that may indicate burnout and a sign to change behavioral patterns in gaming.

## Features of Dota 2 Model
- Load Kaggle CSV that has real Dota 2 matches 
- Simulate Dota 2 match logs of players whose performance is declining
- Use SQLite in python to perform queries and normalize schemas
- Create visual graphs that show patterns such as Kill to Death ratios
- Evaluate the performance and burnout rates using R2 scores, MAE, precision, recall, and F1 scores

## How to Run Dota 2 Model
1. Download all the files from directory/clone
2. If on linux, create a virtual environment via venv. Use the following commands if on linux:
   
   python -m venv .venv
   source .venv/bin/activate
   pip install -r Requirements.txt

   Once you created the virtual environment, run the following:
   python main.py

   If on other operating systems, this won't be necessary

## Data Sources of Dota 2 Model
- Kaggle: https://www.kaggle.com/datasets/devinanzelmo/dota-2-matches/
- OpenDota API for reference: https://api.opendota.com/api/publicMatches
- Simulated player logs using Python
