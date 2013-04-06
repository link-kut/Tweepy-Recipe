import tweepy
import json

def oauth_login(
consumer_key='d2WpB4mVOUMsGCiPHl6XCA',
consumer_secret='7asl1MSrbhV87aHPKgtgNsyNy998V21FYEefQfBKcI',
key='1020202573-qifvNnyIyrUMjUVq0dSoS0QBqRhfp7YNvKAPd94', 
secret='m9dlE7aujarOLwAcnXn0zPXGooi4eeQH0MpsD9QGWk'):  	
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(key, secret)
	return tweepy.API(auth) 
