# -*- coding: utf-8 -*-

import sys
import tweepy
import json
import time
from urllib2 import URLError
from urllib2 import HTTPError
import functools
import tweepy.error
import os
import geopy
import webbrowser



def oauth_login(
consumer_key='WzM7Vji6g7ppvsKhoLj90Q',
consumer_secret='YbqAJmmJtzR1uUyQERbhNTlq641DapEDpvuu84B5Co',
key='225378669-k5IChjgAasI5X8yFDTDIhTFgInLLUzMLFtzelt4D', 
secret='1SqCwJpFyy710iG7aCJt411LEKSUAttudvKwRv5mcQ'):    
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






def geocode_locations(geocoder, locations):

    # Some basic replacement transforms may be necessary for geocoding services to 
    # function properly. You may probably need to add your own as you encounter rough
    # edges in the data or with the geocoding service you settle on. For example, ...

    replacement_transforms = [('sseoul', 'seoul')]

    location_to_coords = {}
    location_to_description = {}

    for location in locations:

        if location is None:
            continue
        
        print "location value : " + location

        # Avoid unnecessary I/O with a simple cache

        if location_to_coords.has_key(location):
            continue

        xformed_location = location
		
        for transform in replacement_transforms:

            xformed_location = xformed_location.replace(*transform)
            while True:

                num_errors = 0
                results = []

                try:
                    # This call returns a generator
                    temp = geocoder.geocode(xformed_location, exactly_one=False, region='ko')
                    #results = geocoder.geocode(xformed_location, exactly_one=False, region='ko')
                    if not temp is None:
                    	results = temp
                    break
                except HTTPError, e:
                    num_errors += 1
                    if num_errors >= MAX_HTTP_ERRORS:
                        sys.exit()
                    print >> sys.stderr, e.message
                    print >> sys.stderr, 'A urllib2 error. Retrying...'
                except UnicodeEncodeError, e:
                    print >> sys.stderr, e
                    print >> sys.stderr, 'A UnicodeEncodeError...', e.message
                    break
                except geopy.geocoders.google.GQueryError, e:
                    print >> sys.stderr, e
                    print >> sys.stderr, 'A GQueryError', e.message
                    break
                  
        for result in results:

            # Each result is of the form ("Description", (X,Y))
            # Unless you have a some special logic for picking the best of many 
            # possible results, choose the first one returned in results and move 
            # along
            location_to_coords[location] = result[1]
            location_to_description[location] = result[0]
            break

    # Use location_to_coords and other information of interest to populate a 
    # visualization. Depending on your particular needs, it is highly likely that 
    # you'll want to further post process the geocoded locations to filter out 
    # location such as "U.S.A." which will plot a placemarker in the geographic 
    # center of the United States yet make the visualization look skewed in favor
    # of places like Oklahoma, for example.

    return location_to_coords, location_to_description


def build_kml(title, location2coords):

    # There are certainly more robust ways to build XML, ut the following approach
    # does the job

    # Substitute a title and list of placemarks into the main KML template

    kml_template = """<?xml version="1.0" encoding="UTF-8"?>
    <kml xmlns="http://earth.google.com/kml/2.0">
      <Folder>
        <name>%s</name>
        %s
      </Folder>
    </kml>"""

    # Substitute (name, lon, lat) tuples into placemark templates

    placemark_template = """<Placemark>
      <Style>
        <LineStyle>
          <color>cc0000ff</color>
          <width>5.0</width>
        </LineStyle>
      </Style>
      <name>%s</name>
      <Point>
        <coordinates>%s,%s,0</coordinates>
      </Point>
    </Placemark>"""


    placemarks = []
    for name, [lat, lon] in location2coords.items():
        placemarks += [placemark_template % (name, lon, lat,)]

    return kml_template % (title, '\n'.join(placemarks),)




if __name__ == '__main__':
	
        
    Q = ' '.join(sys.argv[1:])
    MAX_HTTP_ERRORS = 100
    g = geopy.geocoders.GoogleV3()
        
    print Q
    # Don't forget to pass in keyword parameters if you don't have 
    # a token file stored to disk
    
    t = oauth_login()
    
    # This function returns a few useful maps. Let's use the
    # screen_name => location map and geocode the locations
    
    _, screen_name_to_location, _ = analyze_users_in_search_results(t, Q, max_pages=3)
    locations = screen_name_to_location.values()
    for loca in locations:
    	print loca
    
    location2coords, location2description = geocode_locations(g, locations)
    
    ll = location2coords.values()
    
    # Doing something interesting like building up some KML to visualize in Google Earth/Maps 
    # just involves some simple string munging...
    
    kml = build_kml("Geocoded user profiles for Twitter search results for " + Q, location2coords)
    
    if not os.path.isdir('out'):
    	os.mkdir('out')
    
    f = open(os.path.join(os.getcwd(), 'out', Q + ".kml"), 'w')
    f.write(kml)
    f.close()
    
    htmlString = '''
	<!DOCTYPE html>
	<html>
  	<head>
   	 <meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
   	 	<style type="text/css">
     		html { height: 100% }
      		body { height: 100%; margin: 0; padding: 0 }
      		#map_canvas { height: 100% }
    	</style>
    	<script type="text/javascript" src="http://maps.googleapis.com/maps/api/js?key=AIzaSyD_IYZeYa4KTljAcvohR4F-19saWZTfAZA&sensor=false">
    	</script>
    	<script type="text/javascript">
      		function initialize() {
        		var mapOptions = {
          		center: new google.maps.LatLng(36.764742,127.297726),
          		zoom: 8,
          		mapTypeId: google.maps.MapTypeId.ROADMAP
        		};
        	var map = new google.maps.Map(document.getElementById("map_canvas"), mapOptions);
       	'''
    for i in ll:
		htmlString += '''
			var marker = new google.maps.Marker({
			position: new google.maps.LatLng(%f, %f),
			title: "marker test"
			});
			marker.setMap(map);
        	''' % (i[0], i[1])
    htmlString += '''
    }
    </script>
    </head>
    <body onload="initialize()">
    <div id="map_canvas" style="width:100%; height:100%"></div>
    </body>
    </html>
    '''
       
    f = open('googleMapTest.html', 'w')
    f.write(htmlString)
    f.close()
    
    url = "file:/Users/yongjinjung/PythonFolder/googleMapTest.html"
    webbrowser.open(url)
