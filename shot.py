

class NBAShot:
    def __init__(self, season_1, season_2, team_id, team_name, player_id, player_name,
                 position_group, position, game_date, game_id, home_team, away_team,
                 event_type, shot_made, action_type, shot_type, basic_zone, zone_name,
                 zone_abb, zone_range, loc_x, loc_y, shot_distance, quarter, mins_left, secs_left):
        self.season_1 = season_1
        self.season_2 = season_2
        self.team_id = team_id
        self.team_name = team_name
        self.player_id = player_id
        self.player_name = player_name
        self.position_group = position_group
        self.position = position
        self.game_date = game_date
        self.game_id = game_id
        self.home_team = home_team
        self.away_team = away_team
        self.event_type = event_type
        self.shot_made = shot_made
        self.action_type = action_type
        self.shot_type = shot_type
        self.basic_zone = basic_zone
        self.zone_name = zone_name
        self.zone_abb = zone_abb
        self.zone_range = zone_range
        self.loc_x = loc_x
        self.loc_y = loc_y
        self.shot_distance = shot_distance
        self.quarter = quarter
        self.mins_left = mins_left
        self.secs_left = secs_left

    def __str__(self):
        return f"{self.player_name} ({self.position}) - {self.event_type} ({self.shot_type}) at {self.shot_distance} ft."

    def time_remaining_in_quarter(self):
        """Returns the time remaining in the quarter in seconds."""
        return self.mins_left * 60 + self.secs_left

    def is_three_pointer(self):
        """Returns True if the shot is a 3PT shot."""
        return self.shot_type == "3PT"

    def is_successful(self):
        """Returns True if the shot was made."""
        return self.shot_made

# Example of creating an object
entry = NBAShot(
    season_1=2024, season_2="2023-24", team_id=1610612737, team_name="Atlanta Hawks",
    player_id=1627749, player_name="Dejounte Murray", position_group="G", position="SG",
    game_date="12-08-2023", game_id=22301218, home_team="PHI", away_team="ATL",
    event_type="Missed Shot", shot_made=False, action_type="Pullup Jump shot",
    shot_type="3PT Field Goal", basic_zone="Above the Break 3", zone_name="Right Side Center",
    zone_abb="RC", zone_range="24+ ft.", loc_x=-11, loc_y=31.65, shot_distance=28,
    quarter=4, mins_left=0, secs_left=30
)

# Using the object
print(entry)  # Dejounte Murray (SG) - Missed Shot (3PT Field Goal) at 28 ft.
print(f"Time remaining in quarter: {entry.time_remaining_in_quarter()} seconds")
print(f"Is a three-pointer: {entry.is_three_pointer()}")
print(f"Was the shot successful: {entry.is_successful()}")
