# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 10:16:23 2016

@author: megan squire
"""
import networkx as nx
import matplotlib.pyplot as plt

g = nx.read_weighted_edgelist('data/edgelist24.csv')
degree = nx.degree(g)
 
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
i = 0;
for graph in graphsSorted[0:5]:
    i += 1
    print("num nodes in graph",i,":",nx.number_of_nodes(graph))
    graphDegree = nx.degree(graph)
    
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