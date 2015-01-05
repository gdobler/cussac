import pandas as pd
import sys
import os
import csv
f = os.getcwd()
names = os.listdir(sys.argv[1])
os.chdir(sys.argv[1])
f1 = open('final.csv', 'w')
writer = csv.writer(f1)
c = 0
for i in names:
	f = open(i)
	reader = csv.reader(f)
	if c != 0:
		next(reader)
	c+=1
	for j in reader:
		writer.writerow(j)
	f.close()
f1.close()
