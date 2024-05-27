from .Loader import Loader  
from utils import parseXML
from models.Country import Country
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import select

class XMLLoader(Loader):

    def __init__(self, engine, model_class):
        self.session = Session(engine)
        self.model_class = model_class

    def load(self, file):
        records = parseXML(file)
        with self.session.begin(): # start transaction
            for record in records:
                country_code = record['coutry_code']
                stmt = select(Country).where(Country.code == country_code)
                country = self.session.scalars(stmt).first() 
                if country is not None:
                    model = self.model_class(
                        year=record['year'],
                        value=record['value'],
                        country_id=country.id
                    )
                self.session.add(model)
        # commit

