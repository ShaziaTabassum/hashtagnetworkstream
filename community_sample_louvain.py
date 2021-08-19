import networkx as nx
import community as community_louvain
import matplotlib.pyplot as plt
import matplotlib.cm as cm

# define the graph
# edge = [(1,2),(1,3),(1,4),(1,5),(1,6),(2,7),(2,8),(2,9)]
# G = nx.Graph()
# G.add_edges_from(edge)
# return partition as a dict


G = nx.karate_club_graph()
partition = community_louvain.best_partition(G, resolution=100)

for key in partition.keys():
    print(key, partition[key])

# visualization
pos = nx.spring_layout(G)
# color the nodes according to their partition
cmap = cm.get_cmap('viridis', max(partition.values()) + 1)
nx.draw_networkx_nodes(G, pos, partition.keys(), node_size=40,
                       cmap=cmap, node_color=list(partition.values()))
nx.draw_networkx_edges(G, pos, alpha=0.5)
plt.show()
"""
pos = nx.spring_layout(G)
cmap = cm.get_cmap('viridis', max(partition.values()) + 1)
nx.draw_networkx_nodes(G, pos, partition.keys(), node_size=100,cmap=cmap, node_color=list(partition.values()))
nx.draw_networkx_edges(G, pos, alpha=0.5)
plt.show()"""
