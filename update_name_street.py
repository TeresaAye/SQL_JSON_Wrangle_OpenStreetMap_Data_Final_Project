# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 18:00:50 2017

@author: TA2761
this one is ready for use in my main code & cleaned up for the project
"""

import re

# To print filename and path:
import inspect
print inspect.getfile(inspect.currentframe()) # script filename (usually with path) 

from myDictionaries import  not_found_mapping, type_mapping, expected 

#osmfile = 'nashville_tennessee.osm' - too big for submission
osmfile = 'sample_100.osm'

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

def update_name_street(name):
    m = street_type_re.search(name)
    if m:
        boundaries = re.compile(r'\b'+ m.group() + r'\b') # Boundaries allows me to replace B with Blvd, but not Boulevard with Blvdoulevard
        if m.group() in expected:
            name = name.replace('21st Ave Street', '21st Avenue Street') 
            name = name.replace('south Church Street', 'South Church Street') 
            # There are probably many more street names that need cleaning even though the street type is correct. 
            # And there are many more street names that need cleaning even though the street type is being remapped below.
            # And I could use the words code below for that, in fact for all street names, and greatly simplify the update_name function.
            # But I've learned a lot by having 3 dictionaries, so I'm going to keep all 3 for my project submission and document what I've learned.
        else:
            if m.group() not in expected:
                if m.group() not in type_mapping: 
                    name = name.replace('TN 100','State Highway 100')
                    words = [x.strip() for x in name.split()]
                    for w in range(len(words)):
                        if words[w] in not_found_mapping:
                            words[w] = not_found_mapping[words[w]] 
                    name = " ".join(words)
                else: 
                    name = name.replace('2 avenue', '2nd Avenue')
                    name = name.replace('896 N Water Ave', '896 North Water Avenue') 
                    name = name.replace('C1TY AVENUE', 'City Avenue')
                    name = re.sub(boundaries, type_mapping[m.group()], name)
        
    # print "\n from update_name_street.py <name>: ", name # Prints the full street name
    return name 

