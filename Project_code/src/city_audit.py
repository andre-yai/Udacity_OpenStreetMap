# coding=utf-8

import re
from collections import defaultdict
from unicodedata import normalize

street_type_re = re.compile(r'^([\w\-]+)', re.IGNORECASE)

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

expected = ["Praca","Pateo",'Vale','Largo','Vila','Viaduto','Parque',"Rua", "Avenida", "Rodovia", "Marginal","Alameda","Travessa","Estrada","Viela"]

mapping = { "Av": "Avenida",
            "av": "Avenida",
            "praca": "Praca",
            "R.":"Rua",
            "Av": "Avenida",
            "Al": "Alameda",
            "rua": "Rua",
            "R": "Rua",
            "RUA": "Rua",
            "avenida":"Avenida",
            "estrada":"Estrada",
            "rUa": "Rua",
            "Rue": "Rua"
            }

def remover_acentos(txt, codif='utf-8'):

    return normalize('NFKD', txt.decode(codif)).encode('ASCII','ignore')

def audit_street(tag):

    # YOUR CODE HERE
    if("street" in tag):
	    name = remover_acentos( u''.join(tag["street"]).encode('utf-8'));
	    m = street_type_re.search(name)
	    if m:
	        street_type = m.group()
	        if ((street_type not in expected) and (street_type in mapping)):
                #update Name:

                print(name, " => " mapping[street_type] + name[(len(street_type)):])
	            name = mapping[street_type] + name[(len(street_type)):]
	       
            else:
                if ((street_type not in expected) and (street_type not in mapping)):
	        	  print("Type not included:", street_type,"=>", name);

	    tag["street"] = name;    
    return tag;

PostCodes = {};
# https://thiagorodrigo.com.br/artigo/cep-sao-paulo-lista-de-cep-por-bairro-e-cidade-da-grande-sao-paulo/
def audit_postcode(tag):
	if("postcode" in tag):
		value = tag["postcode"];
		if(not (value[0:4] < "0600" or (value[0:4] > "0800" and value[0:4] < "0850"))):
			print("WRONG POSTCODES tag:",tag);
	return;


