# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 18:07:30 2016
@author: megan squire

This is a little program I wrote with my students to attempt to colorize edges according to weight.

This particular incarnation of the program will show the 2-radius ego graph for user 'batsman' within
the edgelist24.csv file.

The entire thing is a bit of a riff off of the networkx tutorial, found here:
https://networkx.github.io/documentation/networkx-1.10/examples/drawing/weighted_graph.html
"""
import networkx as nx

g = nx.read_weighted_edgelist('edgelist24.csv')

graphs = list(nx.connected_component_subgraphs(g))
graphsSorted = sorted(graphs, key=len, reverse=True)
cc = graphsSorted[0]


ego = nx.Graph(nx.ego_graph(cc, 'batsman', radius=2))
d = nx.degree(ego)

elarge = [(u, v) for (u, v, d) in ego.edges(data=True) if d['weight'] > 1]
esmall = [(u, v) for (u, v, d) in ego.edges(data=True) if d['weight'] <= 1]

pos = nx.spring_layout(ego)

nx.draw(ego,
        pos,
        node_size=[v * 10 for v in d.values()],
        with_labels=True,
        font_size=8)

nx.draw_networkx_nodes(ego,
                       pos,
                       nodelist=['batsman'],
                       node_size=300,
                       node_color='g')

nx.draw_networkx_edges(ego, pos, edgelist=elarge, width=3)
nx.draw_networkx_edges(ego, pos, edgelist=esmall, width=1,
                       alpha=0.5, style='dashed', edge_color='g')
