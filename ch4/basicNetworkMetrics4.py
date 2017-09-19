# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 10:53:27 2016
Updated on Tues Sep 19 15:51:00 2017

@author: megan squire
"""

import networkx as nx
import operator

g = nx.read_weighted_edgelist('data/edgelist24.csv')
graphs = list(nx.connected_component_subgraphs(g))
graphsSorted = sorted(graphs, key=len, reverse=True)
i = 0
for graph in graphsSorted[0:5]:
    i += 1
    print('Number of nodes in graph', i, ':', nx.number_of_nodes(graph))
    graphDegree = nx.degree(graph)
    
    cliques = list(nx.find_cliques(graph))
    print('Cliques for graph ', i)
    print(cliques) 

    ev = nx.eigenvector_centrality_numpy(graph) 
    evSorted = sorted(ev.items(), key=operator.itemgetter(1), reverse=True)
    for key,val in evSorted:
        print(key,str(round(val,2)))
    print("===")
    
