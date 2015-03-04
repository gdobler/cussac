import csv
f = open("edgelist.csv")
reader = csv.reader(f)
d = {}
count = 1
for i in reader:
	if i[0] in d:
		print str(d[i[0]])+",",

	if i[0] not in d:
		d.setdefault(i[0],count)
		print str(count)+",",
		count+=1

	if i[1] in d:
		print str(d[i[1]])
		continue



	if i[1] not in d:
		d.setdefault(i[1],count)
		print str(count)
		count+=1
		continue

