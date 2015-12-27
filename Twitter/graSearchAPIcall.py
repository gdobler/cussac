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
import logging
import math
import re

APIKEYS = pd.read_json(str(os.getenv('CUSSAC_KEYS')) + '/cussacAPIKeys.json', typ = 'series')
CONSUMER_KEY = (APIKEYS['CONSUMER_KEY'])
CONSUMER_SECRET = (APIKEYS['CONSUMER_SECRET'])
ACCESS_TOKEN = (APIKEYS['ACCESS_TOKEN'])
ACCESS_TOKEN_SECRET = (APIKEYS['ACCESS_TOKEN_SECRET'])

t = datetime.datetime.now()

#dummy empty search term
searchterm = ' '

#approximate centroid for New York City, with a radius of 20 miles--needed to 
#capture all of Brooklyn and the Bronx, though includes chunks of New Jersey and
#Long Island.
#THIS STRING MUST NOT HAVE SPACES
location = "40.69,-73.94,20mi"


#location = "40.01,-100.82,1300mi"


class SystemLog(object):
    def __init__(self, name=None):
        self.logger = logging.getLogger(name)

    def write(self, msg, level=logging.INFO):
        self.logger.log(level, msg)

    def flush(self):
        for handler in self.logger.handlers:
            handler.flush()

sys.stdout = SystemLog('stdout')
sys.stderr = SystemLog('stderr')

def config_logger():
    logging.basicConfig(filename = str(os.getenv('CUSSAC_LOGS')) + '/' + re.sub('.py','',os.path.basename(__file__)) + '_' + datetime.datetime.now().strftime('%b_%d_%y_%H_%M') + '.out', filemode = 'a', format = '%(asctime)s, %(msecs)d %(name)s %(levelname)s %(message)s', datefmt='%H:%M:%S', level = logging.DEBUG)


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
    global t
    apicallcount = 0
    # initializing a since_id, which is the earliest tweet ID to return. Prevents duplicates.
    since_id=0
    #initializes empty dataframe
    df = pd.DataFrame()
    t = datetime.datetime.now()
    while apicallcount > -1:
        baseurl = "https://api.twitter.com/1.1/search/tweets.json?q="+searchterm+\
            "&geocode="+location+"&count=100&since_id="+str(since_id)
        try:
            queryResults = oauth_req(baseurl)
            apicallcount += 1
        except:
            logging.info( 'Hit error or exceeded call limit, sleeping for 15 minutes')
            logging.info(datetime.datetime.now())
            now = datetime.datetime.now().strftime("%m-%d-%y_%H-%M-%S")
            df.to_csv(str(os.getenv('CUSSAC_OUTPUT')) + '/nonnyers_tweets' + now +'.csv', index_label='index', 
                encoding='utf-8')
            df = pd.DataFrame()
            #Twitter's call limits are per 15 minute period
            
	    time.sleep(math.ceil(900 -(datetime.datetime.now()-t).total_seconds()))
	    t = datetime.datetime.now()
            continue
        else:
	    logging.info(queryResults)
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
            df.to_csv(str(os.getenv('CUSSAC_OUTPUT')) + '/nonnyers_tweets' + now +'.csv', index_label='index', encoding='utf-8')
            # Once the results from the last 100 calls have been written to csv,
            # the master dataframe has to be cleared out, as below.
            df = pd.DataFrame()

if __name__ == "__main__":
    config_logger()
    getTweets()
