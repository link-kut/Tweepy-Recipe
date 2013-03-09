# appName = soojin3013
# consumer_key='xP7VXTgTpdchvWchMUH5Pg'

import tweepy
import json
    
auth = tweepy.OAuthHandler(consumer_key='xP7VXTgTpdchvWchMUH5Pg', consumer_secret='NumKXQQUBrwhzS25gdpLe2KsGoiEFRzlqAFg8elvYE') 
auth.set_access_token(key='396293322-0uPKFk2X54Gd2nDNQ9h1RtLmAgNx5LnB5ZDokj2h', secret='3WPhYkRSaLMwAWg0jgPWEgWBUSxijKaEMKnysFOWDqg')

api = tweepy.API(auth)

WORLD_WOE_ID = 1 # The Yahoo! Where On Earth ID for the entire world
tren = api.trends_location(WORLD_WOE_ID)


print json.dumps([trend for trend in tren[0]['trends']], indent=1)

