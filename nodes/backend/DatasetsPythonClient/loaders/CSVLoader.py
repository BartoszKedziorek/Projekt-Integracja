from .Loader import Loader
from typing import TextIO
from sqlalchemy.orm import Session
from sqlalchemy import select
from models.Country import Country
from models.Internet import Internet




class CSVLoader(Loader):

    def __init__(self, engine, model_class):
        self.session = Session(engine)
        self.model_class = model_class


    def load(self, file: TextIO):
        lines = file.readlines()
        with self.session.begin():
            for line in lines[1:]:                
                line = line.split(',')
                year, cellularsubscription, internetuserspercent, internetusersnumber, broadbandsubscription \
                = int(line[3]), float(line[4]), float(line[5]), float(line[6]), float(line[7])   
                country_code = line[2]
                country =  stmt = select(Country).where(Country.code == country_code)
                country = self.session.scalars(stmt).first()
                if country is not None:
                    model = Internet(
                        year=year,
                        cellularsubscription=cellularsubscription,
                        internetusersnumber=internetusersnumber,
                        internetuserspercent=internetuserspercent,
                        broadbandsubscription=broadbandsubscription,
                        country_id=country.id
                    )
                    self.session.add(model)
            

    #         id: Mapped[int] = mapped_column(primary_key=True)
    # year: Mapped[int] = mapped_column(Integer(), nullable=False)
    # country_id: Mapped[int] = mapped_column(ForeignKey("country.id"))
    # cellularsubscription: Mapped[float] = mapped_column(Double(), nullable=False)
    # internetuserspercent: Mapped[float] = mapped_column(Double(), nullable=False)
    # internetusersnumber: Mapped[int] = mapped_column(Integer(), nullable=False)
    # broadbandsubscription: Mapped[float] = mapped_column(Double(), nullable=False)
            

            
