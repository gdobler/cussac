import csv
from instagram.client import InstagramAPI

api = InstagramAPI(client_id='16f7ef0d35624ad3a3b07e18c9e45ef8', client_secret='22fdaddd6282489aab74528e16a06cb9')
f = open("unames.csv")
reader = csv.reader(f)
#f1 = open("testID.csv",'w')
#writer = csv.writer(f1)
userid = []
x = 0
for i in reader:
	if x>5:
		break
	try:
		user = api.user_search(q = i[1], count = 1)
		print str(user[0])[6:]+","+ user[0].id
	except:
		continue
	x+=1
