# -*- coding: utf-8 -*-

import sys
import json
import tweepy
import pprint


Q = ' '.join(sys.argv[1:])

MAX_PAGES = 2
RESULTS_PER_PAGE = 2

tweepy_search = tweepy.API(parser=tweepy.parsers.JSONParser())

search_results = []
for page in range(1, MAX_PAGES+1):
    search_results += \
        tweepy_search.search(q=Q, rpp=RESULTS_PER_PAGE, page=page)['results']


print json.dumps(search_results, indent=1)

