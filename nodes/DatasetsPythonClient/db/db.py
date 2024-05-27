from sqlalchemy import create_engine
import os

DB_USERNAME = os.environ.get('DB_USERNAME')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_HOSTNAME = os.environ.get('DB_HOSTNAME')
DB_NAME = os.environ.get('DB_NAME')

engine = create_engine('postgresql+psycopg2://{}:{}@{}/{}'
                       .format(DB_USERNAME, DB_PASSWORD, DB_HOSTNAME, DB_NAME))