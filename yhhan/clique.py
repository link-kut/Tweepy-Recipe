# http://networkx.github.io/documentation/latest/reference/generated/networkx.algorithms.clique.find_cliques.html#networkx.algorithms.clique.find_cliques

import networkx as net
import networkx.algorithms as algo
import matplotlib.pyplot as plt

g=net.Graph()
g.add_edges_from([(1,2), (1,3), (1,4), (2,3), (3,4), (4,5), (4,6), (5,6), (5,7), (5,8), (6,7), (6,8), (7,8), (7,9)])

h_list = list(algo.find_cliques(g))
h = net.subgraph(g, h_list[0])
net.draw(h)
plt.show()
