# Single tweet URL format:
# https://twitter.com/girls_day_minah/status/318253307497955328

import os
import sys
import json
import tweepy
import networkx as nx
import re
import matplotlib.pyplot as plt

def get_rt_origins(tweet):
	rt_patterns = re.compile(r"(RT|via)((?:\b\W*@\w+)+)", re.IGNORECASE)
	rt_origins = []

	try: 
		rt_origins += [ mention.strip() for mention in rt_patterns.findall(tweet.text)[0][1].split()]
	except IndexError, e:
		pass

	'''		
	if tweet.has_key('retweet_count'):
		if tweet['retweet_count'] > 0:
			rt_origins += [ tweet['user']['name'].lower() ]
	try:
		rt_origins += [ mention.strip() for mention in rt_patterns.findall(tweet['text'])[0][1].split()]
	except IndexError, e:
		pass
	'''	

	return list(set([rto.strip("@").lower() for rto in rt_origins]))
	
def create_rt_graph(tweets):
	g = nx.DiGraph()
	
	for tweet in tweets:
		rt_origins = get_rt_origins(tweet)
		if not rt_origins:
			continue		
		for rt_origin in rt_origins:
			g.add_edge(rt_origin, tweet.from_user, {'tweet_id': tweet.id})		
	return g

if __name__ == '__main__':
	Q = ' '.join(sys.argv[1])
	MAX_PAGES = 2
	RESULTS_PER_PAGE = 2
	
	auth = tweepy.OAuthHandler(consumer_key='u6PzLjPnLzSEmYMJzYjFw', consumer_secret='qROGgsYiOmXwBbZUAfxV0Wx13SuD0ro4LyvPOXVL12E') 
	auth.set_access_token(key='60838213-Rd9hm2lwlTfy60f661z46mPCI17AROCaTF6Rox255', secret='t19PCabTmNO4DGBoT3WTJ2UASSO2AO9bBAkrorVK8')

	api = tweepy.API(auth)
	WORLD_WOE_ID = 1132599  #http://woeid.rosselliot.co.nz/lookup
	tren = api.trends_place(WORLD_WOE_ID)
	trends = [ trend['name'] for trend in tren[0]['trends'] ]
	
	search_results = []
	for trend in trends:
		for page in range(1, MAX_PAGES+1):
			search_results += api.search(q=trend, rpp=RESULTS_PER_PAGE, page=page)

	all_tweets = [tweet for tweet in search_results]
	g = create_rt_graph(all_tweets)
	print >> sys.stderr, "Number nodes:", g.number_of_nodes()
	print >> sys.stderr, "Num edges:", g.number_of_edges()
	print >> sys.stderr, "Num connected components:", len(nx.connected_components(g.to_undirected()))
	print >> sys.stderr, "Node degrees:", sorted(nx.degree(g))
	
	nx.draw(g)
	plt.show()
