# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 14:55:30 2016

@author: megan
"""

import networkx as nx
import operator
import matplotlib.pyplot as plt

# create a graph, filling it with one of the edgelists
g = nx.read_weighted_edgelist('data/edgelist24.csv')

# A: analyze the basic graph
# make a Python dictionary full of each node and their degrees
#degree = nx.degree(g)

# calculate some basic stuff about the nodes & degrees
#numNodes = nx.number_of_nodes(g)
#numEdges = nx.number_of_edges(g)
#minDegree = min(degree.values())
#maxDegree = max(degree.values())

#print('numNodes:', numNodes)
#print('numEdges:', numEdges)
#print('minDegree:', minDegree)
#print('maxDegree:', maxDegree)

# sort the dictionary by highest degrees
#degreeSorted = sorted(degree.items(), key=operator.itemgetter(1), reverse=True)
# print out the top ten nodes with the highest degrees
#print(degreeSorted[0:9])

# draw the graph - you will see that it is very crowded, 
# but some structure is apparent
# nx.draw(g)

# B: try to make the graph more understandable
# fix up the network drawing to be more informative:
# (1) remove nodes that only have one connection, 
# to shrink the size of the drawing
#g2 = g.copy()
#d2 = nx.degree(g2)
#for n in g2.nodes():
#    if d2[n] <= 1: 
#        g2.remove_node(n)

# print out the smaller size (it's about half as big now in terms of nodes)
#g2numNodes = nx.number_of_nodes(g2)
#g2numEdges = nx.number_of_edges(g2)
#print('g2numNodes:', g2numNodes)
#print('g2numEdges:', g2numEdges)

# (2) add some parameters to the draw() function
# --scale the size of the node to its degree (high-degree nodes will be bigger)
#nx.draw(g2, node_size=[v * 10 for v in d2.values()])

# C: this didn't really clean it up much - 
# what if we look for subgraphs instead
# first, make sure the graph isn't really 100% connected.
print(nx.is_connected(g))

# next, see how many pieces the graph is actually in
print(nx.number_connected_components(g))

# then, pull out each of these connected components
# and sort them by the number of nodes in them
graphs = list(nx.connected_component_subgraphs(g))
graphsSorted = sorted(graphs, key=len, reverse=True)
# for the top five largest graphs, print the number of nodes 
# and draw the graph in a file
i = 0
for graph in graphsSorted[0:5]:
    i += 1
    print(nx.number_of_nodes(graph))
    graphDegree = nx.degree(graph)
    '''
    # draw one set with name labels
    f1 = plt.figure()
    nx.draw(graph,
            node_size=[v * 10 for v in graphDegree.values()],
            with_labels=True,
            font_size=8)
    filename1 = 'graphLabels'+ str(i) + '.png'
    f1.savefig(filename1) 
    
    # draw one set without name labels
    f2 = plt.figure()
    nx.draw(graph,
            node_size=[v * 10 for v in graphDegree.values()])
    filename2 = 'graph'+ str(i) + '.png'
    f2.savefig(filename2)       
    '''
    cliques = list(nx.find_cliques(graph))
    print('cliques for graph' + str(i))
    print(cliques) 

    ev = nx.eigenvector_centrality_numpy(graph) 
    evSorted = sorted(ev.items(), key=operator.itemgetter(1), reverse=True)
    for key,val in evSorted:
        print(key,str(round(val,2)))
    print(['%s %0.2f'%(node,ev[node]) for node in ev])      
#density = nx.density(g)
#print('density:', density)