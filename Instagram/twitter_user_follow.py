from birdy.twitter import UserClient
import sys
import csv
consumer_key='bUnj1xErZSzxZjMToImER1fLN'
consumer_secret='FOSnFYC0qGzQi7DeD5P8c8YOIzp0QGQuOWDIdsuIprquJ161vo'
access_token='2951620465-ksudvvCcIojksqIR4Mni3cMsyN7WbqXXnq06VEy'
access_token_secret='V3sDNaIgQY1w3WT0Tuy9V6rFyF6VRoWq9KsZZLpJUqA2i'
client = UserClient(consumer_key,consumer_secret,access_token,access_token_secret)

f = open(sys.argv[1])
reader = csv.reader(f)
temp = []
for i in reader:
	temp = i
f.close()
user = {}
for i in temp:
	count = user.setdefault(i, 0)
	user[i] = count + 1
user_list = user.keys()
common_name = []
for i in user_list:
	response = client.api.users.show.get(screen_name = i)
	#if len(response)>0:
	common_name.append(i)
	#print common_name

	#print response.data
f = open(sys.argv[2])
writer = csv.writer(f)
writer.writerow(common_name)
f.close()

