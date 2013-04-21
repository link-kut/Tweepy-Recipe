# -*- coding: utf-8 -*-
import sys
import twitter
from recipe__make_tweepy_request import make_tweepy_request
from oauth_login import oauth_login
import functools

SCREEN_NAME = sys.argv[2]
MAX_IDS = int(sys.argv[3])
TYPE  = sys.argv[4]	
if __name__ == '__main__':
	# Not authenticating lowers your rate limit to 150 requests per hr.
	# Authenticate to get 350 requests per hour.
	oauthID = sys.argv[1]	
	t = oauth_login(oauthID)
	#twitter.Twitter(domain='api.twitter.com', api_version='1')
	# You could call make_twitter_request(t, t.friends.ids, *args, **kw) or
	# use functools to "partially bind" a new callable with these parameters
	if(TYPE == str(0)):	#Friends ids	
		get_friends_ids = functools.partial(make_tweepy_request, t, t.friends_ids)
	elif(TYPE == str(1)):	#Followers ids
		get_followers_ids = functools.partial(make_tweepy_request, t, t.followers_ids)	
	# Ditto if you want to do the same thing to get followers...
	# getFollowerIds = functools.partial(make_twitter_request, t, t.followers.ids)
	cursor = -1
	ids = []
	i = 1	
	while cursor != 0:
		# Use make_twitter_request via the partially bound callable...
		if(MAX_IDS > 5000): 
			count = 5000
		if(TYPE == str(0)):
			response = get_friends_ids(screen_name=SCREEN_NAME, cursor=cursor,count= MAX_IDS)
		elif(TYPE == str(1)):
			response = get_followers_ids(screen_name=SCREEN_NAME, cursor=cursor,count= MAX_IDS)			
		#ids		
		ids += response[0]
		
		#next cursor	
		cursor = response[1][1]
		# Consider storing the ids to disk during each iteration to provide an
		# an additional layer of protection from exceptional circumstances.
		if len(ids) >= MAX_IDS:
			break

	# Do something useful with the ids like store them to disk...
	print ids
	print >> sys.stderr, 'Fetched %i total ids for %s' % (len(ids), SCREEN_NAME)

