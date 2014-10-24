import geopandas as gp
from shapely.geometry import Point
import matplotlib.pyplot as plt

# Creating a geo pandas data frame from the nybb.shp shape file
boros = gp.GeoDataFrame.from_file('nybb_14c/nybb.shp')

# setting the BoroCode to be the data frame index
boros.set_index('BoroCode', inplace=True)

# Converting the coordinates system to lonlat
target_crs = {'datum':'WGS84', 'no_defs':True, 'proj':'longlat'}
boros.to_crs(crs=target_crs, epsg=None, inplace=True)


# Return True iff the point given is in NYC
def isNYC (lat, long):
    ans = False
    for index, row in boros.iterrows():
        if row.geometry.contains(Point(long,lat)):
            ans = True
            break

