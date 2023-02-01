#NFL EPA analysis

import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import nfl_data_py as nfl

df_2021 = nfl.import_pbp_data([2022])
df_players = nfl.import_rosters([2022])
df_teams = nfl.import_team_desc()


#create new df with new attributes

epa_df = pd.DataFrame({
	'offense_epa':df_2021.groupby('posteam')['epa'].sum(),
	'offense_plays':df_2021['posteam'].value_counts(),
	'offense_yards':df_2021.groupby('posteam')['yards_gained'].sum(),
	})

epa_df['off_epa/play'] = epa_df['offense_epa']/epa_df['offense_plays']
epa_df = epa_df.sort_values(by = ['off_epa/play'], ascending = False)

print(epa_df.head(10))
print(epa_df.info(verbose = True))



#do the same for EPA defense - negative is better for defensive stats

epa_df['def_epa'] = df_2021.groupby('defteam')['epa'].sum()
epa_df['defensive_plays'] = df_2021['defteam'].value_counts()
epa_df['defensive_yards_given'] = df_2021.groupby('defteam')['yards_gained'].sum()
epa_df['def_epa/play'] = epa_df['def_epa']/epa_df['defensive_plays']
epa_df = epa_df.sort_values(by = ['def_epa/play'], ascending = False) #descending order will give us the worst defenses


#create list of the index which is the team names
#the team names became the index because of the way we did 'groupby' above
#easy to manipulate with a column with team names
#can also use df.index as done below in the ax.text line

indexval = list(epa_df.index)

epa_df['team'] = indexval

print(epa_df.head(32))



#plot offense/defense EPA

plt.style.use('fivethirtyeight')

x = epa_df['off_epa/play']
y = epa_df['def_epa/play']

fig, ax = plt.subplots(figsize = (15, 10))

ax.vlines(0, -0.2, 0.2, color = 'k', alpha = 0.5, linestyles = 'dashed')
ax.hlines(0, -0.2, 0.2, color = 'k', alpha = 0.5, linestyles = 'dashed')
ax.set_ylim(-0.2,0.2)
ax.set_xlim(-0.2,0.2)
ax.set_title('2021 Team Off/Def EPA per Play')
ax.set_xlabel('Offensive EPA per Play')
ax.set_ylabel('Defensive EPA per Play')

for i in range(len(epa_df)):
	ax.text(x[i], y[i], epa_df.index[i], size = 10)

ax.scatter(x,y)

annot_styles = {
    'bbox': {'boxstyle': 'round,pad=0.375', 'facecolor': 'none', 'edgecolor':'k'},
    'fontsize': 15,
    'color': 'b'
}

ax.annotate('Good Offense, Good Defense', xy = (x.max() - 0.06, y.min() - 0.03), **annot_styles)
ax.annotate('Bad Offense, Good Defense', xy = (x.min(), y.min() -0.03), **annot_styles)
ax.annotate('Good Offense, Bad Defense', xy = (x.max() - 0.06, y.max() + 0.03), **annot_styles)
ax.annotate('Bad Offense, Bad Defense', xy = (x.min(), y.max() +0.03), **annot_styles)


plt.show()