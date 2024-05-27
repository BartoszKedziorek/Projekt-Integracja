from .XMLLoader import XMLLoader
from .CSVLoader import CSVLoader

def get_loader_for_file(file_name: str):
     ext = file_name.split('.')[-1]
     if ext == 'xml':
          return XMLLoader
     elif ext == 'csv':
          return CSVLoader
     else:
          raise Exception("No loader specified for a given file")
          