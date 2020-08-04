import gzip
import json
import datetime

from reference import neutral_site_fields, standardized_field_names, stadium_capacities

class GameData:
  def __init__(self):
    '''Contains all logic to take each JSON game file from Spark and output a dict
    containing the relevant data from that game.'''
    self.output_data = {'stadium': '', 'attendance': 0, 'attendance_percent': 0, 
      'home_plays': 0, 'away_plays': 0, 'home_yards': 0, 'away_yards': 0, 
      'home_penalties': 0, 'away_penalties': 0, 'home_penalty_yards': 0, 
      'away_penalty_yards': 0}
    self.is_valid = True  
  def check_regular_season(self):
    # skip preseason and postseason games
    gametime = datetime.datetime.strptime(self.game["gameTime"], 
      "%Y-%m-%dT%H:%M:%S.000Z")
    # February through August is not regular season
    if gametime.month >= 2 and gametime.month <= 8:
      self.is_valid = False
    # any game in September before the 6th is still preseason
    elif gametime.month == 9 and gametime.day < 6:
      self.is_valid = False
    # any game in January after the 3rd is postseason
    elif gametime.month == 1 and gametime.day > 3:
      self.is_valid = False
  def check_missing_data(self):
    if not self.game["stadium"]:
      self.is_valid = False
    if not self.game["attendance"]:
      self.is_valid = False
    try:
      self.game["drives"]
      self.game["plays"]
    except KeyError:
      self.is_valid = False    
  def check_neutral_site(self):
    if self.game["stadium"] in neutral_site_fields:
      self.is_valid = False  
  def get_stadium_and_attendance(self):
    self.output_data['stadium'] = standardized_field_names[self.game["stadium"]]
    self.output_data['attendance'] = int(self.game["attendance"].replace(',', ''))
    self.output_data['attendance_percent'] = (self.output_data['attendance'] / 
      stadium_capacities[self.output_data['stadium']])
  def get_yards(self):
    for drive in self.game["drives"]:
      try:
        if drive["possessionTeam"]["abbreviation"] == self.home_team:
          self.output_data['home_yards'] += drive["yards"] + drive["yardsPenalized"]
        if drive["possessionTeam"]["abbreviation"] == self.away_team:
          self.output_data['away_yards'] += drive["yards"] + drive["yardsPenalized"]
      # skip drives with missing data
      except TypeError:
        pass
  def get_plays_and_penalties(self):
    for play in self.game["plays"]:
      try:
        if play["possessionTeam"]["abbreviation"] == self.home_team:
          self.output_data['home_plays'] += 1
        if play["possessionTeam"]["abbreviation"] == self.away_team:
          self.output_data['away_plays'] += 1
        if play["penaltyOnPlay"]:
          # check for the play stat with the penalty info (#93)
          for play_stat in play["playStats"]:
            if play_stat["statId"] == 93:
              if play_stat["team"]["abbreviation"] == self.home_team:
                self.output_data['home_penalties'] += 1
                self.output_data['home_penalty_yards'] += play_stat["yards"]
              if play_stat["team"]["abbreviation"] == self.away_team:
                self.output_data['away_penalties'] += 1
                self.output_data['away_penalty_yards'] += play_stat["yards"]  
      # skip plays with missing data
      except TypeError:
        pass
  def check_missing_plays(self):
    if self.output_data["home_plays"] == 0 or self.output_data["away_plays"] == 0:
      self.is_valid = False
  def get_data(self, game_file):
    self.game = json.loads(game_file)
    self.game = self.game["data"]["viewer"]["gameDetail"]
    self.home_team = self.game["homeTeam"]["abbreviation"]
    self.away_team = self.game["visitorTeam"]["abbreviation"]
    self.check_regular_season()
    self.check_missing_data()
    self.check_neutral_site()
    if self.is_valid:
      self.get_stadium_and_attendance()
      self.get_yards()
      self.get_plays_and_penalties()
      self.check_missing_plays()
    if self.is_valid:
      return self.output_data
    else:
      return {}