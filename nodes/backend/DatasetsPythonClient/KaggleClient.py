from WebClient import WebClient
import requests
import kaggle
import subprocess
import shutil
import os
from utils import extract_one_file_zip


class KaggleClient(WebClient):
    # kaggle datasets download -d ashishraut64/internet-users
    def getSource(self, src: str, dest_dir: str):
        command = ["/opt/venv/bin/kaggle", "datasets", "download", "-d", src]
        try:
            subprocess.run(command, shell=False)
            dataset_name = src.split("/")[1]
            open(dest_dir, 'w')
            extract_one_file_zip("{}/{}.zip".format(os.getcwd(), dataset_name), dest_dir)
        except Exception as e:
            print("Wystąpił problem podczas pobierania datasetu: {src}")
            print(str(e))
            raise e
