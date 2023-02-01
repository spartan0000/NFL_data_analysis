#TD regression

#identify rate of TD scored per attempt/rush/target

#look at current season data to see who is underperforming given usage

import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import nfl_data_py as nfl

#load raw data

df_2021 = nfl.import_pbp_data([2021])
df_players = nfl.import_rosters([2021])
df_teams = nfl.import_team_desc()

#df_2021_weekly = nfl.import_weekly_data([2021])

print(df_2021.head())
print(df_2021.columns)

df_2021.info(verbose = True)
#print(df_2021['play_type'])


#Select only regular season games and then select only passing plays
df_2021 = df_2021[df_2021['season_type'] == 'REG']
df_2021 = df_2021[df_2021['two_point_attempt'] == False]
df_2021_pass = df_2021[df_2021['play_type'] == 'pass']

#print(df_2021_pass.head())


#merge with the player roster DF to match player ID with actual names.  Default is an inner merge.

df_2021_pass = pd.merge(df_2021_pass, df_players[['player_id', 'player_name']], left_on = 'passer_player_id', right_on = 'player_id')
#print(df_players.columns)
print(df_2021_pass['player_name'].unique())

#group by player and then aggregate touchdowns and pass attempts

df_agg_pass = df_2021_pass.groupby(['player_name'], as_index = False).agg({'touchdown':'sum', 'pass_attempt':'sum'})


df_agg_pass['TD rate'] = df_agg_pass['touchdown']/df_agg_pass['pass_attempt']


#calculate the league average for all passes

l_average_pass = df_agg_pass['touchdown'].sum()/df_agg_pass['pass_attempt'].sum()
print(f'League average = {l_average_pass}')

#add column to show difference between player and league average
df_agg_pass['diff'] = df_agg_pass['TD rate'] - l_average_pass

df_agg_pass = df_agg_pass.sort_values(by = 'pass_attempt', ascending = False)

print(df_agg_pass.head(40))

#####################################################################################
#same for receivers

#create similar df for receiving
df_2021_rec = pd.merge(df_2021_pass, df_players[['player_id', 'player_name']], left_on = 'receiver_player_id', right_on = 'player_id')

#complete_pass should be receptions
#incomlete_pass plus complete_pass should be total targets (I think)
#need to add defensive stats and maybe weather conditions


#create a column for targets using rationale above

df_2021_rec['targets'] = df_2021_rec['complete_pass'] + df_2021_rec['incomplete_pass']

#df of aggregated and grouped data
df_agg_rec = df_2021_rec.groupby(['player_name_y'], as_index = False).agg({'touchdown':'sum', 'targets':'sum'})

df_agg_rec['TD rate 2021'] = df_agg_rec['touchdown']/df_agg_rec['targets']
l_average_rec = df_agg_rec['touchdown'].sum()/df_agg_rec['targets'].sum()

print(f'League average = {l_average_rec}')

#sort in descending order
df_agg_rec = df_agg_rec.sort_values(by = 'targets', ascending = False)


print(df_agg_rec.head()) #we see there's two outliers with 580 targets

#drop two rows that have outlier number of targets
df_agg_rec = df_agg_rec[df_agg_rec['targets'] < 580]

print(df_agg_rec.head(30))

#take only the top 150 to look at

df_agg_rec_top = df_agg_rec.head(150)

print(df_agg_rec_top.head())

top_average = df_agg_rec_top['touchdown'].sum()/df_agg_rec_top['targets'].sum()

print(f'Average TD rate of top 150 in targets in 2021 = {top_average}')



#read in current season data from PFR in csv format - file saved locally

df_2022_rec = pd.read_csv('Sportsdata\WR_2022_7.csv')
print(df_2022_rec.head())

df_2022_rec['TD rate 2022'] = df_2022_rec['TD']/df_2022_rec['Tgt']

l_average_rec_2022 = df_2022_rec['TD'].sum()/df_2022_rec['Tgt'].sum()

print(f'League average for 2022 receivers (top 250) = {l_average_rec_2022}')

#merge by name to match up 2021 numbers with 2022.  Default is an inner merge

df_2022_rec_m = pd.merge(df_agg_rec_top, df_2022_rec, left_on = 'player_name_y', right_on = 'Player')

print(df_2022_rec_m.head())
print(df_2022_rec_m.info(verbose = True))

#find difference between TD rate in 2021 and 2022 to identify TD regression candidates
#positive number would indicate that they are underperforming this year compared to last year
#might be a candidate for positive TD regression

df_2022_rec_m['diff'] = df_2022_rec_m['TD rate 2022'] - df_2022_rec_m['TD rate 2021'] 


print(df_2022_rec_m.sort_values(by = 'diff', ascending = True).head(50))

df_2022_rec_5 = df_2022_rec_m.sort_values(by = 'diff', ascending = True)

#df_2022_rec_5.to_csv('recTD_regression.csv')

#########################################################################
#do the same thing for rushes

df_2021_rush = df_2021[df_2021['play_type'] == 'run']

df_2021_rush = pd.merge(df_2021_rush, df_players[['player_id', 'player_name']], left_on = 'rusher_player_id', right_on = 'player_id')

#aggregate data based on player

df_2021_agg_rush = df_2021_rush.groupby(['player_name'], as_index = False).agg({'touchdown':'sum', 'rush_attempt':'sum'})

df_2021_agg_rush['TD rate 2021'] = df_2021_agg_rush['touchdown']/df_2021_agg_rush['rush_attempt']

df_2021_agg_rush = df_2021_agg_rush.sort_values(by = 'TD rate 2021', ascending = False)

#eliminate outliers and people who didn't get enough rush attemps.  arbitrary cutoff of min 50 rush attempts

df_2021_agg_rush = df_2021_agg_rush[df_2021_agg_rush['rush_attempt'] > 100]

print(df_2021_agg_rush.head(10))

#read in csv file with 2022 data up to most recent week - file saved locally

df_2022_rush = pd.read_csv('Sportsdata\RB_2022_7.csv')

print(df_2022_rush.head(10))

df_2022_rush['TD rate 2022'] = df_2022_rush['TD']/df_2022_rush['Att']


ave_2021 = df_2021_agg_rush['touchdown'].sum()/df_2021_agg_rush['rush_attempt'].sum()

ave_2022 = df_2022_rush['TD'].sum()/df_2022_rush['Att'].sum()

print(f'League average 2021 (min 50 rushes) = {ave_2021}')
print(f'League average 2022 (top 150 players) = {ave_2022}')

#merge 2021 and 2022 dataframes. 

df_rush_m = pd.merge(df_2021_agg_rush, df_2022_rush, left_on = 'player_name', right_on = 'Player')

print(df_rush_m.info(verbose = True))

df_rush_m['diff'] = df_rush_m['TD rate 2022'] - df_rush_m['TD rate 2021']

df_rush_m = df_rush_m.sort_values(by = 'diff', ascending = True)
print(df_rush_m.head(40))

#save file locally to view
df_rush_m.to_csv('rushTD_regression.csv')