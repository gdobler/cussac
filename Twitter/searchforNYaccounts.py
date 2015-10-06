'''
This script takes a search term (like "Bronx") and returns the username 
results of a call to Twitter's Search API.
Documentation: https://dev.twitter.com/rest/reference/get/users/search
'''
import sys
import os
import pandas as pd
import oauth2 as oauth
import json
import time
import datetime
import string

#Best practice is to NOT keep API keys in public GitHub repos!
APIKEYS = pd.read_json('cussacAPIKeys.json')
CONSUMER_KEY = (APIKEYS['CONSUMER_KEY'].values)[0]
CONSUMER_SECRET = (APIKEYS['CONSUMER_SECRET'].values)[0]
ACCESS_TOKEN = (APIKEYS['ACCESS_TOKEN'].values)[0]
ACCESS_TOKEN_SECRET = (APIKEYS['ACCESS_TOKEN_SECRET'].values)[0]

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
    # print resp['status']
    return content


# example URL = 'https://api.twitter.com/1.1/users/search.json?q=New+York+City&page='+ pagecount +'&count=20'
def get_nyc_accounts(searchterm):
    data = {'UserID' : [], 'location' : [], 'screen_name' : [], 'name': [], 'geo_enabled': [], 
        'followers_count':[], 'verified':[], 'time_zone': [], 'geo': [], 'statuses_count': [],
        'description': []}
    df = pd.DataFrame(data)
    #this checks if a file already exists for this searchterm and creates one if it doesn't exist
    if not os.path.isfile(searchterm + 'Searchuserdetails.csv'):
        df.to_csv(searchterm + 'Searchuserdetails.csv', header = True, columns = ['UserID', 
            'location', 'screen_name', 'name', 'geo_enabled', 'followers_count', 'verified', 
            'time_zone', 'geo', 'statuses_count', 'description'], engine='python')
    for i in range(50):
        #this api is limited to the first 1000 results with a maximum of 20 results per call
        URL = 'https://api.twitter.com/1.1/users/search.json?q=' + searchterm + '&page='+ 
            str(i) +'&count=20'
        try:
            #try-except-else is the PEP-8 standard for try statements, for explanation see:
            #https://www.python.org/dev/peps/pep-0008/#programming-recommendations
            data = oauth_req(URL)
        except:
            print "error after " + str(i) + "calls, exiting program at:"
            # print 'sleeping 1 minute'
            # time.sleep(60)
            print time.time.now()
            break
        else:
            tempdf = pd.DataFrame(data=data)
            #because of the if not...: statement creating file, this can always be opened in 
            #append mode ('a')
            with open(searchterm + 'Searchuserdetails.csv', 'a') as f:
            #using "with open..." saves the trouble of having to put a close() statement after 
            #opening file
                tempdf['name'] = tempdf['name'].apply(lambda x: x.encode('ascii', 'ignore'))
                tempdf['location'] = tempdf['location'].apply(lambda x: x.encode('ascii', 'ignore'))
                tempdf['description'] = tempdf['description'].apply(lambda x: x.encode('ascii', 'ignore'))
                tempdf.to_csv(f, header=False, columns = ['id_str', 'location', 'screen_name', 
                    'name', 'geo_enabled', 'followers_count', 'verified', 'time_zone', 'geo', 
                    'statuses_count', 'description'], engine='python')#, encoding = 'utf-8')
            #debugging statements
            print "number of API calls:" + str(i)
            print 'sleeping now'
            #free API rate limit is one call per 5 seconds.
            time.sleep(5)


def main():
    if len(sys.argv) != 2:
        print 'please specify a search term'
    searchterm = sys.argv[1]
    get_nyc_accounts(searchterm)

if __name__ == '__main__':
    main()

