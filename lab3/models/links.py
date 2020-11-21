from sqlalchemy import Column, Integer, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

links_orders_association = Table(
    'Link_Client-Order', Base.metadata,
    Column('client_id', Integer, ForeignKey('Client.id')),
    Column('order_id', Integer, ForeignKey('Order.id'))
)