import sys
import functools
import tweepy
import locale
import redis
from recipe__make_tweepy_request import make_tweepy_request
from return_api import oauth_login

# A convenience function for consistently creating keys for a
# screen name, user id, or anything else you'd like

def get_redis_id(key_name, screen_name=None, user_id=None):
  if screen_name is not None:	
		return 'screen_name$' + screen_name + '$' + key_name
	elif user_id is not None:
		return 'user_id$' + user_id + '$' + key_name
	else:
		raise Exception("No screen_name or user_id provided to get_redis_id")
