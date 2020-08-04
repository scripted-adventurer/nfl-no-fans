# Understanding a Potentially Fan-Less 2020 NFL Season #

The goal of this project is to understand what impact a reduction or elimination of fans at NFL games in the 2020 season might have on the actual on-field product. American football is an interesting sport to consider this question for because communication (in the form of play calling, audibles, and the snap count) is an integral part of every play, and communication can become quite difficult when a large crowd is making a lot of noise. While strategies to deal with loud crowd noise exist (like hand signals, silent counts, etc.), these strategies may hinder the team's overall effectiveness. Consider that teams typically employ these stragies only when they need to, suggesting that teams operate better when they don't use them. 

## Key Questions For Analysis ##

- Are there any meaningful correlations between the size of the crowd in attendance and game outcomes?
- How are the relationships different for the home team and the away team?

## Dataset ##

To perform this analysis, I will be using a dataset of NFL regular season game data downloaded in JSON form from the NFL.com API in [another project](https://github.com/scripted-adventurer/nfl-mongodb). Although the data set extends back to 2011, attendance data is only available for 2015 to 2019, so I will restrict my analysis to regular season games from those years. I will further restrict analysis by removing games that occurred at a neutral site (like the NFL's London series), since the concept of 'home' and 'away' teams isn't very meaningful in those games. 

## Method ##

In the NFL (and indeed for pretty much all sports) there is a concept of 'home field advantage'. Essentially the idea is that teams perform better when playing at home. This could be due to many different factors (including not having to deal with a sometimes grueling travel schedule), but many fans believe that their team performs better when they are there at the stadium to cheer them on. 
<br><br>
To investigate this phenomenon, I will look at the correlation between attendance and 6 different variables. 
<br><br>
Attendance data will be scaled to a percentage of the total capacity for the stadium where the game is played. This is necessary because each NFL stadium has its own unique capacity and thus the range of raw attendance values will depend heavily on what the capacity is. 
<br><br>
I will consider three variables for both the home and away teams (for a total of 6 dependent measures): yards per play, penalties, and penalty yards. 
- Yards per play is a useful metric that captures how effective a team was on offense. Teams that played well have a larger yards per play measure (and vice versa). This should help us answer the question of "my team plays better when I'm there to cheer them on" (and also "the visiting team plays worse when I'm there to boo them"). 
- Penalties and penalty yards will help determine a different sort of metric - the emotional 'feel' of the game. There's another common idea in football that teams that get more penalties are 'undisciplined', letting their emotions drive their actions on the field. So we can consider the total number of penalties and penalty yards enforced against teams as a proxy for players' subjective experience of the game.- 
<br><br>
The Python scripts included in this module contain all the steps for this analysis. At a high level, the process is as follows:
- Extract the interesting data from the JSON files using Spark and aggregate it into a single data set. (Yes, normally you wouldn't use Spark for such a small dataset, but one of the main goals of this project is to demonstrate Spark usage.)
- Use Python's scipy module to calculate linear regressions on the dataset and find any interesting relationships. For this analysis, I will consider data aggregated at the league level (i.e. from all stadiums) and data aggregated at the stadium level. 'Interesting' will be defined as any relationship with a p-value of less than 0.1. This is somewhat arbitrary, but it's useful as a starting point. 
<br><br>
- For any interesting relationships, display the scatter plot (and regression line) using Python's matplotlib module.

## Hypotheses ##

Based on the common conception of 'home field advantage', we can make two predictions about the data for yards per play:
- Home yards per play will be positively correlated with the attendance percentage
- Away yards per play will be negatively correlated with the attendance percentage
These two predictions essentially state the informal idea of "teams play better in front of their own fans and worse in front of other teams' fans".
<br><br>
Based on the view of penalties being associated with 'undisciplined' teams and the crowds' psychological impact on the players, we can make another prediction about penalties and penalty yards: 
- Home penalties, away penalties, home penalty yards, and away penalty yards will be positively correlated with attendance percentage
This prediction states that as the crowd size percentage gets larger, players from both teams will be more 'fired up' psychologically, resulting in more penalties and penalty yards. 

## Results and Analysis ##

First let's check out the league wide results:
<br><br>
Found relation for All Stadiums away_yards_per_play
- slope = -0.8432521291980726
- intercept = 4.899133645015511
- r = -0.062369561287414506
- p = 0.02689919128289022
- std. error = 0.3806017463469944
<br><br>
We see there is a statistically significant relationship between attendance percentage and away yards per play, but it's so small (r = -0.06) as to not be meaningful.
<br><br>
Moving on to individual stadiums, below are the interesting relationships and associated scatter plots for each stadium.

### M&T Bank Stadium (Home of the Ravens) ###
home_penalty_yards
- slope = 1724.5545022616084
- intercept = -1655.3012678307018
- r = 0.3054799278197031
- p = 0.0552555751735802
- std. error = 872.0270299880134

![M&T Bank Home Penalty Yards](/images/m&t-bank-home-penalty-yards.png)

### State Farm Stadium (Home of the Cardinals) ###
home_yards_per_play
- slope = 9.882588738869032
- intercept = -5.6266834761947315
- r = 0.2828596032709899
- p = 0.07696908663261087
- std. error = 5.436252931142679

![State Farm Home Yards Per Play](/images/state-farm-home-yards-per-play.png)

away_yards_per_play
- slope = -15.780326943723209
- intercept = 19.668764908949722
- r = -0.45713944996261857
- p = 0.0030220590491511403
- std. error = 4.980468486457741

![State Farm Away Yards Per Play](/images/state-farm-away-yards-per-play.png)

### TIAA Bank Field (Home of the Jaguars) ###
away_penalty_yards
- slope = -193.35927004643224
- intercept = 237.73055573809066
- r = -0.3233499433273027
- p = 0.09326285245223097
- std. error = 110.97494732606489

![TIAA Bank Field Away Penalty Yards](/images/tiaa-bank-away-penalty-yards.png)

### Fedex Field (Home of the Washington Football Team) ###
home_yards_per_play
- slope = 5.1225565603029395
- intercept = -0.40724632518102055
- r = 0.49180529387757904
- p = 0.0009402081489627919
- std. error = 1.4339523094012787

![Fedex Field Home Yards Per Play](/images/fedex-home-yards-per-play.png)

### Arrowhead Stadium (Home of the Chiefs) ###
away_yards_per_play
- slope = -6.762268555553182
- intercept = 10.777516920749225
- r = -0.33607042268895637
- p = 0.03398938742868192
- std. error = 3.074298313974131

![Arrowhead Stadium Away Yards Per Play](/images/arrowhead-away-yards-per-play.png)

home_penalties
- slope = 20.176941375848852
- intercept = -13.365532386901085
- r = 0.3190380154258958
- p = 0.044795648421962236
- std. error = 9.723244099160205

![Arrowhead Stadium Home Penalties](/images/arrowhead-home-penalties.png)

home_penalty_yards
- slope = 200.52668649669548
- intercept = -142.52833375198367
- r = 0.3417253057301533
- p = 0.030914940080711946
- std. error = 89.46200433659396

![Arrowhead Stadium Home Penalty Yards](/images/arrowhead-home-penalty-yards.png)

### AT&T Stadium (Home of the Cowboys) ###
home_penalties
- slope = 55.78186334198074
- intercept = -42.79790764458458
- r = 0.26551569101510475
- p = 0.09774379246125806
- std. error = 32.85761646529953

![AT&T Stadium Home Penalties](/images/at&t-home-penalties.png)

### Gillette Stadium (Home of the Patriots) ###
away_penalties
- slope = -89.78363789512012
- intercept = 96.70217213471389
- r = -0.2914741035240586
- p = 0.06445725228061765
- std. error = 47.183009126001366

![Gillette Stadium Away Penalties](/images/gillette-away-penalties.png) 

away_penalty_yards
- slope = -891.3478319921752
- intercept = 954.8311709920805
- r = -0.28522620006137317
- p = 0.07066651558027688
- std. error = 479.6225465138294

![Gillette Stadium Away Penalty Yards](/images/gillette-away-penalty-yards.png)

### Hard Rock Stadium (Home of the Dolphins) ###
home_penalty_yards
- slope = 339.2581172259913
- intercept = -267.2769914040549
- r = 0.27302058296372206
- p = 0.09722300181376718
- std. error = 199.23350613125578

![Hard Rock Stadium Home Penalty Yards](/images/hard-rock-home-penalty-yards.png)

### FirstEnergy Stadium (Home of the Browns) ###
away_yards_per_play
- slope = 6.219896571530161
- intercept = -1.767116975855556
- r = 0.4600941597127852
- p = 0.0032083180247233145
- std. error = 1.9732632381749844

![FirstEnergy Stadium Away Yards Per Play](/images/firstenergy-away-yards-per-play.png)

### U.S. Bank Stadium (Home of the Vikings) ###
home_yards_per_play
- slope = -252.35662295229696
- intercept = 257.0993799551365
- r = -0.5525481311673949
- p = 0.0010407791602907671
- std. error = 69.4991774919478

![U.S. Bank Stadium Home Yards Per Play](/images/us-bank-home-yards-per-play.png)

### MetLife Stadium (Home of the Jets & Giants) ###
away_penalties
- slope = -35.63300908537334
- intercept = 40.25817995044361
- r = -0.21580389021980467
- p = 0.05453662650012415
- std. error = 18.255344543256285

![MetLife Stadium Away Penalties](/images/metlife-away-penalties.png)

### Paul Brown Stadium (Home of the Bengals) ###
home_yards_per_play
- slope = 2.818141501537086
- intercept = 1.8785493373546411
- r = 0.3384908888423694
- p = 0.03505134070316749
- std. error = 1.287925005032272

![Paul Brown Stadium Home Yards Per Play](/images/paul-brown-home-yards-per-play.png)

away_penalties
- slope = -8.596740709638214
- intercept = 14.505632786330438
- r = -0.36591964368672547
- p = 0.021968376619957562
- std. error = 3.5944460245796366

![Paul Brown Stadium Away Penalties](/images/paul-brown-away-penalties.png)

away_penalty_yards
- slope = -65.32738431001529
- intercept = 119.53885148953356
- r = -0.2679205201526043
- p = 0.09914156232002093
- std. error = 38.62011493763165

![Paul Brown Stadium Away Penalty Yards](/images/paul-brown-away-penalty-yards.png)

### New Era Field (Home of the Bills) ###
home_penalties
- slope = 20.753151994935273
- intercept = -12.422561499037064
- r = 0.27595680365878655
- p = 0.08477880760793859
- std. error = 11.726040423697384

![New Era Field Home Penalties](/images/new-era-home-penalties.png)

home_penalty_yards
- slope = 284.30496318632623
- intercept = -207.65907762098163
- r = 0.38794196357060684
- p = 0.013380222315947718
- std. error = 109.57408153389325

![New Era Field Home Penalty Yards](/images/new-era-home-penalty-yards.png)

### Los Angeles Memorial Coliseum (Home of the Rams) ###
home_yards_per_play
- slope = -3.542616739916723
- intercept = 7.530984111636795
- r = -0.32621957796747764
- p = 0.08415365539528916
- std. error = 1.9756007303163272

![Los Angeles Memorial Coliseum](/images/la-coliseum-home-yards-per-play.png)

### Dignity Health Sports Park (Home of the Chargers) ###
home_penalties
- slope = 411.5255988597116
- intercept = -380.55552270200826
- r = 0.5222459168396408
- p = 0.012656774911174621
- std. error = 150.26277924347784

![Dignity Health Sports Park Home Penalties](/images/dignity-health-home-penalties.png)

home_penalty_yards
- slope = 3382.039974721734
- intercept = -3125.7871537499964
- r = 0.489868199949028
- p = 0.020655159810692436
- std. error = 1345.859159555431

![Dignity Health Sports Park Home Penalty Yards](/images/dignity-health-home-penalty-yards.png)

## Conclusions ##

The below results fit with our prediction for yards per play:
- State Farm Stadium (Home of the Cardinals) home yards per play
- State Farm Stadium (Home of the Cardinals) away yards per play
- Fedex Field (Home of the Washington Football Team) home yards per play
- Arrowhead Stadium (Home of the Chiefs) away yards per play
- Paul Brown Stadium (Home of the Bengals) home yards per play

The below results were the opposite of our prediction for yards per play:
- FirstEnergy Stadium (Home of the Browns) away yards per play
- U.S. Bank Stadium (Home of the Vikings) home yards per play
- Los Angeles Memorial Coliseum (Home of the Rams) home yards per play

The below results fit with our prediction for penalties and penalty yards:
- M&T Bank Stadium (Home of the Ravens) home penalty yards
- Arrowhead Stadium (Home of the Chiefs) home penalties
- Arrowhead Stadium (Home of the Chiefs) home penalty yards
- AT&T Stadium (Home of the Cowboys) home penalties
- Hard Rock Stadium (Home of the Dolphins) home penalty yards
- New Era Field (Home of the Bills) home penalties
- New Era Field (Home of the Bills) home penalty yards
- Dignity Health Sports Park (Home of the Chargers) home penalties
- Dignity Health Sports Park (Home of the Chargers) home penalty yards

The below results were the opposite of our prediction for penalties and penalty yards: 
- TIAA Bank Field (Home of the Jaguars) away penalty yards
- Gillette Stadium (Home of the Patriots) away penalties
- Gillette Stadium (Home of the Patriots) away penalty yards
- MetLife Stadium (Home of the Jets & Giants) away penalties
- Paul Brown Stadium (Home of the Bengals) away penalties
- Paul Brown Stadium (Home of the Bengals) away penalty yards

The results for yards per play are a little surprising - especially the result for U.S. Bank Stadium (Minnesota Vikings) which had the strongest observed relationship (r = -0.55) between attendance percentage and home yards per play, only it was negative! 
<br><br>
Two things to note here:
1. This analysis does not take into account which team the fans are rooting for. We assume that the fans are primarily rooting for the home team, but there may be circumstances where this is not the case (and many NFL fans have certainly seen games with a large proportion of away fans in the stands). Perhaps this explains the result for FirstEnergy Stadium (Cleveland Browns) and away yards per play: The Browns have been so bad for so long that fans have mostly given up on the team, and a high attendance percentage is actually a signal that many away fans are attending the game. 
2. This analysis ignores any correlation between the quality of the opponent and the attendance percentage. We might expect that fans are more likely to attend a game they think will be competitive, i.e. a matchup between two good teams. In that case, the predicted relationship between attendance percentage and yards per play might flip simply due to the fact that the quality of the opponent is much greater. This may help explain the result for U.S. Bank Stadium (Vikings) and the LA Coliseum (Rams). This would be an interesting area for further analysis. 
<br><br>
The results for penalties and penalty yards are very interesting. It seems that (for some teams at least) there is a relationship between attendance percentage and penalties and penalty yards, but that the relationship is positive for home teams and negative for away teams. So how can we explain higher attendance being correlated with more penalties and penalty yards for the home team but fewer penalties and penalty yards for the away team? Perhaps a large and energetic home crowd increases the emotional energy of the home team but decreases it for the away team because the perceived group identity of each player affects whether the crowd energy excites or depresses them. 
<br><br>
It's important to note that this analysis looks at the penalties called by the referees (and is not, therefore, a perfect measure of fouls actually committed). Perhaps large crowds increase how likely referees are to make a call against the home team (maybe as an attempt to 'keep the game under control' if they feel like the large crowd is getting unruly). 
<br><br>
As a final wrap-up, what conclusions can we draw from this analysis? In general, the impact of fan attendance on NFL games is complicated and depends on the individual teams and stadiums involved. However for some teams there does seem to be a positive relationship between fan attendance and penalties and penalty yards for the home team, and a negative relationship between fan attendance and penalties and penalty yards for the away team. Of course these are correlations, not causations, so we can't conclusively say that in a season without fans these teams will see fewer penalties for themselves and more for their opponents at their home games. But if our reasoning about crowd size and the emotional impact on players is correct, maybe we can expect teams to play with more similar emotional styles, whether they are at home or on the road. 