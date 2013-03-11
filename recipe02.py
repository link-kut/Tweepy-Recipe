# appName = soojin3013
# consumer_key='xP7VXTgTpdchvWchMUH5Pg'

import tweepy
import json
    
auth = tweepy.OAuthHandler(consumer_key='xxxx', consumer_secret='xxxx') 
auth.set_access_token(key='xxxxx', secret='xxxx')

api = tweepy.API(auth)

WORLD_WOE_ID = 1 # The Yahoo! Where On Earth ID for the entire world
tren = api.trends_location(WORLD_WOE_ID)


print json.dumps([trend for trend in tren[0]['trends']], indent=1)

