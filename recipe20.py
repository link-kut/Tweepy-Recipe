# -*- coding: utf-8 -*-
import os
import re
import shutil
import webbrowser
import sys
import tweepy
import json
import time
from urllib2 import URLError
import functools
import tweepy.error

def getAuthenticatedAPI(oauthId):
  api = None
	if (oauthId == str(1)):
		#Young-Jun Jung - thekey16
		auth = tweepy.OAuthHandler(consumer_key='WzM7Vji6g7ppvsKhoLj90Q', consumer_secret='YbqAJmmJtzR1uUyQERbhNTlq641DapEDpvuu84B5Co')
		auth.set_access_token(key='225378669-k5IChjgAasI5X8yFDTDIhTFgInLLUzMLFtzelt4D', secret='1SqCwJpFyy710iG7aCJt411LEKSUAttudvKwRv5mcQ')
		api = tweepy.API(auth)
	if (oauthId == str(2)):
		#link.kut - moonriver365, GH_PARK
		auth = tweepy.OAuthHandler(consumer_key='DkbCOmT0lbAOI88K5ag', consumer_secret='BD2X0xw9jm6iFGZv4WXXLvwCycQuPM4VWTocTNkrM')
		auth.set_access_token(key='955340989-b5j9sIX5iuTSpLouTOGjESycoz787KZoq8loOWIr', secret='NbLxUUVYyvSPUVwRa4eJWJs1UWGiu3VMjvG5Lwakpw')
		api = tweepy.API(auth)
	if (oauthId == str(3)):
		#yh21.han - oisoo, BoA
		auth = tweepy.OAuthHandler(consumer_key='u6PzLjPnLzSEmYMJzYjFw', consumer_secret='qROGgsYiOmXwBbZUAfxV0Wx13SuD0ro4LyvPOXVL12E')
		auth.set_access_token(key='60838213-Rd9hm2lwlTfy60f661z46mPCI17AROCaTF6Rox255', secret='t19PCabTmNO4DGBoT3WTJ2UASSO2AO9bBAkrorVK8')
		api = tweepy.API(auth)
	if (oauthId == str(4)):
		#cmdr - kwang82
		auth = tweepy.OAuthHandler(consumer_key='QNkh1PTs2REwpNXPt2osDw', consumer_secret='quiVAvMGRv7CJgkPiojgJwhf28wvWPVXk3QSEYcXM')
		auth.set_access_token(key='45127896-oujh240kkQ02yxSs0JUsKpL5nQ3JbLwi3EJsL1UPn', secret='9gUYI4aw18EuHDggjvEn2nUiC4K5NAU4cLemNyxbjkY')
		api = tweepy.API(auth)
	if (oauthId == str(5)):
		#sujin
		auth = tweepy.OAuthHandler(consumer_key='xP7VXTgTpdchvWchMUH5Pg', consumer_secret='NumKXQQUBrwhzS25gdpLe2KsGoiEFRzlqAFg8elvYE')
		auth.set_access_token(key='396293322-0uPKFk2X54Gd2nDNQ9h1RtLmAgNx5LnB5ZDokj2h', secret='3WPhYkRSaLMwAWg0jgPWEgWBUSxijKaEMKnysFOWDqg')
		api = tweepy.API(auth)
	return api

def get_info_by_screen_name(api, screen_names):
    sn_to_info = {}
    for screen_name in screen_names:
        user = api.get_user(screen_name)
        sn_to_info.update({user.id:user})
    return sn_to_info
	
def analyze_users_in_search_results(t, q, max_pages=10, results_per_page=20):

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

	
def get_state_frequencies(locations):
    
    state_names_to_abbrevs = \
        dict([
            ('ALABAMA', 'AL'),
            ('ALASKA', 'AK'),
            ('ARIZONA', 'AZ'),
            ('ARKANSAS', 'AR'),
            ('CALIFORNIA', 'CA'),
            ('COLORADO', 'CO'),
            ('CONNECTICUT', 'CT'),
            ('DELAWARE', 'DE'),
            ('FLORIDA', 'FL'),
            ('GEORGIA', 'GA'),
            ('HAWAII', 'HI'),
            ('IDAHO', 'ID'),
            ('ILLINOIS', 'IL'),
            ('INDIANA', 'IN'),
            ('IOWA', 'IA'),
            ('KANSAS', 'KS'),
            ('KENTUCKY', 'KY'),
            ('LOUISIANA', 'LA'),
            ('MAINE', 'ME'),
            ('MARYLAND', 'MD'),
            ('MASSACHUSETTS', 'MA'),
            ('MICHIGAN', 'MI'),
            ('MINNESOTA', 'MN'),
            ('MISSISSIPPI', 'MS'),
            ('MISSOURI', 'MO'),
            ('MONTANA', 'MT'),
            ('NEBRASKA', 'NE'),
            ('NEVADA', 'NV'),
            ('NEW HAMPSHIRE', 'NH'),
            ('NEW JERSEY', 'NJ'),
            ('NEW MEXICO', 'NM'),
            ('NEW YORK', 'NY'),
            ('NORTH CAROLINA', 'NC'),
            ('NORTH DAKOTA', 'ND'),
            ('OHIO', 'OH'),
            ('OKLAHOMA', 'OK'),
            ('OREGON', 'OR'),
            ('PENNSYLVANIA', 'PA'),
            ('RHODE ISLAND', 'RI'),
            ('SOUTH CAROLINA', 'SC'),
            ('SOUTH DAKOTA', 'SD'),
            ('TENNESSEE', 'TN'),
            ('TEXAS', 'TX'),
            ('UTAH', 'UT'),
            ('VERMONT', 'VT'),
            ('VIRGINIA', 'VA'),
            ('WASHINGTON', 'WA'),
            ('WEST VIRGINIA', 'WV'),
            ('WISCONSIN', 'WI'),
            ('WYOMING', 'WY')
        ])

    state_abbrevs = state_names_to_abbrevs.values()

    states_freqs = dict([(abbrev, 0) for abbrev in state_abbrevs])

    for location in locations:
        if location is None:
            continue

        for name, abbrev in state_names_to_abbrevs.items():
            if location.upper().find(name) > -1:
                states_freqs[abbrev] += 1
                break

            if re.findall(r'\b(' + abbrev + r')\b', location, re.IGNORECASE):
                states_freqs[abbrev] += 1
                break

    return states_freqs


if __name__ == '__main__':

    Q = ' '.join(sys.argv[1:])
    t = getAuthenticatedAPI("4")

    sn2info, sn2location, sn2tweet_ids = analyze_users_in_search_results(t, Q)
    locations = sn2location.values()
    print locations

    states_freqs = get_state_frequencies(locations)

    json_data = {}
    for state, freq in states_freqs.items():
        json_data[state] = {'value': freq}

    if not os.path.isdir('out'):
        os.mkdir('out')

    shutil.rmtree('out/dorling_cartogram', ignore_errors=True)
    shutil.rmtree('out/protovis-3.2', ignore_errors=True)

    shutil.copytree('etc/protovis/dorling_cartogram','out/dorling_cartogram')

    shutil.copytree('etc/protovis/protovis-3.2','out/protovis-3.2')

    html = open('etc/protovis/dorling_cartogram/dorling_cartogram.html').read() % \
        (json.dumps(json_data),)

    f = open(os.path.join(os.getcwd(), 'out', 'dorling_cartogram', 
                      'dorling_cartogram.html'), 'w')
    f.write(html)
    f.close()

    print >> sys.stderr, 'Data file written to: %s' % f.name
    webbrowser.open('file://' + f.name)
