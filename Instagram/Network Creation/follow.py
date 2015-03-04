from instagram.client import InstagramAPI
import csv
api = InstagramAPI(client_id='16f7ef0d35624ad3a3b07e18c9e45ef8', client_secret='22fdaddd6282489aab74528e16a06cb9')
f = open("testID.csv")
reader = csv.reader(f)
for row in reader:
	#print row
	try:
		follows = api.user_follows(row[1])[0]
		for i in follows:
			follower = str(i.id)
			print row[1]+","+ follower
			f1 = api.user_follows(follower)[0]
			#print f1
			#print follows
			for j in f1:
				print str(i.id)+","+str(j.id)
		
		followed_by = api.user_followed_by(row[1])[0]
		for i in followed_by:
			followed = str(i.id)
			print followed+","+row[1]
			f1 = api.user_followed_by(followed)[0]
			for j in f1:
				print followed+","+str(j.id)		
	except:
		continue