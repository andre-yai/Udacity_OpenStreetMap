# coding=utf-8

import re
from collections import defaultdict
from unicodedata import normalize

street_type_re = re.compile(r'^([\w\-]+)', re.IGNORECASE)

def remove_pontuations(txt, codif='utf-8'):
    
    """
    This function will remove the pontuation of a certain text.
    """

    return normalize('NFKD', txt.decode(codif)).encode('ASCII','ignore')

def audit_street(tag,expected_types, mapping_to_expected):

    """
    This function will evaluate the tag for street looking if it part of the expected list of in the mapping diccionary.
    If it is in the map it will update it value. It will return a status true if it is in mapping diccionary of in expected list
    otherwise it will return false and it also returns the street name. 
    """

    is_valid = True
    if("street" in tag):
        name = remove_pontuations( u''.join(tag["street"]).encode('utf-8'))
        m = street_type_re.search(name)
	    
        if m:
            street_type = m.group()
            if((street_type not in expected_types) and (street_type in mapping_to_expected)):
                name = mapping_to_expected[street_type] + name[(len(street_type)):]
            else:
                if ((street_type not in expected_types) and (street_type not in mapping_to_expected)):
                    is_valid = False
                    print("Type not included:", street_type,"=>", name)
        tag["street"] = name;    
    
    return is_valid,tag;

def audit_postcode(tag,is_valid_postcode):
    """
    This function will evaluate the tag for postcode. If it is a Sao Paulo  postcode it returns true otherwise false.
    """
    
    is_valid = True
    if("postcode" in tag):
        value = tag["postcode"]
        if(is_valid_postcode(value)):
            print("WRONG POSTCODES tag:",tag)
            is_valid = False
    return is_valid;


