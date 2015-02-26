'''
https://pypi.python.org/pypi/textblob
$ pip install -U textblob
$ python -m textblob.download_corpora
'''
from textblob import TextBlob
import yaml
import csv
import os
import matplotlib.pyplot as plt

def sentimet_score_tweet (text):
    score = 0
    blob = TextBlob(text)
    for sentence in blob.sentences:
        score += sentence.sentiment.polarity
    return score
    
def sentimet_score_file (filename, data):
    with open(filename,'rU') as f:
        csvReader = csv.reader(f)
        headers = csvReader.next()    
        for row in csvReader:
            try:
                geoObj = yaml.load(row[8])
                lat = geoObj["u'coordinates'"][0]
                long = geoObj["u'coordinates'"][1]
                data.append([[lat,long] ,sentimet_score_tweet(row[9])])
            except:
                continue
    return data

def draw_map(data):
    x = [d[0][1] for d in data]
    y = [d[0][0] for d in data]
    colors = []
    for d in data:
        if d[1] < 0:
            colors.append('#e41a1c') # red
        elif d[1] > 0:
            colors.append('#4daf4a') # green
        else:
            colors.append('#f0f0f0') # grey
    
    plt.scatter(x = x, y = y,color = colors, alpha = 0.5, marker = '.', linewidths=0)
    plt.show()

def main():
    data = []
    for filename in os.listdir ('Data/'):
        data = sentimet_score_file('Data/' + filename, data)
    print "num of geo tag tweets displayed: " + str(len(data))
    draw_map(data)
        
if __name__ == '__main__':
    main()