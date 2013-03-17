# -*- coding: utf-8 -*-

import json
import twitter_text

def get_entities(tweet):
  
	extractor = twitter_text.Extractor(tweet['text'])
	entities = {} 
	entities['user_mentions_indices'] = []
	for um in extractor.extract_mentioned_screen_names_with_indices():
		entities['user_mentions_indices'].append(um)

	entities['hashtags_indices'] = []
	for hts in extractor.extract_hashtags_with_indices():
		entities['hashtags_indices'].append(hts)

	entities['urls_indices'] = []
	for url in extractor.extract_urls_with_indices():
		entities['urls_indices'].append(url)
		
#	entities['user_name']  = []
#	for un in extractor.extract_mentioned_screen_names():
#		entities['user_name'].append(un)
	
#	entities['hashtag'] = []
#	for ht in extractor.extract_hashtags():
#		entities['hashtag'].append(ht)
	
#	entities['url']  = []
#	for ur in extractor.extract_urls():
#		entities['url'].append(ur)	
		
	return entities
	
if __name__ == '__main__':

	tweets = \
		[
			{
			 'text' : 'Get @SocialWebMining example code at http://bit.ly/biais2 #wOOt'
			},
			{
			 'text' : 'Test text @Takeardor http://tst.py/link #Temp #test'
			}
		]
		
	for tweet in tweets:
		tweet['entities'] = get_entities(tweet)
	
	print json.dumps(tweets, indent=1)

			
