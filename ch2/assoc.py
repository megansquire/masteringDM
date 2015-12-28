# -*- coding: utf-8 -*-
"""
File: assoc.py
@author: Megan Squire
Purpose: Finds frequent itemsets for tags used to describe Freecode projects.

Notes: 
1. Uses a MySQL database to store the tags, doubletons, tripletons. Code for
  SQL setup is in attached file.
2. Minimum support for itemsets is set in the MINSUPPORT constant.
"""
import itertools
import pymysql

# set threshold
# 2325 is a 5% threshold in the Freecode data set
MINSUPPORT = 2325

allSingletonTags = []
allDoubletonTags = set()

doubletonList = set()
tripletonList = set()


def findDoubletons():
    # use the list of allSingletonTags to make the doubleton candidates
    doubletonCandidates = list(itertools.combinations(allSingletonTags, 2))
    
    for (index, candidate) in enumerate(doubletonCandidates):
        # figure out if this doubleton candidate is frequent
        tag1 = candidate[0]
        tag2 = candidate[1]
        cursor.execute("SELECT count(fpt1.project_id) \
                        FROM fc_project_tags fpt1 \
                        INNER JOIN fc_project_tags fpt2 \
                        ON fpt1.project_id = fpt2.project_id \
                        WHERE fpt1.tag_name = %s \
                        AND fpt2.tag_name = %s", (tag1, tag2))
        row = cursor.fetchone()
        count = row[0]

        # if doubleton is frequent, write into db table                
        if count > MINSUPPORT:
            print ("frequent doubleton found: ",tag1,tag2,"[",count,"]")
            
            cursor.execute("INSERT INTO fc_project_tag_pairs \
                            (tag1, tag2, num_projs) \
                            VALUES (%s,%s,%s)",(tag1, tag2, count))
            
            # save the frequent doubleton to our final list
            doubletonList.add(candidate)          
            # add terms to a set of all doubleton terms (no duplicates)
            allDoubletonTags.add(tag1)
            allDoubletonTags.add(tag2)
        
  
def findTripletons():
    # use the list of allDoubletonTags to make the tripleton candidates
    tripletonCandidates = list(itertools.combinations(allDoubletonTags,3))
    
    for (index, candidate) in enumerate(tripletonCandidates):  
        # all doubletons inside this tripleton candidate MUST also be frequent
        # in order for this tripleton to even be considered
        doubletonsInsideTripleton = list(itertools.combinations(candidate,2))
        tripletonCandidateRejected = 0
        for (index, doubleton) in enumerate(doubletonsInsideTripleton):
            # test to see if this doubleton is in the frequent doubletonList
            # if it's not, then reject this candidate and break out of loop
            if doubleton not in doubletonList:
                tripletonCandidateRejected = 1
                break
        if tripletonCandidateRejected == 0:
            cursor.execute("SELECT count(fpt1.project_id) \
                FROM fc_project_tags fpt1 \
                INNER JOIN fc_project_tags fpt2 \
                ON fpt1.project_id = fpt2.project_id \
                INNER JOIN fc_project_tags fpt3 \
                ON fpt2.project_id = fpt3.project_id \
                WHERE fpt1.tag_name = %s \
                AND fpt2.tag_name = %s \
                AND fpt3.tag_name = %s", (candidate[0],
                                          candidate[1],
                                          candidate[2]))
            row = cursor.fetchone()
            count = row[0]
            if count > MINSUPPORT:
                print ("found frequent tripleton: ",candidate,count)
                cursor.execute("INSERT INTO fc_project_tag_triples \
                                (tag1, tag2, tag3, num_projs) \
                                VALUES (%s,%s,%s,%s)",
                                (candidate[0],
                                 candidate[1],
                                 candidate[2],
                                 count))
            
                 
    
# Open local database connection
db = pymysql.connect(host='grid6.cs.elon.edu',
                     db='test',
                     user='megan',
                     passwd='',
                     port=3306,
                     charset='utf8mb4')
cursor = db.cursor()

# fc_freq_tags_5pc is a view created to hold each tag and its count of projects
query = "SELECT DISTINCT tag_name \
        FROM fc_freq_tags_5pc \
        ORDER BY num_projs DESC"
cursor.execute(query)
singletons = cursor.fetchall()

for(singleton) in singletons:
    allSingletonTags.append(singleton[0])

findDoubletons()
findTripletons()
db.close()


