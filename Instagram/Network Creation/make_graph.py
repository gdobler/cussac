import networkx as nx
import csv
import matplotlib.pyplot as plt
f = open("edgelist.csv")
edges = []
z = 0
reader = csv.reader(f)
G = nx.Graph()
for i in reader:
	#if len(i)==2:
	#edges.append((int(i[0]),int(i[1])))
	G.add_edge(int(i[0]),int(i[1]))
	z+=1
#print edges
nx.draw(G)
#G.add_edges_from(edges)
#G=nx.random_geometric_graph(200,0.125)
#print G.
#pos = nx.get_node_attributes(G,'pos')
#nx.draw_networkx_edges(G,pos)
#nx.draw_networkx_nodes(G,pos)
#nx.draw(G)
plt.show()