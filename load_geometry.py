import json
import re
from matplotlib import pyplot
import numpy as np
#from collections import defaultdict

with open('ca_boundaries.json', 'r') as f:
    ca_json = json.load(f)
#

# this file really has city-level boundaries as well as 
# county, but doesn't have aggregate county data...
#
# build county-level tools here.

# basic structure... (just of what we need)
# dict
# |- features (list)
# |- |- attributes (dict; city and county information; camelcase + "County"
# |- |- geometry (dict)
# |- |- |- rings (list of connectected regions; each a list of duples of (lon, lat)

county_dict = {}
for geom in ca_json['features']:
    county = geom['attributes']['COUNTY']
    county = re.match('([a-zA-Z\ ]{1,}) County', county).groups(0)[0].upper()
    if county not in county_dict:
        county_dict[county] = geom['geometry']['rings']
    else:
        county_dict[county] += geom['geometry']['rings']
#

def state_map(df, colname, vmin=None, vmax=None, ax=None, cmap=pyplot.cm.viridis):
    vals = df[colname].values
    counties = df['COUNTY'].values
    if vmin is None:
        vmin = np.nanmin(vals)
    if vmax is None:
        vmax = np.nanmax(vals)
    if vmax==vmin:
        vmax = vmin + 1
    #
    color = lambda xx : cmap( float( (xx-vmin)/(vmax-vmin) ) )
    
    if ax is None:
        print('noax')
        returnflag = True
        fig,ax = pyplot.subplots(1,1) 
    else:
        returnflag = False
    #
    for c,v in zip(counties,vals):
#        print(c,v)
        for r in county_dict[c]:
            xy = np.array(r, dtype=float)
            ax.fill(xy[:,0], xy[:,1], facecolor=color(v), edgecolor=[0,0,0,0])
    #
    ax.axis('equal')
    return ax
#
