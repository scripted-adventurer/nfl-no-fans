import gzip
import json

def get_game_data(game_file):
  # takes a compressed JSON game file and outputs a a dict containing the revelant 
  # data from that game
  game = json.loads(game_file)
  game = game["data"]["viewer"]["gameDetail"]
  # skip preseason and postseason games
  # later than or equal to 

  home_team = game["homeTeam"]["abbreviation"]
  away_team = game["visitorTeam"]["abbreviation"]
  output_data = {'attendance': 0, 'home_points': 0, 'away_points': 0, 
    'home_drives': 0, 'away_drives': 0, 'home_plays': 0, 'away_plays': 0, 
    'home_first_downs': 0, 'away_first_downs': 0, 'home_penalties': 0, 
    'away_penalties': 0, 'home_penalty_yards': 0, 'away_penalty_yards': 0}
  # skip games without attendance info
  if not game["attendance"]:
    return {}
  else:
    output_data['attendance'] = int(game["attendance"].replace(',', ''))
  # skip games with missing data
  try:
    output_data['home_points'] = game["homePointsTotal"]
    output_data['away_points'] = game["visitorPointsTotal"]
    game["drives"]
    game["plays"]
  except KeyError:
    return {}

  for drive in game["drives"]:
    try:
      if drive["possessionTeam"]["abbreviation"] == home_team:
        output_data['home_drives'] += 1
      if drive["possessionTeam"]["abbreviation"] == away_team:
        output_data['away_drives'] += 1
    # skip drives with missing data
    except TypeError:
      pass

  for play in game["plays"]:
    try:
      if play["possessionTeam"]["abbreviation"] == home_team:
        output_data['home_plays'] += 1
      if play["possessionTeam"]["abbreviation"] == away_team:
        output_data['away_plays'] += 1  
      if play["possessionTeam"]["abbreviation"] == home_team and play["firstDown"]:
        output_data['home_first_downs'] += 1
      if play["possessionTeam"]["abbreviation"] == away_team and play["firstDown"]:
        output_data['away_first_downs'] += 1  
      if play["penaltyOnPlay"]:
        # check for the play stat with the penalty info (#93)
        for play_stat in play["playStats"]:
          if play_stat["statId"] == 93:
            if play_stat["team"]["abbreviation"] == home_team:
              output_data['home_penalties'] += 1
              output_data['home_penalty_yards'] += play_stat["yards"]
            if play_stat["team"]["abbreviation"] == away_team:
              output_data['away_penalties'] += 1
              output_data['away_penalty_yards'] += play_stat["yards"]  
    # skip plays with missing data
    except TypeError:
      pass

  return output_data