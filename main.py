from pyspark import SparkContext, SparkConf
import matplotlib.pyplot as plt
from scipy import stats 

from game_data import GameData

class CalculateAndDisplay:
  '''Contains all logic to calculate regressions and display plots for all the
  NFL data from GameData.'''
  def __init__(self):
    self.conf = SparkConf().setAppName('nfl_no_fans').setMaster('local')
    self.sc = SparkContext(conf=self.conf)
    self.data = []
    self.analysis_fields = ['home_yards_per_play', 'away_yards_per_play', 
      'home_penalties', 'away_penalties', 'home_penalty_yards', 
      'away_penalty_yards']
  def _scatterplot(self, x_vals, y_vals, intercept, slope, field):
    plt.scatter(x_vals, y_vals)
    predicted_y = [(intercept + slope * x) for x in x_vals]
    plt.plot(x_vals, predicted_y)
    plt.xlabel('Attendance Percentage')
    plt.ylabel(field)
    plt.show()
  def _linear_regression(self, x_vals, y_vals, dataset, field):
    slope, intercept, r_value, p_value, std_err = stats.linregress(x_vals, y_vals)
    if p_value < 0.1:
      print(f"Found relation for {dataset} {field}")
      print(f"\tslope = {slope}")
      print(f"\tintercept = {intercept}")
      print(f"\tr = {r_value}")
      print(f"\tp = {p_value}")
      print(f"\tstd. error = {std_err}\n")
      self._scatterplot(x_vals, y_vals, intercept, slope, field)
  def get_data(self):
    self.games = self.sc.textFile('/home/jjj/Documents/GitHub/nfl_mongodb/json/games')
    self.games = self.games.map(GameData().get_data)
    # remove empty elements 
    self.games = self.games.filter(lambda x: x)
    self.games.cache()
    self.data = self.games.collect()
  def check_all_stadiums(self):
    attendance = [row['attendance_percent'] for row in self.data] 
    for field in self.analysis_fields:
      if field == 'home_yards_per_play':
        data_points = [(row['home_yards'] / row['home_plays']) for row in self.data]
      elif field == 'away_yards_per_play':
        data_points = [(row['away_yards'] / row['away_plays']) for row in self.data]  
      else:
        data_points = [row[field] for row in self.data]
      self._linear_regression(attendance, data_points, 'All Stadiums', field)
  def check_each_stadium(self):
    for stadium in set([row['stadium'] for row in self.data]):
      for field in self.analysis_fields:
        attendance = []
        data_points = []
        for row in self.data:
          if row['stadium'] == stadium:
            attendance.append(row['attendance_percent'])
            if field == 'home_yards_per_play':
              data_points.append(row['home_yards'] / row['home_plays'])
            elif field == 'away_yards_per_play':
              data_points.append(row['away_yards'] / row['away_plays']) 
            else:
              data_points.append(row[field])
        self._linear_regression(attendance, data_points, stadium, field) 
  def run(self):
    self.get_data()
    self.check_all_stadiums()
    self.check_each_stadium()


if __name__ == '__main__':
  calc = CalculateAndDisplay()
  calc.run()

'''
def main():
  conf = SparkConf().setAppName('nfl_no_fans').setMaster('local')
  sc = SparkContext(conf=conf)

  games = sc.textFile('/home/jjj/Documents/GitHub/nfl_mongodb/json/games')
  #games = sc.textFile('/home/jjj/Documents/GitHub/nfl_mongodb/json/games/10160000-0574-8451-a9c8-f5ed049dd175.json.gz')
  games = games.map(GameData().get_data)
  # remove empty elements 
  games = games.filter(lambda x: x)
  games.cache()

  data = games.collect()
  
  attendance = [row['attendance'] for row in data]
  attendance_percent = [row['attendance_percent'] for row in data]

  # home_penalties = [row['home_penalties'] for row in data]
  # slope, intercept, r_value, p_value, std_err = stats.linregress(attendance_percent, home_penalties)
  # print(f"Home penalties r-value is: {r_value}")
  # print(f"Slope is {slope}")
  
  # away_penalties = [row['away_penalties'] for row in data]
  # slope, intercept, r_value, p_value, std_err = stats.linregress(attendance_percent, away_penalties)
  # print(f"Away penalties r-value is: {r_value}")
  # print(f"Slope is {slope}")

  # home_penalty_yards = [row['home_penalty_yards'] for row in data]
  # slope, intercept, r_value, p_value, std_err = stats.linregress(attendance_percent, home_penalty_yards)
  # print(f"Home penalty_yards r-value is: {r_value}")
  # print(f"Slope is {slope}")

  # away_penalty_yards  = [row['away_penalty_yards'] for row in data]
  # slope, intercept, r_value, p_value, std_err = stats.linregress(attendance_percent, away_penalty_yards)
  # print(f"Away penalty_yards r-value is: {r_value}")
  # print(f"Slope is {slope}")
  
  # check for each team
  # for stadium in set([row['stadium'] for row in data]):
  #   print(f"\nStadium is: {stadium}")
  #   attendance = []
  #   away_penalty_yards = []
  #   home_penalty_yards = []
  #   for row in data:
  #     if row['stadium'] == stadium:
  #       attendance.append(row['attendance_percent'])
  #       away_penalty_yards.append(row['away_penalty_yards'])
  #       home_penalty_yards.append(row['home_penalty_yards'])
  #   slope, intercept, r_value, p_value, std_err = stats.linregress(attendance, home_penalty_yards)
  #   print(f"Home penalty yards r-value is {r_value}")
  #   if abs(r_value) > .3:
  #     print(f"Predicted value for x = -4 is {(intercept + slope * -4)}")
  #     plt.scatter(attendance, home_penalty_yards)
  #     predicted_y = [(intercept + slope * x) for x in attendance]
  #     plt.plot(attendance, predicted_y)
  #     plt.show()
  #   slope, intercept, r_value, p_value, std_err = stats.linregress(attendance, away_penalty_yards)
  #   print(f"Away penalty yards r-value is {r_value}")
  #   if abs(r_value) > .3:
  #     plt.scatter(attendance, away_penalty_yards)
  #     plt.show()

  for stadium in set([row['stadium'] for row in data]):
    print(f"\nStadium is: {stadium}")
    for stat in ['home_points', 'away_points', 'home_drives', 'away_drives', 
    'home_plays', 'away_plays', 'home_first_downs', 'away_first_downs', 
    'home_penalties', 'away_penalties', 'home_penalty_yards', 'away_penalty_yards']:
      attendance = []
      stat_data = []
      for row in data:
        if row['stadium'] == stadium:
          attendance.append(row['attendance_percent'])
          stat_data.append(row[stat])
      slope, intercept, r_value, p_value, std_err = stats.linregress(attendance, stat_data)
      if abs(r_value) > .3:
        print(f"{stat} r-value is {r_value}")
        # plt.scatter(attendance, stat_data)
        # predicted_y = [(intercept + slope * x) for x in attendance]
        # plt.plot(attendance, predicted_y)
        # plt.show()

  for stadium in set([row['stadium'] for row in data]):
    print(f"\nStadium is: {stadium}")
    attendance = []
    home_ypp = []
    away_ypp = []
    for row in data:
      if row['stadium'] == stadium:
        attendance.append(row['attendance_percent'])
        home_ypp.append(row['home_yards'] / row['home_plays'])
        away_ypp.append(row['away_yards'] / row['away_plays'])
    slope, intercept, r_value, p_value, std_err = stats.linregress(attendance, home_ypp)
    if abs(r_value) > .3:
      print(f"Home ypp r-value is {r_value}")
    slope, intercept, r_value, p_value, std_err = stats.linregress(attendance, away_ypp)
    if abs(r_value) > .3:
      print(f"Away ypp r-value is {r_value}")      

  # check r values for various regressions 
  # home_yards_per_play = [row['home_yards'] / row['home_plays'] for row in data]
  # slope, intercept, r_value, p_value, std_err = stats.linregress(attendance_percent, home_yards_per_play)
  # print(f"Home yards per play r-value is: {r_value}")
  # print(f"Slope is {slope}")
  
  # away_yards_per_play = [row['away_yards'] / row['away_plays'] for row in data]
  # slope, intercept, r_value, p_value, std_err = stats.linregress(attendance_percent, away_yards_per_play)
  # print(f"Away yards per play r-value is: {r_value}")
  # print(f"Slope is {slope}")

  # check r values for various regressions 
  home_points = [row['home_points'] for row in data]
  slope, intercept, r_value, p_value, std_err = stats.linregress(attendance_percent, home_points)
  print(f"Home points r-value is: {r_value}")
  print(f"Slope is {slope}")
  
  away_points = [row['away_points'] for row in data]
  slope, intercept, r_value, p_value, std_err = stats.linregress(attendance_percent, away_points)
  print(f"Away points r-value is: {r_value}")
  print(f"Slope is {slope}")
  
  home_drives = [row['home_drives'] for row in data]
  slope, intercept, r_value, p_value, std_err = stats.linregress(attendance_percent, home_drives)
  print(f"Home drives r-value is: {r_value}")
  print(f"Slope is {slope}")
  
  away_drives = [row['away_drives'] for row in data]
  slope, intercept, r_value, p_value, std_err = stats.linregress(attendance_percent, away_drives)
  print(f"Away drives r-value is: {r_value}")
  print(f"Slope is {slope}")

  home_plays = [row['home_plays'] for row in data]
  slope, intercept, r_value, p_value, std_err = stats.linregress(attendance_percent, home_plays)
  print(f"Home plays r-value is: {r_value}")
  print(f"Slope is {slope}")
  
  away_plays = [row['away_plays'] for row in data]
  slope, intercept, r_value, p_value, std_err = stats.linregress(attendance_percent, away_plays)
  print(f"Away plays r-value is: {r_value}")
  print(f"Slope is {slope}")

  home_first_downs = [row['home_first_downs'] for row in data]
  slope, intercept, r_value, p_value, std_err = stats.linregress(attendance_percent, home_first_downs)
  print(f"Home first downs r-value is: {r_value}")
  print(f"Slope is {slope}")
  
  away_first_downs = [row['away_first_downs'] for row in data]
  slope, intercept, r_value, p_value, std_err = stats.linregress(attendance_percent, away_first_downs)
  print(f"Away first downs r-value is: {r_value}")
  print(f"Slope is {slope}")

  home_penalties = [row['home_penalties'] for row in data]
  slope, intercept, r_value, p_value, std_err = stats.linregress(attendance_percent, home_penalties)
  print(f"Home penalties r-value is: {r_value}")
  print(f"Slope is {slope}")
  
  away_penalties = [row['away_penalties'] for row in data]
  slope, intercept, r_value, p_value, std_err = stats.linregress(attendance_percent, away_penalties)
  print(f"Away penalties r-value is: {r_value}")
  print(f"Slope is {slope}")

  home_penalty_yards = [row['home_penalty_yards'] for row in data]
  slope, intercept, r_value, p_value, std_err = stats.linregress(attendance_percent, home_penalty_yards)
  print(f"Home penalty_yards r-value is: {r_value}")
  print(f"Slope is {slope}")

  away_penalty_yards  = [row['away_penalty_yards'] for row in data]
  slope, intercept, r_value, p_value, std_err = stats.linregress(attendance_percent, away_penalty_yards)
  print(f"Away penalty_yards r-value is: {r_value}")
  print(f"Slope is {slope}")

  # plots 
  # plt.hist(attendance)
  # plt.show()

  plt.scatter(attendance, home_penalty_yards)
  plt.show()

  # plt.scatter(attendance, away_penalty_yards)
  # plt.show()

  # plt.scatter(attendance, home_points)
  # plt.show()
  '''
  

  