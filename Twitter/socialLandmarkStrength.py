'''
This script creates a matrix of nyers and the landmarks they follow
'''
import os
import pandas as pd
import numpy as np
import json

with open(str(os.getenv('CUSSAC_OUTPUT')) + '/ny_followings.json', 'r') as f:
    ny_friends = json.load(f)
    
nyers = pd.read_csv(str(os.getenv('CUSSAC_OUTPUT')) + '/nyers.csv', index_col = 0)

nyers = nyers.drop_duplicates(subset = 'id')
nyers = nyers.reset_index(drop = True)
social_landmarks = (nyers[nyers['followers_count'] >= 1000])
social_landmarks = social_landmarks.reset_index(drop = True)

sl_strength = np.zeros((len(ny_friends.keys()),len(social_landmarks)), dtype = np.int)
sl_strength = np.matrix(sl_strength)

nyer_lookup = pd.DataFrame(ny_friends.keys(), columns = ['screen_name'])

for key in ny_friends.iterkeys():
    indices = (social_landmarks[social_landmarks['id'].isin(ny_friends[key][0])]).index.values
    sl_strength[nyer_lookup[nyer_lookup['screen_name'] == key ].index.values[0], indices]+=1
    
np.save(os.getenv('CUSSAC_OUTPUT') + '/social_landmark_strength.npy', sl_strength)
