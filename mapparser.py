#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 17:45:40 2017

@author: TA2761
This one is ready for project
"""
# From DAND P3 Problem Set "case study" quiz "Iterative Parsing"
"""
Your task is to use the iterative parsing to process the map file and
find out not only what tags are there, but also how many, to get the
feeling on how much of which data you can expect to have in the map.
Fill out the count_tags function. It should return a dictionary with the 
tag name as the key and number of times this tag can be encountered in 
the map as value.

I used filename = 'nashville_tennessee.osm' - too big for submission
I had to use 'sample_100.osm'
"""
import xml.etree.cElementTree as ET
import pprint

#filename = 'nashville_tennessee.osm' # Too big for submission
filename = 'sample_100.osm'

def count_tags(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    tagscount = {}
    tagscount[root.tag] = tagscount.get(root.tag, 0) + 1

    for child in root:
        tagscount[child.tag] = tagscount.get(child.tag, 0) + 1
    
        for subchild in child:
            tagscount[subchild.tag] = tagscount.get(subchild.tag, 0) + 1
    
    return(tagscount)


def test():

    tags = count_tags(filename)
    pprint.pprint(tags)
    
test()

'''
this is what is output:
    
runfile('C:/DA/DA P3/DA P3 Project/mapparser.py', wdir='C:/DA/DA P3/DA P3 Project')
{'bounds': 1,
 'member': 16862,
 'nd': 1510808,
 'node': 1325949,
 'osm': 1,
 'relation': 1904,
 'tag': 924006,
 'way': 136702}
'''