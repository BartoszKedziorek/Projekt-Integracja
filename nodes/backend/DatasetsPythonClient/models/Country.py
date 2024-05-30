from .Base import Base
from sqlalchemy.orm import Mapped
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column

    
class Country(Base):
    __tablename__ = 'country'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    code: Mapped[str] = mapped_column(String(4), unique=True, nullable=False)