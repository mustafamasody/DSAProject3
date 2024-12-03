# main.py
# Main file for the project

from tqdm import tqdm
from global_var import nba_shots
from shot import NBAShot
import csv
from flask import request, jsonify
from tf_idf_search import TFIDFSearch

# ok were now merged

def load_shots_from_csv(file_path):
    csv_file = file_path  # Use the provided file path
    total_lines = sum(1 for _ in open(csv_file, encoding='utf-8')) - 1  # Total rows (excluding header)

    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in tqdm(reader, total=total_lines, desc="Loading NBA Shots", unit="shots"):
            shot = NBAShot(
                season_1=int(row["SEASON_1"]),
                season_2=row["SEASON_2"],
                team_id=int(row["TEAM_ID"]),
                team_name=row["TEAM_NAME"],
                player_id=int(row["PLAYER_ID"]),
                player_name=row["PLAYER_NAME"],
                position_group=row["POSITION_GROUP"],
                position=row["POSITION"],
                game_date=row["GAME_DATE"],
                game_id=int(row["GAME_ID"]),
                home_team=row["HOME_TEAM"],
                away_team=row["AWAY_TEAM"],
                event_type=row["EVENT_TYPE"],
                shot_made=row["SHOT_MADE"] == "TRUE",
                action_type=row["ACTION_TYPE"],
                shot_type=row["SHOT_TYPE"],
                basic_zone=row["BASIC_ZONE"],
                zone_name=row["ZONE_NAME"],
                zone_abb=row["ZONE_ABB"],
                zone_range=row["ZONE_RANGE"],
                loc_x=float(row["LOC_X"]),
                loc_y=float(row["LOC_Y"]),
                shot_distance=int(row["SHOT_DISTANCE"]),
                quarter=int(row["QUARTER"]),
                mins_left=int(row["MINS_LEFT"]),
                secs_left=int(row["SECS_LEFT"])
            )
            nba_shots.append(shot)

# @app.route("/search", methods=["GET"])
# def search_shots():
#     query = request.args.get("query", "")
#     if not query:
#         return jsonify({"Error: Query parameter missing"}), 400
#     results = tfidf.search(query)
#     return jsonify([str(shot) for shot in results])

def main():

    file_path = "NBA_2024_Shots.csv"  # Replace with the path to your CSV
    print("Loading NBA shots...")
    load_shots_from_csv(file_path)

    tfidf = TFIDFSearch()
    tfidf.preprocessData()
    tfidf.compute_TF_IDF()
    
    print("Welcome message")
    while True: 
        print("\nPlease choose an option:")
        print("1. Search for NBA shots (with filters)")
        print("2. Search with AI")
        print("3. Exit")

        choice = input("Enter your choice (1/2/3): ").strip()

        if choice == '1':
            print("This program supports querying by the following parameters:")
            print("1. Player name")
            print("2. Event type")
            print("3. Shot type")
            print("4. Basic zone")
            print("5. Zone name")
            print("6. Action type")

            parameter_choice = input("Enter the number of the parameter you want to query by: ").strip()
            
            query_map = {
                '1': 'player_name',
                '2': 'event_type',
                '3': 'shot_type',
                '4': 'basic_zone',
                '5': 'zone_name',
                '6': 'action_type'
            }
            
            if parameter_choice in query_map:
                parameter = query_map[parameter_choice]
                query = input(f"Enter your query for {parameter}: ").strip()
                results = tfidf.search(parameter, query)  # Pass both parameter and query
                print(f"Found {len(results)} results:")
                for shot in results:
                    print(shot)
            else:
                print("Invalid parameter choice.")
        elif choice == '2':
            print("2")
        elif choice == '3':
            print("Exiting the program...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()