import networkx as net
import networkx.algorithms as algo
import matplotlib.pyplot as plt
import numpy as np
import numpy.linalg as la
import Pycluster

g=net.Graph()
g.add_edges_from([(1,2), (1,3), (1,4), (2,3), (3,4), (4,5), (4,6), (5,6), (5,7), (5,8), (6,7), (6,8), (7,8), (7,9)])
proximity_matrix = algo.all_pairs_shortest_path_length(g)
p = [[proximity_matrix[i][j] for i in range(1,10)] for j in range(1,10)]
p = np.mat(p)

one = [1 for i in range(1,10)]
one = np.mat(one).T

identity = np.identity(9)

sub1 = np.subtract(identity, (1.0 / 9.0) * one * one.T)  # np.subtract - element-wise matrix subtract
sub2 = np.multiply(p, p) # np.multiply - element-wise matrix multiplication
p2 = -1 * (1.0 / 2.0) * sub1 * sub2 * sub1

w, v = la.eig(p2)
A = [[0.0 for i in range(1,3)] for k in range(1,10)]
A = np.mat(A)
A[:,0] += v[:,0]
A[:,1] += v[:,1]
B = np.diag((w[0], w[1])) # diagonal matrix built with the top 2 eigenvalues of p2

S = A * np.sqrt(B)

labels = Pycluster.kcluster(S, 2)

labels
