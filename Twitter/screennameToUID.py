'''
NOTE:

Upto 100 comma seperated values allowed in each request.
'''

import numpy as np
import sys
import os
import pandas as pd
import oauth2 as oauth
import json
import time
import datetime
import glob
import logging
import math
import re


APIKEYS = pd.read_json('cussacAPIKeys.json', typ = 'series')
CONSUMER_KEY = (APIKEYS['CONSUMER_KEY'])
CONSUMER_SECRET = (APIKEYS['CONSUMER_SECRET'])
ACCESS_TOKEN = (APIKEYS['ACCESS_TOKEN'])
ACCESS_TOKEN_SECRET = (APIKEYS['ACCESS_TOKEN_SECRET'])

t = datetime.datetime.now()


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
    logging.basicConfig(filename = str(os.getenv('CUSSAC_LOGS')) + 'cussac_' + re.sub('.py','',os.path.basename(__file__)) + '_' + datetime.datetime.now().strftime('%b_%d_%y_%H_%M') + '.out', filemode = 'a', format = '%(asctime)s, %(msecs)d %(name)s %(levelname)s %(message)s', datefmt='%H:%M:%S', level = logging.DEBUG)



def oauth_req(url, http_method="GET", post_body='', http_headers=None):
    consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
    token = oauth.Token(key=ACCESS_TOKEN, secret=ACCESS_TOKEN_SECRET)
    client = oauth.Client(consumer, token)
    resp, content = client.request( url, method=http_method, body=post_body, headers=http_headers)
    content = json.loads(content)
    if resp['status'] != '200':
        raise Exception("Invalid response %s." % resp['status'])
        # TODO: consider terminating the script if theres an error
    return content

def screenname_to_uid(username_list):
    global t
    apicallcount = 0
    numberofrecords = 0
    print str(username_list)
    print str(type(username_list))
    usernames = ','.join(username_list)

    baseApiUrl = 'https://api.twitter.com/1.1/users/lookup.json?screen_name=' + str(usernames)
    print str((900 -(datetime.datetime.now()-t).total_seconds()))
    try:
        queryResults = oauth_req(baseApiUrl)
    except:
        logging.info('Exceeded call limit, sleeping for 15 minutes')
        logging.info(datetime.datetime.now())
        time.sleep(math.ceil(900 -(datetime.datetime.now()-t).total_seconds()))
        t = datetime.datetime.now()
    else:
        columns = ['id', 'screen_name', 'friends_count', 'followers_count']
        tweeters = pd.DataFrame(columns = columns)
        for i in range(len(queryResults)):
            tweeters.loc[i] = [queryResults[i]['id_str'], queryResults[i]['screen_name'], int(queryResults[i]['friends_count']), int(queryResults[i]['followers_count'])]
        logging.info(datetime.datetime.now())
        apicallcount +=1
        logging.info("number of API calls:" + str(apicallcount))
        logging.info('number of records:' +  str(len(queryResults)))
        return tweeters

def main():
    global t
    config_logger()
    chunk_size = 100
    nyers = pd.Series()
    for file_name in glob.glob(str(os.getenv('CUSSAC_DATA')) + 'nyers/*.csv'):
        temp_df = pd.read_csv(file_name, index_col = 0)
        nyers = pd.concat([temp_df['username'], nyers])

    nyers = nyers.reset_index(drop = True)
    #an errant nan value was present here.
    nyers = nyers.drop(77419)
    t = datetime.datetime.now()
    for i in range(0, len(nyers), chunk_size):
        uid_df = screenname_to_uid(nyers[i : i + chunk_size])
        if os.path.isfile(str(os.getenv('CUSSAC_OUTPUT')) + 'all_nyers.csv'):
            temp_df = pd.read_csv(str(os.getenv('CUSSAC_OUTPUT')) + 'all_nyers.csv', index_col = 0)
            temp_df = pd.concat([temp_df, uid_df], ignore_index = True, axis = 0)
            temp_df.to_csv(str(os.getenv('CUSSAC_OUTPUT')) + 'all_nyers.csv')
        else:
            uid_df.to_csv(str(os.getenv('CUSSAC_OUTPUT')) + 'all_nyers.csv', mode = 'w')


if __name__ == '__main__':
    main()

