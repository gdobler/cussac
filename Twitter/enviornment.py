'''
This script is used for all enviornment related configuration. It supports outh authentication and logging.

'''

import sys
import os
import pandas as pd
import oauth2 as oauth
import json
import time
import datetime
import logging
import re


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

    def config_logger(self):
        logging.basicConfig(filename = str(os.getenv('CUSSAC_LOGS')) + '/cussac_' + re.sub('.py','',os.path.basename(__file__)) + '_' + datetime.datetime.now().strftime('%b_%d_%y_%H_%M') + '.out', filemode = 'a', format = '%(asctime)s, %(msecs)d %(name)s %(levelname)s %(message)s', datefmt='%H:%M:%S', level = logging.DEBUG)


#class TwitterAuth(object):
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


#sys.stdout = SystemLog('stdout')
#sys.stderr = SystemLog('stderr')
