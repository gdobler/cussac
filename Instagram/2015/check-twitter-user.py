
import argparse
import urllib2
import json
import sys
import csv

USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1'
URL_TEMPLATE = 'https://www.twitter.com/users/username_available?suggest=1&username=%s&full_name=&email=&suggest_on_username=true&context=front&custom=1'

def check_name(screen_name):
    url = URL_TEMPLATE % screen_name

    req = urllib2.Request(url)

    """
        Response will be in the form

        {"desc":"Available!","reason":"available","msg":"Available!","valid":true,"suggestions":[]}
        {"suggestions":[],"desc":"That username has been taken. Please choose another.","reason":"taken","msg":"Username has already been taken","valid":false}
    """
    try:
        json_res = urllib2.urlopen(req).read()
        resp = json.loads(json_res)
        return resp["reason"]
    except urllib2.HTTPError, e:
        return "error: %s" % (e.code,)

def print_result(screen_name, msg):
    display = "[%s] %s %s\n"
    if "taken" in msg:
        print screen_name
        return screen_name

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="check-twitter-user")
    parser.add_argument('username', help="name to check for")
    args = parser.parse_args()
    f = open(sys.argv[1])
    reader = csv.reader(f)
    next(reader)
    f1 = open('common_names.csv', 'w')
    writer = csv.writer(f1)
    for i in reader:
        screen_name = i[1]
        msg = check_name(screen_name)
        x = [print_result(screen_name, msg)]
        writer.writerow(x)

