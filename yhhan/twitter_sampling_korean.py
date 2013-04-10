# -*- coding: utf-8 -*-
import MySQLdb as mdb
import tweepy
import networkx as net
import matplotlib.pyplot as plt
import time
import sys
import json

connection = mdb.connect(host="127.0.0.1", port=3306, user="root", passwd="0113", db="twitter_user")
connection.query("set character_set_connection=utf8;")
connection.query("set character_set_server=utf8;")
connection.query("set character_set_client=utf8;")
connection.query("set character_set_results=utf8;")
connection.query("set character_set_database=utf8;")

def isHangul(s):
  for c in unicode(s):
		if u'\uac00' <= c <= u'\ud7a3':
			return True
	return False
		
def isKoreanUser(user):	
	isHangulName = isHangul(user.name)
	isKoreanLang = ('ko' == user.lang)
	isTimeZoneKorea = ('Seoul' == user.time_zone)
	isKoreaLocation = ('seoul' in user.location or 'Korea' in user.location or 'korea' in user.location or 'KOREA' in user.location or 'KOR' in user.location or 'Seoul' in user.location or 'Deajeon' in user.location or 'pusan' in user.location)
	if (isHangulName or isKoreanLang or isKoreaLocation or isTimeZoneKorea):
		return True
	else:
		return False

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

def rateLimitCheckSleep(api, apiName):
	try:
		remaining = 1000
		rate_limit_info = api.rate_limit_status()
		remaining = rate_limit_info['resources']['application']['/application/rate_limit_status']['remaining']
		if remaining <= 16:
			print "Sleep by RateLimit - /application/rate_limit_status\n"
			time.sleep(900)
			rate_limit_info = api.rate_limit_status()
		remaining = 1000		
		if apiName == '/followers/ids':
			remaining = rate_limit_info['resources']['followers']['/followers/ids']['remaining']
			if remaining <= 1:
				while(True):
					print "Sleep by RateLimit - /followers/ids...\n"
					time.sleep(60)		
					rate_limit_info = api.rate_limit_status()
					remaining = rate_limit_info['resources']['followers']['/followers/ids']['remaining']
					if remaining > 1:	
						break
		if apiName == '/friends/ids':
			remaining = rate_limit_info['resources']['friends']['/friends/ids']['remaining']
			if remaining <= 1:
				while(True):
					print "Sleep by RateLimit - /friends/ids...\n"
					time.sleep(60)
					rate_limit_info = api.rate_limit_status()
					remaining = rate_limit_info['resources']['friends']['/friends/ids']['remaining']
					if remaining > 1:
						break
		if apiName == '/users/show/:id':
			remaining = rate_limit_info['resources']['users']['/users/show/:id']['remaining']
			if remaining <= 1:
				while(True):
					print "Sleep by RateLimit -	 /users/show/:id...\n"
					time.sleep(60)
					rate_limit_info = api.rate_limit_status()
					remaining = rate_limit_info['resources']['users']['/users/show/:id']['remaining']
					if remaining > 1:
						break	
	except tweepy.error.TweepError as msg:
		if msg.reason == "[{u'message': u'Rate limit exceeded', u'code': 88}]":
			print "[Exeption] Rate Limit Exceeded in rateLimitCheckSleep!"
			time.sleep(900)
			rateLimitCheckSleep(api, apiName)
		if msg.reason == "[{u'message': u'Over capacity', u'code': 130}]":
			print "[Exception] Over Capacity in getFollowers!"
			time.sleep(1)
			rateLimitCheckSleep(api, apiName)

def isUserExistInBothDB(userId):   
	try:
		global connection
		cur = connection.cursor()
		cur.execute("SELECT userId FROM userlist WHERE userId=%s", (userId))
		result1 = cur.fetchone()
		cur.execute("SELECT userId FROM nonkoreanuserlist WHERE userId=%s", (userId))
		result2 = cur.fetchone()
		if result1 == None and result2 == None:
			return False
		else:
			return True
	except connection.Error, e:
		connection.rollback()
		print "Error %d: %s" % (e.args[0], e.args[1])
		sys.exit(1)
	finally:
		cur.close()

def isUserExistInKoreanDB(userId):
	try:
		global connection
		cur = connection.cursor()
		cur.execute("SELECT userId FROM userlist WHERE userId=%s", (userId))
		result = cur.fetchone()
		if result == None:
			return False
		else:
			return True
	except connection.Error, e:
		connection.rollback()
		print "Error %d: %s" % (e.args[0], e.args[1])
		sys.exit(1)
	finally:
		cur.close()

def getFSamplingStatus(userId):
	try:
		global connection
		cur = connection.cursor()
		cur.execute("SELECT fSamplingStatus FROM userlist WHERE userId=%s", (userId))
		result = cur.fetchone()
		return result[0]
	except connection.Error, e:
		connection.rollback()
		print "Error %d: %s" % (e.args[0], e.args[1])
		sys.exit(1)
	finally:
		cur.close()
	
def isEdgeExistInDB(followerId, userId):
	try:
		global connection
		cur = connection.cursor()
		cur.execute("SELECT * FROM edgelist WHERE followerId=%s AND userId=%s", (followerId, userId))
		results = cur.fetchone()
		if results == None:
			return False
		else:
			return True
	except connection.Error, e:
		connection.rollback()
		print "Error %d: %s" % (e.args[0], e.args[1])
		sys.exit(1)
	finally:
		cur.close()

def insertKoreanUser(user):
	try:
		global connection
		cur = connection.cursor()

		userId = str(user.id).strip()
		name = "" if user.name == None else user.name.strip().encode('utf-8')
		screenName = "" if user.screen_name == None else json.dumps(user.screen_name.strip().encode('utf-8'))
		lang = "" if user.lang == None else json.dumps(user.lang.strip().encode('utf-8'))
		timeZone = "" if user.time_zone == None else json.dumps(user.time_zone.strip().encode('utf-8'))
		location = "" if user.location == None else json.dumps(user.location.strip().encode('utf-8'))

		cur.execute("INSERT INTO userlist(userId, name, screenName, lang, timeZone, location) VALUES (%s, %s, %s, %s, %s, %s)", [userId, name, screenName, lang, timeZone, location])

		print "Add a user %s(%s) to userlist table" % (userId, name)
		connection.commit()
	except connection.Error, e:
		connection.rollback()
		print "Error %d: %s" % (e.args[0], e.args[1])
		sys.exit(1)
	finally:
		cur.close()

def insertNonKoreanUser(user, friendId):
	try:
		global connection
		cur = connection.cursor()

		userId = str(user.id).strip()
		friendId = str(friendId).strip()
		name = "" if user.name == None else user.name.strip().encode('utf-8')
		screenName = "" if user.screen_name == None else json.dumps(user.screen_name.strip().encode('utf-8'))
		lang = "" if user.lang == None else json.dumps(user.lang.strip().encode('utf-8'))
		timeZone = "" if user.time_zone == None else json.dumps(user.time_zone.strip().encode('utf-8'))
		location = "" if user.location == None else json.dumps(user.location.strip().encode('utf-8'))
		
		cur.execute("INSERT INTO nonkoreanuserlist(userId, friendId, name, screenName, lang, timeZone, location) VALUES (%s, %s, %s, %s, %s, %s, %s)", [userId, friendId, name, screenName, lang, timeZone, location])

		print "Add a non-korean user %s(%s) to userlist table\n" % (userId, name)
		connection.commit()
	except connection.Error, e:
		connection.rollback()
		print "Error %d: %s" % (e.args[0], e.args[1])
		sys.exit(1)
	finally:
		cur.close()

def insertEdge(followerId, userId):
	try:
		global connection
		cur = connection.cursor()		
		cur.execute("INSERT INTO edgelist(followerId, userId) VALUES (%s, %s)", (followerId, userId))
		connection.commit()
	except connection.Error, e:
		connection.rollback()
		print "DB-Error %d: %s" % (e.args[0], e.args[1])
		sys.exit(1)
	finally:
		cur.close()

def updateSamplingStatus(userId, status):
	try:
		global connection
		cur = connection.cursor()
		cur.execute("UPDATE	userlist SET fSamplingStatus=%s WHERE userId=%s", (status, userId))
		connection.commit()
	except connection.Error, e:
		connection.rollback()
		print "DB-Error %d: %s" % (e.args[0], e.args[1])
		sys.exit(1)
	finally:
		cur.close()
    	
def getFollowers(api, user):
	followerIDs = []
	try:
		rateLimitCheckSleep(api, '/followers/ids')	
		for page in tweepy.Cursor(api.followers_ids, id=user.id).pages():
			for followerId in page:
				fuser = api.get_user(followerId)

				if not(isUserExistInBothDB(followerId)):  
					if isKoreanUser(fuser):
						insertKoreanUser(fuser)
						if not(isEdgeExistInDB(followerId, user.id)):
							insertEdge(followerId, user.id)
							followerIDs.append(followerId)
							print "Insert an edge [followerId: %d ==> %d(%s)]\n" % (followerId, user.id, user.screen_name)
						else:
							print "The edge [followerId: %d ==> %d(%s)] already exist.\n" % (followerId, user.id, user.screen_name)
					else:
						insertNonKoreanUser(fuser, user.id)
				elif isUserExistInKoreanDB(followerId):
					if not(isEdgeExistInDB(followerId, user.id)):
						print "The follower %d already exist in the korean db" % (followerId)
						insertEdge(followerId, user.id)
						followerIDs.append(followerId)
						print "Insert an edge [followerId: %d ==> %d(%s)]\n" % (followerId, user.id, user.screen_name)
				else:
					print "The follower %d already exist in the non-korean db\n" % (followerId)	
					 
		updateSamplingStatus(user.id, "Complete")	
		print "End of followers sampling for %d(%s)\n" % (user.id, user.screen_name)
		return followerIDs
	except tweepy.error.TweepError as msg:
		if msg.reason == "[{u'message': u'Rate limit exceeded', u'code': 88}]":
			print "[Exeption] Rate Limit Exceeded in getFollowers!"
			updateSamplingStatus(user.id, "Partial")
			print "(Prematurely) End of followers sampling for %d(%s)\n" % (user.id, user.screen_name)
			return followerIDs
		elif msg.reason == "[{u'message': u'Over capacity', u'code': 130}]":			
			print "[Exception] Over Capacity in getFollowers!"
			updateSamplingStatus(user.id, "Partial")
			print "(Prematurely) End of followers sampling for %d(%s)\n" % (user.id, user.screen_name)
			return followerIDs
		else:
			print msg.reason
			updateSamplingStatus(user.id, "Partial")
			print "(Prematurely) End of followers sampling for %d(%s)\n" % (user.id, user.screen_name)
			return followerIDs	
            
def snowball_sampling(api, node, max_depth=2, current_depth=0):
	if current_depth==max_depth:
		return
	else:
		rateLimitCheckSleep(api, '/users/show/:id')
		user = api.get_user(node)

		if not(isUserExistInBothDB(user.id)):  
			if isKoreanUser(user):
				insertKoreanUser(user)
			else:
				insertNonKoreanUser(user, 0)
				return
	
		print "Start to sample the followers for %d(%s)\n" % (user.id, user.screen_name)
		followerIDs = getFollowers(api, user)
		if (followerIDs == None):
			followerIDs = []

		for node in followerIDs:
			snowball_sampling(api, node, max_depth=max_depth, current_depth = current_depth + 1)
            
userScreenName = sys.argv[1]
oauthId = sys.argv[2]
	
api = getAuthenticatedAPI(oauthId)
	
snowball_sampling(api, userScreenName)
print "Complete to create %s's snowball network...\n" % userScreenName
