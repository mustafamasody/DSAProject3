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

load_dotenv()  # Load environment variables from a .env file

app = Flask(__name__)

# Enable Cross-Origin Resource Sharing for all routes under /api/*
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

def load_shots_from_csv(file_path):
    """Generator function to load NBA shots from a CSV file."""
    with open(file_path, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Yield a NBAShot instance for each row in the CSV
            yield NBAShot(
                season_1=int(row["SEASON_1"]),
                season_2=row["SEASON_2"],
                team_id=int(row["TEAM_ID"]),
                team_name=row["TEAM_NAME"],
                player_id=int(row["PLAYER_ID"]),
                player_name=row["PLAYER_NAME"].strip().lower(),
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

# Load shots from CSV and append to the global nba_shots list
for shot in load_shots_from_csv("shots.csv"):
    nba_shots.append(shot)

def main():
    # Initialize search algorithms
    tfidf = TFIDFSearch()
    tfidf.preprocessData()
    tfidf.compute_TF_IDF()

    inverted_index = InvertedIndexSearch()
    inverted_index.preprocessData()

    print("Welcome to the NBA Shot Search Engine!")
    while True:
        # Display the main menu
        print("\nPlease choose an option:")
        print("1. Search for NBA shots with TF-IDF Searching Algorithm")
        print("2. Search for NBA shots with Inverted Index Searching Algorithm")
        print("3. Exit")

        choice = input("Enter your choice (1/2/3): ").strip()

        if choice == '1':
            # TF-IDF search selected
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

                # Measure search time
                time_before = time.time()
                results = tfidf.search(parameter, query, result_count)  # Pass parameter, query, and result count
                time_after = time.time()

                print(f"Found {len(results)} results in {time_after - time_before:.4f} seconds:")
                for shot in results:
                    print(shot)
            else:
                print("Invalid parameter choice.")
        elif choice == '2':
            # Inverted Index search selected
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

                # Measure search time
                time_before = time.time()
                results = inverted_index.search(parameter, query, result_count)
                time_after = time.time()

                print(f"Found {len(results)} results in {time_after - time_before:.4f} seconds:")
                for shot in results:
                    print(shot)
            else:
                print("Invalid parameter choice.")
        elif choice == '3':
            # Exit the program
            print("Exiting the program...")
            break
        else:
            print("Invalid choice. Please try again.")

# Mapping of user input to parameter names
query_map = {
    '1': 'player_name',
    '2': 'event_type',
    '3': 'shot_type',
    '4': 'basic_zone',
    '5': 'zone_name',
    '6': 'action_type'
}

def print_choices():
    """Print the list of searchable parameters."""
    print("This program supports querying by the following parameters:")
    print("1. Player name")
    print("2. Event type")
    print("3. Shot type")
    print("4. Basic zone")
    print("5. Zone name")
    print("6. Action type")

@app.route('/api/query', methods=['POST'])
def handle_post():
    """Handle POST requests for search queries via the API."""
    data = request.get_json()  # Parse JSON body
    if data is None:
        return jsonify({"error": "Invalid or missing JSON"}), 400

    # Validate required fields in the JSON data
    required_fields = ['request_type', 'param', 'value', 'result_limit']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing '{field}' in JSON"}), 400

    request_type = data['request_type']
    param = data['param']
    value = data['value']
    result_limit = data['result_limit']

    # Validate parameter and result_limit
    if param not in query_map.values():
        return jsonify({"error": "Invalid parameter"}), 400

    try:
        result_limit = int(result_limit)
        if not 1 <= result_limit <= 218702:
            raise ValueError
    except ValueError:
        return jsonify({"error": "Invalid 'result_limit' value"}), 400

    # Process the search based on request type
    if request_type == 'tfidf':
        tfidf = TFIDFSearch()
        tfidf.preprocessData()
        tfidf.compute_TF_IDF()

        time_before = time.time()
        results = tfidf.search(param, value, result_limit)
        time_after = time.time()

        time_took = f"{time_after - time_before:.4f}"
        result_count = len(results)

        # Return search results as JSON
        return jsonify({"results": [shot.__dict__ for shot in results], "time": time_took, "count": result_count})
    elif request_type == 'iis':
        inverted_index = InvertedIndexSearch()
        inverted_index.preprocessData()

        time_before = time.time()
        results = inverted_index.search(param, value, result_limit)
        time_after = time.time()

        time_took = f"{time_after - time_before:.4f}"
        result_count = len(results)

        # Return search results as JSON
        return jsonify({"results": [shot.__dict__ for shot in results], "time": time_took, "count": result_count})

    return jsonify({"error": "Invalid 'request_type' value"}), 400

def start_server():
    """Start the Flask web server."""
    tfidf = TFIDFSearch()
    tfidf.preprocessData()
    tfidf.compute_TF_IDF()

    inverted_index = InvertedIndexSearch()
    inverted_index.preprocessData()

    app.run(debug=False)

if __name__ == '__main__':
    mode = os.getenv("APP_MODE")

    print("Loading data...")

    if mode == '1':
        main()  # Run in command-line mode
    elif mode == '2':
        start_server()  # Run in server mode
    else:
        print("Invalid mode. Starting in server mode.")
        start_server()
