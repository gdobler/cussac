'''
This script runs an API call to get every follower ID of a "social landmark"
IMPORTANT: It takes in the Twitter handle of the social landmark
as a command-line argument.
DOUBLE IMPORTANT: this ONLY returns IDs. In order to get the full profile
information for that user, another API call is needed -- see
returnfollowerdetails.py
Documentation: https://dev.twitter.com/rest/reference/get/followers/ids
'''

# example of url : oauth_req( 'https://api.twitter.com/1.1/followers/ids.json?cursor=-1&screen_name=nypost&count=5000')

import sys
import os
import pandas as pd
import oauth2 as oauth
import json
import time
import datetime

#Best practice is to NOT keep API keys in public GitHub repos!

APIKEYS = pd.read_json(os.getenv('CUSSAC_KEYS') + '/cussacAPIKeys.json', typ = 'series')
CONSUMER_KEY = (APIKEYS['CONSUMER_KEY'])
CONSUMER_SECRET = (APIKEYS['CONSUMER_SECRET'])
ACCESS_TOKEN = (APIKEYS['ACCESS_TOKEN'])
ACCESS_TOKEN_SECRET = (APIKEYS['ACCESS_TOKEN_SECRET'])

#APIKEYS = pd.read_json('cussacAPIKeys.json')
#CONSUMER_KEY = (APIKEYS['CONSUMER_KEY'].values)[0]
#CONSUMER_SECRET = (APIKEYS['CONSUMER_SECRET'].values)[0]
#ACCESS_TOKEN = (APIKEYS['ACCESS_TOKEN'].values)[0]
#ACCESS_TOKEN_SECRET = (APIKEYS['ACCESS_TOKEN_SECRET'].values)[0]

#Setting up API authentication
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

def getAllFollowers(username):
    apicallcount = 0
    numberofrecords = 0
    baseApiUrl = 'https://api.twitter.com/1.1/followers/ids.json?screen_name=' + username + '&count=5000'
#a 'cursor' in the context of API calls is the way you track which page of results you're
#currently on. Twitter counts down from most recent followers to oldest followers,
#and gives the cursor of 0 when you reach the last page of results, and allows you to indicate
#initialize the call with -1
    cursor = -1
    data = {'UserID' : []}
    df = pd.DataFrame(data)
    #checks to see if there's already a file with followers for this user --
    #if not, creates new csv file
    if not os.path.isfile('sociallandmarks/'+ username + 'followerids.csv'):
        df.to_csv('sociallandmarks/'+ username + 'followerids.csv')
    while cursor !='0':
        #try-except-else is the PEP-8 standard for try loops, for explanation see:
        #https://www.python.org/dev/peps/pep-0008/#programming-recommendations
        try:
            requestUrl = baseApiUrl + '&cursor=' + str(cursor)
            queryResults = oauth_req(requestUrl)
        except:
            print 'Exceeded call limit, sleeping for 15 minutes'
            #it's possible to hit exceptions for something other than call
            #limit--improvement to create if-statement to display the exact
            #exception, handle exceptions differently.
            print datetime.datetime.now()
            print 'latest cursor:' + cursor
            time.sleep(900)
            continue
        else:
            actualCursor = queryResults['next_cursor_str']
            cursor = actualCursor
            #creates dataframe. TODO: look into editing index start point (not critical)
            data = {'UserID' : queryResults['ids']}
            tempdf = pd.DataFrame(data)
            #append to csv continuously, because this script can take hours and
            #hours to run--better to save partially complete work than lose everything.
            with open('sociallandmarks/'+ username + 'followerids.csv', 'a') as f:
                tempdf.to_csv(f, header=False)
            #debugging/status update printing
            print datetime.datetime.now()
            apicallcount +=1
            print "number of API calls:" + str(apicallcount)
            numberofrecords = numberofrecords + len(queryResults['ids'])
            print 'number of records:' +  str(numberofrecords)
            #debugging: making sure the cursor is changing, save most recent
            #cursor in case script breaks before completing
            print 'latest cursor:' + cursor
            print 'sleeping now'
            #free API access has a limit of one call per minute (specifically,
            #15 calls per 15 minutes)
            #time.sleep(60)



def main():
    if len(sys.argv) != 2:
        print 'correct input is script name followed by the username being searched, i.e. NYTimes'
    username = sys.argv[1]
    # intiate call to fetch all followers for that username
    getAllFollowers(username)


if __name__ == '__main__':
    main()
