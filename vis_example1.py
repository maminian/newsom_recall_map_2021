import load_county_populations
import load_recall_counts
import load_geometry

from matplotlib import pyplot

fig,ax = pyplot.subplots(1,1)
load_geometry.state_map( load_county_populations.df, 2019, ax=ax )

fig.show()