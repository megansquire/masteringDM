# -*- coding: utf-8 -*-
"""
File: entityAttributeMetrics.py
@author: Megan Squire
Purpose: Finds various string similarity metrics between project URLs stored
  in a database, writes these to a database table

"""
import pymysql
import sys
from nltk.metrics import *

password = sys.argv[1]

def soundex(name, len=4):
    """ soundex module conforming to Knuth's algorithm
        implementation 2000-12-24 by Gregory Jorgensen
        public domain
        available at: 
        http://code.activestate.com/recipes/52213-soundex-algorithm/
    """

    # digits holds the soundex values for the alphabet
    digits = '01230120022455012623010202'
    sndx = ''
    fc = ''

    # translate alpha chars in name to soundex digits
    for c in name.upper():
        if c.isalpha():
            if not fc: fc = c   # remember first letter
            d = digits[ord(c)-ord('A')]
            # duplicate consecutive soundex digits are skipped
            if not sndx or (d != sndx[-1]):
                sndx += d

    # replace first digit with first alpha character
    sndx = fc + sndx[1:]

    # remove all 0s from the soundex code
    sndx = sndx.replace('0','')

    # return soundex code padded to len characters
    return (sndx + (len * '0'))[:len]


# Open local database connection
db = pymysql.connect(host='localhost',
                     db='rfrg',
                     user='',
                     passwd='',
                     port=3306,
                     charset='utf8mb4')
cursor = db.cursor()
cursor1 = db.cursor()

# get all projects with matching URLs
cursor.execute("INSERT INTO book_entity_matches (rf_project_name, \
                                                rg_project_name) \
                SELECT rf.project_name, rg.project_name \
                FROM book_rf_entities rf \
                INNER JOIN book_rg_entities rg ON rf.url = rg.url")

# get additional projects that have matching project names
cursor.execute("INSERT INTO book_entity_matches(rf_project_name, \
                                                rg_project_name) \
                SELECT rf.project_name, rg.project_name \
                FROM book_rf_entities rf \
                INNER JOIN book_rg_entities rg \
                ON rf.project_name = rg.project_name \
                WHERE rf.project_name NOT IN ( \
                    SELECT bem.rf_project_name \
                    FROM book_entity_matches bem)")


# for each match candidate, calculate string metrics and fuzzy strings
cursor.execute("SELECT bem.rf_project_name, \
                       bem.rg_project_name, \
                       rfe.url, \
                       rge.url \
                FROM book_entity_matches bem \
                INNER JOIN book_rg_entities rge \
                  ON bem.rg_project_name = rge.project_name \
                INNER JOIN book_rf_entities rfe \
                  ON bem.rf_project_name = rfe.project_name \
                ORDER BY bem.rf_project_name")
projectPairs = cursor.fetchall()

for(projectPair) in projectPairs:
    RFname = projectPair[0]
    RGname = projectPair[1]
    RFurl  = projectPair[2]
    RGurl  = projectPair[3]
    
    # lowercase everything
    RFnameLC = RFname.lower()
    RGnameLC = RGname.lower()
    RFurlLC  = RFurl.lower()
    RGurlLC  = RGurl.lower()
    
    # calculate string metrics 
    levNames = edit_distance(RFnameLC, RGnameLC)
    levURLs  = edit_distance(RFurlLC, RGurlLC)
    soundexRFname = soundex(RFnameLC)
    soundexRGname = soundex(RGnameLC)
    
    # is the RF project name inside the RG project name?
    if RFnameLC in RGnameLC:
        rf_in_rg = 1
    else:
        rf_in_rg = 0

    # is the RF project name inside the RG project URL?
    if RFnameLC in RGurl:
        rf_in_rgurl = 1
    else:
        rf_in_rgurl = 0 

    # is any dev on the RF candidate in the dev list for the RG candidate?
    cursor1.execute("SELECT rf.dev_username, rf.dev_realname \
                    FROM book_rf_entity_people rf \
                    WHERE rf.project_name =  %s \
                    AND (rf.dev_username IN ( \
                        SELECT rg.person_name \
                        FROM book_rg_entity_people rg \
                        WHERE rg.project_name =  %s) \
                        OR \
                        rf.dev_realname IN ( \
                        SELECT rg.person_name \
                        FROM book_rg_entity_people rg \
                        WHERE rg.project_name = %s))",
                        (RFname, RGname, RGname))
    result = cursor1.fetchone()
    if result is not None:
        rfdev_in_rgdev = 1
    else:
        rfdev_in_rgdev = 0
    
    cursor1.execute("UPDATE book_entity_matches \
                        SET rf_name_soundex    = %s,\
                            rg_name_soundex    = %s, \
                            url_levenshtein    = %s, \
                            name_levenshtein   = %s, \
                            rf_name_in_rg_name = %s, \
                            rf_name_in_rg_url  = %s, \
                            rf_dev_in_rg_dev   = %s \
                        WHERE rf_project_name = %s \
                        AND rg_project_name = %s", 
                        (soundexRFname,
                         soundexRGname,
                         levURLs,
                         levNames,                         
                         rf_in_rg, 
                         rf_in_rgurl, 
                         rfdev_in_rgdev, 
                         RFname, 
                         RGname))

db.close()
