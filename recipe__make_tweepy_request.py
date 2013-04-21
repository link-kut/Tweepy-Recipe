import sys
import time
from urllib2 import URLError
import tweepy
import functools
import tweepy.error
import json

def make_tweepy_request(t, tweepyFunction, max_errors=3, *args, **kwArgs):
  def handle_http_error(e, t, wait_period=2):
		#de =  json.loads()
		if wait_period > 3600: # Seconds
			print >> sys.stderr, "Too many retries. Quitting."
			raise e
		if e.args == 401:
			print >> sys.stderr, 'Encountered 401 Error (Not Authorized)'
			return None
		elif e.args in (502, 503):
			print >> sys.stderr, 'Encountered %i Error. Will retry in %i seconds' % \
			(e.e.code, wait_period)
			time.sleep(wait_period)
			wait_period *= 1.5
			return wait_period
		elif  t.rate_limit_status()['resources']['friends']['/friends/ids']['remaining']== 0:	#friends/ids
			status = t.rate_limit_status()
			now = time.time() # UTC
			when_rate_limit_resets = status['resources']['friends']['/friends/ids']['reset'] # UTC
			sleep_time = when_rate_limit_resets - now
			print >> sys.stderr, 'Rate limit reached: sleeping for %i secs' % \
			(sleep_time, )
			time.sleep(sleep_time)
			return 2	
		elif  t.rate_limit_status()['resources']['followers']['/followers/ids']['remaining']== 0:	#followers/ids
			status = t.rate_limit_status()
			now = time.time() # UTC
			when_rate_limit_resets = status['resources']['followers']['/followers/ids']['reset'] # UTC
			sleep_time = when_rate_limit_resets - now
			print >> sys.stderr, 'Rate limit reached: sleeping for %i secs' % \
			(sleep_time, )
			time.sleep(sleep_time)
			return 2
		else:
			raise e

	wait_period = 2
	error_count = 0
	while True:
		try:
			return tweepyFunction(*args, **kwArgs)
		except tweepy.error.TweepError as e:
			error_count = 0
			wait_period = handle_http_error(e, t, wait_period)
			if wait_period is None:
				return
		except URLError, e:
			error_count += 1
			print >> sys.stderr, "URLError encountered. Continuing."
			if error_count > max_errors:
				print >> sys.stderr, "Too many consecutive errors...bailing out."
				raise
