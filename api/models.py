from sqlalchemy import Column, Integer, String
from api.database import Base

class Hero(Base):
    __tablename__ = "heroes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    power = Column(String, nullable=False)
