# -*- coding: utf-8 -*-
"""
File: assocPairsOnly.py
@author: Megan Squire
Purpose: Finds frequent itemsets of ws entities.

Notes:
1. Uses a MySQL database to store the tags, doubletons, tripletons. Code for
  SQL setup is in attached file.
2. Minimum support for itemsets is set in the MINSUPPORT constant.
"""
import itertools
import pymysql

# set threshold as a percent
MINSUPPORTPCT = .25

# database connection parameters
dbhost = 'cs.elon.edu'
dbschema = 'test'
dbuser = 'msquire'
dbpasswd = getpass.getpass()
dbport = 3306
dbcharset = 'utf8mb4'

# variables to hold our sets of possible singletons, possible pairs, and definite pairs
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
        e1 = candidate[0]
        e2 = candidate[1]
        print("Looking at:", e1, ",", e2)
        cursor.execute("SELECT count(ws1.personID) \
                        FROM ws_distinct_people_entity_tags ws1 \
                        INNER JOIN ws_distinct_people_entity_tags ws2 \
                        ON ws1.personID = ws2.personID \
                        WHERE ws1.entityType = %s \
                        AND ws2.entityType = %s", (e1, e2))
        count = cursor.fetchone()[0]

        # add frequent doubleton to database
        if count > minsupport:
            print("Success: ", e1, e2, " [", count, "]", sep='')

            cursor.execute("INSERT INTO ws_entity_pairs \
                            (e1, e2, num_people) \
                            VALUES (%s,%s,%s)", (e1, e2, count))
            # save the frequent doubleton to our final list
            doubletonSet.add(candidate)
            # add terms to a set of all doubleton terms (no duplicates)
            allDoubletonTags.add(e1)
            allDoubletonTags.add(e2)


def generateRules():
    print("======")
    print("Association Rules:")
    print("======")

    # pull final list of pairs to make the rules
    cursor.execute("SELECT e1, e2, num_people FROM ws_entity_pairs")
    pairs = cursor.fetchall()
    for(pair) in pairs:
        tag1 = pair[0]
        tag2 = pair[1]
        ruleSupport = pair[2]

        calcSCAV(tag1, tag2, ruleSupport)
        calcSCAV(tag2, tag1, ruleSupport)
        print("***")


def calcSCAV(tagA, tagB, ruleSupport):
    # Support
    ruleSupportPct = round((ruleSupport/baskets), 4)

    # Confidence
    confQuery = "SELECT count(distinct personID) \
              FROM ws_distinct_people_entity_tags \
              WHERE entityType = %s"
    cursor.execute(confQuery, (tagA))
    ASupport = cursor.fetchone()[0]
    confidence = round((ruleSupport / ASupport), 4)

    # Added Value
    query2 = "SELECT count(distinct personID) \
            FROM ws_distinct_people_entity_tags \
            WHERE entityType= %s"
    cursor.execute(query2, tagB)
    supportTagB = cursor.fetchone()[0]
    supportTagBPct = supportTagB/baskets
    addedValue = round((confidence - supportTagBPct), 4)

    # Result
    print(tagA, "->", tagB,
          "[S=", ruleSupportPct,
          ", C=", confidence,
          ", AV=", addedValue,
          "]", sep='')

# Open local database connection
db = pymysql.connect(host=dbhost,
                     db=dbschema,
                     user=dbuser,
                     passwd=dbpasswd,
                     port=dbport,
                     charset=dbcharset,
                     autocommit=True)
cursor = db.cursor()

# calculate total number of baskets (people)
queryBaskets = "SELECT count(DISTINCT personID) \
                FROM ws_distinct_people_entity_tags;"
cursor.execute(queryBaskets)
baskets = cursor.fetchone()[0]

# calculate minimum number of baskets based on minimum support threshold
minsupport = baskets*(MINSUPPORTPCT/100)
print("Minimum support count:",
      minsupport,
      "(",
      MINSUPPORTPCT,
      "% of",
      baskets,
      ")", sep='')

# get entities that meet our minimum support threshold
cursor.execute("SELECT DISTINCT entityType \
                FROM ws_distinct_people_entity_tags \
                GROUP BY 1 \
                HAVING COUNT(entityType) >= %s ORDER BY entityType",
               (minsupport))
singletons = cursor.fetchall()

for(singleton) in singletons:
    allSingletonTags.append(singleton[0])

findDoubletons()
generateRules()

db.close()
