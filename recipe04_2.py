# -*- coding: utf-8 -*-

import os
import sys
import json
import tweepy
#from recipe__extract_tweet_entities import get_entities
from recipe03_twitter import get_entities

MAX_PAGES = 2
RESULTS_PER_PAGE = 2

# Get the trending topics

auth = tweepy.OAuthHandler(consumer_key='xxx', consumer_secret='xxx')
auth.set_access_token(key='xxx', secret='xxx')

api = tweepy.API(auth)

WORLD_WOE_ID = 1  #http://woeid.rosselliot.co.nz/lookup

tren = api.trends_place(WORLD_WOE_ID)


trends = [ trend['name'] for trend in tren[0]['trends'] ]

idx = 0
for trend in trends:
    print '[%i] %s' % (idx, trend,)
    idx += 1

# Prompt the user

trend_idx = int(raw_input('\nPick a trend: '))

q = trends[trend_idx]

print >> sys.stderr, 'Fetching tweets for %s...' % (q, )

tweepy_search = tweepy.API(parser=tweepy.parsers.JSONParser())

search_results = []
for page in range(1, MAX_PAGES+1):
    search_results += \
        tweepy_search.search(q=q, rpp=RESULTS_PER_PAGE, page=page)['results']
        
for result in search_results:
        result['entities'] = get_entities(result)

if not os.path.isdir('out'):
        os.mkdir('out')

f = open(os.path.join(os.getcwd(), 'out', 'search_results.json'), 'w')
f.write(json.dumps(search_results, indent=1))
f.close()

print >> sys.stderr, "Entities for tweets about trend '%s' saved to %s" % (q, f.name,)
