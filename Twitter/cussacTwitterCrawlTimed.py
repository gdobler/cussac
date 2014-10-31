#!/usr/bin/python
# -*- coding: utf-8 -*-

from TwitterSearch import *
import datetime as dt
import pandas as pd
import time
import os

def saveRecordsToCSV (records,outputFileIndex):
    # Create a data frame from tweets saved in records
    twitterFrame = pd.DataFrame.from_records(records, columns=['Tweet ID','Tweeted_At','Profile_Create_at','Username','Location','Enabled','Place','Geo','Text','Retweeted_Count'])
    # Append tweets to CSV file
    with open('csv_tweets' + str(outputFileIndex) + '.csv', 'a') as f:
        header = False
        if os.path.getsize('csv_tweets' + str(outputFileIndex) + '.csv') == 0:
            header = True
        twitterFrame.to_csv(f, header = header)
        records = []
        
    return records

def queryTwitter(records,outputFileIndex,totalRunTime,writeToFileTime, sleepTime):
    req = 0
    next_max_id = 0
    startTime = time.time()
    lastWriteTime = startTime
    tso = None
    ts = None
    while time.time() - startTime < totalRunTime:
        try:
            now = time.time()
            print 'Total running time: ' + str(now-startTime) + ' seconds'
            # Check if it is time to write to file                           
            if now-lastWriteTime>writeToFileTime:
                print 'Writing to CSV ' + str(len(records)) + ' Tweets'
                records = saveRecordsToCSV (records,outputFileIndex)
                lastWriteTime = now               
            # Create new twitter search object
            if tso == None:
                tso = TwitterSearchOrder()
                tso.setKeywords([''])
                #tso.setLanguage('en')
                tso.setCount(100)
                tso.setIncludeEntities(False)
                tso.setGeocode(40.69, -73.94, 1, km = False)
                #tso.setUntil(dt.date(2014, 03, 24))        
                ts = TwitterSearch(consumer_key='FqjFRT1OHl6xyIGoq9uXSA',
                                   consumer_secret='KuhoVREmf7ngwjOse2JOLJOVXNCi2IVEzQZu2B8',
                                   access_token='114454541-xcjy2sbl7Rr4oIaogsaBrlVL5H4CvcdvOSMy3MnR',
                                   access_token_secret='yyBBOJhxgfw9pezZda2hWF94doONSd50y0JoylYjL3rmY', verify=False)

            # Query the Twitter API  
            text_file = open('json_tweets' + str(outputFileIndex) + '.txt', 'a')
            text_fileE = open('error_log.txt', 'a')
            req += 1
            print 'Request # ' + str(req)
            response = ts.searchTweets(tso)

            # check all tweets according to their ID
            for tweet in response['content']['statuses']:
                text_file.write(str(tweet))
                text_file.write('\n')
                tup = ()
                tweet_id = tweet['id']
                tup = tup + (tweet_id, )
                tup = tup + (str(tweet['created_at']), )
                tup = tup + (str(tweet['user']['created_at']), )
                tup = tup + (str(tweet['user']['screen_name']), )
                tup = tup + (str(tweet['user']['location'].encode('ascii', 'ignore')), )
                tup = tup + (str(tweet['user']['geo_enabled']), )
                tup = tup + (str(tweet['place']), )
                tup = tup + (str(tweet['geo']), )
                tup = tup + (str(tweet['text'].encode('ascii', 'ignore')), )
                tup = tup + (str(tweet['retweet_count']), )
                records.append(tup)

                # current ID is lower than current next_max_id?
                if tweet_id < next_max_id or next_max_id == 0:
                    next_max_id = tweet_id
                    next_max_id -= 1  # decrement to avoid seeing this tweet again

            # set lowest ID as MaxID
            tso.setMaxID(next_max_id)
            
            print 'Number of Tweets in memory: ' + str(len(records))
            # Sleep time was calculated in order to not exceed Twitter's limit = 180 requests per 15 min
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
            outputFileIndex = outputFileIndex + 1
            text_fileE.write(str(e))
            text_fileE.write('\n')
            text_fileE.close()
            time.sleep(900)
            # Set tso to None to create new Twitter search object 
            tso = None

def runCollectTweets (outputFileIndex,totalRunTime, writeToFileTime=300, sleepTime=4.35):            
    records = []
    print 'Started querying...'
    queryTwitter(records, outputFileIndex, totalRunTime, writeToFileTime, sleepTime)
    print 'Last save to CSV'
    records = saveRecordsToCSV(records,outputFileIndex)
    print 'Number of Tweets in memory: ' + str(len(records))
    print 'Done!'

