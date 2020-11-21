from sqlalchemy import Column, Integer, String, Date, func, ForeignKey
from sqlalchemy.orm import relationship, backref
from db import Base

class Product(Base):
    __tablename__ = 'Product'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    brand = Column(String)
    manufacturer = Column(String)
    manufacture_date = Column(Date, default=func.now())
    category_id = Column(Integer, ForeignKey('Category.id'))
    order_id = Column(Integer, ForeignKey('Order.id'))
    Order = relationship("Order", backref=backref("Product", uselist=False))
    Category = relationship("Category", backref=backref("Product", uselist=False))

    def __repr__(self):
      return "<Category(name='%s'," \
             " brand='%s'," \
             " manufacturer='%s'," \
             " manufacture_date='%s'," \
             " category_id='%i'," \
             " order_id='%i')>" % \
             (self.name,
              self.brand,
              self.manufacturer,
              self.manufacture_date,
              self.category_id,
              self.order_id)

    def __init__(self,
                 name: str,
                 brand: str,
                 manufacturer: str,
                 manufacture_date: str,
                 category_id: int,
                 order_id: int):
        self.name = name
        self.brand = brand
        self.manufacturer = manufacturer
        self.manufacture_date = manufacture_date
        self.category_id = category_id
        self.order_id = order_id
