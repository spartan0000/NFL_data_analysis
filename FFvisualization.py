#visualization practice

import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re

ff_df = pd.read_csv('Sportsdata\FF2021stats.csv')

print(ff_df.head())

#find just the running backs by creating new DF where FantPos = RB
#call the new dataframe rb_df
#we want to separate out RB from WR because their usage isn't comparable

rb_df = ff_df.loc[ff_df['FantPos'] == 'RB'].copy()
print(rb_df.head())

wr_df = ff_df.loc[ff_df['FantPos'] == 'WR'].copy()
print(rb_df.head())

#rerank all the players
rb_df['Rk'] = [i for i in range(len(rb_df))]
rb_df.set_index(rb_df['Rk'], inplace = True)

wr_df['Rk'] = [i for i in range(len(wr_df))]
wr_df.set_index(wr_df['Rk'], inplace = True)

#define usage for RB
rb_df['Usage/G'] = ((rb_df['RuAtt']/rb_df['G']) + (rb_df['ReTgt']/rb_df['G']))
rb_df['FFP/G'] = (rb_df['FantPt']/rb_df['G'])

#define usage for WR
wr_df['Usage/G'] = ((wr_df['ReTgt']/wr_df['G']))
wr_df['FFP/G'] = ((wr_df['FantPt']/wr_df['G']))

print(rb_df.head())


#create a function to calculate fantasy points
#2PM has empty cells, need to fill the empty ones with zeros using line below
#otherwise, python doesn't handle the NaN in the empty cells very well

rb_df['2PM'] = [0 if i != i else i == i for i in rb_df['2PM']]

#rb_df.info(verbose = True)
####Example of a function to calculate FFP using a dictionary to assign points
ff_weights = {
	'RuYds' : 0.1,
	'RuTD' : 6,
	'ReYds' : 0.1,
	'ReTD' : 6,
	'ReRec' : 0.5,
	'FL' : -2,
	'2PM' : 2,
}


def ff_points(row):
	game = row['G']
	fantasy_points = sum([row[column]*weight for column, weight in ff_weights.items()])
	return fantasy_points/game


rb_df['FantasyPoints/game (exp)'] = rb_df.apply(ff_points, axis = 1)

print(rb_df.head())
######################################


#create plots

plt.style.use('fivethirtyeight')

x = rb_df['Usage/G']
y = rb_df['FFP/G']

x1 = wr_df['Usage/G']
y1 = wr_df['FFP/G']

fig, (ax1, ax2) = plt.subplots(nrows = 1, ncols = 2, figsize = (15,15))
ax1.scatter(x,y, label = '2021 Data', color = 'k', marker = 'v', edgecolor = 'black', alpha = 0.5, linewidth=2)
ax1.set_xlabel('Usage per game (Rush Att + Targets)')
ax1.set_ylabel('Fantasy Points per game')
ax1.set_title('2021 RB Usage vs. Fantasy Points')

for i in range(len(rb_df)):
	ax1.text(x[i], y[i], rb_df['Player'][i], size = 5)



ax2.scatter(x1,y1, color = 'r', marker = '^', edgecolor = 'black', alpha = 0.5, linewidth = 2)
ax2.set_xlabel('Usage per game (Targets)')
ax2.set_ylabel('Fantasy Points per game')
ax2.set_title('2021 WR Usage vs. Fantasy points')

for i in range(len(wr_df)):
	ax2.text(x1[i], y1[i], wr_df['Player'][i], size = 5)

plt.show()

#sns.scatterplot(data = rb_df, x = 'Usage/G', y = 'FFP/G')