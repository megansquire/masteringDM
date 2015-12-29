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

# set threshold as a percent (example, 5% of Freecode baskets is about 2325)
MINSUPPORTPCT = 5

allSingletonTags = []
allDoubletonTags = set()

doubletonSet = set()
tripletonSet = set()


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
        count = cursor.fetchone()[0]

        # add frequent doubleton to database                
        if count > minsupport:
            print ("frequent doubleton found: ",tag1,tag2,"[",count,"]")
            
            #cursor.execute("INSERT INTO fc_project_tag_pairs \
            #                (tag1, tag2, num_projs) \
            #                VALUES (%s,%s,%s)",(tag1, tag2, count))
            
            # save the frequent doubleton to our final list
            doubletonSet.add(candidate)         
            # add terms to a set of all doubleton terms (no duplicates)
            allDoubletonTags.add(tag1)
            allDoubletonTags.add(tag2)
        
  
def findTripletons():
    # use the list of allDoubletonTags to make the tripleton candidates
    tripletonCandidates = list(itertools.combinations(allDoubletonTags,3))

    # sort each candidate tuple and add these to a new sorted candidate list    
    tripletonCandidatesSorted = []
    for tc in tripletonCandidates:
        tripletonCandidatesSorted.append(sorted(tc))
    
    # figure out if this tripleton candidate is frequent
    for (index, candidate) in enumerate(tripletonCandidatesSorted):          
        # all doubletons inside this tripleton candidate MUST also be frequent
        doubletonsInsideTripleton = list(itertools.combinations(candidate,2))
        tripletonCandidateRejected = 0
        for (index, doubleton) in enumerate(doubletonsInsideTripleton):
            if doubleton not in doubletonSet:
                tripletonCandidateRejected = 1
                break
        # add frequent tripleton to database
        if tripletonCandidateRejected == 0:
            cursor.execute("SELECT count(fpt1.project_id) \
                FROM fc_project_tags fpt1 \
                INNER JOIN fc_project_tags fpt2 \
                ON fpt1.project_id = fpt2.project_id \
                INNER JOIN fc_project_tags fpt3 \
                ON fpt2.project_id = fpt3.project_id \
                WHERE (fpt1.tag_name = %s \
                AND fpt2.tag_name = %s \
                AND fpt3.tag_name = %s)", (candidate[0],
                                          candidate[1],
                                          candidate[2]))
            count = cursor.fetchone()[0]
            if count > minsupport:
                print ("frequent tripleton found: ",
                       candidate[0],
                       candidate[1],
                       candidate[2],
                       "[",count,"]")
                #cursor.execute("INSERT INTO fc_project_tag_triples \
                #                (tag1, tag2, tag3, num_projs) \
                #                VALUES (%s,%s,%s,%s)",
                #                (candidate[0],
                #                 candidate[1],
                #                 candidate[2],
                #                 count))

def generateRules():
    # 1. generate list of rules from triples    
    # 2. generate confidence
    # 3. print rule with support and confidence

    # pull final list of tripletons to make the rules
    cursor.execute("SELECT tag1, tag2, tag3, num_projs \
                        FROM fc_project_tag_triples")
    triples = cursor.fetchall()
    for(triple) in triples:
        tag1 = triple[0]
        tag2 = triple[1]
        tag3 = triple[2]
        ruleSupport = triple[3]
        ruleSupportPct = round((ruleSupport/baskets),2)
        
        # confidence(tag1,tag2 -> tag3) = support(tag1,tag2,tag3) / support(tag1,tag2)
        # Since we have the numerator already, we just need to caldulate the denominator
        
        # calculate tag1, tag2 -> tag3
        cursor.execute("SELECT num_projs FROM fc_project_tag_pairs \
            WHERE (tag1 = %s AND tag2 = %s) or (tag2 = %s AND tag1 = %s)",
            (tag1, tag2, tag2, tag1))
        pairSupportA = cursor.fetchone()[0]
        confidenceA = round((ruleSupport / pairSupportA),2)
        print(tag1,",",tag2,"->",tag3, "[support=",ruleSupportPct,", confidence=",confidenceA,"]")
        
        # calculate tag1, tag3 -> tag2
        cursor.execute("SELECT num_projs FROM fc_project_tag_pairs \
            WHERE (tag1 = %s AND tag2 = %s) or (tag2 = %s AND tag1 = %s)",
            (tag1, tag3, tag3, tag1))
        pairSupportB = cursor.fetchone()[0]
        confidenceB = round((ruleSupport / pairSupportB),2)
        print(tag1,",",tag3,"->",tag2, "[support=",ruleSupportPct,", confidence=",confidenceB,"]")    
        
        # calculate tag2, tag3 -> tag1
        cursor.execute("SELECT num_projs FROM fc_project_tag_pairs \
            WHERE (tag1 = %s AND tag2 = %s) or (tag2 = %s AND tag1 = %s)",
            (tag2, tag3, tag3, tag2))
        pairSupportC = cursor.fetchone()[0]
        confidenceC = round((ruleSupport / pairSupportC),2) 
        print(tag2,",",tag3,"->",tag1, "[support=",ruleSupportPct,", confidence=",confidenceC,"]")
        
    
# Open local database connection
db = pymysql.connect(host='localhost',
                     db='test',
                     user='megan',
                     passwd='',
                     port=3306,
                     charset='utf8mb4')
cursor = db.cursor()

# calculate number of baskets
queryBaskets = "SELECT count(DISTINCT project_id) FROM fc_project_tags;"
cursor.execute(queryBaskets)
baskets = cursor.fetchone()[0]

# calculate minimum number of baskets based on minimum support threshold
minsupport = baskets*(MINSUPPORTPCT/100)
print(minsupport)

# get tags that meet our minimum support threshold
cursor.execute("SELECT DISTINCT tag_name \
            FROM fc_project_tags \
            GROUP BY 1 \
            HAVING COUNT(project_id) >= %s ORDER BY tag_name",(minsupport))
singletons = cursor.fetchall()

for(singleton) in singletons:
    allSingletonTags.append(singleton[0])

findDoubletons()
findTripletons()
generateRules()

db.close()
