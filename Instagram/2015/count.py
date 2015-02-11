import csv
import sys

f = open(sys.argv[1])
reader = csv.reader(f)
c = 0
for i in reader:
	#print i
	if len(i[0])>3:
		c+=1
print c