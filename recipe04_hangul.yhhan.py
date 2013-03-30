# -*- coding: utf-8 -*-

import os
import sys
import json
import tweepy
import twitter_text

def get_entities(tweet):                                                                                                                    
  extractor = twitter_text.Extractor(tweet['text'])                   
	entities = {}                                                       
	entities['user_mentions_indices'] = []                              
	for um in extractor.extract_mentioned_screen_names_with_indices():  
		entities['user_mentions_indices'].append(um)                      
                                                                      
	entities['hashtags_indices'] = []                                   
	for hts in extractor.extract_hashtags_with_indices():               
		entities['hashtags_indices'].append(hts)                          
                                                                      
	entities['urls_indices'] = []                                       
	for url in extractor.extract_urls_with_indices():                   
		entities['urls_indices'].append(url)                              

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
	print '[%i] %s' % (idx, trend,)
	idx += 1

trend_idx = int(raw_input('\nPick a trend: '))

q = trends[trend_idx]

print >> sys.stderr, 'Fetching tweets for %s...' % (q, )

tweepy_search = tweepy.API(parser=tweepy.parsers.JSONParser())

search_results = []
for page in range(1, MAX_PAGES+1):
	search_results += tweepy_search.search(q=q, rpp=RESULTS_PER_PAGE, page=page)['results']
        
for result in search_results:
	result['entities'] = get_entities(result)

if not os.path.isdir('out'):
	os.mkdir('out')

#data = json.dumps(search_results, indent=1)

print

for tweet in search_results:
	print tweet['text'], '\n'

'''
f = open(os.path.join(os.getcwd(), 'out', 'search_results.json'), 'w')
#f = codecs.open(os.path.join(os.getcwd(), 'out', 'search_results.json'), 'w', encoding='utf-8')
f.write(json.dumps(search_results, indent=1))
f.close()

print >> sys.stderr, "Entities for tweets about trend '%s' saved to %s" % (q, f.name,)
print
print >> sys.stderr, "Read the tweets about trend '%s' from %s" % (q, f.name,)

f = codecs.open(os.path.join(os.getcwd(), 'out', 'search_results.json'), "r", encoding='utf-8')
search_results2 = f.read()
f.close()

print search_results2.decode('string_escape')
'''
