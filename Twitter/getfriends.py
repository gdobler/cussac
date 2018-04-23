'''
This script runs an API call to get every following ID of a users known to have tweeted from new york
IMPORTANT: It reads csv files containg the screen_name in a column called 'username'
DOUBLE IMPORTANT: this ONLY returns IDs. In order to get the full profile
information for that user, another API call is needed

Documentation: https://dev.twitter.com/rest/reference/get/friends/ids
'''



# example of url : oauth_req( 'https://api.twitter.com/1.1/followers/ids.json?cursor=-1&screen_name=nypost&count=5000')

import sys
import os
import pandas as pd
import oauth2 as oauth
import json
import time
import datetime
import logging
import re


#Best practice is to NOT keep API keys in public GitHub repos!

APIKEYS = pd.read_json(os.getenv('CUSSAC_KEYS') + '/cussacAPIKeys.json', typ = 'series')
CONSUMER_KEY = (APIKEYS['CONSUMER_KEY'])
CONSUMER_SECRET = (APIKEYS['CONSUMER_SECRET'])
ACCESS_TOKEN = (APIKEYS['ACCESS_TOKEN'])
ACCESS_TOKEN_SECRET = (APIKEYS['ACCESS_TOKEN_SECRET'])

class RateLimitException(Exception):
    pass

class NotAuthorizedException(Exception):
    #This class was created to ensure private users info wasn't being pulled.
    #Other reasons possible
    pass

class NotFoundException(Exception):
    #User not found
    pass

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
    logging.basicConfig(filename = str(os.getenv('CUSSAC_LOGS')) + '/cussac_' + re.sub('.py','',os.path.basename(__file__)) + '_' + datetime.datetime.now().strftime('%b_%d_%y_%H_%M') + '.out', filemode = 'a', format = '%(asctime)s, %(msecs)d %(name)s %(levelname)s %(message)s', datefmt='%H:%M:%S', level = logging.DEBUG)


#Setting up API authentication
def oauth_req(url, http_method="GET", post_body='', http_headers=None):
    consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
    token = oauth.Token(key=ACCESS_TOKEN, secret=ACCESS_TOKEN_SECRET)
    client = oauth.Client(consumer, token)
    resp, content = client.request( url, method=http_method, body=post_body, headers=http_headers)
    content = json.loads(content)
    if resp['status'] == '200':
	return content
    elif resp['status'] == '429':
	logging.info(str(resp))
	logging.info("Too many requests")
	raise RateLimitException("Invalid response %s." % resp['status'])
    elif resp['status'] == '401':
        raise NotAuthorizedException("Not authorized %s." % resp['status'])
        # TODO: consider terminating the script if theres an error
    elif resp['status'] == '404':
	logging.info("User not Found %s" % resp['status'])
	raise NotFoundException()
    else:
	logging.info("Error code : " + str(resp['status']))
	raise Exception("Invalid response %s." % resp['status'])

def getAllFriends(username):
    apicallcount = 0
    numberofrecords = 0
    baseApiUrl = 'https://api.twitter.com/1.1/friends/ids.json?user_id=' + str(username) + '&count=5000'

    # TODO : handle script for more than 5000 followings
    cursor = -1
    while cursor !='0':
        #try-except-else is the PEP-8 standard for try loops, for explanation see:
        #https://www.python.org/dev/peps/pep-0008/#programming-recommendations
        try:
	    t0 =  datetime.datetime.now()
            requestUrl = baseApiUrl + '&cursor=' + str(cursor)
            queryResults = oauth_req(requestUrl)
        except RateLimitException as e:
	    print e
            logging.info('Exceeded call limit, sleeping for 15 minutes')
            logging.info(datetime.datetime.now())
            logging.info('latest cursor:' + str(cursor))
            for i in range(15):
		t1 =  datetime.datetime.now()
		time.sleep(60)
		logging.info('Been sleeping for so far ' + str((t0 - datetime.datetime.now()).total_seconds()) + "seconds")

	    logging.info("Time between request and now " + str((t0 - datetime.datetime.now()).total_seconds())+ "seconds")
            continue
	except NotAuthorizedException:
	    logging.info("Private account - " + str(username) + ", Getting next username")
	    return None
	except NotFoundException:
	    logging.info("Handle not found - "+ str(username))
	    return None
	except Exception as e:
	    logging.error("Unknown Exception occured" + str(e))
        else:
	    logging.info("Time to get followings for " + str(username) + " " + str((t0 - datetime.datetime.now()).total_seconds())+ "seconds")
            actualCursor = queryResults['next_cursor_str']
            cursor = actualCursor
            #creates dataframe. TODO: look into editing index start point (not critical)
            #data = {'UserID' : queryResults['ids']}
            record = { username : [queryResults['ids'], str(datetime.datetime.now())]}

        logging.info(datetime.datetime.now())
        apicallcount +=1
        logging.info("Number of API calls:" + str(apicallcount))
        numberofrecords = numberofrecords + len(queryResults['ids'])
        logging.info('Number of records:' +  str(numberofrecords))
        #debugging: making sure the cursor is changing, save most recent
        #cursor in case script breaks before completing
        logging.info('Latest cursor:' + str(cursor))
        return record



def main():
    config_logger()
    logging.info("Running " + str(os.path.basename(__file__ )))
    records = {}


    if len(sys.argv) < 2:
        logging.info('correct input is script name followed by the csv filename with twitter handles')

    #Code to test
    #Input multiple twitter handles as command line arguments while running script

#    for username in sys.argv[1:]:
#       logging.info("Getting follows for @" + username)
#    	response = getAllFriends(username)
#    	records[username] = response[username]
#	if len(records.keys()) > 2:
#	    if os.path.isfile('output/cmdlinesamplefollowingids.json'):
#	    	with open('output/cmdlinesamplefollowingids.json', 'r') as f:
#			temp_dict = json.load(f)
			#The following code will take keys from record in case of key conflict. Essential to clean data to have only unique users
#			temp_dict.update(records)
#
#		with open ('output/cmdlinesamplefollowingids.json', 'w') as f:
#			json.dump(temp_dict, f)
#			records = {}
#	    else:
#		with open('output/cmdlinesamplefollowingids.json', 'w') as f:
#			json.dump(records, f)
#
#    with open( 'output/cmdlinesamplefollowingids.json', 'r') as f:
#	temp_dict = json.load(f)
#	temp_dict.update(temp_dict, f)
#    with open('output/cmdlinesamplefollowingids.json', 'w') as f:
#        json.dump(records, f)
#	records = {}


    file_name = sys.argv[1]
    users = pd.read_csv(str(os.getenv('CUSSAC_DATA')) + str('/') + str(file_name), index_col = 0)
    users = users.reset_index(drop = True)
    for user in users['ids']:
	response = getAllFriends(user)
	if response == None:
	    logging.info('None Response : ' + str(user))
	    continue
        records[user] = response[user]
	if len(records.keys()) > 50:
            if os.path.isfile('output/'+ re.sub('.csv','',file_name) + 'followingids.json'):
                with open('output/'+ re.sub('.csv','',file_name) + 'followingids.json', 'r') as f:
                        temp_dict = json.load(f)
                        #The following code will take keys from record in case of key conflict.
			#Essential to use cleaned data that has only unique users
                        temp_dict.update(records)

                with open ('output/'+ re.sub('.csv','',file_name) + 'followingids.json', 'w') as f:
                        json.dump(temp_dict, f)
                        records = {}
            else:
		logging.info('First write')
                with open('output/'+ re.sub('.csv','',file_name) + 'followingids.json', 'w') as f:
                        json.dump(records, f)

    logging.info('Out of forloop, before modulus write')
    with open('output/'+ re.sub('.csv','',file_name) + 'followingids.json', 'r') as f:
	logging.info('Reading in existing file for end of file')
        temp_dict = json.load(f)
        temp_dict.update(temp_dict, f)
    with open('output/'+ re.sub('.csv','',file_name) + 'followingids.json', 'w') as f:
        logging.info('Writing to existing file for end of file')
	json.dump(records, f)
        records = {}



if __name__ == '__main__':
    main()
