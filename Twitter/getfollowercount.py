import os
import pandas as pd
import numpy as np
from lxml import html
import requests as req
import re
import matplotlib.pyplot as plt
plt.style.use('ggplot')

k_pattern = re.compile(r'K')
m_pattern = re.compile(r'M')

for file_name in os.listdir(os.readlink('tweets')):


    df = pd.read_csv(os.readlink('tweets') + file_name)
    followers = list()
    print file_name
    for user in df['Username']:
        page = req.get('https://twitter.com/'+ str(user))
        tree = html.fromstring(page.text)
        n_followers = tree.xpath('//a[@data-nav="followers"]/*/text()')
        if n_followers:
            n_followers[1] = re.sub(r',', '', n_followers[1])
            if k_pattern.search(n_followers[1]):
                n_followers[1] = re.sub(r'K', '', n_followers[1])
                n_followers[1] = int( float(n_followers[1])*1000)
            elif m_pattern.search(n_followers[1]):
                n_followers[1] = re.sub(r'M', '', n_followers[1])
                n_followers[1] = int(float(n_followers[1])*1000000)
            else:
                n_followers[1] = int(n_followers[1])

            followers.append([user, n_followers[1]])
    columns = ['username', 'followers']
    followers_df = pd.DataFrame(data = followers, columns=columns)
    followers_df.to_csv(os.readlink('output') + "followers_count.csv", mode='a+')
