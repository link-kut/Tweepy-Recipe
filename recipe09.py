import sys
import time
from urllib2 import URLError
import twitter
import functools

SCREEN_NAME = sys.argv[1]
MAX_IDS = int(sys.argv[2])

def make_twitter_request(t, twitterFunction, max_errors=3, *args, **kwArgs):
  def handle_http_error(e, t, wait_period=2):
		if wait_period > 3600: # Seconds
			print >> sys.stderr, "Too many retries. Quitting."
			raise e
		if e.e.code == 401:
			print >> sys.stderr, 'Encountered 401 Error (Not Authorized)'
			return None
		elif e.e.code in (502, 503):
			print >> sys.stderr, 'Encountered %i Error. Will retry in %i seconds' % \
			(e.e.code, wait_period)
			time.sleep(wait_period)
			wait_period *= 1.5
			return wait_period
		elif t.account.rate_limit_status()['remaining_hits'] == 0:
			status = t.account.rate_limit_status()
			now = time.time() # UTC
			when_rate_limit_resets = status['reset_time_in_seconds'] # UTC
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
			return twitterFunction(*args, **kwArgs)
		except twitter.api.TwitterHTTPError, e:
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

if __name__ == '__main__':

    # Not authenticating lowers your rate limit to 150 requests per hr.
    # Authenticate to get 350 requests per hour.

	t = twitter.Twitter(domain='api.twitter.com', api_version='1')

    # You could call make_twitter_request(t, t.friends.ids, *args, **kw) or
    # use functools to "partially bind" a new callable with these parameters
	i = 0
	while i < 1:
		get_friends_ids = functools.partial(make_twitter_request, t, t.friends.ids)
		i = i + 1

		# Ditto if you want to do the same thing to get followers...

		# getFollowerIds = functools.partial(make_twitter_request, t, t.followers.ids)

		cursor = -1
		ids = []
		while cursor != 0:

			# Use make_twitter_request via the partially bound callable...

			response = get_friends_ids(screen_name=SCREEN_NAME, cursor=cursor)
			ids += response['ids']
			cursor = response['next_cursor']
			print >> sys.stderr, 'Fetched %i total ids for %s' % (len(ids), SCREEN_NAME)

			# Consider storing the ids to disk during each iteration to provide an
			# an additional layer of protection from exceptional circumstances

			if len(ids) >= MAX_IDS:
				break

		# Do something useful with the ids like store them to disk...

	print ids 
