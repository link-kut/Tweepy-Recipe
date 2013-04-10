# -*- coding: utf-8 -*-
import networkx as net
import matplotlib.pyplot as plt

def overlap(H, edge):
  node_i = edge[0]
	node_j = edge[1]
	degree_i = H.degree(node_i)
	degree_j = H.degree(node_j)
	if degree_i > 1 or degree_j > 1:
		neigh_i = set(H.neighbors(node_i))
		neigh_j = set(H.neighbors(node_j))
		neigh_ij = neigh_i.intersection(neigh_j)
		num_cn = len(neigh_ij)
		return float(num_cn) / (degree_i + degree_j - num_cn - 2)
	else:
		return 0
		
