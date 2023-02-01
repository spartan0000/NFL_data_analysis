#nfl data

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

#save the dataframe as a csv file
#df_2021_pass.to_csv('nfl2021.csv')


###columns of interest

#columns 57 and 58 are posteam and def team score at time of the play
#column 259 is 'weather'
#170 - passer_player_id
#171 - passer_player_name
#172 - passing_yards
#173 - receiver_player_id, 174 receiver_player_name, 175 - receiving_yards
#176 - rusher_player_id, 177 - rusher_player_name, 178 - rushing yards



df_agg_pass = df_2021_pass.groupby(['player_name', 'posteam', 'week', 'total_line'], as_index = False).agg({'passing_yards':'sum','pass_touchdown':'sum'})

#see what specific players stats look like
#print(df_agg_pass[df_agg_pass['player_name'] == 'Josh Allen'])
#print(df_agg_pass[df_agg_pass['player_name'] == 'Kyler Murray'])




###################################################
#create similar df for receiving
df_2021_rec = pd.merge(df_2021_pass, df_players[['player_id', 'player_name']], left_on = 'receiver_player_id', right_on = 'player_id')


# print(df_2021_rec.head())
# print(df_2021_rec['player_name_y'].unique())

####################################################
#complete_pass should be receptions
#incomlete_pass plus complete_pass should be total targets (I think)
#need to add defensive stats and maybe weather conditions


#create a column for targets using rationale above

df_2021_rec['targets'] = df_2021_rec['complete_pass'] + df_2021_rec['incomplete_pass']

###See if we can calculate the percent of positive EPA plays vs. negative ones.
#create new columns with dummy variable for positive epa and negative epa plays
#df_2021_rec['pos_epa'] = [1 if i>0 else i == 0 for i in df_2021_rec['epa']]
#df_2021_rec['neg_epa'] = [1 if i<=0 else i == 1 for i in df_2021_rec['epa']]

###Did the above and it doesn't seem all that useful


#group by player name and team and then aggregate stats

df_agg_rec = df_2021_rec.groupby(['player_name_y', 'posteam', 'defteam', 'week', 'total_line'], as_index = False).agg({'receiving_yards':'sum', 'air_yards':'sum','complete_pass':'sum','targets':'sum',
	'touchdown':'sum', 'wpa':'sum', 'epa':'sum'})

#add column to calculate fantasy points using 1/2 PPR
df_agg_rec['FP'] = (df_agg_rec['complete_pass']/2) + (df_agg_rec['receiving_yards']/10) + (df_agg_rec['touchdown']*6)


print(df_agg_rec.info(verbose = True))

#get a statisitical overview of the df
print(df_agg_rec.describe())

#get a statistical overview of a specific column of data
print(df_agg_rec['FP'].describe())

#sort the df by air yards to get top weekly performace by air yards
df_rec_sort = df_agg_rec.sort_values(by = ['air_yards'], ascending = False)


print(df_rec_sort.head(15))
print(df_agg_rec.head(15))





#see what a specific WR data looks like
print(df_agg_rec[df_agg_rec['player_name_y'] == 'Marquise Brown'])


###
#Plot weekly catch rate - 

# fig, ax = plt.subplots(figsize = (10,10))
# ax.plot()
# ax.set_xlabel('Week')
# ax.set_ylabel('Catch rate')

# for i in range(len(df_agg_rec)):
# 	ax.text(x[i], y[i], df_agg_rec['player_name_y'][i])

#plt.show()


###
#create same sort of df with rush stats
df_2021_rush = df_2021[df_2021['play_type'] == 'run']

df_2021_rush = pd.merge(df_2021_rush, df_players[['player_id', 'player_name']], left_on = 'rusher_player_id', right_on = 'player_id')

df_2021_rush['FP'] = df_2021_rush['rushing_yards']*0.1 + df_2021_rush['touchdown']*6

df_2021_rush_agg = df_2021_rush.groupby(['player_name', 'posteam', 'week', 'defteam'], as_index = False).agg({'rushing_yards':'sum', 'touchdown':'sum', 'epa':'sum','wpa':'sum','FP':'sum'})



print(df_2021_rush_agg[df_2021_rush_agg['player_name'] == 'Nick Chubb'])


# nchubb = df_2021_rush_agg[df_2021_rush_agg['player_name'] == 'Nick Chubb']
# plt.scatter(nchubb['week'], nchubb['rushing_yards'], color = 'r', marker = '*', )
# plt.xlabel('Week')
# plt.ylabel('yards')
# plt.title('Nick Chubb weekly yards')
# plt.show()

###
#also need to add opposing team stats  - their scoring/performace will affect game script and offensive stats
 
