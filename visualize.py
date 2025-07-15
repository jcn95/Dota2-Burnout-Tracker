import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# If user has linux and uses a terminal that doesn't have a GUI then this will be necessary
matplotlib.use("TkAgg")
sns.set(style="whitegrid")

# Matplotlib used to create visual graphs of KDA and burnout flags
def visualize(df):
    sample_players = df['player_id'].unique()[:10]

    plt.figure(figsize=(12, 6))
    for dotaplayer_id in sample_players:
        subset = df[df['player_id'] == dotaplayer_id]
        plt.plot(subset['start_time'], subset['kda_ratio'], label=f"Player {dotaplayer_id}")
    plt.title("KDA Ratio")
    plt.legend()
    plt.savefig("dota2_kda.png")
    plt.show()

    if 'burnout_flag' in df.columns:
        plt.figure(figsize=(12, 6))
        burnout = df[df['burnout_flag']]
        plt.scatter(burnout['start_time'], burnout['kda_ratio'], color='red', label='Burnout')
        plt.title("Detected Burnouts")
        plt.legend()
        plt.savefig("dota2_burnout.png")
        plt.show()


