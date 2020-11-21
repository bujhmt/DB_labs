from sqlalchemy import Column, Integer, String
from db import Base

class Category(Base):
    __tablename__ = 'Category'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)

    def __repr__(self):
      return "<Category(name='%s', type='%s')>" % \
             (self.name, self.type)

    def __init__(self, name: str, type: str):
        self.name = name
        self.type = type


