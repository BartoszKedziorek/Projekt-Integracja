import zipfile
import shutil
import os

def extract_one_file_zip(zip_path: str, dest_path: str):
    file_name = dest_path.split('/')[-1]
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(dest_path.replace(file_name, ''))
                shutil.move(dest_path.replace(file_name, '') + zip_ref.filelist[0].filename, dest_path)
                os.remove(zip_path)