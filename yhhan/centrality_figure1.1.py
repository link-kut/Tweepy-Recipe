import networkx as net
import matplotlib.pyplot as plt
import operator
from math import sqrt
import networkx.linalg as la

def sort_map(map):
  sortedList = map.items()
	sortedList.sort(key=operator.itemgetter(1), reverse=True)
	return sortedList
	
def eigenvector_centrality(G, max_iter = 100, tol = 1.0e-6, nstart = None):
	if type(G) == net.MultiGraph or type(G) == net.MultiDiGraph:
		raise Exception("eigenvector_centrality() not defined for multigraphs.")
	if len(G)==0:
		raise net.NetworkXException("eigenvector_centrality(): empty graph.")
	if nstart is None:
		# choose starting vector with entries of 1/len(G) 
		x=dict([(n,1.0/len(G)) for n in G])
	else:
		x=nstart

	nnodes=G.number_of_nodes()
	
	# normalize starting vector
	s=1.0/sum(x.values())
	for k in x: 
		x[k]*=s

	# make up to max_iter iterations        
	for i in range(max_iter):
		xlast=x
		x=dict.fromkeys(xlast.keys(),0)
		# do the multiplication y=Ax
		for n in x:
			for nbr in G[n]:
				x[n]+=xlast[nbr]*G[n][nbr].get('weight',1)
		# normalize vector
		try:
			s=1.0/sqrt(sum(v**2 for v in x.values()))
		except ZeroDivisionError:
			s=1.0
		for n in x: 
			x[n]*=s
		# check convergence            
		err=sum([abs(x[n]-xlast[n]) for n in x])
		if err < nnodes*tol:
			return x
	raise net.NetworkXError("eigenvector_centrality(): power iteration failed to converge in %d iterations." % (i+1))

def eigenvector_centrality2(G, max_iter = 100, tol = 1.0e-6, nstart = None):
	if type(G) == net.MultiGraph or type(G) == net.MultiDiGraph:
		raise Exception("eigenvector_centrality() not defined for multigraphs.")
	if len(G)==0:
		raise net.NetworkXException("eigenvector_centrality(): empty graph.")
	if nstart is None:
		# choose starting vector with entries of 1/len(G) 
		x=dict([(n,1.0/len(G)) for n in G])
	else:
		x=nstart

	nnodes=G.number_of_nodes()
		
	aj_matrix = la.adjacency_matrix(g)
	
	# normalize column vector
	for j in range(0, nnodes):
		column_sum = 0
		for i in range(0, nnodes):
			column_sum += aj_matrix[i,j]
		for i in range(0, nnodes):
			aj_matrix[i,j] = aj_matrix[i,j]/column_sum

	# make up to max_iter iterations        
	for i in range(max_iter):
		xlast=x
		x=dict.fromkeys(xlast.keys(),0)
		# do the multiplication y=Ax
		for n in x:
			for nbr in G[n]:
				x[n]+=xlast[nbr]*aj_matrix[n-1,nbr-1]
		# normalize vector
		try:
			s=1.0/sqrt(sum(v**2 for v in x.values()))
		except ZeroDivisionError:
			s=1.0
		for n in x: 
			x[n]*=s
		# check convergence            
		err=sum([abs(x[n]-xlast[n]) for n in x])
		if err < nnodes*tol:
			return x
	raise net.NetworkXError("eigenvector_centrality(): power iteration failed to converge in %d iterations." % (i+1))
	   
g=net.Graph()
g.add_edges_from([(1,2), (1,3), (1,4), (2,3), (3,4), (4,5), (4,6), (5,6), (5,7), (5,8), (6,7), (6,8), (7,8), (7,9)])

degree_centrality = net.degree_centrality(g)
sorted_degree_centrality = sort_map(degree_centrality)

closeness_centrality = net.closeness_centrality(g)
sorted_closeness_centrality = sort_map(closeness_centrality)

bet_centrality = net.betweenness_centrality(g)
sorted_bet_centrality = sort_map(bet_centrality)

init = {1:1.0, 2:1.0, 3:1.0, 4:1.0, 5:1.0, 6:1.0, 7:1.0, 8:1.0, 9:1.0}
#eigenvector_centrality = net.eigenvector_centrality(g, nstart=init)
eigenvector_centrality = eigenvector_centrality2(g, nstart=init)
sorted_eigenvector_centrality = sort_map(eigenvector_centrality)

rounded_degree_centrality = {k: round(v, 3) for k, v in degree_centrality.items()}
rounded_closeness_centrality = {k: round(v, 3) for k, v in closeness_centrality.items()}
rounded_bet_centrality = {k: round(v, 3) for k, v in bet_centrality.items()}
rounded_eigenvector_centrality = {k: round(v, 3) for k, v in eigenvector_centrality.items()}

table = [[node, rounded_degree_centrality[node], rounded_closeness_centrality[node], rounded_bet_centrality[node], rounded_eigenvector_centrality[node]] for node in g.nodes()]

table
