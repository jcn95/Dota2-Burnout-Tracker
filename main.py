from src.fetch_data import dota2_simulate_logs
from src.database import dota2_database
from src.preprocess import preprocess_data
from src.model import run_dota_model
from src.visualize import visualize
from src.load_kaggle import load_dota_matches

# Asks user input for type of data source
def main():
    print("Choose the data source you want to use for Dota 2 player logs:")
    print("1) Simulated match data using python script")
    print("2) Kaggle dataset - may take a few seconds")
    choice = input("Enter 1 or 2: ").strip()

# If else statement for 1 or 2 input
    if choice == '1':
        print("Using simulated Dota 2 data")
        dota2_simulate_logs(num_players=10, num_matches=75)
        data_source = 'simulated'
        dota2_database(data_source)
        df = preprocess_data(data_source)

    elif choice == '2':
        print("Loading Kaggle dataset")
        df = load_dota_matches()

    else:
        print("Invalid input, simulated data will be used.")
        dota2_simulate_logs(num_players=10, num_matches=75)
        data_source = 'simulated'
        dota2_database(data_source)
        df = preprocess_data(data_source)

    print("Running model")
    df = run_dota_model(df)

    print("Visualizing results...")
    visualize(df)

if __name__ == '__main__':
    main()

