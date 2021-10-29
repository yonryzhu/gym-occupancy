from sqlalchemy import Column, DateTime, Float, Integer, SmallInteger

from database import Base


class Record(Base):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, index=True)
    occupancy = Column(SmallInteger)
    remaining = Column(SmallInteger)
    ratio = Column(Float)
