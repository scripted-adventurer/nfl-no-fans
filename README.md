# Understanding a Potentially Fan-Less 2020 NFL Season #

The goal of this project is to understand what impact a reduction or elimination of fans at NFL games in the 2020 season might have on the actual on-field product. American football is an interesting sport to consider this question for, because communication (in the form of play calling, audibles, and the snap count) is an integral part of every play. 

While strategies to deal with loud crowd noise exist (like hand signals, silent counts, etc.), these strategies may hinder the team's overall effectiveness. Consider that teams typically employ these stragies only when they need to, suggesting that teams operate better when they don't use them. 

## Key Questions For Analysis ##

- Is there a meaningful relationsip between the size of the crowd and any quantifiable game outcome (like points scored, penalties, etc.)?
- If such relationships exist, what predictions can we make about how games will be different without any fans? 

## Dataset ##

To perform this analysis, I will be using a dataset of NFL regular season game data downloaded in JSON form from the NFL.com API in [another project](https://github.com/scripted-adventurer/nfl-mongodb). Attendance data is only available for 2015 to 2019, and I will further restrict the data to regular season games only. 

## Method ##

For each game in the data set, I will look at 6 different variables, split into groups for the home and away teams: 
- total points scored
- total offensive drives
- total offensive plays run
- total first downs gained 
- total penalties 
- total penalty yards

I will use Spark to extract these measures from the JSON data and aggregate them into a single data set. Then I will examine the dataset for any interesting correlations. Finally, I will make a regression model of any interesting correlations to predict what the impact may be of a season with reduced or eliminated fans. 

## Results ##

First, let's examine the attendance data. The histogram below shows the distribution of the attendance data. 