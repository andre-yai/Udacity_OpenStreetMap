

import csv
import codecs
import pprint
import re
import xml.etree.cElementTree as ET

import cerberus

import schema


DIR_TO = './../csvs/'
NODES_PATH = DIR_TO + "nodes.csv"
NODE_TAGS_PATH = DIR_TO + "nodes_tags.csv"
WAYS_PATH = DIR_TO + "ways.csv"
WAY_NODES_PATH = DIR_TO + "ways_nodes.csv"
WAY_TAGS_PATH = DIR_TO + "ways_tags.csv"

NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']

# ================================================== #
#               Helper Functions                     #
# ================================================== #

class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in row.iteritems()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

def process_map(context):
    """Iteratively process each XML element and write to csv(s)"""

    with codecs.open(NODES_PATH, 'w') as nodes_file, \
         codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file, \
         codecs.open(WAYS_PATH, 'w') as ways_file, \
         codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file, \
         codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:

      if(len(context["nodes"]) > 0):

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        
        nodes_writer.writeheader()
        node_tags_writer.writeheader()

        for node in context["nodes"]:
          nodes_writer.writerow(node["node"])
          node_tags_writer.writerows(node['node_tags'])
      
      if(len(context["ways"]) > 0):
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        for way in context["ways"]:
          ways_writer.writerow(way['way'])
          way_nodes_writer.writerows(way['way_nodes'])
          way_tags_writer.writerows(way['way_tags'])
