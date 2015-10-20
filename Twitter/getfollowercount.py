import os
import pandas as pd
import numpy as np
from lxml import html
import requests as req

path =  r'/projects/open/SocMedia/tweets/'
if not os.path.exists(path+'FollowerCount'):
    os.mkdir(path+'FollowerCount', mode=0777)

for file_name in os.listdir(path):
    #df = pd.read_csv(path + str('csv_tweetsFeb_22_2015_14_37.csv'))
    df = pd.read_csv(path + file_name)
    columns = ['username', 'followers']
    followers_df = pd.DataFrame(data=None, index=None, columns=columns)

    for user in df['Username']:
        page = req.get('https://twitter.com/'+ str(user))
        tree = html.fromstring(page.text)
        n_followers = tree.xpath('//a[@data-nav="followers"]/*/text()')
        if n_followers:
            print user, n_followers[1]
            followers_df.append(pd.DataFrame(list(user, n_followers[1]), columns=columns))
            print followers_df









#csv_tweetsFeb_22_2015_14_37.csv
