#!/usr/bin/python
# -*- coding: utf-8 -*-

from TwitterSearch import *
from datetime import datetime,date,time
import pandas as pd
import time
import os
import yaml
from geoLocator import GeoLocator

def getFile_index():
    return datetime.strftime(datetime.utcnow(), "%Y-%m-%d_%H-%M-%S")


def saveRecordsToCSV (records,outputFileIndex):
    twitterFrame = pd.DataFrame.from_records(records, columns=['Tweet ID','Tweeted_At','Profile_Create_at','Username','UserID','Location','Enabled','Place','Geo','Text','Retweeted_Count'])
    with open('csv_tweets' + str(outputFileIndex) + '.csv', 'w') as f:
        twitterFrame.to_csv(f, header = True)
# more new lines c/o MM
    with open('json_tweets' + str(outputFileIndex) + '.json', 'w') as fj:
        twitterFrame.to_json(fj)
    records = []
    outputFileIndex = getFile_index() 
    return records, outputFileIndex

def queryTwitter(records,outputFileIndex,totalRunTime,writeToFileTime, sleepTime):
    n = GeoLocator()
    req = 0
    next_max_id = 0
    startTime = time.time()
    lastWriteTime = startTime
    tso = None
    ts = None
#     while time.time() - startTime < totalRunTime:
    while True:
        try:
            now = time.time()
            print 'Total running time: ' + str(now-startTime) + ' seconds'
            # Check if it is time to write to file                           
            if now-lastWriteTime>writeToFileTime:
                print 'Writing to CSV ' + str(len(records)) + ' Tweets'
                records, outputFileIndex = saveRecordsToCSV (records,outputFileIndex)
                lastWriteTime = now               
            # If first run, or recover after exception, create new twitter search object
            if tso == None:
                tso = TwitterSearchOrder()
                tso.set_keywords([''])
                #tso.setLanguage('en')
                tso.set_count(100)
#!!! figure out what "include entities" refers to
                tso.set_include_entities(False)
                tso.set_geocode(40.69, -73.94, 20, imperial_metric = False)
                # tso.setUntil(datetime.date(2014, 03, 24))        
                ts = TwitterSearch(consumer_key='FqjFRT1OHl6xyIGoq9uXSA',
                                   consumer_secret='KuhoVREmf7ngwjOse2JOLJOVXNCi2IVEzQZu2B8',
                                   access_token='114454541-xcjy2sbl7Rr4oIaogsaBrlVL5H4CvcdvOSMy3MnR',
                                   access_token_secret='yyBBOJhxgfw9pezZda2hWF94doONSd50y0JoylYjL3rmY', verify=False)

            # Query the Twitter API  
            text_file = open('json_tweets' + str(outputFileIndex) + '.txt', 'a')
            text_fileE = open('error_log.txt', 'a')
            req += 1
            print 'Request # ' + str(req)
            response = ts.search_tweets(tso)

            # check all tweets according to their ID
#!!! this shoudl all really be torn apart and put back together
            for tweet in response['content']['statuses']:
                text_file.write(str(tweet))
                text_file.write('\n')
                tup = ()
                tweet_id = tweet['id']
                tup = tup + (tweet_id, )
                tup = tup + (str(tweet['created_at']), )
                tup = tup + (str(tweet['user']['created_at']), )
                tup = tup + (str(tweet['user']['screen_name']), )
                tup = tup + (str(tweet['user']['id']), )
                tup = tup + (str(tweet['user']['location'].encode('ascii', 'ignore')), )
                tup = tup + (str(tweet['user']['geo_enabled']), )
                tup = tup + (str(tweet['place']), )
                tup = tup + (str(tweet['geo']), )
                tup = tup + (str(tweet['text'].encode('ascii', 'ignore')), )
                tup = tup + (str(tweet['retweet_count']), )
                # Save only tweets with Geo within NYC or without geo at all
                try:
                    geoObj = yaml.load(tup[7])
                    lat = geoObj["u'coordinates'"][0]
                    long = geoObj["u'coordinates'"][1]
                    if n.isNYC(lat,long):
                        records.append(tup)
                except:
                    records.append(tup)

                # current ID is lower than current next_max_id?
                if tweet_id < next_max_id or next_max_id == 0:
                    next_max_id = tweet_id
                    next_max_id -= 1  # decrement to avoid seeing this tweet again

            # set lowest ID as MaxID
            tso.set_max_id(next_max_id)
            
            print 'Number of Tweets in memory: ' + str(len(records))
            print 'Sleeping...'
            time.sleep(sleepTime)
                           
        except TwitterSearchException, e:
            print e
            if len(records) == 0:
                next_max_id = 0
            if text_file.closed:
                pass
            else:
                text_file.close()
            outputFileIndex = getFile_index()
            text_fileE.write(str(e))
            text_fileE.write('\n')
            text_fileE.close()
            print 'sleeping for 900 seconds after error...'
#new line c/o MM
            print datetime.now()
            time.sleep(900)
            # Set tso to None to create new Twitter search object 
            tso = None

def runCollectTweets (outputFileIndex,totalRunTime, writeToFileTime=300, sleepTime=7):            
    records = []
    print 'Started querying'
    queryTwitter(records, outputFileIndex, totalRunTime, writeToFileTime, sleepTime)
    print 'Last save to CSV'
    #next line so that the last call is saved to a csv
    records, outputFileIndex = saveRecordsToCSV(records,outputFileIndex)
    print 'Number of Tweets in memory: ' + str(len(records))
    print 'Done!'
    
def main():
    # set running params:
    # set the name of the first csv file
    i = getFile_index()
#     totalRunTime=3600
    totalRunTime=float('Inf')
    #time in seconds
    writeToFileTime=300
    # Sleep time was calculated in order to not exceed Twitter's limit = 180 requests per 15 min
    #BUT THAT'S NOT WORKING RIGHT
    sleepTime = 7
    
    print "------------------------------------------"
    print "Run Params:"
    print "file index starts at " + str(i)
    print "total running time " + str(totalRunTime)
    print "write to file every " + str(writeToFileTime)
    print "sleep time " + str(sleepTime)
    print "------------------------------------------"

    
    runCollectTweets(i,totalRunTime=totalRunTime ,writeToFileTime=writeToFileTime, sleepTime = sleepTime)
 
if __name__ == '__main__':
    main()

