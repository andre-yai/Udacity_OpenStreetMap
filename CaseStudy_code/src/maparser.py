import xml.etree.cElementTree as ET
import pprint
import re
from collections import defaultdict

osmfile = './saopaulo_small.osm';

street_type_re = re.compile(r'^([\w\-]+)', re.IGNORECASE)

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

expected = ["Praça","Rúa","Pateo",'Vale','Largo','Vila','Viaduto','Parque',"Rua", "Avenida", "Rodovia", "Marginal","Alameda","Travessa","Estrada","Viela","Pra",]

mapping = { "Av": "Avenida",
            "Al": "Alameda",
            "av": "Avenida",
            "praça": "Praça",
            "R.":"Rua"
            }

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types


def count_tags(filename):
        # YOUR CODE HERE
    tags = {};
    for event,elem in ET.iterparse(filename,events=("start",)):
        if elem.tag in tags:
            tags[elem.tag] += 1;
        else:
            tags[elem.tag] = 1;

    return tags;

def update_name(name, mapping):

    # YOUR CODE HERE
    m = street_type_re.search(name)
    if m:
        street_type = m.group()
        if mapping[street_type]:
            print(street_type, "=>", mapping[street_type]);
            name = name[0:(len(name)-len(street_type))] + mapping[street_type];    
    return name

'''
iter.tag;

'''

def test():

    st_types = audit(osmfile);

    for st_type, ways in st_types.items():
         for name in ways:
             better_name = update_name(name, mapping);
             print("Better name:",better_name);
    print(st_types);

if __name__ == "__main__":
    test()