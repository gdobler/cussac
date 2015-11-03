''' Script that scrapes number of followers from a twitter timeline '''
import os
import pandas as pd
import numpy as np
from lxml import html
import requests as req
import re
import matplotlib.pyplot as plt
from multiprocessing import Pool

plt.style.use('ggplot')

def getHTML(username):
    page = req.get('https://twitter.com/'+ str(username))
    tree = html.fromstring(page.text)
    return tree

def writeFollowerCount(followers):
    columns = ['username', 'followers']
    followers_df = pd.DataFrame(data = followers, columns=columns)
    followers_df.to_csv(os.readlink('output') + "followers_count.csv", mode='a+')


def getFollowerCount(tweet_df): #change to html
    k_pattern = re.compile(r'K')
    m_pattern = re.compile(r'M')

    followers = list()
    for user in tweet_df['Username']:
        tree = getHTML(user)
        #Extracts a list of title and value
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
    return followers
    #writeFollowerCount(followers)
        #columns = ['username', 'followers']
        #followers_df = pd.DataFrame(data = followers, columns=columns)
        #followers_df.to_csv(os.readlink('output') + "followers_count.csv", mode='a+')



if __name__ == '__main__':
    # Read csv data from files
    i=0
    for file_name in os.listdir(os.readlink('tweets')):

        if i > 1:
            break

        tweet_df = pd.read_csv(os.readlink('tweets') + file_name)
        for user in tweet_df['Username']:
            pool = Pool(8)
            html_pages = getHTML(user)
            followers = pool.map(getFollowerCount, html_pages)
        writeFollowerCount(followers)
        i=i+1
