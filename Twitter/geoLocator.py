import geopandas as gp
from shapely.geometry import Point
import matplotlib.pyplot as plt
import os

class GeoLocator:

    def __init__(self):
        # Creating a geo pandas data frame from the nybb.shp shape file      
        self.boros = gp.GeoDataFrame.from_file('nybb_14c/nybb.shp')
        
        # setting the BoroCode to be the data frame index
        self.boros.set_index('BoroCode', inplace=True)
        
        # Converting the coordinates system to lonlat
        target_crs = {'datum':'WGS84', 'no_defs':True, 'proj':'longlat'}
        self.boros.to_crs(crs=target_crs, epsg=None, inplace=True)
    
    
    # Return True iff the point given is in NYC
    def isNYC (self, lat, long):
        for index, row in self.boros.iterrows():
            if row.geometry.contains(Point(long,lat)):
                return True
        return False
