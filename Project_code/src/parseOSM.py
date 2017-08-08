
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
import audit

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


def parser_audit(file,audit_Method):

  """
  This function will parse the given file looking for node and way. And returns a map with nodes and ways.
  >> parse('example.osm')
  {"Nodes": [], "Maps": []}
  
  Params: 
    file: input file

  Output: map contaning a list of nodes and ways in file.
  """

  context = {"nodes":[],"ways":[]}
	
  for element in get_element(file, tags=('node', 'way')):
           
    is_valid = False

    if(element.tag == 'node'):
      is_valid, context_audited = parse_audit_node(element,audit_Method)
    elif (element.tag == 'way'):
      is_valid, context_audited = parse_audit_way(element,audit_Method)

    if is_valid == True:
      context[element.tag+"s"].append(context_audited)

  return context

def get_element(osm_file, tags=('node', 'way')):

    """ 
    This function will iterate through a field looking for ceartain tags. 
    Then it Yield element if it is the right type of tag.
    """

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


def parse_audit_node(element,audit_Method):
  
  """
    This function fill take the text element and process it content as node. And then we will audit the element.
    And as a result it will return a bool that indicate if is sutable to include in our db and a mapt with it content
  """

  node_attribs = {}
  tags = [] 

  tags_fields =  ['id', 'key', 'value', 'type'] 
  node_attr_fields = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
  
  node_attribs = associateElementFields(element,node_attr_fields)
  tags = getTags(element,tags_fields,node_attribs['id'])
  # audit element
  is_valid,tags = audit_Method(tags)

  return is_valid,{'node': node_attribs, 'node_tags': tags}


def parse_audit_way(element,audit_Method):
    """
    This function fill take the text element and process it content as way And then we will audit the element.
    And as a result it will return a bool that indicate if is sutable to include in our db and a mapt with it content
    """

    way_attribs = {}
    way_nodes = []
    tags = [] 

    tags_fields =  ['id', 'key', 'value', 'type']  
    way_attr_fields = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
    way_nodes_fields = ['id', 'node_id', 'position']
    
    way_attribs = associateElementFields(element,way_attr_fields)
    way_nodes = getWayNodes(element,way_nodes_fields,way_attribs['id'])
    tags = getTags(element,tags_fields,way_attribs['id'])
    include = True
    # audit element
    is_valid,tags = audit_Method(tags)

    return include,{'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}

def getWayNodes(element,way_nodes_fields, way_id):
  """
  This function recieves the context of way, a list of fields of way nodes and the way_id.
  And it will return a dic containing the information about the way nodes fields.
  """

  way_nodes = []
  found = 0
  for node in element.iter("nd"):
    node_attribs = {}
    for field in way_nodes_fields:

      if(field == "id"):
        node_attribs[field] = way_id

      elif(field == "node_id"):
        node_attribs[field] = node.attrib["ref"]

      elif(field == "position"):
        node_attribs[field] = found;
        found += 1;

    way_nodes.append(node_attribs);

  return way_nodes;

def getTags(element,FIELDS, parent_id):

  """
    This function recieves the context of way or node, a list of fields of tags and the parent id (that is the way_id or node_id).
    It will parse the key to see it type if it does not have problem chars it will proceed gathering the information.
    And it will return a dic containing the information about the way/nodes tags fields.
  """

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
      tag_attribs = {'id':parent_id,'value':tag.attrib['v'],'type': part_initial,'key': part_final};
    tags.append(tag_attribs);

  return tags;

def getKeytype(element):
    
  """
  It will analyse the key and return it type according to regex. 
  """

  k_value = element.attrib['k']
  
  if LOWER_COLON.search(k_value):
      return "lower_colon"
  
  elif PROBLEMCHARS.search(k_value):
      return "problemchars"
  
  return "normal";

def associateElementFields(element,Fields):
  
  """
  This will simply associate the element content with the fields and return a diccitinary as a result.
  """

  attribs = {};
  
  for field in Fields:
          attribs[field] = element.attrib[field];
  return attribs;

