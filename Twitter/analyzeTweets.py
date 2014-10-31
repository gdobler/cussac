import pandas as pd
from datetime import datetime
import numpy as np
import cussacTwitterCrawlTimed as tct
import time
import matplotlib.pyplot as plt
import math

requestsTimes = []
n=5
for i in range (n):
    requestsTimes.append(datetime.utcnow())
    tct.runCollectTweets (i,totalRunTime=600,writeToFileTime=300)
    time.sleep(10)
 

colTypes = {'Tweet ID':np.str,'Enabled':np.bool}
rows = math.ceil(n/3.0)
meanTweetsTimes = []
maxTweetsTimes = []
minTweetsTimes = []


for i in range(n):
    df = pd.read_csv("csv_tweets"+str(i)+".csv", parse_dates = [3,4], dtype = colTypes)
    f = lambda x: datetime.strptime(x.replace('+0000 ',''),"%a %b %d %H:%M:%S %Y")
    tweetsTimes = df["Tweeted_At"].apply(f)
    decimalTime = [t.hour + t.minute/60. for t in tweetsTimes]
    meanTweetsTimes.append(np.mean(decimalTime))
    maxTweetsTimes.append(tweetsTimes.max())
    minTweetsTimes.append(tweetsTimes.min())

    # Plotting hist in correct location
    if i % 2 == 0:
        plt.figure(1)
        plt.subplot(rows,3,i+1)    
        plt.hist(decimalTime, bins = 24*60/15)
        plt.title('Request time ' + str(requestsTimes[i]) + '\n mean: ' + str(meanTweetsTimes[i]))


plt.figure(2)
plt.plot(requestsTimes,meanTweetsTimes, 'ro')
plt.xlabel('Request time (UTC)')
plt.ylabel('Tweets mean time per request (UTC)')
plt.title('Mean tweets time per request time')
    
plt.show()

print 'requests times: '
print [datetime.strftime(t,"%a %b %d %H:%M:%S %Y") for t in requestsTimes]
print'---------------'
print 'mean tweets time: '
print meanTweetsTimes
print'---------------'
print 'range tweets time: '
print minTweetsTimes
print maxTweetsTimes
print'---------------'

# for i in range(0,4):
#     df = pd.read_csv("csv_tweets"+str(t)+str(i)+".csv", parse_dates = [3,4], dtype = colTypes)
#     df = df[(df["Tweet ID"]!='0')]
#     tweetsIDs = df.groupby(["Tweet ID"])["Tweet ID"].count().order(ascending=False).head(10)
#     print tweetsIDs



      
