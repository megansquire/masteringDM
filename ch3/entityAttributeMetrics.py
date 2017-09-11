# -*- coding: utf-8 -*-
"""
File: entityAttributeMetrics.py
@author: Megan Squire
Purpose: Finds various string similarity metrics between project URLs stored
  in a database, writes these to a database table

"""
import pymysql
from nltk.metrics import *
import getpass
from soundex import soundex

# database connection params
dbhost = 'cs.elon.edu'
dbschema = 'msquire'
dbuser = 'msquire'
dbpasswd = getpass.getpass()
dbport = 3306
dbcharset = 'utf8mb4'

# set up queries
peopleQuery = "SELECT rf.dev_username, rf.dev_realname \
               FROM rfrg.book_rf_entity_people rf \
               WHERE rf.project_name =  %s \
               AND (rf.dev_username IN ( \
                    SELECT rg.person_name \
                    FROM rfrg.book_rg_entity_people rg \
                    WHERE rg.project_name =  %s) \
                    OR \
                    rf.dev_realname IN ( \
                    SELECT rg.person_name \
                    FROM rfrg.book_rg_entity_people rg \
                    WHERE rg.project_name = %s))"

updateQuery = "UPDATE book_entity_matches \
               SET rf_name_soundex    = %s,\
                   rg_name_soundex    = %s, \
                   url_levenshtein    = %s, \
                   name_levenshtein   = %s, \
                   rf_name_in_rg_name = %s, \
                   rf_name_in_rg_url  = %s, \
                   rf_dev_in_rg_dev   = %s \
               WHERE rf_project_name = %s \
               AND rg_project_name = %s"

# Open local database connection
db = pymysql.connect(host=dbhost,
                     db=dbschema,
                     user=dbuser,
                     passwd=dbpasswd,
                     port=dbport,
                     charset=dbcharset,
                     autocommit=True)
cursor = db.cursor()

# get all projects with matching URLs
cursor.execute("INSERT INTO book_entity_matches (rf_project_name, \
                                                rg_project_name) \
                SELECT rf.project_name, rg.project_name \
                FROM rfrg.book_rf_entities rf \
                INNER JOIN rfrg.book_rg_entities rg ON rf.url = rg.url")

# get additional projects that have matching project names
cursor.execute("INSERT INTO book_entity_matches(rf_project_name, \
                                                rg_project_name) \
                SELECT rf.project_name, rg.project_name \
                FROM rfrg.book_rf_entities rf \
                INNER JOIN rfrg.book_rg_entities rg \
                ON rf.project_name = rg.project_name \
                WHERE rf.project_name NOT IN ( \
                    SELECT bem.rf_project_name \
                    FROM book_entity_matches bem)")


# for each match candidate, calculate string metrics and fuzzy strings
cursor.execute("SELECT bem.rf_project_name, \
                       bem.rg_project_name, \
                       rfe.url, \
                       rge.url \
                FROM rfrg.book_entity_matches bem \
                INNER JOIN rfrg.book_rg_entities rge \
                  ON bem.rg_project_name = rge.project_name \
                INNER JOIN rfrg.book_rf_entities rfe \
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
    cursor.execute(peopleQuery,
                   (RFname, RGname, RGname))
    result = cursor.fetchone()
    if result is not None:
        rfdev_in_rgdev = 1
    else:
        rfdev_in_rgdev = 0

    cursor.execute(updateQuery,
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
