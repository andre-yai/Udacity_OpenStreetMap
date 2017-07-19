


'''
Library
'''
import csv
import codecs
import pprint
import re
import xml.etree.cElementTree as ET
import cerberus
import schema


LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

# Make sure the fields order in the csvs matches the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']


def parser(file):
	context = {"nodes":[],"ways":[]};
	for element in get_element(file, tags=('node', 'way')):
            el = shape_element(element)
            if(element.tag == 'node'):
            	context["nodes"].append(el);
            elif element.tag == 'way':
            	context["ways"].append(el);
	return context;

def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()

def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_type='regular'):
    """Clean and shape node or way XML element to Python dict"""

    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []  # Handle secondary tags the same way for both node and way elements

    # YOUR CODE HERE
    if element.tag == 'node':

        node_attribs = associateElementFields(element,NODE_FIELDS);
        tags = getTags(element,NODE_TAGS_FIELDS,node_attribs['id']);
        return {'node': node_attribs, 'node_tags': tags}

    elif element.tag == 'way':
        way_attribs = associateElementFields(element,WAY_FIELDS);
        way_nodes = getWayNodes(element,WAY_NODES_FIELDS,way_attribs['id']);
        tags = getTags(element,WAY_TAGS_FIELDS,way_attribs['id']);

        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}

def getWayNodes(element,FIELDS, id):
  way_nodes = [];
  found = 0;
  for node in element.iter("nd"):
    node_attribs = {};
    for field in FIELDS:
      if(field == "id"):
        node_attribs[field] = id;
      elif(field == "node_id"):
        node_attribs[field] = node.attrib["ref"]
      elif(field == "position"):
        node_attribs[field] = found;
        found += 1;
    way_nodes.append(node_attribs);

  return way_nodes;

def getTags(element,FIELDS, id):
  tags = [];
  for tag in element.iter("tag"):
    tag_attribs = {};
    key_type = getKeytype(tag);
    k_value =  tag.attrib['k'];
    if(key_type != "problemchars"):
      if(key_type == "lower_colon"):
            part_initial = k_value.split(':',1)[0]
            part_final = k_value.split(':',1)[1]
      else:
          part_initial = "regular"
          part_final = k_value
      tag_attribs = {'id':id,'value':tag.attrib['v'],'type': part_initial,'key': part_final};
    tags.append(tag_attribs);

  return tags;

def getKeytype(element):
      k_value =  element.attrib['k']
      if LOWER_COLON.search(k_value):
          return "lower_colon"
      elif PROBLEMCHARS.search(k_value):
          return "problemchars"
      return "normal";

def associateElementFields(element,Fields):
  attribs = {};
  for field in Fields:
          attribs[field] = element.attrib[field];
  return attribs;





