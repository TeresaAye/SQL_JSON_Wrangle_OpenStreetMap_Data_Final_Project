# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 18:00:50 2017

@author: TA2761
this one is ready for use in my main code
"""
# audit.py
import xml.etree.cElementTree as ET
from collections import defaultdict
import re

# To print filename and path:
import inspect
print inspect.getfile(inspect.currentframe()) # script filename (usually with path) 

osmfile = 'sample_100.osm'
#osmfile = 'nashville_tennessee.osm' too big for submission

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

from myDictionaries import  not_found_mapping, type_mapping, expected

'''
expected = ["Alley", "Avenue", "Boulevard", "Broadway", "Bypass", "Center", "Circle", "Commons", "Court", "Cove", \
            "Drive", "Fork", "Glen", "Heights", "Highway", "Hills", "Hollow", "Landing", "Lane", "North", \
            "Park", "Parkway", "Pass", \
            "Pike", "Place", \
            "Plaza", "Road", "Square", \
            "Street", "Terrace", "Trace", 
            "Trail", "Way"]

type_mapping = { "A": "Avenue", # not a good idea. Replaces any capital A But I added boundaries so this would not be a problem - same for others
            "ave": "Avenue",
            "Ave": "Avenue",
            "avenue": "Avenue",
            "AVENUE": "Avenue",
            "B": "Boulevard", 
            "Blvd": "Boulevard",
            "BLVD": "Boulevard",
            "Cir": "Circle",
            "Crt": "Court",
            "Ct": "Court",
            "Dr": "Drive",
            "hills": "Hills",
            "Hwy": "Highway",
            "Hwy.": "Highway",
            "Ln": "Lane",
            "pike": "Pike",
            "Pk": "Park",
            "Pkwy": "Parkway",
            "Pky": "Parkway",
            "Pl": "Place",
            "Rd": "Road",
            "Rd.": "Road",
            "S": "South", 
            "st": "Street",
            "St": "Street",
            "St.": "Street",
            }

not_found_mapping = {
        "1705": "",
        "1800": "",
        "37076,": "",
        "Ave": "Avenue",
        "Ave,": "Avenue",
        "B": "Boulevard",
        "Blvd": "Boulevard",
        "E": "East",
        "Dr": "Drive",
        "Hermitage,": "",
        "Hwy": "Highway",
        "Ln": "Lane",
        "N": "North",
        "Parkway,": "Parkway",
        "Pike,": "Pike",
        "S": "South",
        "S.": "South",
        "st.": "Street",
        "St.": "Street",
        "States": "State",
        "Ste": "Suite",
        "TN": "",
        "TN-76": "State Highway 76",
        "W": "West",
        "USA": "",
        }
'''

def audit_street_type(street_types_expected, street_types_to_clean, street_types_not_found, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type in expected:
            street_types_expected[street_type].add(street_name)
        elif street_type not in expected:
            if street_type not in type_mapping:
                street_types_not_found[street_type].add(street_name)
            else:
                street_types_to_clean[street_type].add(street_name)

def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types_expected = defaultdict(set)
    street_types_to_clean = defaultdict(set)
    street_types_not_found = defaultdict(set) 
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types_expected, street_types_to_clean, street_types_not_found, tag.attrib['v'])
    osm_file.close()
    print "street_types_expected: ", street_types_expected # New
    return street_types_expected, street_types_to_clean, street_types_not_found



