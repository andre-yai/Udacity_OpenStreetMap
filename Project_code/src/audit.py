# coding=utf-8

import re
from collections import defaultdict
from operator import itemgetter

import city_audit


def audit_tags(tags):
	tag_attrib = {};
	
	for tag in tags:
		if(("key" in tag) and ("value" in tag)):
			tag_attrib[tag["key"]] = tag["value"]
		else:
			print("ERRO:",tag);

	tag = city_audit.audit_street(tag_attrib)
	city_audit.audit_postcode(tag_attrib);

	for tag in tags:
		if(("key" in tag) and ("value" in tag)):
			tag["value"] = tag_attrib[tag["key"]]

	return tags;

def audit_nodes(nodes):
	dic = {};
	for node in nodes:
		if(node["node_tags"]):
			node_tags = audit_tags(node["node_tags"]);
			node["node_tags"] = node_tags;
	return nodes;


def audit_ways(ways):
	dic = {};
	for way in ways:
		if(way["way_tags"]):
			way_tags = audit_tags(way["way_tags"]);
			way["way_tags"] = way_tags;

	return ways;	

