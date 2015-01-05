import pandas as pd
import sys
import os
import csv
f = os.getcwd()
names = os.listdir(sys.argv[1])
os.chdir(sys.argv[1])
d = {}
c = 0
for i in names:
	df = pd.read_csv(i)
	c+=1
	splits = df['hashtags'].str.split(',')
	for i in splits:
		try:
			for j in i:
				count = d.setdefault(j, 0)
				d[j] = count + 1
		except:
			pass
	print c
key = d.keys()
value = d.values()
df2 = pd.DataFrame({'Key':key,'Value':value})
df2.dropna()
df2 = df2[df2['Key']!='']
df2 = df2.sort(['Value'], ascending = False)
#print df2.head()
df2 = df2[df2['Key'].str.len() >3]
df2['Key'] = df2['Key'].str[2:-1]

l1 = ["#2015","#nye","#2015\"","#nye\"","2015\"","#happynewyear","#newyearseve","nye","NYE","#NYE","2015","#newyear","#2014","happynewyear","#newyears","nyc","#happynewyear\""]
a = []
l2 = []
for i in l1:
    l2.append(i.lower())
#print l1
#df2['Class'] = df[]
for i in df2.Key:
    if str(i).lower() in l2:
        a.append(0)
        #print "Hi"
    elif "newyear" in str(i).lower():
        a.append(0)
    elif "201" in str(i).lower():
    	a.append(0)
    else:
        a.append(1)
df2['Class'] = a
df2.head(50)
print df2.head()
df2.to_csv('total hashtag.csv')