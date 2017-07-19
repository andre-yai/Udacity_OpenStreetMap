
'''
Libray
'''
import csv
import codecs
import pprint
import re
import xml.etree.cElementTree as ET
import cerberus
import schema

'''
Files
'''
import parseOSM
import audit
import createCSV


'''
OSM Files
'''
DIR_FROM = './../osms/'
OSM_PATH = DIR_FROM + "example.osm"
SAOPAULO_OSM_SMALL = DIR_FROM + "saopaulo_small.osm";
SAOPAULO_OSM = DIR_FROM + "sao-paulo_brazil.osm";



def main():

	# Parse OSM
	context = parseOSM.parser(SAOPAULO_OSM)
	
	#Audit Nodes and Ways Content.

	context["nodes"] = audit.audit_nodes(context["nodes"]);
	context["ways"] = audit.audit_ways(context["ways"]);

	
	# Create CSV.
	createCSV.process_map(context);

	return;


if __name__ == '__main__':
	main()