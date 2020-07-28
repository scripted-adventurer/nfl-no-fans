from pyspark import SparkContext, SparkConf

from get_game_data import get_game_data 

def main():
  conf = SparkConf().setAppName('nfl_no_fans').setMaster('local')
  sc = SparkContext(conf=conf)

  # make this temp nfl json 
  games = sc.textFile('/home/jjj/Documents/GitHub/nfl_mongodb/json/games')
  #games = sc.textFile('/home/jjj/Documents/GitHub/nfl_mongodb/json/games/10160000-0574-8451-a9c8-f5ed049dd175.json.gz')

  games = games.map(get_game_data)

  # remove empty elements 
  games = games.filter(lambda x: x)

  games.collect()

  print(games.count())


if __name__ == '__main__':
  main()   