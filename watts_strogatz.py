import networkx as net
import matplotlib.pyplot as plt
import networkx.algorithms as algo
import pylab as pl

#g = net.watts_strogatz_graph(20, 4, 0.0)
#net.draw(g)
#plt.show()

def clustering_coefficiency_from_graph(p):
	g = net.watts_strogatz_graph(300, 4, p)
	c_list = algo.clustering(g).values()
	return (sum(c_list) / len(c_list), net.diameter(g))

p_list = pl.frange(0, 1, 0.1)

print "watts_strogatz_graph(300, 4, p)"

c_list = []
d_list = []

for p in p_list:
	pair = clustering_coefficiency_from_graph(p)
	c_list.append(pair[0])
	d_list.append(pair[1])
	print pair

plt.figure(1)
plt.subplot(2,1,1)	
plt.plot(p_list, c_list, '-o')
plt.axis([0, 1, min(c_list), max(c_list)])

plt.subplot(2,1,2)
plt.plot(p_list, d_list, '-o')
plt.axis([0, 1, min(d_list), max(d_list)])	

'''
g = net.erdos_renyi_graph(200, 0.5)
plt.hist(g.degree().values(), 10)

g = net.watts_strogatz_graph(300, 4, 0.2)
plt.hist(g.degree().values(), 10)

g = net.barabasi_albert_graph(300, 1)
plt.hist(g.degree().values(), 10)
'''
