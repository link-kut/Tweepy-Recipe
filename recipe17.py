import os
import sys
import redis
import tweepy
import time
import return_api
import networkx as net
import matplotlib.pyplot as plt
from recipe__setwise_operations import get_redis_id


SCREEN_NAME = sys.argv[1]

api = return_api.oauth_login()

user = api.get_user(screen_name = SCREEN_NAME)


_id = user.id_str;


g = net.DiGraph()
r = redis.Redis()

ids = [_id] + list(r.smembers(get_redis_id('friends_ids', user_id=_id)))


[g.add_edge(api.get_user(_id).screen_name, api.get_user(friend).screen_name) for friend in ids]

for current_id in ids:
  print >> sys.stderr, 'Processing user with id', current_id
	friend_ids = list(r.smembers(get_redis_id('friends_ids', user_id = current_id)))
	print 'before : ' + str(len(friend_ids))
	
	try:
		friend_ids = [fid for fid in friend_ids if fid in ids]
	except Exception, e:
		print >> sys.stderr, 'Processing user with id', current_id

	print 'after : ' + str(len(friend_ids))
	for friend_id in friend_ids :
		print >> sys.stderr, 'Adding edge %s => %s' % (current_id, friend_id)
		current_name = api.get_user(current_id).screen_name
		friend_name = api.get_user(friend_id).screen_name
		g.add_edge(current_name, friend_name)
		
if not os.path.isdir('out'):
	os.mkdir('out')

f = os.path.join('out', SCREEN_NAME + '-friendships.gpickle')
net.write_gpickle(g, f)
net.draw(g)
plt.show()

print >> sys.stderr, 'Pickle file stored in', f	
