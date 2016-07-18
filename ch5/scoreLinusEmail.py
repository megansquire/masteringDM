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
                    FROM lkml_ch5"
                    
updateScoreQuery = "UPDATE lkml_ch5 \
                    SET sentiment_score = %s, \
                    max_pos_score = %s, \
                    max_neg_score = %s \
                    WHERE url = %s"
selectCursor.execute(selectEmailQuery)
emails = selectCursor.fetchall()

for email in emails:
    url = email[0]
    body = email[1]
    
    # variables to hold the overall average compound score for message
    finalScore = 0
    roundedFinalScore = 0
    
    # variables to hold the highest positive score in the message
    # and highest negative score in the message
    maxPosScore = 0
    maxNegScore = 0
    
    print("===")
    sid = SentimentIntensityAnalyzer()
    emailLines = tokenize.sent_tokenize(body)
    for line in emailLines:
        ss = sid.polarity_scores(line)
        # uncomment these lines if you want to print out sentences & scores
        '''
        line = line.replace('\n', ' ').replace('\r', '')
        print(line)
        for k in sorted(ss):
            print(' {0}: {1}\n'.format(k,ss[k]), end='')
        '''
        lineCompoundScore = ss['compound']
        finalScore += lineCompoundScore
        
        if ss['pos'] > maxPosScore:
            maxPosScore = ss['pos']
        elif ss['neg'] > maxNegScore:
            maxNegScore = ss['neg']
            
    # roundedFinalScore is the average compound score for the entire message
    roundedFinalScore = round(finalScore/len(emailLines),4)
    print("***Final Email Score", roundedFinalScore)
    print("Most Positive Sentence Score:", maxPosScore)
    print("Most Negative Sentence Score:", maxNegScore)
    
    # update table with calculated fields
    try:
        updateCursor.execute(updateScoreQuery,(roundedFinalScore, maxPosScore, maxNegScore, url))
        db.commit()
    except:
        db.rollback()
db.close()
