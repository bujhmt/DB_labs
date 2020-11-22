from sqlalchemy import Column, Integer, String, Date, func
from sqlalchemy.orm import relationship
from models.links import links_orders_association
from db import Base

class Client(Base):
    __tablename__ = 'Client'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    birthday_date = Column(Date, default=func.now())
    email = Column(String)

    Orders = relationship("Order", secondary=links_orders_association)

    def __repr__(self):
      return "<Client(name='%s', birthday_date='%s', email='%s')>" % \
             (self.name, self.birthday_date, self.email)

    def __init__(self, name: str, birthday_date: str, email: str):
        self.name = name
        self.birthday_date = birthday_date
        self.email = email

