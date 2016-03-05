# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 14:22:51 2016

@author: megan squire
"""
import networkx as nx

g = nx.read_weighted_edgelist('data/edgelist12987.csv')

graphs = list(nx.connected_component_subgraphs(g))
for graph in graphs:
    if graph.has_node('tirsen'):
        graphDegree = nx.degree(graph)

        pos=nx.spring_layout(graph)

        nx.draw(graph,
            pos,
            node_size=[v * 10 for v in graphDegree.values()],
            with_labels=False,
            font_size=8)
        
        nx.draw_networkx_nodes(graph, 
                               pos, 
                               nodelist=['tirsen'],
                               node_size=300, 
                               node_color='g')