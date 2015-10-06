'''
This script gets the full profile information for a UserID. It is meant
to complement the information gathered in the getfollowers.py script,
which MUST be run first. The output of that script is the input for this one.
The full profile information for a user is necessary to surmise whether they
are a New Yorker by using the text in their "location" field. The output of 
this script is fed into locationinfo.py.
Documentation: https://dev.twitter.com/rest/reference/get/users/lookup
'''
#TODO: make the script dynamic for follower ID.
import sys
import os
import pandas as pd
import oauth2 as oauth
import json
import time
import datetime
import itertools as it
import string

#Best practice is to NOT keep API keys in GitHub!
APIKEYS = pd.read_json('cussacAPIKeys.json')
CONSUMER_KEY = (APIKEYS['CONSUMER_KEY'].values)[0]
CONSUMER_SECRET = (APIKEYS['CONSUMER_SECRET'].values)[0]
ACCESS_TOKEN = (APIKEYS['ACCESS_TOKEN'].values)[0]
ACCESS_TOKEN_SECRET = (APIKEYS['ACCESS_TOKEN_SECRET'].values)[0]


def oauth_req(url, http_method="GET", post_body='', http_headers=None):
    consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
    token = oauth.Token(key=ACCESS_TOKEN, secret=ACCESS_TOKEN_SECRET)
    client = oauth.Client(consumer, token)
    resp, content = client.request( url, method=http_method, body=post_body, headers=http_headers)
    content = json.loads(content)
    if resp['status'] != '200':
        raise Exception("Invalid response %s." % resp['status'])
        # TODO: consider terminating the script if theres an error
    # print resp['status']
    return content

#you can only search for 100 users' details at a time -- this allows for
#paging through all of the user ids in batches of 100.
def followers_slice(listofFollowers, apicallcount):
    start = apicallcount * 100
    end = start + 99
    useridSlice = it.islice(listofFollowers, start, end)
    useridSliceCommaSep = ','.join(map(str,useridSlice))
    return useridSliceCommaSep


def get_follower_details():
    # This is pulling from a master list of all of the user ids from all of the
    # social landmarks. Could be changed to just run for one social landmark at
    # a time through command line.
    followersDF = pd.read_csv('sociallandmarks/APISearchuserids.csv')
    listofFollowers = followersDF['UserID'].tolist()
    numberOfFollowers = len(listofFollowers)
    apicallcount = 0
    endOfCurrSlice = apicallcount * 100 + 99
    baseApiUrl = 'https://api.twitter.com/1.1/users/lookup.json?user_id=' 
    #initializing dataframe for API call results
    data = {'UserID' : [], 'location' : [], 'screen_name' : [], 'name': [], 'geo_enabled': []}
    df = pd.DataFrame(data)
    #checks to see if there's already a file with follower details, creates one if not.
    if not os.path.isfile('sociallandmarks/APISearchuserdetails.csv'):
        df.to_csv('sociallandmarks/APISearchuserdetails.csv', header = True, columns = ['UserID', 
            'location', 'screen_name', 'name', 'geo_enabled'], engine='python')
    while endOfCurrSlice < numberOfFollowers:
        #try-except-else is the PEP-8 standard for try loops, for explanation see:
        #https://www.python.org/dev/peps/pep-0008/#programming-recommendations
        try:
            useridlistSlice = followers_slice(listofFollowers, apicallcount)
            requestUrl = baseApiUrl + useridlistSlice
            queryResults = oauth_req(requestUrl)
        except:
            print 'Exceeded call limit, sleeping for 15 minutes'
            print datetime.datetime.now()
            time.sleep(900)
            continue
        else:
            data = queryResults
            #creates a dataframe with the full query results (quite a lot of 
            #columns, most irrelevant)
            tempdf = pd.DataFrame(data=data)
            with open('sociallandmarks/APISearchuserdetails.csv', 'a') as f:
                #there are all sorts of special characters in Twitter text fields,
                #this drops any that are not ascii, using an anonymous (lambda) function
                tempdf['name'] = tempdf['name'].apply(lambda x: x.encode('ascii', 'ignore'))
                tempdf['location'] = tempdf['location'].apply(lambda x: x.encode('ascii', 'ignore'))
                #limits to only the fields in the query results that are relevant to this search.
                tempdf.to_csv(f, header=False, columns = ['id_str', 'location', 'screen_name','name', 'geo_enabled'], engine='python')#, encoding = 'utf-8')
            #debugging script
            print datetime.datetime.now()
            apicallcount +=1
            endOfCurrSlice = apicallcount * 100 + 99
            print "number of API calls:" + str(apicallcount)
            print 'sleeping now'
            #the free rate limit is one call per 5 seconds for this particular REST API
            time.sleep(5)


def main():
    get_follower_details()

if __name__ == '__main__':
    main()
