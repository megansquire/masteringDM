# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 10:01:20 2016

@author: megan
"""
import networkx as nx

g = nx.read_weighted_edgelist('data/edgelist24.csv')
degree = nx.degree(g)

# try to make the graph more understandable
# (1) remove nodes that only have one connection, to shrink size of drawing
g2 = g.copy()
d2 = nx.degree(g2)
for n in g2.nodes():
    if d2[n] <= 1: 
        g2.remove_node(n)

# print out the smaller size (it's about half as big now in terms of nodes)
g2numNodes = nx.number_of_nodes(g2)
g2numEdges = nx.number_of_edges(g2)
print('g2numNodes:', g2numNodes)
print('g2numEdges:', g2numEdges)

# (2) add some parameters to the draw() function
# --scale the size of the node to its degree (high-degree nodes will be bigger)
nx.draw(g2, node_size=[v * 10 for v in d2.values()])