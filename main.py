# main.py
# Main file for the project

from flask import Flask
from tqdm import tqdm
from global_var import nba_shots
from shot import NBAShot
import csv

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

app = Flask(__name__)

file_path = "NBA_2024_Shots.csv"  # Replace with the path to your CSV
print("Starting server and loading NBA shots...")
load_shots_from_csv(file_path)

@app.route("/test")
def hello():
    return "Hello, World!"

if __name__ == "__main__":
    app.run(debug=True)