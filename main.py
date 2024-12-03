# main.py
# Main file for the project

import time
from tqdm import tqdm
from global_var import nba_shots
from shot import NBAShot
import csv
from tf_idf_search import TFIDFSearch
from inverted_index_search import InvertedIndexSearch
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

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
                player_name=row["PLAYER_NAME"].strip().lower(), # KEEP
                position_group=row["POSITION_GROUP"],
                position=row["POSITION"],
                game_date=row["GAME_DATE"],
                game_id=int(row["GAME_ID"]),
                home_team=row["HOME_TEAM"],
                away_team=row["AWAY_TEAM"],
                event_type=row["EVENT_TYPE"], # KEEP
                shot_made=row["SHOT_MADE"] == "TRUE",
                action_type=row["ACTION_TYPE"], # KEEP
                shot_type=row["SHOT_TYPE"], # KEEP
                basic_zone=row["BASIC_ZONE"], # KEEP
                zone_name=row["ZONE_NAME"], # KEEP
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

def main():

    file_path = "shots.csv"  # Replace with the path to your CSV
    print("Loading NBA shots...")
    load_shots_from_csv(file_path)

    tfidf = TFIDFSearch()
    tfidf.preprocessData()
    tfidf.compute_TF_IDF()

    inverted_index = InvertedIndexSearch()
    inverted_index.preprocessData()

    
    print("Welcome to the NBA Shot Search Engine!")
    while True: 
        print("\nPlease choose an option:")
        print("1. Search for NBA shots with TF-IDF Searching Algorithm")
        print("2. Search for NBA shots with Inverted Index Searching Algorithm")
        print("3. Exit")

        choice = input("Enter your choice (1/2/3): ").strip()

        if choice == '1':
            print_choices()
            parameter_choice = input("Enter the number of the parameter you want to query by: ").strip()
            result_count = input("How many results would you like? (Enter 1-218702): ")

            if not result_count.isdigit():
                print("Invalid input. Please enter a number.")
                continue

            result_count = int(result_count)
            if not 1 <= result_count <= 218702:
                print("Invalid input. Please enter a number between 1 and 218,702.")
                continue
            
            if parameter_choice in query_map:
                parameter = query_map[parameter_choice]
                query = input(f"Enter your query for {parameter}: ").strip()

                time_before = time.time()
                results = tfidf.search(parameter, query, result_count)  # Pass parameter, query, and result count
                time_after = time.time()

                print(f"Found {len(results)} results in {time_after - time_before:.4f} seconds:")
                for shot in results:
                    print(shot)
            else:
                print("Invalid parameter choice.")
        elif choice == '2':
            print_choices()

            parameter_choice = input("Enter the number of the parameter you want to query by: ").strip()
            result_count = input("How many results would you like? (Enter 1-218702): ")

            if not result_count.isdigit():
                print("Invalid input. Please enter a number.")
                continue

            result_count = int(result_count)
            if not 1 <= result_count <= 218702:
                print("Invalid input. Please enter a number between 1 and 218,702.")
                continue
            
            if parameter_choice in query_map:
                parameter = query_map[parameter_choice]
                query = input(f"Enter your query for {parameter}: ").strip()

                time_before = time.time()
                results = inverted_index.search(parameter, query, result_count)
                time_after = time.time()

                print(f"Found {len(results)} results in {time_after - time_before:.4f} seconds:")
                for shot in results:
                    print(shot)
        elif choice == '3':
            print("Exiting the program...")
            break
        else:
            print("Invalid choice. Please try again.")

query_map = {
    '1': 'player_name',
    '2': 'event_type',
    '3': 'shot_type',
    '4': 'basic_zone',
    '5': 'zone_name',
    '6': 'action_type'
}

def print_choices():
    print("This program supports querying by the following parameters:")
    print("1. Player name")
    print("2. Event type")
    print("3. Shot type")
    print("4. Basic zone")
    print("5. Zone name")
    print("6. Action type")

@app.route('/api/query', methods=['POST'])
def handle_post():
    # Access JSON data from the request body
    data = request.get_json()  # Parses JSON body
    if data is None:
        return jsonify({"error": "Invalid or missing JSON"}), 400
    
    if 'request_type' not in data:
        return jsonify({"error": "Missing 'request_type' in JSON"}), 400
    
    request_type = data['request_type']

    if 'param' not in data:
        return jsonify({"error": "Missing 'param' in JSON"}), 400
    
    param = data['param']

    if param not in query_map.values():
        return jsonify({"error": "Invalid parameter"}), 400
    
    if 'value' not in data:
        return jsonify({"error": "Missing 'value' in JSON"}), 400
    
    value = data['value']

    if 'result_limit' not in data:
        return jsonify({"error": "Missing 'result_limit' in JSON"}), 400
    
    result_limit = data['result_limit']

    # parse result_limit as an integer
    result_limit = int(result_limit)

    if not isinstance(result_limit, int) or not 1 <= result_limit <= 218702:
        return jsonify({"error": "Invalid 'result_limit' value"}), 400
    
    if request_type == 'tfidf':
        tfidf = TFIDFSearch()
        tfidf.preprocessData()
        tfidf.compute_TF_IDF()

        time_before = time.time()
        results = tfidf.search(param, value, result_limit)
        time_after = time.time()

        time_took = f"{time_after - time_before:.4f}"
        result_count = len(results) 

        return jsonify({"results": [shot.__dict__ for shot in results], "time": time_took, "count": result_count})
    elif request_type == 'iis':
        inverted_index = InvertedIndexSearch()
        inverted_index.preprocessData()

        time_before = time.time()
        results = inverted_index.search(param, value, result_limit)
        time_after = time.time()

        time_took = f"{time_after - time_before:.4f}"
        result_count = len(results)

        return jsonify({"results": [shot.__dict__ for shot in results], "time": time_took, "count": result_count})
    
    return jsonify({"received": data})

def start_server():
    load_shots_from_csv("shots.csv")  # Preload shots for web mode
    tfidf = TFIDFSearch()
    tfidf.preprocessData()
    tfidf.compute_TF_IDF()

    inverted_index = InvertedIndexSearch()
    inverted_index.preprocessData()
    tfidf.preprocessData()
    tfidf.compute_TF_IDF()
    inverted_index.preprocessData()
    app.run(debug=False)

if __name__ == '__main__':
    mode = os.getenv("APP_MODE")

    if mode == '1':
        main()
    elif mode == '2':
        start_server()
    else:
        print("Invalid mode. Starting in server mode.")
        start_server()