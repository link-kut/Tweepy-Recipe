# -*- coding: utf-8 -*-
import tweepy
import networkx as net
import matplotlib.pyplot as plt
import sys

def getFollowers(g, api, user_id):
	for page in tweepy.Cursor(api.followers_ids, id=user_id).pages():
		for followerId in page:
			g.add_edge(followerId, user_id)
	print "End of followers sampling for %s\n" % (user_id)

def snowball_sampling(g, api, center_id, max_depth=1, current_depth=0, center_list=[]):
	if current_depth==max_depth:
		return
	if center_id in center_list:
		return
	else:
		print "Start to sample the followers for %s" % (center_id)
		center_list.append(center_id)
		followerIDs = getFollowers(g, api, center_id)
		for follower_id in g.predecessors(center_id):
			snowball_sampling(g, api, follower_id, max_depth=max_depth, current_depth = current_depth + 1, center_list=center_list)

if __name__ == '__main__':
	userScreenName = sys.argv[1]

	g = net.DiGraph()

	auth = tweepy.OAuthHandler(consumer_key='u6PzLjPnLzSEmYMJzYjFw', consumer_secret='qROGgsYiOmXwBbZUAfxV0Wx13SuD0ro4LyvPOXVL12E')
	auth.set_access_token(key='60838213-Rd9hm2lwlTfy60f661z46mPCI17AROCaTF6Rox255', secret='t19PCabTmNO4DGBoT3WTJ2UASSO2AO9bBAkrorVK8')
	api = tweepy.API(auth)

	user_id = api.get_user(userScreenName).id
	snowball_sampling(g, api, user_id, max_depth=1)
	print "Complete to create %s's snowball network...\n" % userScreenName
	net.draw(g)
	plt.show()
