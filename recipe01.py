# appName = soojin3013
# consumer_key='xP7VXTgTpdchvWchMUH5Pg'

import tweepy
import webbrowser

auth = tweepy.OAuthHandler(consumer_key='xxx', consumer_secret='xxx') 
auth_url = auth.get_authorization_url()
print('Please authorze: ' + auth_url)
webbrowser.open(auth_url)

verifier = input("PIN: ")
auth.get_access_token(verifier)

print("ACCESS_KEY = '%s'" % auth.access_token.key)
print("ACCESS_SECRET = '%s'" % auth.access_token.secret)

 
