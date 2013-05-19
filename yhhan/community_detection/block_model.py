import networkx as net
import networkx.algorithms as algo
import matplotlib.pyplot as plt
import numpy as np
import numpy.linalg as la
import Pycluster

g=net.Graph()
g.add_edges_from([(1,2), (1,3), (1,4), (2,3), (3,4), (4,5), (4,6), (5,6), (5,7), (5,8), (6,7), (6,8), (7,8), (7,9)])
adj_m = net.adjacency_matrix(g)

w, v = la.eig(adj_m)

S = [[0.0 for i in range(1,3)] for k in range(1,10)]
S = np.mat(S)
S[:,0] += v[:,0]
S[:,1] += v[:,1]
B = np.diag((w[0], w[1])) # diagonal matrix built with the top 2 eigenvalues of adj_m

labels = Pycluster.kcluster(S, 2)
