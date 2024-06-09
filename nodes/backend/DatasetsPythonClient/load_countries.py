from utils import parseXML
from models.Country import Country
from sqlalchemy.orm import Session, sessionmaker
from db.db import engine
import os
from utils import parseXML
from copy import copy

files = [
    os.environ.get('DEST_DIR') + '/' + 'internet.csv',
    os.environ.get('DEST_DIR') + '/' + 'population.xml',
    os.environ.get('DEST_DIR') + '/' + 'unemployment.xml'
]

countries_dict = {}

def add_country(country_code, country_name):
    #if(country_code not in countries_dict.keys()):
        # jeżeli jakieś państwo ma wiele kodów w plikach
        # to nie bierzemy go pod uwagę
    countries_dict[country_code] = country_name
    # elif countries_dict[country_code] != country_name:
    #     countries_dict[country_code]  = None



def remove_duplicate_coutries():
    # remove coutries who has
    # different codes in input files
    global countries_dict
    count_coutries_dict = {}
    for item in countries_dict.values():
        if item in count_coutries_dict.keys():
            count_coutries_dict[item] += 1
        else:
            count_coutries_dict[item] = 1
    to_delete = [item for item in count_coutries_dict.keys() if count_coutries_dict[item] != 1]

    countries_dict = {key:val for key,val in countries_dict.items() if val not in to_delete} 


for file in files:
    input_file = open(file, 'r')
    ext = file.split('.')[-1]
    if ext == 'csv':
        
        rows = input_file.readlines()
        for row in rows:
            row_tab = row.split(',')
            country_name, country_code = row_tab[1], row_tab[2]
            add_country(country_code, country_name)
    elif ext == 'xml':
        records = parseXML(input_file)
        for record in records:
            country_name, country_code = record['coutry_name'], record['coutry_code']
            add_country(country_code, country_name)
    input_file.close()
    

remove_duplicate_coutries()
session = Session(engine)
with session.begin():
    for ct_code, ct_name in countries_dict.items():
        country = Country(name=ct_name, code=ct_code)
        session.add(country)

    
    

