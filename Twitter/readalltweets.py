import os
import sys
import pandas as pd
import glob

csvcount = 0

for csvfile in glob.glob('cussac/*.csv'):
	if csvcount == 0:
		df = pd.read_csv(csvfile)
		print "df created"
		csvcount += 1
	else:
		tempfile = pd.read_csv(csvfile)
		df = df.append(tempfile)
		csvcount +=1
		# print "file appended"
	print csvcount
	print csvfile
df = df[df.Place != None]
df = df.drop_duplicates(['Tweet ID'])
	# print df.tail(1)
df.to_csv('concat.csv')
print 'Done'
print df.shape