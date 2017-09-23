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
import getpass

# set threshold as a percent (example, 5% of Freecode baskets is about 2325)
MINSUPPORTPCT = 5
# database connection parameters
dbhost = 'cs.elon.edu'
dbschema = 'test'
dbuser = 'msquire'
dbpasswd = getpass.getpass()
dbport = 3306
dbcharset = 'utf8mb4'

allSingletonTags = []
allDoubletonTags = set()

doubletonSet = set()

def findDoubletons():
    print("======")
    print("Frequent doubletons found:")
    print("======")
    # use the list of allSingletonTags to make the doubleton candidates
    doubletonCandidates = list(itertools.combinations(allSingletonTags, 2))
    for (index, candidate) in enumerate(doubletonCandidates):
        # figure out if this doubleton candidate is frequent
        tag1 = candidate[0]
        tag2 = candidate[1]
        getDoubletonFrequencyQuery = "SELECT count(fpt1.project_id) \
                                     FROM fc_project_tags fpt1 \
                                     INNER JOIN fc_project_tags fpt2 \
                                     ON fpt1.project_id = fpt2.project_id \
                                     WHERE fpt1.tag_name = %s \
                                     AND fpt2.tag_name = %s"
        insertPairQuery = "INSERT INTO msquire.fc_project_tag_pairs \
                                (tag1, tag2, num_projs) \
                                VALUES (%s,%s,%s)"
        cursor.execute(getDoubletonFrequencyQuery, (tag1, tag2))
        count = cursor.fetchone()[0]

        # add frequent doubleton to database                
        if count > minsupport:
            print (tag1,tag2,"[",count,"]")
            
            
            cursor.execute(insertPairQuery,(tag1, tag2, count))
            
            # save the frequent doubleton to our final list
            doubletonSet.add(candidate)         
            # add terms to a set of all doubleton terms (no duplicates)
            allDoubletonTags.add(tag1)
            allDoubletonTags.add(tag2)
        
  
def findTripletons():
    print("======")
    print("Frequent tripletons found:")
    print("======")
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
        # set up queries
        getTripletonFrequencyQuery = "SELECT count(fpt1.project_id) \
                                        FROM fc_project_tags fpt1 \
                                        INNER JOIN fc_project_tags fpt2 \
                                        ON fpt1.project_id = fpt2.project_id \
                                        INNER JOIN fc_project_tags fpt3 \
                                        ON fpt2.project_id = fpt3.project_id \
                                        WHERE (fpt1.tag_name = %s \
                                        AND fpt2.tag_name = %s \
                                        AND fpt3.tag_name = %s)"
        insertTripletonQuery = "INSERT INTO msquire.fc_project_tag_triples \
                                (tag1, tag2, tag3, num_projs) \
                                VALUES (%s,%s,%s,%s)"
        # insert frequent tripleton into database
        if tripletonCandidateRejected == 0:
            cursor.execute(getTripletonFrequencyQuery, (candidate[0],
                                                        candidate[1],
                                                        candidate[2]))
            count = cursor.fetchone()[0]
            if count > minsupport:
                print (candidate[0],",",
                       candidate[1],",",
                       candidate[2],
                       "[",count,"]")
                cursor.execute(insertTripletonQuery,
                                (candidate[0],
                                 candidate[1],
                                 candidate[2],
                                 count))

def generateRules():
    print("======")    
    print("Association Rules:")
    print("======")

    # pull final list of tripletons to make the rules
    getFinalListQuery = "SELECT tag1, tag2, tag3, num_projs \
                   FROM msquire.fc_project_tag_triples"
    cursor.execute(getFinalListQuery)
    triples = cursor.fetchall()
    for(triple) in triples:
        tag1 = triple[0]
        tag2 = triple[1]
        tag3 = triple[2]
        ruleSupport = triple[3]
        
        calcSCAV(tag1, tag2, tag3, ruleSupport)
        calcSCAV(tag1, tag3, tag2, ruleSupport)
        calcSCAV(tag2, tag3, tag1, ruleSupport)
        print("*")

def calcSCAV(tagA, tagB, tagC, ruleSupport):
    # Support
    ruleSupportPct = round((ruleSupport/baskets),2)

    # Confidence    
    queryConf = "SELECT num_projs \
              FROM msquire.fc_project_tag_pairs \
              WHERE (tag1 = %s AND tag2 = %s) \
              OR    (tag2 = %s AND tag1 = %s)"
    cursor.execute(queryConf, (tagA, tagB, tagA, tagB))
    pairSupport = cursor.fetchone()[0]
    confidence = round((ruleSupport / pairSupport),2)
    
    # Added Value
    queryAV = "SELECT count(*) \
              FROM test.fc_project_tags \
              WHERE tag_name= %s"
    cursor.execute(queryAV, tagC)
    supportTagC = cursor.fetchone()[0]
    supportTagCPct = supportTagC/baskets
    addedValue = round((confidence - supportTagCPct),2)
    
    # Result
    print(tagA,",",tagB,"->",tagC,
          "[S=",ruleSupportPct,
          ", C=",confidence,
          ", AV=",addedValue,
          "]")
          
# Open local database connection
db = pymysql.connect(host=dbhost,
                     db=dbschema,
                     user=dbuser,
                     passwd=dbpasswd,
                     port=dbport,
                     charset=dbcharset,
                     autocommit=True)
cursor = db.cursor()

# calculate number of baskets
queryBaskets = "SELECT count(DISTINCT project_id) \
                FROM fc_project_tags;"
cursor.execute(queryBaskets)
baskets = cursor.fetchone()[0]

# calculate minimum number of baskets based on minimum support threshold
minsupport = baskets*(MINSUPPORTPCT/100)
print("Minimum support count:",minsupport,"(",MINSUPPORTPCT,"% of",baskets,")")

# get tags that meet our minimum support threshold
tagNameQuery = "SELECT DISTINCT tag_name \
                FROM fc_project_tags \
                GROUP BY 1 \
                HAVING COUNT(project_id) >= %s \
                ORDER BY tag_name"
cursor.execute(tagNameQuery,(minsupport))
singletons = cursor.fetchall()

for(singleton) in singletons:
    allSingletonTags.append(singleton[0])

findDoubletons()
findTripletons()
generateRules()

db.close()
