# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 15:18:00 2017

@author: TA2761
******* create the query for the first function for the files that need sizing
"""

import sqlite3
import pandas as pd
import os
#from hurry.filesize import size

sqlite_file = 'myNashvilleOSMdb.db'
conn = sqlite3.connect(sqlite_file)
cur = conn.cursor()

#the new python input
try:
    input = raw_input
except NameError: #Python 3
    pass

RESTART = 'active'

def intro():
    global RESTART
    print '''\nWelcome! This program will display the results of my, Teresa Aysan's, SQL Queries for you.\n
    For your convenience I have divided them into groups because I have created so may SQL queries,\n
    and I want you to be able to display them in a reasonably sized window.\n
    This program will allow you to select the group that you want to run; or to select all groups.\n
    Here are the groups.\n
    '''
    listGroups()
    while RESTART == 'active':
        restart()

def restart():
    global RESTART
    restartPrompt = str.upper(input("Do you wish to make another Query group selection? [y]Yes then Enter or any other key then Enter to terminate: "))
    if restartPrompt == 'Y':
        listGroups()
    else:
        RESTART = 'finished'

def listGroups():
    global RESTART
    print "\n0. Cleaning data proof."
    print "1. File sizes."
    print "2. Simple Query: Printing a list without using pandas dataframes(df) (the other queries are on pandas df output)."
    print "3. Various COUNT queries using DISTINCT, WHERE, GROUP BY, ORDER BY, LIMIT."
    print "4. Using queries to understand the values of the tags."
    print "5. Using queries and subqueries for averages and for greater than and less than."
    print "6. Building the basis for the Airport Road queries. Finding TAGs, KEYs, VALUEs with meaningful data."
    print "7. More complex Airport Road queries and subqueries."
    print "8. Queries to find statistics on which Counties Airport Road goes through."
    print "9. Run all queries"
   
    listGroupPrompt = "Position your cursor after the : and enter your choice by number, then press Enter. Press any other key then Enter to terminate: "
    choice = input(listGroupPrompt)

    if choice == '0':
        cleanDataProof()
        
    elif choice == '1':
        fileSize()

    elif choice == '2':
        simpleQuery()

    elif choice == '3':
        countQueries()

    elif choice == '4':
        valueQueries()

    elif choice == '5':
        subqAvgQueries()
        
    elif choice == '6':
        tagKeysQueries()
        
    elif choice == '7':
        complexAirportQueries()
        
    elif choice == '8':
        airportCountiesQueries()

    elif choice == '9':
        cleanDataProof()
        fileSize()
        airportCountiesQueries()
        simpleQuery()
        countQueries()
        valueQueries()
        subqAvgQueries()
        tagKeysQueries()
        complexAirportQueries()
        airportCountiesQueries()
   
    else:
        RESTART = 'finished'   

def cleanDataProof(): # Proof as reported
    print "\nLook for street name 'C1TY AVENUE - note the number 1 in the C1TY' "
    print "\nShow that no record is found after cleaning in the street key for both nodes_tags and ways_tags."
    
    queries_list = (['''SELECT *
                     FROM nodes_tags  
                     WHERE value = 'C1TY AVENUE' ;''',
                       '''SELECT *
                     FROM nodes_tags  
                     WHERE value = 'City Avenue' ;''',
                     '''SELECT *
                     FROM ways_tags  
                     WHERE value = 'C1TY AVENUE' ;''',
                       '''SELECT *
                     FROM ways_tags  
                     WHERE value = 'City Avenue' ;'''
                    ])
    for query in queries_list:
        print "\nFor query: ", query, "\nOutput is:"
        cur.execute(query)
        # Printing with panda dataframe
        names = [description[0] for description in cur.description]
        rows = cur.fetchall()
        print "\nNumber of rows: ", len(rows)
        if len(rows) == 0:
            print "\nThere are no records found.\n"
        else:
            df = pd.DataFrame(rows)
            df.columns = names
            print df
def fileSize(): # File Sizes 
    from hurry.filesize import size
    print "\nThis program prints your files' sizes.\nIf you are Teresa, the path will automatically be chosen. \nIf not, then you will be prompted to enter a path to your files."
    prompt = 'Are you Teresa?\nPosition your cursor after the colon at the end of this prompt and enter Y or any other key if you are not.\nThen press enter: '
    response = str.upper(input(prompt))
    if response == 'Y':
        dirpath = 'C:\DA\DA P3\DA P3 Project\Files that need sizing'
    else:
        prompt = "\nPosition your cursor after the colon at the end of this prompt.\nThen enter the directory path where your files are.\nThen press enter.\nIf you enter an invalid path, no files will be printed: "
        dirpath = input(prompt)
    print "\n YOUR FILE SIZES ARE: \n"
    files_list = []
    for path, dirs, files in os.walk(dirpath):
        files_list.extend([(filename, size(os.path.getsize(os.path.join(path, filename)))) for filename in files])
    for filename, size in files_list: # This works regardless of the spyder warning
        print '{:.<40s}: {:5s}'.format(filename,size)

def simpleQuery():
    print "\nSimple Query: Printing a list without using pandas df: "
    print "\nCount the number of node_tags grouped by city upper or lowercase city names. \nPrinted as a list: "
    cur.execute('''SELECT value, count(*) as num from nodes_tags where key='city' group by upper(value) order by num desc;''') # Combines total count for cities that have upper or lower case mix
    alist = (cur.fetchall())
    for item in alist:
        print item[0], item[1] 

def countQueries():
    print "\nVarious COUNT queries using DISTINCT, WHERE, GROUP BY, ORDER BY, LIMIT."
    print "\nPut the queries in a queries_list called by a for statement to reduce the amount of code."
    print "\nPrint the output in pandas dataframe for easier readability."
    queries_list = ('''SELECT COUNT(*) FROM nodes ;''', 
                    '''SELECT id, COUNT(*) FROM nodes ;''', 
                    '''SELECT COUNT(DISTINCT nodes.id) FROM nodes ;''', 
                    '''SELECT COUNT(*) FROM nodes_tags;''', 
                    '''SELECT COUNT(*) FROM ways;''', 
                    '''SELECT COUNT(*) FROM ways_tags;''', 
                    '''SELECT COUNT(DISTINCT nodes_tags.value) FROM nodes_tags WHERE key='city' ;''',
                    '''SELECT value, COUNT(*) AS num FROM nodes_tags WHERE key='city' GROUP BY UPPER(value) 
                    ORDER BY num DESC LIMIT 10;''',
                    '''SELECT value, COUNT(*) AS num FROM nodes_tags WHERE key = 'city' ORDER BY num DESC;''', 
                    '''SELECT COUNT(DISTINCT nodes_tags.value) FROM nodes_tags WHERE key='city' ;'''
                    )
    for query in queries_list:
        print "\nFor query: ", query, "\nOutput is:"
        cur.execute(query)
        # Printing with panda dataframe
        names = [description[0] for description in cur.description]
        rows = cur.fetchall()
        print "\nNumber of rows: ", len(rows)
        if len(rows) == 0:
            print "\nThere are no records found.\n"
        else:
            df = pd.DataFrame(rows)
            df.columns = names
            print df

def valueQueries():
    print "\nUsing queries to understand the values of the tags."
    print "\nUse subqueries. Using UNION, HAVING."
    print "\nCreating uid queries."    
    queries_list = (
                    '''SELECT key, COUNT(*) FROM nodes_tags GROUP BY key ORDER BY COUNT(*) DESC LIMIT 30;''',
                    '''SELECT DISTINCT nodes_tags.value FROM nodes_tags ;''',    
                    '''SELECT DISTINCT nodes_tags.key FROM nodes_tags ;''',
                    '''SELECT key FROM nodes_tags ;''',
                    '''SELECT uid, COUNT(*) AS uid_count FROM nodes''',
                    '''SELECT uid, COUNT(*) AS uid_count FROM nodes GROUP BY uid ORDER BY COUNT(*) DESC LIMIT 40;''',
                    '''SELECT uid, user, COUNT(uid) AS uid_count FROM nodes GROUP BY uid ORDER BY COUNT(*) DESC LIMIT 10;''',                    '''SELECT uid, COUNT(*) AS uid_count FROM nodes WHERE uid > 100000''',
                    '''SELECT COUNT(DISTINCT(subq1.uid)) FROM (SELECT uid FROM nodes UNION ALL SELECT uid FROM ways) subq1;''',
                    '''SELECT COUNT(*) FROM (SELECT subq1.user, COUNT(*) as num FROM 
                    (SELECT user FROM nodes UNION ALL SELECT user FROM ways) subq1 GROUP BY subq1.user HAVING num=1) subq2;''',
                    '''SELECT uid, COUNT(*) AS uid_count FROM nodes GROUP BY uid ORDER BY COUNT(*) DESC;'''
                    )
    for query in queries_list:
        print "\nFor query: ", query, "\nOutput is:"
        cur.execute(query)
        # Printing with panda dataframe
        names = [description[0] for description in cur.description]
        #print "\ncur.description: ", cur.description
        rows = cur.fetchall()
        print "\nNumber of rows: ", len(rows)
        if len(rows) == 0:
            print "\nThere are no records found.\n"
        else:
            df = pd.DataFrame(rows)
            df.columns = names
            print df

def subqAvgQueries():
    print "\nUsing queries and subqueries for averages and for greater than and less than."
    queries_list = (
                    '''SELECT uid, avg(uid_count) AS average FROM (SELECT uid, COUNT(*) AS uid_count FROM nodes 
                    GROUP BY uid ORDER BY COUNT(*) DESC) as subquery;''',
                    '''SELECT avg(uid_count) AS average FROM (SELECT uid, COUNT(*) AS uid_count FROM nodes 
                    GROUP BY uid ORDER BY COUNT(*) DESC) as subquery;''',
                    '''SELECT id, lat, lon, user, uid, version, changeset, timestamp FROM nodes, (SELECT avg(lat) 
                    AS average FROM nodes) AS subq1 WHERE lat>average;''',
                    '''SELECT id, lat, lon, user, uid, version, changeset, timestamp FROM nodes, (SELECT avg(lat) 
                    AS lat_avg FROM nodes) AS subq1, 
                    (SELECT avg(lon) AS lon_avg FROM nodes) AS subq2 WHERE lat>lat_avg AND lon>lon_avg;'''

                    )
    for query in queries_list:
        print "\nFor query: ", query, "\nOutput is:"
        cur.execute(query)
        # Printing with panda dataframe
        names = [description[0] for description in cur.description]
        rows = cur.fetchall()
        print "\nNumber of rows: ", len(rows)
        if len(rows) == 0:
            print "\nThere are no records found.\n"
        else:
            df = pd.DataFrame(rows)
            df.columns = names
            print df

def tagKeysQueries():
    print "\nBuilding the basis for the Airport Road queries. Finding TAGs, KEYs, VALUEs with meaningful data."
    print "\nI want to know which counties Airport Road goes through."    
    queries_list = (
                    '''SELECT * FROM ways_tags WHERE value = 'Airport Road' ;''',
                    '''SELECT * FROM ways_tags WHERE id = '5109312' ;''',
                    '''SELECT * FROM ways_tags WHERE key = 'county' ;''',
                    '''SELECT key, COUNT(*) FROM ways_tags GROUP BY key ORDER BY COUNT(*) DESC LIMIT 30;''',
                    '''SELECT value, COUNT(*) FROM ways_tags WHERE key = 'highway' GROUP BY key ORDER BY COUNT(*) DESC LIMIT 30;''',
                    '''SELECT value, COUNT(*) AS num FROM ways_tags WHERE key='highway' GROUP BY UPPER(value) 
                    ORDER BY num DESC LIMIT 10 ;''',
                    '''SELECT type, COUNT(*) FROM ways_tags GROUP BY type ORDER BY COUNT(*) DESC LIMIT 30 ;''',
                    '''SELECT value, COUNT(*) AS num FROM ways_tags WHERE type='addr' GROUP BY UPPER(value) 
                    ORDER BY num DESC LIMIT 30 ;''',
                    '''SELECT value FROM ways_tags ;''',
                    '''SELECT value FROM ways_tags WHERE value='Airport Road' ;''',
                    '''SELECT id, key, value, type FROM ways_tags WHERE value='Airport Road' ;''',
                    '''SELECT id, node_id, position FROM ways_nodes WHERE id='259070783' ;''',
                    '''SELECT id, key, value, type FROM nodes_tags WHERE key = 'County' ;'''
                    )
                    
    for query in queries_list:
        print "\nFor query: ", query, "\nOutput is:"
        cur.execute(query)
        # Printing with panda dataframe
        names = [description[0] for description in cur.description]
        #print "\ncur.description: ", cur.description
        rows = cur.fetchall()
        print "\nNumber of rows: ", len(rows)
        if len(rows) == 0:
            print "\nThere are no records found.\n"
        else:
            df = pd.DataFrame(rows)
            df.columns = names
            print df               

def complexAirportQueries():
    print "\nMore complex Airport Road queries and subqueries."
    print "\nI want to know how many entries are there for 'Airport Road' in nodes_tags that have a reference in ways_nodes; and what are they."
    queries_list = (
                    '''SELECT sq1.id FROM 
                    (SELECT id, key, value, type FROM ways_tags WHERE key = 'street' AND value='Airport Road') sq1 ;''',
                    '''SELECT ways_nodes.id, node_id, position FROM ways_nodes, 
                    (SELECT id, key, value, type FROM ways_tags WHERE key = 'street' AND value='Airport Road') sq1 
                    WHERE ways_nodes.id=sq1.id ;''',
                    '''SELECT ways_tags.id, ways_tags.type, ways_tags.key, ways_tags.value, 
                    ways_nodes.node_id, ways_nodes.position, 
                    nodes_tags.key, nodes_tags.value 
                    FROM (ways_tags JOIN ways_nodes ON ways_tags.id = ways_nodes.id) AS w_id
                    JOIN nodes_tags ON ways_nodes.node_id = nodes_tags.id 
                    GROUP BY ways_tags.key AND ways_tags.value 
                    ;''',
                    '''SELECT ways_tags.id, ways_tags.type, ways_tags.key, ways_tags.value, 
                    ways_nodes.node_id, ways_nodes.position, 
                    nodes_tags.key, nodes_tags.value 
                    FROM (ways_tags JOIN ways_nodes ON ways_tags.id = ways_nodes.id)  
                    JOIN nodes_tags ON ways_nodes.node_id = nodes_tags.id 
                    GROUP BY ways_tags.key AND ways_tags.value 
                    ;''',
                    '''SELECT ways_tags.id, ways_tags.type, ways_tags.key, ways_tags.value, 
                    ways_nodes.node_id as node_id, ways_nodes.position as position, 
                    nodes_tags.key as ntags_key, nodes_tags.value as ntags_value
                    FROM ways_tags JOIN ways_nodes JOIN nodes_tags 
                    ON ways_tags.id = ways_nodes.id AND ways_nodes.node_id = nodes_tags.id ;''',
                    '''SELECT ways_tags.id, ways_tags.type, ways_tags.key, ways_tags.value, count(ways_tags.value) AS wtv_count,
                    ways_nodes.node_id as node_id, ways_nodes.position as position, 
                    nodes_tags.key as ntags_key, nodes_tags.value as ntags_value
                    FROM ways_tags JOIN ways_nodes JOIN nodes_tags 
                    ON ways_tags.id = ways_nodes.id AND ways_nodes.node_id = nodes_tags.id 
                    GROUP BY ways_tags.value
                    ORDER BY wtv_count DESC;''',
                    '''SELECT key, id, value FROM nodes_tags 
                    JOIN (SELECT DISTINCT(node_id)
                    FROM ways_nodes
                    JOIN (SELECT DISTINCT(id)
                    FROM ways_tags
                    WHERE value = {0}) as subq
                    ON ways_nodes.id = subq.id) as subq1
                    ON nodes_tags.id = subq1.node_id;'''.format("'Airport Road'"),
                    '''SELECT key, id, value, COUNT(value) FROM nodes_tags 
                    JOIN (SELECT DISTINCT(node_id)
                    FROM ways_nodes 
                    JOIN (select DISTINCT(id) FROM ways_tags WHERE value = {0}) as subq
                    ON ways_nodes.id = subq.id) as subq1
                    ON nodes_tags.id = subq1.node_id
                    GROUP BY value;'''.format("'Airport Road'"),
                    '''SELECT * FROM nodes WHERE id = '2643985680' ;''',
                    '''SELECT * FROM nodes_tags WHERE id = '2643985680' ;'''
                    )
                    
    for query in queries_list:
        print "\nFor query: ", query, "\nOutput is:"
        cur.execute(query)
        # Printing with panda dataframe
        names = [description[0] for description in cur.description]
        #print "\ncur.description: ", cur.description
        rows = cur.fetchall()
        print "\nNumber of rows: ", len(rows)
        if len(rows) == 0:
            print "\nThere are no records found.\n"
        else:
            df = pd.DataFrame(rows)
            df.columns = names
            print df

def airportCountiesQueries():
    print "\nQueries to find statistics on which Counties Airport Road goes through."
    queries_list = (['''SELECT id, key, value, type FROM ways_tags WHERE ((key='name' OR key='street') 
    AND value='Airport Road') and key='county';''',
    '''SELECT id, key, value, type, COUNT(value) FROM ways_tags WHERE key = 'highway' GROUP BY (key) ;''',
     '''SELECT id, key, value, type, COUNT(value) AS wt_value FROM ways_tags GROUP BY (key) ORDER BY wt_value DESC;''',
     '''SELECT id, key, value, type, COUNT(value) AS wt_value FROM ways_tags WHERE key = 'highway' GROUP BY (key) 
     ORDER BY wt_value DESC;''',
     '''SELECT id, key, value, type FROM ways_tags 
                     WHERE key = 'county' ;''',
                     '''SELECT id, key, value, type FROM ways_tags 
                     WHERE (key = 'name' AND value = 'Airport Road') and key = 'county' ;''',
                     '''SELECT id, key, value, type FROM ways_tags 
                     WHERE value = 'Airport Road' ;''',
                     '''SELECT ways_tags.id, ways_tags.key, ways_tags.value, ways_tags.type, sq1.id, sq1.key, sq1.value, sq1.type
                     FROM ways_tags JOIN (SELECT id, key, value, type FROM ways_tags 
                     WHERE value = 'Airport Road') as sq1 ON ways_tags.id = sq1.id WHERE ways_tags.key = 'county' ;''',
                     '''SELECT ways_tags.id, ways_tags.key, ways_tags.value, sq1.id, sq1.value, COUNT('ways_tags.value') as num
                     FROM ways_tags JOIN (SELECT id, key, value FROM ways_tags 
                     WHERE value = 'Airport Road') as sq1 ON ways_tags.id = sq1.id WHERE ways_tags.key = 'county' 
                     GROUP BY (ways_tags.value) ;'''
                    ])
    for query in queries_list:
        print "\nFor query: ", query, "\nOutput is:"
        cur.execute(query)
        # Printing with panda dataframe
        names = [description[0] for description in cur.description]
        rows = cur.fetchall()
        print "\nNumber of rows: ", len(rows)
        if len(rows) == 0:
            print "\nThere are no records found.\n"
        else:
            df = pd.DataFrame(rows)
            df.columns = names
            print df


intro()
conn.close()
