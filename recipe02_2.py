# appName = soojin3013
# consumer_key='xP7VXTgTpdchvWchMUH5Pg'

import os
import sys
import datetime
import time

import tweepy
import json

auth = tweepy.OAuthHandler(consumer_key='xP7VXTgTpdchvWchMUH5Pg', consumer_secret='NumKXQQUBrwhzS25gdpLe2KsGoiEFRzlqAFg8elvYE') 
auth.set_access_token(key='396293322-0uPKFk2X54Gd2nDNQ9h1RtLmAgNx5LnB5ZDokj2h', secret='3WPhYkRSaLMwAWg0jgPWEgWBUSxijKaEMKnysFOWDqg')

api = tweepy.API(auth)
WORLD_WOE_ID = 1 

tren = api.trends_location(WORLD_WOE_ID)


if not os.path.isdir('test/trends_data'):
        os.makedirs('test/trends_data')

while True:

    now = str(datetime.datetime.now())

    trends = json.dumps([trend for trend in tren[0]['trends']], indent=1)

    f = open(os.path.join(os.getcwd(), 'test', 'trends_data', now), 'w')
    f.write(trends)
    f.close()

    print >> sys.stderr, "Wrote data file", f.name
    print >> sys.stderr, "Zzz..."

    time.sleep(60) # 60 seconds
