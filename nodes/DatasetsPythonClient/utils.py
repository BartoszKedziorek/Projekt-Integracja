import zipfile
import shutil
import os
import xml.etree.ElementTree as ET
from models.Country import Country
from models.Population import Population
from models.Unemployment import Unemployment
from models.Internet import Internet



def extract_one_file_zip(zip_path: str, dest_path: str):
    file_name = dest_path.split('/')[-1]
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(dest_path.replace(file_name, ''))
                shutil.move(dest_path.replace(file_name, '') + zip_ref.filelist[0].filename, dest_path)
                os.remove(zip_path)


def parseXML(xmlfile): 
    tree = ET.parse(xmlfile) 
    root = tree.getroot() 
 
    result_records = [] 
    
    records = root.findall('./data/record')
    for item in records: 
   
        record_fields = {} 

        # iterate child elements of item 
        for child in item:
            match(child.attrib['name']):
                case 'Country or Area':
                    record_fields['coutry_name'] = child.text
                    record_fields['coutry_code'] = child.attrib['key']
                case 'Year':
                    record_fields['year'] = child.text

                case 'Value':
                    record_fields['value'] = child.text
        result_records.append(record_fields)
    return result_records


def get_model_for_file(file_name):
    match file_name:
        case "unemployment.xml":
            return Unemployment
        case "population.xml":
            return Population
        case "internet.csv":
            return Internet
        case _:
            raise Exception("No model secified for a given file")     
