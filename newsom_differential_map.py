import load_county_populations
import load_recall_counts
import load_election
import load_geometry

import matplotlib
matplotlib.style.use('seaborn-whitegrid')
matplotlib.rcParams['font.size'] = 12
from matplotlib import pyplot

##
from sklearn import linear_model
import numpy as np
import pandas
import seaborn

###

fig,ax = pyplot.subplots(1,1, constrained_layout=True)

load_election.df['pct_biden'] = load_election.df['Biden']/load_election.df.sum(axis=1)

x = load_election.df['pct_biden'].values
y = load_recall_counts.df['TOTAL VALID SIGNATURES'].values/load_county_populations.df[2019].values

ax.scatter(x,y)
ax.set_xlabel('2020 election (fraction Biden)')
ax.set_ylabel('Valid signatures (fraction of county)')
ax.set_title('California per-county Newsom recall statistics',loc='left')

# predict
lr = linear_model.LinearRegression()
lr.fit(x.reshape(-1,1), y)
ypred = lr.predict(x.reshape(-1,1))
err = ypred - y

#top3 = np.argsort(-err)[:2]
#bot3 = np.argsort(err)[:2]
#both = np.concatenate([top3,bot3])
#for ii in both:
#    ax.text(x[ii]-0.005,y[ii]-0.001, load_election.df['COUNTY'].iloc[ii], fontsize=10, ha='right', va='top')
##

fig.savefig('newsom_recall_stats.png')

##
df = pandas.DataFrame()
df['COUNTY'] = load_election.df['COUNTY']
df['pct_biden'] = x
df['recall_fraction'] = y
df['abs_err'] = abs(err)
df['rel_err'] = abs(err)/y
df['signed_err'] = err

POPSCALE = False

fig2,ax2 = pyplot.subplots(1,3, figsize=(10,3), constrained_layout=True)
load_geometry.state_map( df, 'pct_biden', ax=ax2[0], vmin=0.3, vmax=0.7, popscale=POPSCALE, cmap=pyplot.cm.RdYlBu)
load_geometry.state_map( df, 'recall_fraction', ax=ax2[1], vmin=0, popscale=POPSCALE, cmap=seaborn.cubehelix_palette(dark=0, light=1, as_cmap=True, reverse=False) )
load_geometry.state_map( df, 'abs_err', ax=ax2[2], vmin=0, vmax=0.05, popscale=POPSCALE, cmap=seaborn.cubehelix_palette(rot=-0.4, dark=0, light=1, as_cmap=True, reverse=False) )

for axi,title in zip(ax2, ['2020 election', 'Recall signatures per capita', 'Rel. deviation from trendline']):
    axi.set_facecolor('#ddd')
    axi.grid()
    axi.set_yticks([])
    axi.set_xticks([])
    axi.set_title(title, loc='left')
#

if POPSCALE:
    fig2.savefig('newsom_recall_maps_scaled.png')
else:
    fig2.savefig('newsom_recall_maps.png')
#

fig.show()
fig2.show()
