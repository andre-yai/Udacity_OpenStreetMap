# coding=utf-8

import re
from collections import defaultdict
from operator import itemgetter
import city_audit


def audit_tags(tags,expected_types,mapping_to_expected,postcode_method):
	"""
		This function will evaluate tags. 
		It receives as parameters the specifications of the city paramenters a
		nd returns if it is suatble or not and the result tag. 
	"""
	tag_attrib = {}
	isValid = True

	for tag in tags:
		if(("key" in tag) and ("value" in tag)):
			tag_attrib[tag["key"]] = tag["value"]
		else:
			print("ERRO:",tag);
			is_valid = False

	is_valid,tag = city_audit.audit_street(tag_attrib,expected_types,mapping_to_expected)
	is_valid = city_audit.audit_postcode(tag_attrib,postcode_method);

	for tag in tags:
		if(("key" in tag) and ("value" in tag)):
			tag["value"] = tag_attrib[tag["key"]]

	return is_valid,tags

def audit_data_sao_paulo_city(tags):
	"""
		This function will call other methods to evaluate the tags for Sao Paulo  
	"""
	expected_types = ["Praca","Pateo",'Vale','Largo','Vila','Viaduto','Parque',"Rua", "Avenida", "Rodovia", "Marginal","Alameda","Travessa","Estrada","Viela"]
	mapping_to_expected = { "Av": "Avenida", "av": "Avenida","praca": "Praca", "R.":"Rua", "Av": "Avenida","Al": "Alameda","rua": "Rua","R": "Rua","RUA": "Rua","avenida":"Avenida","estrada":"Estrada","rUa": "Rua","Rue": "Rua"}

	is_valid, tags = audit_tags(tags,expected_types,mapping_to_expected,is_saopaulo_postcode)

	return is_valid, tags

def is_saopaulo_postcode(postcode_text):
	"""
		This function will evaluate if it is a valid postcode for Sao Paulo.
		Reference for postcodes valid in Sao Paulo:  https://thiagorodrigo.com.br/artigo/cep-sao-paulo-lista-de-cep-por-bairro-e-cidade-da-grande-sao-paulo/
	"""

	if(not (postcode_text[0:4] < "0600" or (postcode_text[0:4] > "0800" and postcode_text[0:4] < "0850"))):
		return True
	return False
