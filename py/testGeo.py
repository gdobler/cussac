import geopandas as gp
from shapely.geometry import Point
import matplotlib.pyplot as plt


boros = gp.GeoDataFrame.from_file('nybb_14c/nybb.shp')
boros.set_index('BoroCode', inplace=True)
boros.sort()
print boros
   
boros.plot()
plt.show()

for index, row in boros.iterrows():
    print row.geometry.contains(Point(40.64946808, -73.93384131))
    
