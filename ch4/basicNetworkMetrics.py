# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 09:36:47 2016

@author: megan squire
"""

import networkx as nx
import operator

# create a graph, filling it with one of the edgelists
g = nx.read_weighted_edgelist('data/edgelist24.csv')

# analyze the basic graph
# make a Python dictionary full of each node and their degrees
degree = nx.degree(g)

# calculate some basic stuff about the nodes & degrees
numNodes = nx.number_of_nodes(g)
numEdges = nx.number_of_edges(g)
minDegree = min(degree.values())
maxDegree = max(degree.values())

print('numNodes:', numNodes)
print('numEdges:', numEdges)
print('minDegree:', minDegree)
print('maxDegree:', maxDegree)


# sort the dictionary by highest degrees
degreeSorted = sorted(degree.items(), key=operator.itemgetter(1), reverse=True)
# print out the top ten nodes with the highest degrees
print(degreeSorted[0:9])

# draw the graph - you will see that it is very crowded, 
# but some structure is apparent
nx.draw(g)