# -*- coding: utf-8 -*-
import sys
import tweepy
import json
import time
from urllib2 import URLError
import functools
import tweepy.error


def oauth_login(
consumer_key='QNkh1PTs2REwpNXPt2osDw',
consumer_secret='quiVAvMGRv7CJgkPiojgJwhf28wvWPVXk3QSEYcXM',
key='45127896-oujh240kkQ02yxSs0JUsKpL5nQ3JbLwi3EJsL1UPn', 
secret='9gUYI4aw18EuHDggjvEn2nUiC4K5NAU4cLemNyxbjkY'):    
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(key, secret)
	return tweepy.API(auth) 
	
		
def get_info_by_screen_name(api, screen_names):
    sn_to_info = {}
    for screen_name in screen_names:
        user = api.get_user(screen_name)
        sn_to_info.update({user.id:user})
    return sn_to_info

def analyze_users_in_search_results(t, q, max_pages=1, results_per_page=10):
    tweepy_search = tweepy.API(parser=tweepy.parsers.JSONParser())

    search_results = []
    for page in range(1, max_pages+1):
        search_results += \
            tweepy_search.search(q=q, rpp=results_per_page, page=page)['results']

    screen_name_to_tweet_ids = {}
    for result in search_results:

        screen_name = result['from_user']

        if not screen_name_to_tweet_ids.has_key(screen_name):
            screen_name_to_tweet_ids[screen_name] = []

        screen_name_to_tweet_ids[screen_name] += [ result['id'] ]

    screen_name_to_info = get_info_by_screen_name(t, screen_name_to_tweet_ids.keys())
    screen_name_to_location = dict([(sn, info.location) for sn, info in screen_name_to_info.items()])

    return screen_name_to_info, screen_name_to_location, screen_name_to_tweet_ids

if __name__ == '__main__':

    Q = ' '.join(sys.argv[1:])
    t = oauth_login()
    sn2info, sn2location, sn2tweet_ids = analyze_users_in_search_results(t, Q)
