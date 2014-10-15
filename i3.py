'''Instagram API used to collect posts in New York City
Written by; Sriniketh Vijayaraghavan
NYU, CUSP
sv1272
In this code, I have not yet checked the amount of requests that are allowed at a time after which
we get throttled, so no sleep function is used. Also getting a lot of repeats in a short time
so weeded out those posts. Still working on getting the exact location of a geotagged post instead
of just looking through the latitude and longitude. Code works indefinitely and can be stopped
by using a keyboard interrupt. The file is continuously written to so at any point of time
if the code stops prematurely then the data collected so far still remains.

That's it for now. Cheers! Sorry it took so long to upload. Just wanted to check some functionalities.
'''

from instagram.client import InstagramAPI
import time
import csv

#Creating the csv file at the current directory named 'dump'
f = open('dump.csv','w')
f.write('')
f.close()
#Appending to this file every time the program is run. If the file already exists
#and you want to just append to it comment out the previous part
f = open('dump.csv', 'a+')
insta_write = csv.writer(f,delimiter = ',')
#creating the following headers for the instagram dump file : Location has a geocode attached
#to it sometimes which could be used to identify the exact location in words rather than the 
#latitudes and longitudes. Working on that now
header = ['Photo URL','created_time','Location','Like Count','hashtags','caption']
insta_write.writerow(header)
#set the latitude and longitude to encompass New York City
lt,lon = 40.69, -73.94
#I will be sharing my client ID and secret. But you can get your own by applying for a new 
#application
api = InstagramAPI(client_id='1979574ea044469b8de19ca2004024b7', client_secret='da15b429178046508a469abf148f415e')
count = 0
#store = []
#storing only unique posts, which are identified by their ID which we store in a dictionary
#There are no retweets in general for instagram posts so not caring to take only the last instance
#whatever that means for instagram
id_count = {}

while True:
	#Press 'ctrl + c' to stop the code from running. Otherwise it continuously keeps 
	#appending to the file.
	try:
		#api = InstagramAPI(client_id='1979574ea044469b8de19ca2004024b7', client_secret='da15b429178046508a469abf148f415e')
		#store.append([])
		#popular_media is another way to go about it but we need only posts from New York.
		popular_media = api.media_popular(count=2000)
		#This searches only posts from New York using the lat and lng of the post
		new_york = api.media_search(lat = lt, lng = lon)
		#tags = new_york.tag_search(count = 20)
		#print tags

		#iterating through the posts which are brought up
		for media in new_york:
			store = []
			#if post is unique, its id is added to the dictionary 'id_count''s keys
			if media.id not in id_count:
				count += 1
				#printing the count to keep track of the number of posts appended to the file
				print count
				id_count[media.id] = 1
				store.append(media.images['standard_resolution'].url)
				store.append(media.created_time)
				store.append(media.location)
				store.append(media.like_count)

				#store[len(store)-1].append(media.id)
				#store[len(store)-1].append(media.Media)
				token = str(media.caption)
				token = token.split(' ')
				hashtag = []
				#collecting all the hashtags separately
				for i in token:
					if i:
						if i[0] == '#':
							hashtag.append(i)
						elif i[0] == '"' and i[1] == '#':
							hashtag.append(i)
				store.append(hashtag)
				store.append(media.caption)
				#writing into the csv file at each step
				insta_write.writerow(store)
	except KeyboardInterrupt: #Keyboard interrupt
		print 'interrupted'
		break
print id_count
keys = id_count.keys()
print keys.sort()
f.close()

	#time.sleep(30)
#for media in popular_media:
#    print media.images['standard_resolution'].url
