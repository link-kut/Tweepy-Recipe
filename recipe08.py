# -*- coding: utf-8 -*-

import sys
import tweepy
import webbrowser
import ssl

if __name__ == '__main__':

# Query terms
  Q = sys.argv[1:] 

#Consumer, Token setting
	CONSUMER_KEY = '3CGRcxEN4f5tsvGvmgDEew'
	CONSUMER_SECRET = 'AVzDXHbrB7EMk0jZ9wJYmCKTlOWxcn0p7R62UywUr4'
	
	ACCESS_TOKEN = '127006727-37wj9ltrasr9hmdBDZKRL8f04mbYOZ2gEFj6tw8h'
	ACCESS_TOKEN_SECRET = 'ZMdQnpShmKzd1TEeCvEXpw1xmCp4O2fHC1fJPzQ0jY'

#Auth
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Note: Had you wanted to perform the full OAuth dance instead of using
# an access key and access secret, you could have uses the following 
# four lines of code instead of the previous line that manually set the
# access token via auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
# 
# auth_url = auth.get_authorization_url(signin_with_twitter=True)
# webbrowser.open(auth_url)
# verifier = raw_input('PIN: ').strip()
# auth.get_access_token(verifier)
	
	class CustomStreamListener(tweepy.StreamListener):
	
		def on_status(self, status):
		
		# We'll simply print some values in a tab-delimited format
		# suitable for capturing to a flat file but you could opt 
		# store them elsewhere, retweet select statuses, etc.
			print "start try"
			
			try:
			    print "%s\t%s\t%s\t%s" % (status.text, 
			                              status.author.screen_name, 
			                              status.created_at, 
			                              status.source, 
 			                              )
			except Exception, e:
			    print >> sys.stderr, 'Encountered Exception:', e
			    pass
		
		def on_error(self, status_code):
#			print >> sys.stderr, 'Encountered error with status code:', status_code
			return True # Don't kill the stream
		
		def on_timeout(self):
			print >> sys.stderr, 'Timeout...'
			return True # Don't kill the stream
# Create a streaming API and set a timeout value of 60 seconds
#	streaming_api = tweepy.streaming.Stream(auth, CustomStreamListener(), timeout=1)
	streaming_api = tweepy.streaming.Stream(auth, CustomStreamListener())

# Optionally filter the statuses you want to track by providing a list
# of users to "follow"

	print >> sys.stderr, 'Filtering the public timeline for "%s"' % (' '.join(sys.argv[1:]),)
# print >> sys.stderr, '"%s"' % Q
	
	streaming_api.filter(follow=None, track=Q)
# streaming_api.filter(track=Q, async=True)
