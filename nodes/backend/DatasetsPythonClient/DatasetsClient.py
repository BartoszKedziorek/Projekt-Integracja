import requests
import sys
from dotenv import load_dotenv
import os
import json
from clientConfig import get_client
from loaders.XMLLoader import XMLLoader
from db.db import engine
from utils import get_model_for_file
from loaders.utils import get_loader_for_file


 
def getDataset(host: str, src: str, dest_dir: str) -> bool:
    webClient = get_client(host)
    webClient.getSource(src, dest_dir)


class DatasetsClient():

    def fetch_data_into_db(self):
        if not load_dotenv():
            print("Błąd podczas wczytywania zmiennych środowiskowych")
            exit(-1)
        
        source_entries = None
        try:
            source_entries = json.loads(open("source.json", "r").read())
        except:
            raise Exception("Wystąpił problem podczas pobierania danych o plikach wejściowych")
        
        for entry in source_entries:
            fileName = entry['result_file']
            dest_dir = os.environ.get("DEST_DIR", "/") + "/" + fileName
            ext = fileName.split('.')[-1]
            getDataset(entry['host'], entry['src'], dest_dir)
            with open(dest_dir, 'r') as input_file:
                loader_class = get_loader_for_file(fileName) 
                loader = loader_class(engine, get_model_for_file(fileName))
                loader.load(input_file)    
