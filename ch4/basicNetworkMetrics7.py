# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 14:22:51 2016

@author: megan squire
"""

import networkx as nx

g = nx.read_weighted_edgelist('data/edgelist12987.csv')


cc =nx.node_connected_component(g, 'tirsen')
G = nx.Graph()
G.add_nodes_from(cc)

degree = nx.degree(G)

# calculate some basic stuff about the nodes & degrees
numNodes = nx.number_of_nodes(G)
numEdges = nx.number_of_edges(G)
minDegree = min(degree.values())
maxDegree = max(degree.values())

print('numNodes:', numNodes)
print('numEdges:', numEdges)
print('minDegree:', minDegree)
print('maxDegree:', maxDegree)

graphDegree = nx.degree(G)

pos=nx.spring_layout(G)

nx.draw(G,
        pos,
        node_size=[v * 100 for v in graphDegree.values()],
        with_labels=False,
        font_size=8)
      
nx.draw_networkx_nodes(G,
                       pos,
                       nodelist=['tirsen'],
                       node_size=300,
                       node_color='g')
