from .Base import Base
from sqlalchemy.orm import Mapped
from sqlalchemy import String, Integer, DECIMAL, Double
from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column


class Internet(Base):
    __tablename__ = 'internet'

    id: Mapped[int] = mapped_column(primary_key=True)
    year: Mapped[int] = mapped_column(Integer(), nullable=False)
    country_id: Mapped[int] = mapped_column(ForeignKey("country.id"))
    cellularsubscription: Mapped[float] = mapped_column(Double(), nullable=False)
    internetuserspercent: Mapped[float] = mapped_column(Double(), nullable=False)
    internetusersnumber: Mapped[int] = mapped_column(Integer(), nullable=False)
    broadbandsubscription: Mapped[float] = mapped_column(Double(), nullable=False)
    