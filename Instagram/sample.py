import geopandas as gp
from shapely.geometry import Point
import matplotlib.pyplot as plt


boros = gp.GeoDataFrame.from_file('nyss.shp')
#print boros
'''boros.set_index('BoroCode', inplace=True)
#boros.sort()
print boros
'''   
boros.plot()
plt.show()
for x,i in boros.iterrows():
	#print i.geometry.contains(Point(40.64946808, -73.93384131))
	print i.geometry.contains(Point(920000, 140000))
#for index, row in boros.iterrows():
#    print row.geometry.contains(Point(40.64946808, -73.93384131))
#    print row.geometry.contains(Point(920000, 140000))


