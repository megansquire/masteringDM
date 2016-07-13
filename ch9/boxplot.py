# -*- coding: utf-8 -*-
"""
Created on Tue Jul 05 11:01:19 2016

@author: megan
"""
import matplotlib.pyplot as plt

with open('sloc.txt', encoding='utf-8') as f:
    data = f.readlines()
newdata = list(map(int, data))
flierprops = dict(marker='o', 
                  markerfacecolor='green', 
                  markersize=8,
                  linestyle='none')
plt.boxplot(newdata, 
            showmeans=True, 
            flierprops=flierprops)
plt.show()
