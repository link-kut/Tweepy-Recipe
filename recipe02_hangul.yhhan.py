# -*- coding: utf-8 -*-

import os
import sys
import datetime
import time
import tweepy
import json
import urllib2

auth = tweepy.OAuthHandler(consumer_key='u6PzLjPnLzSEmYMJzYjFw', consumer_secret='qROGgsYiOmXwBbZUAfxV0Wx13SuD0ro4LyvPOXVL12E') 
auth.set_access_token(key='60838213-Rd9hm2lwlTfy60f661z46mPCI17AROCaTF6Rox255', secret='t19PCabTmNO4DGBoT3WTJ2UASSO2AO9bBAkrorVK8')

api = tweepy.API(auth)
WORLD_WOE_ID = 1132599 # woeid = 1132599 --> Seoul

trends_location = api.trends_place(WORLD_WOE_ID)

for trend in trends_location[0]['trends']:
  print urllib2.unquote(trend['query'].encode('utf-8')).decode('utf-8')

print
	
for trend in trends_location[0]['trends']:
	print trend['name']  
