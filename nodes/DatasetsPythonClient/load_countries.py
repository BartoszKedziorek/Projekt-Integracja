from utils import parseXML
from models.Country import Country
from sqlalchemy.orm import Session, sessionmaker
from db.db import engine
import os

files = [
    os.getcwd() + '/data/internet.csv',
    os.getcwd() + '/data/population.xml',
    os.getcwd() + '/data/unemployment.xml'
]

countries_dict = {}

for file in files:
    input_file = open(file, 'r')
    ext = file.split('.')[-1]
    if ext == 'csv':

        rows = input_file.readlines()
        for row in rows:
            row_tab = row.split(',')
            country_name, country_code = row_tab[1], row_tab[2]
            countries_dict[country_code] = country_name
    input_file.close()

session = Session(engine)
with session.begin():
    for ct_code, ct_name in countries_dict.items():
        country = Country(name=ct_name, code=ct_code)
        session.add(country)

    
    

