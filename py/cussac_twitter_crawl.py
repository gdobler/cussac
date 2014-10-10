#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Created on Sun Mar 09 22:32:29 2014

@author: Anjaney
"""

from TwitterSearch import *
import datetime as dt
import pandas as pd
import time
req = 0
t = 500
next_max_id = 0
while True:
    try:
        tso = TwitterSearchOrder()
        tso.setKeywords([''])
        #tso.setLanguage('en')
        tso.setCount(100)
        tso.setIncludeEntities(False)
        tso.setGeocode(40.69, -73.94, 5)
        #tso.setUntil(dt.date(2014, 03, 24))

        ts = TwitterSearch(consumer_key='FqjFRT1OHl6xyIGoq9uXSA',
                           consumer_secret='KuhoVREmf7ngwjOse2JOLJOVXNCi2IVEzQZu2B8',
                           access_token='114454541-xcjy2sbl7Rr4oIaogsaBrlVL5H4CvcdvOSMy3MnR',
                           access_token_secret='yyBBOJhxgfw9pezZda2hWF94doONSd50y0JoylYjL3rmY', verify=False)
        records = []
        while True:

        # first query the Twitter API

            text_file = open('json_tweets' + str(t) + '.txt', 'a')
            text_fileE = open('error_log.txt', 'a')
            response = ts.searchTweets(tso)
            print 'req ' + str(req)
            req = req + 1
            todo = not len(response['content']['statuses']) == 0

        # check all tweets according to their ID

            for tweet in response['content']['statuses']:
                text_file.write(str(tweet))
                text_file.write('\n')
                tup = ()
                tweet_id = tweet['id']

        # print tweet_id,t

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
            print 'len: ' + str(len(records))
            tso.setMaxID(next_max_id)
            #raise TwitterSearchException(1000)
        

    except TwitterSearchException, e:

    # take care of all those ugly errors if there are some

        twitterFrame = pd.DataFrame.from_records(records, columns=[
            'Tweet ID',
            'Tweeted_At',
            'Profile_Create_at',
            'Username',
            'Location',
            'Enabled',
            'Place',
            'Geo',
            'Text',
            'Retweeted_Count',
            ])
        print 'Created DataFrame', len(twitterFrame)
        twitterFrame.to_csv('csv_tweets' + str(t) + '.csv')
        if len(twitterFrame) == 0:
            next_max_id = 0
        if text_file.closed:
            pass
        else:
            text_file.close()
        t = t + 1
        records = []
        print e
        text_fileE.write(str(e))
        text_fileE.write('\n')
        text_fileE.close()
        time.sleep(900)