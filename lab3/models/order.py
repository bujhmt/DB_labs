from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Numeric, Date, func, ForeignKey
from sqlalchemy.orm import relationship
from models.links import links_orders_association
Base = declarative_base()


class Order(Base):
    __tablename__ = 'Order'

    id = Column(Integer, primary_key=True)
    taxes_sum = Column(Numeric)
    transaction_date = Column(Date, default=func.now())
    clients = relationship("Client", secondary=links_orders_association)

    def __init__(self, transaction_date: str, taxes_sum: int, client_id: int):
        self.taxes_sum = taxes_sum
        self.transaction_date = transaction_date

