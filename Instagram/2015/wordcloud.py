import pandas as pd
import sys
import csv

f = open(sys.argv[1])
reader = csv.reader(f)
header = next(reader)
a = []
for i in reader:
	c = 0
	flag = 0
	for j in i[1]:
		if j == '#':
			a.append(i[1][c+1:])
			flag = 1
			break
		else:
			c+=1
	if flag == 0:
		a.append(i[1])
	#string = i[1][]
df = pd.read_csv(sys.argv[1])
print len(a),len(df.Value)
b = list(df.Value)
c = 0
data = pd.DataFrame({'Tag':a,'Count':b})
for i in data.Count.head(100):
	for j in xrange(int(i)):
		print a[c],
	c+=1 
