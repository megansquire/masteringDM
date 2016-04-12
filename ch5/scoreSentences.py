# -*- coding: utf-8 -*-
"""
Created on Fri Apr  8 13:26:48 2016

@author: megan
"""

from nltk.sentiment.vader import SentimentIntensityAnalyzer

with open('data/ubuntu2016-04-04/ubuntu.txt', encoding='utf-8') as ubuntu:
    ubuntuLines = [line.strip() for line in ubuntu.readlines()]
    
with open('data/ubuntu2016-04-04/ubuntu-devel.txt', encoding='utf-8') as ubuntuDevel:
    ubuntuDevelLines = [line.strip() for line in ubuntuDevel.readlines()]

ubuntu.close()
ubuntuDevel.close()

sid = SentimentIntensityAnalyzer()
finalScore = 0
for line in ubuntuLines[0:20]:
    print(line)
    ss = sid.polarity_scores(line)    
    for k in sorted(ss):
        print(' {0}: {1}\n'.format(k,ss[k]), end='')
    print()