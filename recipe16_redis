# -*- coding: utf-8 -*-

import time
import tweepy
import redis
import return_api
from recipe__setwise_operations import get_redis_id


#get friends nodes
def get_friends(api, iden):
	cursor = tweepy.Cursor(api.friends_ids, id = iden).iterator
	friends = []

	user_info = api.get_user(iden)
	if (user_info.friends_count != 0):
		while cursor.next_cursor != 0:
			try:
				print 'calling next page of {}'.format(iden)
				c_friends = cursor.next()
				friends += c_friends
			except tweepy.error.TweepError as e:
				print e
				time.sleep(60)
		
	return friends


#visitor
def get_information(api, ids):
	#someting needs are here to return
	user = api.get_user(ids)
	return user.screen_name
	

if __name__ == '__main__':
	api = return_api.oauth_login()
	queue = {} #traversing target list
	informations = {} #collected information
	edges = []

	r = redis.Redis()

	#initialize queue
	queue = {'1417479073': False} #bangdduck's id

	limit_level = 2;
	current_level = 1; 

	while current_level <= limit_level:
		current_targets = [];
		for key, value in queue.iteritems():
			if (value == False):
				current_targets.append(key)

		#start traverse
		for target_ids in current_targets:
			friends = get_friends(api, target_ids)
			#database works
			rid = get_redis_id('friends_ids', user_id = str(target_ids))
			print target_ids
			[ r.sadd(rid, _id) for _id in friends]
					
			#for each user		
			for iden in friends:
				edges.append([iden, target_ids])
				if not queue.has_key(iden):
					queue.update({iden: False})
					print 'saving {} on queue'.format(iden)
					#works.. for a user
					#now we just save screen_name in memory
					#info = get_information(api, iden)
					#informations.update({iden: info})

			queue.update({target_ids: True})

		print 'current queue .. {}'.format(len(queue))
		time.sleep(3)
		current_level += 1		
