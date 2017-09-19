# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 13:19:47 2016
Updated on Tue Sep 19 13:54:00 2017
@author: megan
"""

import networkx as nx

g = nx.read_weighted_edgelist('data/edgelist24.csv')
graphDegree = nx.degree(g)

pos = nx.spring_layout(g)

nx.draw(g,
        pos,
        node_size=[v * 10 for v in graphDegree.values()],
        with_labels=False,
        font_size=8)

'''
nx.draw_networkx_nodes(g,
                       pos,
                       nodelist=['tirsen'],
                       node_size=300,
                       node_color='g')
'''

nx.draw_networkx_nodes(g,
                       pos,
                       nodelist=['tirsen',
                                 'shen',
                                 'mlee',
                                 'ged',
                                 'objo',
                                 'stellsmi',
                                 'cowboyd',
                                 'asong',
                                 'christkv',
                                 'hisnice',
                                 'duelin_markers',
                                 'stillflame'],
                       node_size=300,
                       node_color='g')
