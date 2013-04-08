# -*- coding: utf-8 -*-
import tweepy
import networkx as net
import matplotlib.pyplot as plt
import sys

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
	oauthId = sys.argv[2]

	g = net.DiGraph()

	api = getAuthenticatedAPI(oauthId)
	user_id = api.get_user(userScreenName).id
	snowball_sampling(g, api, user_id, max_depth=1)
	print "Complete to create %s's snowball network...\n" % userScreenName
	net.draw(g)
	plt.show()
