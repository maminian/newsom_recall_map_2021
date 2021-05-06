#import load_county_populations
#import load_recall_counts
import load_election
import load_geometry

from matplotlib import pyplot

fig,ax = pyplot.subplots(1,2, figsize=(10,5))

load_election.df['pct_biden'] = load_election.df['Biden']/load_election.df.sum(axis=1)

load_geometry.state_map( load_election.df, 'pct_biden', ax=ax[0], vmin=0.3, vmax=0.7, cmap=pyplot.cm.bwr_r )
load_geometry.state_map( load_election.df, 'pct_biden', ax=ax[1], vmin=0.3, vmax=0.7, cmap=pyplot.cm.bwr_r, popscale=True )

fig.show()
