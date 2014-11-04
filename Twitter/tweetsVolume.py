import pandas as pd
from datetime import datetime
import numpy as np
import cussacTwitterCrawlTimed as tct
import time
import matplotlib.pyplot as plt
import math

print '------------------'
print '15 mins run: '
print '------------------'


colTypes = {'Tweet ID':np.str,'Enabled':np.bool}

ids = set()
for i in range(10):
    df = pd.read_csv("csv_tweets"+str(i)+".csv", parse_dates = [3,4], dtype = colTypes)
    for _, id in df['Tweet ID'].iteritems():
        ids.add(id)
        
    numGeo = df[(df["Geo"] != 'None')]["Tweeted_At"].count()
    numNotGeo = df[(df["Geo"] == 'None')]["Tweeted_At"].count()
    total = df["Tweeted_At"].count()
    
    print 'file: ' + str(i)
    print '\t len(df) - '+ str(len(df))
    print '\t len(ids) - '+ str(len(ids))
    print '\t Geo enabled: ' + str (numGeo) + ' (' + str(numGeo*100.00/total) + '%)'
    print '\t Geo disabled: ' + str (numNotGeo) + ' (' + str(numNotGeo*100.00/total) + '%)'
    print '\t Total: ' + str(total)