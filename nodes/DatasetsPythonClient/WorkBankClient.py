from WebClient import WebClient
import requests
import zipfile
import shutil
import os
from utils import extract_one_file_zip


class WorkBankClient(WebClient):
    
    def getSource(self, url: str, dest_dir: str):
        resp = requests.get(url)
        if resp.status_code != 200:
            raise Exception("Failed to download requested file")
        try:
            ext = dest_dir.split('.')[-1]
            zip_dir = dest_dir.replace(ext, 'zip') 
            open(zip_dir, 'wb').write(resp.content)
            extract_one_file_zip(zip_dir, dest_dir)
            

        except Exception as e:
            print("Wystąpił błąd podczas zapisywania zasobu")
            raise e
        
