from sqlalchemy import Column, Integer, Numeric, Date, func
from sqlalchemy.orm import relationship
from models.links import links_orders_association
from  db import Base


class Order(Base):
    __tablename__ = 'Order'

    id = Column(Integer, primary_key=True)
    taxes_sum = Column(Numeric)
    transaction_date = Column(Date, default=func.now())
    Clients = relationship("Client", secondary=links_orders_association)

    def __repr__(self):
      return "<Order(taxes_sum='%i', transaction_date='%s')>" % \
             (self.taxes_sum, self.transaction_date)

    def __init__(self, transaction_date: str, taxes_sum: int):
        self.taxes_sum = taxes_sum
        self.transaction_date = transaction_date

