# -*- coding: utf-8 -*-
# tweepy search - http://stackoverflow.com/questions/3256981/tweepy-api-how-to-get-a-users-id-from-a-status-searchresult-object

import sys
import tweepy

MAX_PAGES = 10
RESULTS_PER_PAGE = 2

auth = tweepy.OAuthHandler(consumer_key='u6PzLjPnLzSEmYMJzYjFw', consumer_secret='qROGgsYiOmXwBbZUAfxV0Wx13SuD0ro4LyvPOXVL12E') 
auth.set_access_token(key='60838213-Rd9hm2lwlTfy60f661z46mPCI17AROCaTF6Rox255', secret='t19PCabTmNO4DGBoT3WTJ2UASSO2AO9bBAkrorVK8')

api = tweepy.API(auth)

WORLD_WOE_ID = 1132599  #http://woeid.rosselliot.co.nz/lookup

tren = api.trends_location(WORLD_WOE_ID)
	
trends = [ trend['name'] for trend in tren[0]['trends'] ]

idx = 0
for trend in trends:
	print "[%i] %s" % (idx, trend)
	idx += 1

trend_idx = int(raw_input('\nPick a trend: '))

q = trends[trend_idx]

print >> sys.stderr, 'Fetching tweets for %s...' % (q, )

search_results = []
for page in range(1, MAX_PAGES+1):
	search_results += api.search(q=q, rpp=RESULTS_PER_PAGE, page=page)

for tweet in search_results:
	print tweet
	print "User '%s(%s)' uploads the tweet:\n%s \n" % (tweet.from_user, tweet.from_user_id, tweet.text)
