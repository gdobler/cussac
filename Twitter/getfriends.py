
import sys
import os
import pandas as pd
import oauth2 as oauth
import json
import time
import datetime

APIKEYS = pd.read_json('../../cussacTest/cussacAPIKeys.json', typ = 'series')
CONSUMER_KEY = (APIKEYS['CONSUMER_KEY'])
CONSUMER_SECRET = (APIKEYS['CONSUMER_SECRET'])
ACCESS_TOKEN = (APIKEYS['ACCESS_TOKEN'])
ACCESS_TOKEN_SECRET = (APIKEYS['ACCESS_TOKEN_SECRET'])

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

def getAllFriends(username):
    apicallcount = 0
    numberofrecords = 0
    baseApiUrl = 'https://api.twitter.com/1.1/friends/ids.json?screen_name' + username + '&count=5000'
    
