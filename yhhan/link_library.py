# -*- coding: utf-8 -*-
import networkx as net
import matplotlib.pyplot as plt
import math

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
		
def my_jaccard(self, node1, node2):
        """jaccard similarity

        Parameters
        ----------
        node1
        node2

        Examples
        --------
        >>> G=nx.Graph()   # or DiGraph, MultiGraph, MultiDiGraph, etc
        >>> G.my_jaccard(3, 4)

        """
        list1 = self.neighbors(node1)
        list2 = self.neighbors(node2)
        n = len(set(list1).intersection(set(list2)))
        return n / float(len(list1) + len(list2) - n )
                    
def my_jaccard_modify(self, node1, node2):
        """jaccard modify similarity

        Parameters
        ----------
        node1
        node2

        Examples
        --------
        >>> G=nx.Graph()   # or DiGraph, MultiGraph, MultiDiGraph, etc
        >>> G.my_jaccard_modify(7, 9)

        """
        list1 = self.neighbors(node1)
        list2 = self.neighbors(node2)
        
        list1.append(node1)
        list2.append(node2)
        
        n = len(set(list1).intersection(set(list2)))
        return n / float(len(list1) + len(list2) - n )
        
def my_cosine(self, node1, node2):
        """cosine similarity

        Parameters
        ----------
        node1
        node2

        Examples
        --------
        >>> G=nx.Graph()   # or DiGraph, MultiGraph, MultiDiGraph, etc
        >>> G.my_cosine(3, 4)

        """
        list1 = self.neighbors(node1)
        list2 = self.neighbors(node2)
        n = len(set(list1).intersection(set(list2)))
        
        return n / (math.sqrt( len(list1) * len(list2) ) )
        
def my_cosine_modify(self, node1, node2):
	"""cosine modify similarity

        Parameters
        ----------
        node1
        node2

        Examples
        --------
        >>> G=nx.Graph()   # or DiGraph, MultiGraph, MultiDiGraph, etc
        >>> G.my_cosine_modify(7, 9)
        """
	list1 = self.neighbors(node1)
	list2 = self.neighbors(node2)
	list1.append(node1)
	list2.append(node2)
	n = len(set(list1).intersection(set(list2)))
        
        return n / (math.sqrt( len(list1) * len(list2) ) )
	
def my_modularity(self, *attr):
	"""modularity

        Parameters
        ----------
        list
        list ...

        Examples
        --------
        >>> G=nx.Graph()   # or DiGraph, MultiGraph, MultiDiGraph, etc
        >>> G.my_modularity(list)
        >>> G.my_modularity(list1, list2)
        >>> G.my_modularity(list1, list2, list3, ...)
        >>> G.my_modularity([1,2,3], [7,9], ...)
        """
	m = self.number_of_edges()
	sum = 0
	for x in attr:
		print x
		for i in range(0, len(x)):
			for j in range(i+1, len(x)):
				sum += float((self.has_edge(x[i], x[j]))) - (float(self.degree(x[i]))*float(self.degree(x[j]))) / float((2*m))
	result = float(sum) / float( (2*m) )
	return result
