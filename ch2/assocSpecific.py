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
import pymysql

X = 'Internet'
Y = 'Web'

# Open local database connection
db = pymysql.connect(host='',
                     db='',
                     user='',
                     passwd='',
                     port=3306,
                     charset='utf8mb4')
cursor = db.cursor()

# grab basic counts from the database that we need

numBasketsQuery = "SELECT count(DISTINCT project_id) FROM fc_project_tags"
cursor.execute(numBasketsQuery)
numBaskets = cursor.fetchone()[0]

supportForXQuery = "SELECT count(*) FROM fc_project_tags WHERE tag_name=%s" 
cursor.execute(supportForXQuery, (X))
supportForX = cursor.fetchone()[0]

supportForYQuery = "SELECT count(*) FROM fc_project_tags WHERE tag_name=%s"
cursor.execute(supportForYQuery, (Y))
supportForY = cursor.fetchone()[0]

pairSupportQuery = "SELECT num_projs FROM fc_project_tag_pairs WHERE tag1=%s AND tag2=%s"
cursor.execute(pairSupportQuery,(X,Y))
pairSupport = cursor.fetchone()[0]
 
# calculate support : support of pair, divided by num baskets
pairSupportAsPct = pairSupport / numBaskets

# calculate confidence of X->Y
supportForXAsPct = supportForX / numBaskets
confidenceXY = pairSupportAsPct / supportForXAsPct

# calculate confidence of Y->X
supportForYAsPct = supportForY / numBaskets
confidenceYX = pairSupportAsPct/ supportForYAsPct

# calculate added value X->Y
AVXY = confidenceXY - supportForYAsPct
AVYX = confidenceYX - supportForXAsPct

print("Support for ",X,"U",Y,":", round(pairSupportAsPct, 2))
print("Conf.",X,"->",Y,":", round(confidenceXY, 2))
print("Conf.",Y,"->",X,":", round(confidenceYX, 2))
print("AV",X,"->",Y,":", round(AVXY, 2))
print("AV",Y,"->",X,":", round(AVYX, 2))

db.close()