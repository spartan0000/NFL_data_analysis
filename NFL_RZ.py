#redzone utilization
#find those WR and RBs who get the redzone targets and rushes which are higher value touches.

import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import nfl_data_py as nfl

df_2022 = nfl.import_pbp_data([2022])
df_players = nfl.import_rosters([2022])
df_teams = nfl.import_team_desc()

# a = df_2022['yardline_100']

# fig, ax = plt.subplots(figsize = (10,10))

# ax.hist(a, bins = 10)
# plt.show()

#print(df_2022['yardline_100'].describe())

print(df_2022.info(verbose = True))


#find all plays that originate at 20 yard line or less

df_2022_rz = df_2022[df_2022['yardline_100'] <= 20]
print(df_2022_rz.head())

#from the redzone dataframe, find pass plays only
df_2022_rz_pass = df_2022_rz[df_2022_rz['play_type'] == 'pass']

#merge with player name df

df_2022_rz_rec = pd.merge(df_2022_rz_pass, df_players[['player_id', 'player_name']], left_on = 'receiver_player_id', right_on = 'player_id')

#group by player name and aggregate passes and touchdowns

df_2022_rz_rec_agg = df_2022_rz_rec.groupby(['player_name'], as_index = False).agg({'complete_pass':'sum', 'incomplete_pass':'sum', 'touchdown':'sum'})

#create new column called 'targets' which is simply complete passes plus incomplete passes

df_2022_rz_rec_agg['targets'] = df_2022_rz_rec_agg['complete_pass'] + df_2022_rz_rec_agg['incomplete_pass']

#sort the etire df by targets to find people with most targets

df_2022_rz_rec_agg = df_2022_rz_rec_agg.sort_values(by = 'targets', ascending = False)


print(df_2022_rz_rec_agg.head(50))




#from the redzone dataframe, find rush plays only
df_2022_rz_rush = df_2022_rz[df_2022_rz['play_type'] == 'run']

df_2022_rz_rush = pd.merge(df_2022_rz_rush, df_players[['player_id', 'player_name']], left_on = 'rusher_player_id', right_on = 'player_id')

df_2022_rz_rush_agg = df_2022_rz_rush.groupby(['player_name'], as_index = False).agg({'rush_attempt':'sum', 'touchdown':'sum'})

df_2022_rz_rush_agg = df_2022_rz_rush_agg.sort_values(by = 'rush_attempt', ascending = False)

print(df_2022_rz_rush_agg.head(50))

#df_2022_rz_rush_agg.to_csv('redzoneRush.csv')
#df_2022_rz_rec_agg.to_csv('redzoneRec.csv')

#read in dataframes from the other file for TD regression

# df_rec_td = pd.read_csv('recTD_regression.csv')
# df_rush_td = pd.read_csv('rushTD_regression.csv')

# #merge by player name to find players on both the high redzone rushes list and TD regression list

# df_rush_merged = pd.merge(df_2022_rz_rush_agg, df_rush_td, left_on = 'player_name', right_on = 'player_name')

# df_rec_merged = pd.merge(df_2022_rz_rec_agg, df_rec_td, left_on = 'player_name', right_on = 'player_name_y') #the receiver df merge resulted in player_name_y

# #df_rec_merged.to_csv('recRZ_TD.csv', index = False)
# #df_rush_merged.to_csv('rushRZ_TD.csv', index = False)