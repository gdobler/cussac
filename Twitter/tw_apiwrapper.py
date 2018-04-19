'''
This script is a wrapper to the twitter API. It supports GET of friends and followers for a user.
'''
import time
import datetime
import logging
import enviornment

class TwitterAPI():
    def getAllFriends(username):
        apicallcount = 0
        numberofrecords = 0
        baseApiUrl = 'https://api.twitter.com/1.1/friends/ids.json?user_id=' + str(username) + '&count=5000'

        # TODO : handle script for more than 5000 followings
        cursor = -1
        while cursor !='0':
            #try-except-else is the PEP-8 standard for try loops, for explanation see:
            #https://www.python.org/dev/peps/pep-0008/#programming-recommendations
            t0 =  datetime.datetime.now()
            try:
                requestUrl = baseApiUrl + '&cursor=' + str(cursor)
                queryResults = enviornment.TwitterAuth.oauth_req(requestUrl)
            except enviornment.RateLimitException as e:
                print(e)
                logging.info('Exceeded call limit, sleeping for 15 minutes')
                logging.info(datetime.datetime.now())
                logging.info('latest cursor:' + str(cursor))
                time.sleep(60)
                logging.info('Been sleeping for so far ' + str((t0 - datetime.datetime.now()).total_seconds()) + "seconds")
                logging.info("Time between request and now " + str((t0 - datetime.datetime.now()).total_seconds())+ "seconds")
                continue
            except enviornment.NotAuthorizedException:
                logging.info("Private account - " + str(username) + ", Getting next username")
                return None
            except enviornment.NotFoundException:
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
                #out of else... maybe in else??
                logging.info(datetime.datetime.now())
                apicallcount +=1
                logging.info("Number of API calls:" + str(apicallcount))
                numberofrecords = numberofrecords + len(queryResults['ids'])
                logging.info('Number of records:' +  str(numberofrecords))
                #debugging: making sure the cursor is changing, save most recent
                #cursor in case script breaks before completing
                logging.info('Latest cursor:' + str(cursor))
                return record
