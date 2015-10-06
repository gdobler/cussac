'''
This script is the basic twitter API search with some specifications:
Only pulls geocoded tweets, defined by a central lat/long and a search 
radius. Pulls all tweets from the last 5 seconds that match the filters.
This will run endlessly in the background unless the process specifically 
stopped. 
Documentation: https://dev.twitter.com/rest/public/search
'''
# example URL : https://api.twitter.com/1.1/search/tweets.json?q=&geocode=-22.912214,-43.230182,1km
import sys
import os
import pandas as pd
import oauth2 as oauth
import json
import time
import datetime

#Best practice is to NOT keep API keys in GitHub, but it's too late for that!
APIKEYS = pd.read_json('cussacAPIKeys.json')
CONSUMER_KEY = (APIKEYS['CONSUMER_KEY'].values)[0]
CONSUMER_SECRET = (APIKEYS['CONSUMER_SECRET'].values)[0]
ACCESS_TOKEN = (APIKEYS['ACCESS_TOKEN'].values)[0]
ACCESS_TOKEN_SECRET = (APIKEYS['ACCESS_TOKEN_SECRET'].values)[0]

#dummy empty search term
searchterm = ' '

#approximate centroid for New York City, with a radius of 20 miles--needed to 
#capture all of Brooklyn and the Bronx, though includes chunks of New Jersey and
#Long Island.
location = "40.69,-73.94,20mi"

def oauth_req(url, http_method="GET", post_body='', http_headers=None):
    consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
    token = oauth.Token(key=ACCESS_TOKEN, secret=ACCESS_TOKEN_SECRET)
    client = oauth.Client(consumer, token)
    resp, content = client.request( url, method=http_method, body=post_body,
        headers=http_headers)
    content = json.loads(content)
    if resp['status'] != '200':
        raise Exception("Invalid response %s." % resp['status'])
        # TODO: consider terminating the script if theres an error
    return content

def getTweets():
    apicallcount = 0
    # initializing a since_id, which is the earliest tweet ID to return. Prevents duplicates.
    since_id=0
    #initializes empty dataframe
    df = pd.DataFrame()
    while apicallcount > -1:
        baseurl = "https://api.twitter.com/1.1/search/tweets.json?q="+searchterm+\
            "&geocode="+location+"&count=100&since_id="+str(since_id)
        try:
            queryResults = oauth_req(baseurl)
            apicallcount += 1
        except:
            print 'Hit error or exceeded call limit, sleeping for 15 minutes'
            print datetime.datetime.now()
            now = datetime.datetime.now().strftime("%m-%d-%y_%H-%M-%S")
            df.to_csv('TwitterSearchOutput/tweets' + now +'.csv', index_label='index', 
                encoding='utf-8')
            df = pd.DataFrame()
            #Twitter's call limits are per 15 minute period
            time.sleep(901)
            continue
        else:
            data = queryResults['statuses']
            tempdf = pd.DataFrame(data=data)
            # this creates a new "since_id" which prevents duplicates, unless
            # no results have been returned in the last API call (which would)
            # throw an index out of range error.
            if len(tempdf) > 0:
                since_id = tempdf['id_str'].values[-1]
            #adding the latest query results to our master dataframe above
            df = df.append(tempdf)
            time.sleep(5)
        #saves to csv after every 100 API calls.
        if apicallcount % 100 == 0:
            now = datetime.datetime.now().strftime("%m-%d-%y_%H-%M-%S")
            df.to_csv('TwitterSearchOutput/tweets' + now +'.csv', index_label='index', encoding='utf-8')
            # Once the results from the last 100 calls have been written to csv,
            # the master dataframe has to be cleared out, as below.
            df = pd.DataFrame()

if __name__ == "__main__":
    getTweets()
