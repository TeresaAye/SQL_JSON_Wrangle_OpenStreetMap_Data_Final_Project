# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 17:52:02 2017

@author: TA2761
ready for project
"""

import xml.etree.cElementTree as ET
import pprint

"""
Your task is to explore the data a bit more.
The first task is a fun one - find out how many unique users
have contributed to the map in this particular area!

The function process_map should return a set of unique user IDs ("uid")
"""

#filename = 'nashville_tennessee.osm' # Too big for file submission
filename = 'sample_100.osm'

def get_user(element):
    return

def process_map(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        tag = element.tag

        if tag in [ 'node', 'way', 'relation']:

            id = element.attrib['uid']
            users.add(id)

    return users


def test():

    users = process_map(filename)
    pprint.pprint(users)

test()
