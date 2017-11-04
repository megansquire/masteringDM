# -*- coding: utf-8 -*-
"""
Created on Sat Apr 16 13:58:50 2016

@author: megan
"""

import nltk
import pprint

# sample files that we use in this chapter
#filename = 'apacheMeetingMinutes.txt'
#filename = 'djangoIRCchat.txt'
#filename = 'gnueIRCsummary.txt'
filename = 'lkmlEmailsReduced.txt'

with open(filename, 'r', encoding='utf8') as sampleFile:
    text=sampleFile.read()

en = {}
try:   
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences = sent_detector.tokenize(text.strip())
    
    for sentence in sentences:
        tokenized = nltk.word_tokenize(sentence)
        tagged = nltk.pos_tag(tokenized)
        chunked = nltk.ne_chunk(tagged)
      
        # this was the original code in the book:
        '''
        for tree in chunked:
            if hasattr(tree, 'label'):
                ne = ' '.join(c[0] for c in tree.leaves())
                en[ne] = [tree.label(), ' '.join(c[1] for c in tree.leaves())]
        '''
        # here is another way to write it that might be easier for new programmers"
        for tree in chunked:
            if hasattr(tree, 'label'):
                ne = ''
                for c in tree.leaves():
                    ne += c[0] + ' '
                ne = ne.rstrip()
                en[ne] = tree.label()
    for key in en.keys():
        print(key, ':', en[key])
except Exception as e:
    print(str(e))
    
'''
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(en)
'''
