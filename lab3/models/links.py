from sqlalchemy import Column, Integer, Table, ForeignKey
from  db import Base

links_orders_association = Table(
    'Link_Client-Order', Base.metadata,
    Column('client_id', Integer, ForeignKey('Client.id')),
    Column('order_id', Integer, ForeignKey('Order.id'))
)



