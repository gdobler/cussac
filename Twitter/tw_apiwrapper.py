'''
This script is a wrapper to the twitter API. It supports GET of friends and followers for a user.
'''
import time
import datetime
import logging
import enviornment
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


#Gets the ids of @screen_name's friends
def get_all_friends(file_name = 'all_friends.json', screen_name = '', user_id = ''):
    if screen_name:
        apicallcount = 0
        numberofrecords = 0
        baseApiUrl = 'https://api.twitter.com/1.1/friends/ids.json?screen_name=' + str(screen_name) + '&count=5000'

        # TODO : handle script for more than 5000 followings
        cursor = -1
        while cursor !='0':
            #try-except-else is the PEP-8 standard for try loops, for explanation see:
            #https://www.python.org/dev/peps/pep-0008/#programming-recommendations
            t0 =  datetime.datetime.now()
            try:
                requestUrl = baseApiUrl + '&cursor=' + str(cursor)
                queryResults = enviornment.oauth_req(requestUrl)
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
                logging.info("Private account - " + str(screen_name) + ", Getting next screen_name")
            except enviornment.NotFoundException:
                logging.info("Handle not found - "+ str(screen_name))
            except Exception as e:
                logging.error("Unknown Exception occured" + str(e))
            else:
                logging.info("Time to get followings for " + str(screen_name) + " " + str((t0 - datetime.datetime.now()).total_seconds())+ "seconds")
                actualCursor = queryResults['next_cursor_str']
                cursor = actualCursor
                #creates dataframe. TODO: look into editing index start point (not critical)
                record = { 'user_id' : user_id , 'screen_name' : screen_name , 'friend_ids': queryResults['ids'], 'time_stamp': str(datetime.datetime.now())}
                logging.info(datetime.datetime.now())
                apicallcount +=1
                logging.info("Number of API calls:" + str(apicallcount))
                numberofrecords = numberofrecords + len(queryResults['ids'])
                logging.info('Number of records:' +  str(numberofrecords))
                #debugging: making sure the cursor is changing, save most recent
                #cursor in case script breaks before completing
                logging.info('Latest cursor:' + str(cursor))
                return record

    elif user_id:
        apicallcount = 0
        numberofrecords = 0
        baseApiUrl = 'https://api.twitter.com/1.1/friends/ids.json?user_id=' + str(user_id) + '&count=5000'

        # TODO : handle script for more than 5000 followings
        cursor = -1
        while cursor !='0':
            #try-except-else is the PEP-8 standard for try loops, for explanation see:
            #https://www.python.org/dev/peps/pep-0008/#programming-recommendations
            t0 =  datetime.datetime.now()
            try:
                requestUrl = baseApiUrl + '&cursor=' + str(cursor)
                queryResults = enviornment.oauth_req(requestUrl)
            except enviornment.RateLimitException as e:
                print(e)
                logging.info('Exceeded call limit, sleeping for 15 minutes')
                logging.info(datetime.datetime.now())
                logging.info('latest cursor:' + str(cursor))
                time.sleep(60*15)
                logging.info('Been sleeping for so far ' + str((t0 - datetime.datetime.now()).total_seconds()) + "seconds")
                logging.info("Time between request and now " + str((t0 - datetime.datetime.now()).total_seconds())+ "seconds")
                continue
            except enviornment.NotAuthorizedException:
                logging.info("Private account - " + str(user_id) + ", Getting next user_id")
            except enviornment.NotFoundException:
                logging.info("user ID found - "+ str(user_id))
            except Exception as e:
                logging.error("Unknown Exception occured" + str(e))
            else:
                logging.info("Time to get followings for " + str(user_id) + " " + str((t0 - datetime.datetime.now()).total_seconds())+ "seconds")
                actualCursor = queryResults['next_cursor_str']
                cursor = actualCursor
                #creates dataframe. TODO: look into editing index start point (not critical)
                record = { 'user_id' : user_id , 'screen_name' : screen_name , 'friend_ids': queryResults['ids'], 'time_stamp': str(datetime.datetime.now())}
                logging.info(datetime.datetime.now())
                apicallcount +=1
                logging.info("Number of API calls:" + str(apicallcount))
                numberofrecords = numberofrecords + len(queryResults['ids'])
                logging.info('Number of records:' +  str(numberofrecords))
                #debugging: making sure the cursor is changing, save most recent
                #cursor in case script breaks before completing
                logging.info('Latest cursor:' + str(cursor))
                return record

#Bulk converts ids to handle
#API only accepts the 100 ids/handles at a Time
def lookup_users_info(screen_name_list = '', user_id_list = ''):
    apicallcount = 0
    numberofrecords = 0
    query_limit = 100
    queryResults = []
    for i in range(len(user_id_list.split(','))/query_limit + 1):
        user_id_list_segment = str(map(int, user_id_list.split(',')[i*100 : (i*100) + 100])).strip('[]').replace(' ','')
        baseApiUrl = 'https://api.twitter.com/1.1/users/lookup.json?user_id=' + str(user_id_list_segment)

        t0 =  datetime.datetime.now()
        try:
            requestUrl = baseApiUrl
            queryResults.extend(enviornment.oauth_req(requestUrl, http_method='POST'))
        except enviornment.RateLimitException as e:
            print(e)
            logging.info('Exceeded call limit, sleeping for 15 minutes')
            logging.info(datetime.datetime.now())
            logging.info('latest cursor:' + str(cursor))
            time.sleep(60*15)
            logging.info('Been sleeping for so far ' + str((t0 - datetime.datetime.now()).total_seconds()) + "seconds")
            logging.info("Time between request and now " + str((t0 - datetime.datetime.now()).total_seconds())+ "seconds")
            continue
        #TODO: Fix exception messaging
        except enviornment.NotAuthorizedException:
            logging.info("Private account - "  + ", Getting next user_id")
        except enviornment.NotFoundException:
            logging.info("user ID found - ")
        except Exception as e:
            logging.error("Unknown Exception occured" + str(e))
        else:
            logging.info("Time to get followings for iteration " + str(i) + " " + str((t0 - datetime.datetime.now()).total_seconds())+ "seconds")
    return queryResults


def get_tweets(hashtag, n_requests = 1):
    max_id = 0
    queryResults = []
    t0 =  datetime.datetime.now()
    for i in range(n_requests):
        try:
            if max_id:
                baseApiUrl = 'https://api.twitter.com/1.1/search/tweets.json?q=' + str(hashtag) + '&max_id=' + str(max_id) + '&count=100'
            else:
                baseApiUrl = 'https://api.twitter.com/1.1/search/tweets.json?q=' + str(hashtag) + '&count=100'
            requestUrl = baseApiUrl
            queryResults.append(enviornment.oauth_req(requestUrl, http_method='GET'))
        except enviornment.RateLimitException as e:
            print(e)
            logging.info('Exceeded call limit, sleeping for 15 minutes')
            logging.info(datetime.datetime.now())
            logging.info('latest cursor:' + str(cursor))
            time.sleep(60*15)
            logging.info('Been sleeping for so far ' + str((t0 - datetime.datetime.now()).total_seconds()) + "seconds")
            logging.info("Time between request and now " + str((t0 - datetime.datetime.now()).total_seconds())+ "seconds")
            continue
        #TODO: Fix exception messaging
        except enviornment.NotAuthorizedException:
            logging.info("Private account - "  + ", Getting next user_id")
            continue
        except enviornment.NotFoundException:
            logging.info("user ID found - ")
            continue
        except Exception as e:
            logging.error("Unknown Exception occured" + str(e))
            continue
        else:
            logging.info("Got data "  + str((t0 - datetime.datetime.now()).total_seconds())+ "seconds")
            max_id = (queryResults[-1]['statuses'][-1]['id']) - 1
    return queryResults
