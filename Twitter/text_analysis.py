from nltk.corpus import stopwords
from nltk import word_tokenize
import nltk.stem.porter as stem
import re
import matplotlib.pyplot as plt
import csv


def count_word_in_file (filename, dict, stemDict):
    with open(filename,'rU') as f:
        csvReader = csv.reader(f)
        headers = csvReader.next()    
        for row in csvReader:
            if len(row)!=11:
                continue
            count_words(row[9], dict, stemDict)
    
def count_words(tweetText, dict, stemDict):
    # convert to lower case
    tweetText = tweetText.lower()
    # leave only alphanumeric chars, spaces, #, @
    tweetText = re.sub('[^\\w@#\\s]', '', tweetText)
    
    words = tweetText.split(' ')
    
    stopWords = set(stopwords.words('english')+['http','','@'])
    stemmer = stem.PorterStemmer()
    
    for w in words:
        if w not in stopWords:
            if w in dict:
                dict[w]+=1
            else:
                dict[w]=1
            s = stemmer.stem(w)
            if s in stemDict:
                stemDict[s]+=1
            else:
                stemDict[s]=1


def draw_hist(dict,title):
    n = 25
    tuples = sorted(dict.items(), key = lambda x: x[1], reverse = True)
    plt.bar(range(n),[v for _,v in tuples][:n], width = 0.2, color='k')
    plt.xticks(range(n), [k for k,_ in tuples][:n], rotation = 90)
    plt.show()


def main():
    dict = {}
    stemDict = {}
    files = []
    for i in range(31,50):
        files.append('csv_tweetsNov_10_2014_15_'+str(i)+'.csv')
    for f in files:
        count_word_in_file (f, dict, stemDict)
    draw_hist(dict, "words count")
    draw_hist(dict, "stems count")
 
if __name__ == '__main__':
    main()
