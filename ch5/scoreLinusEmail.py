# -*- coding: utf-8 -*-
"""
Created on Fri Apr  8 13:26:48 2016

@author: megan
"""
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
import pymysql
import sys

password = sys.argv[1]
db = pymysql.connect(host='localhost',
                     db='test',
                     user='megan',
                     passwd=password,
                     port=3306,
                     charset='utf8mb4')
selectCursor = db.cursor()
updateCursor = db.cursor()

selectEmailQuery = "SELECT url, body \
                    FROM lkml_stripped_torvalds_2016_01"
                    
updateScoreQuery = "UPDATE lkml_stripped_torvalds_2016_01 \
                    SET sentiment_score = %s, \
                    max_pos_score = %s, \
                    max_neg_score = %s \
                    WHERE url = %s"
selectCursor.execute(selectEmailQuery)
emails = selectCursor.fetchall()

for email in emails:
    url = email[0]
    body = email[1]
    
    print("===")
    sid = SentimentIntensityAnalyzer()    
    finalScore = 0
    maxPosScore = 0
    maxNegScore = 0
    
    emailLines = tokenize.sent_tokenize(body)
    for line in emailLines:
        line = line.replace('\n', ' ').replace('\r', '')
        #print(line)
        ss = sid.polarity_scores(line) 
        #for k in sorted(ss):
        #    print(' {0}: {1}\n'.format(k,ss[k]), end='')
        lineCompoundScore = ss['compound']
        finalScore += lineCompoundScore
        
        if ss['pos'] > maxPosScore:
            maxPosScore = ss['pos']
        elif ss['neg'] > maxNegScore:
            maxNegScore = ss['neg']
            
    roundedScore = round(finalScore/len(emailLines),4)
    print("***Final Email Score", roundedScore)
    print("Most Positive Sentence Score:", maxPosScore)
    print("Most Negative Sentence Score:", maxNegScore)
    
    #Use scores to update table
    try:
        updateCursor.execute(updateScoreQuery,(roundedScore, maxPosScore, maxNegScore, url))
        db.commit()
    except:
        db.rollback()
db.close()
