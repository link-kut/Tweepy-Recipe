import networkx as net
import matplotlib.pyplot as plt

g = net.erdos_renyi_graph(10, 0.1, directed=True)
g.edges()
net.draw(g)
plt.show()

wcc = net.connected_components(g.to_undirected())
print wcc
wcc_g = net.connected_component_subgraphs(g.to_undirected())[0]

scc = net.strongly_connected_components(g)
print scc
scc_g = net.strongly_connected_component_subgraphs(g)[0]
