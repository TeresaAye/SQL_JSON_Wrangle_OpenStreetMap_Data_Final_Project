# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 18:04:05 2017

@author: TA2761
cleaned up ready for project
"""

import csv
import codecs
import pprint
import re
import xml.etree.cElementTree as ET
import cerberus
import schema
import update_name_street
import inspect
print inspect.getfile(inspect.currentframe()) # script filename (usually with path) 

osmfile = 'sample_100.osm'
#osmfile = 'nashville_tennessee.osm' too big for submission

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

#OSM_PATH = "nashville_tennessee.osm" # Too big for file submission
OSM_PATH = "sample_100.osm"

NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"

LOWER = re.compile(r'^([a-z]|_)*$')
LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

SCHEMA = schema.schema

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]
POS = ["lat", "lon"]

# Make sure the fields order in the csvs matches the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp'] 
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type'] 
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp'] 
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type'] 
WAY_NODES_FIELDS = ['id', 'node_id', 'position']

id_list = []

def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_type='regular'):
    """Clean and shape node or way XML element to Python dict"""

    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []  # Handle secondary tags the same way for both node and way elements

    if element.tag == 'node':
        # code for 'node' element (the parent)
        id = element.attrib['id']
        for item in node_attr_fields:
            node_attribs[item] = element.attrib[item]
    if element.tag == 'way':
        # code for 'way' element (the parent)
        id = element.attrib['id']
        for item in way_attr_fields:
            way_attribs[item] = element.attrib[item]
        
    pos=0
    for child in element:
        # code for child elements
        
        if child.tag == 'tag':
            # code for 'tag' children
            if child.attrib["k"] == 'addr:street':
                print "\n child.attrib[v] before update", child.attrib["v"] # Prints the full street name
                child.attrib["v"] = update_name_street.update_name_street(child.attrib["v"])
                print "\n child.attrib[v] after update", child.attrib["v"] # Prints the full street name
            if problem_chars.match(child.attrib['k']):
                continue
            else:
                traits = {}
                traits['id'] = id
                traits["value"] = child.attrib["v"]                           
                if ":" in child.attrib["k"]:
                    loc = child.attrib["k"].find(":")
                    key = child.attrib["k"]
                    traits["key"] = key[loc+1:]
                    traits["type"] = key[:loc]
                else:
                    traits["key"] = child.attrib["k"]
                    traits["type"] = "regular"

                if traits["key"] == "street":
                    if False:
                        print "\n traits[key] just before append: ", traits["key"] # the key prints "street"
                        print "\n traits[value] just before append: ", traits["value"] # The value prints the whole street name              
                tags.append(traits)

        if child.tag == 'nd':
            # code for 'nd' children
            way_node = {} 
            way_node["id"] = element.attrib["id"]
            way_node["node_id"] = child.attrib["ref"]
            way_node["position"] = pos
            way_nodes.append(way_node)
            pos=pos+1
    
    if element.tag == 'node':
        return {'node': node_attribs, 'node_tags': tags}
    elif element.tag == 'way':
        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}


# ================================================== #
#               Helper Functions                     #
# ================================================== #
def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()

def validate_element(element, validator, schema=SCHEMA):
    """Raise ValidationError if element does not match schema"""
    if validator.validate(element, schema) is not True:
        field, errors = next(validator.errors.iteritems())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_string = pprint.pformat(errors)
        
        raise Exception(message_string.format(field, error_string))

class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in row.iteritems()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


# ================================================== #
#               Main Function                        #
# ================================================== #
def process_map(file_in, validate):
    """Iteratively process each XML element and write to csv(s)"""

    with codecs.open(NODES_PATH, 'w') as nodes_file, \
         codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file, \
         codecs.open(WAYS_PATH, 'w') as ways_file, \
         codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file, \
         codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        validator = cerberus.Validator()

        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                if validate is True:
                    validate_element(el, validator)

                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])

if __name__ == '__main__':
    # Note: Validation is ~ 10X slower. For the project consider using a small
    # sample of the map when validating.
    # I turned off validation with =False
    process_map(OSM_PATH, validate=False) 
    print "process_map finished - what time were csv files created - take a look - to make sure they are recent"

