import sys
from dotenv import load_dotenv
import os
import json
from models.Unemployment import Unemployment
from models.Population import Population
from models.Internet import Internet
from clientConfig import get_client
from loaders.XMLLoader import XMLLoader
from db.db import engine
from utils import get_model_for_file
from loaders.utils import get_loader_for_file
from sqlalchemy.orm import Session
import sys
from datetime import date

 
def getDataset(host: str, src: str, dest_dir: str) -> bool:
    webClient = get_client(host)
    webClient.getSource(src, dest_dir)


class DatasetsClient():
    def remove_data(self):
        session = Session(engine)
        models = [Internet, Population, Unemployment]
        with session.begin():
            for model in models:
                to_delete = session.query(model).all()
                for my_del in to_delete:
                    session.delete(my_del)
                

    def fetch_data_into_db(self):
        # if not load_dotenv():
        #     print("Błąd podczas wczytywania zmiennych środowiskowych")
        #     exit(-1)
        
        source_entries = None
        try:
            source_entries = json.loads(open(os.environ.get('DATASETS_SOURCE_FILE'), "r").read())
        except Exception as e:
            raise Exception(str(e))
        
        for entry in source_entries:
            fileName = entry['result_file']
            dest_dir = os.environ.get("DEST_DIR", "/") + "/" + fileName
            ext = fileName.split('.')[-1]
            getDataset(entry['host'], entry['src'], dest_dir)
            with open(dest_dir, 'r') as input_file:
                loader_class = get_loader_for_file(fileName) 
                loader = loader_class(engine, get_model_for_file(fileName))
                loader.load(input_file)

if __name__ == '__main__':
    try:
        dsClient = DatasetsClient()
        if len(sys.argv) > 1 and sys.argv[1] == 'refresh':
            dsClient.remove_data()
            today = str(date.today())
            with open(os.environ.get("APPDIR") + "/refresh.log", 'a') as f:
                f.write(today + '\n')
        dsClient.fetch_data_into_db()
    except Exception as e:
        with open(os.environ.get("APPDIR") + "/error.log", 'w') as err:
            err.write(str(e)) 