from .Base import Base
from sqlalchemy.orm import Mapped
from sqlalchemy import String, Integer, DECIMAL
from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column


class Unemployment(Base):
    __tablename__ = 'unemployment'

    id: Mapped[int] = mapped_column(primary_key=True)
    year: Mapped[int] = mapped_column(Integer(), nullable=False)
    country_id: Mapped[int] = mapped_column(ForeignKey("country.id"))
    
    
    value: Mapped[int] = mapped_column(DECIMAL(6, 3))