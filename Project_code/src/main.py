
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
import createCSV
import audit

'''
OSM Files
'''
DIR_FROM = './../osms/'
SAOPAULO_OSM_SMALL = DIR_FROM + "saopaulo_small.osm";
SAOPAULO_OSM = DIR_FROM + "sao-paulo_brazil.osm";



def main():

	# it will parse OSM and also audit it fields.
	auditMethod = audit.audit_data_sao_paulo_city
	context = parseOSM.parser_audit(SAOPAULO_OSM,auditMethod)
		
	# Create CSV.
	createCSV.process_map(context);

	return;


if __name__ == '__main__':
	main()