import time
import tweepy

#get child nodes
def get_ids(api, iden):
	cursor = tweepy.Cursor(api.followers_ids, id = iden).iterator
	followers = []

	while cursor.next_cursor != 0:
		try:
			print 'calling next page of {}'.format(iden)
			c_followers = cursor.next()
			followers += c_followers
		except tweepy.error.TweepError as e:
			print e
			time.sleep(60)
		
	return followers

#visitor
def get_information(api, ids):
	#someting needs are here to return
	user = api.get_user(ids)
	return user.screen_name
	

if __name__ == '__main__':
	import myauth
	api = myauth.get_api()
	queue = {} #traversing target list
	informations = {} #collected information
	edges = []

	#initialize queue
	queue = {215661128: False} #ladofa9's id

	while len(queue) < 1000000:
		current_targets = [];
		for key, value in queue.iteritems():
			if (value == False):
				current_targets.append(key)

		#start traverse
		for target_ids in current_targets:
			followers = get_ids(api, target_ids)
			queue.update({key: True})

			#for each user		
			for iden in followers:
				edges.append([iden, target_ids])
				if not queue.has_key(iden):
					queue.update({iden: False})
					print 'saving {} on queue'.format(iden)
					#works.. for a user
					#now we just save screen_name in memory
					#info = get_information(api, iden)
					#informations.update({iden: info})
		print 'current queue .. {}'.format(len(queue))
		time.sleep(3)
		queue
