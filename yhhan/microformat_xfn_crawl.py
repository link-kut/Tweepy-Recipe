# -*- coding: utf-8 -*-

import sys
import os
import urllib2
from BeautifulSoup import BeautifulSoup
import HTMLParser
import networkx as net
import matplotlib.pyplot as plt

ROOT_URL = sys.argv[1]

if len(sys.argv) > 2:
    MAX_DEPTH = int(sys.argv[2])
else:
    MAX_DEPTH = 1

XFN_TAGS = set([
    'colleague',
    'sweetheart',
    'parent',
    'co-resident',
    'co-worker',
    'muse',
    'neighbor',
    'sibling',
    'kin',
    'child',
    'date',
    'spouse',
    'me',
    'acquaintance',
    'met',
    'crush',
    'contact',
    'friend',
    ])

depth = 0

g = net.DiGraph()

next_queue = [ROOT_URL]

while depth < MAX_DEPTH:
  depth += 1
	(queue, next_queue) = (next_queue, [])

	for item in queue:
		if not g.has_node(item):
			g.add_node(item)

		try:
			page = urllib2.urlopen(item)
		except urllib2.URLError:
			print 'Failed to fetch ' + item
			continue
			
		try:
			soup = BeautifulSoup(page)
		except HTMLParser.HTMLParseError:
			print 'Failed to parse ' + item
			continue

		anchorTags = soup.findAll('a')

		for a in anchorTags:
			if a.has_key('rel'):
				if len(set(a['rel'].split()) & XFN_TAGS) > 0:
					friend_url = a['href']
					g.add_edge(item, friend_url)
					g[item][friend_url]['label'] = a['rel'].encode('utf-8')
					g.node[friend_url]['label'] = a.contents[0].encode('utf-8')
					print a.contents[0], a['href'], a['rel']
					next_queue.append(friend_url)

net.draw(g)     
plt.show()
