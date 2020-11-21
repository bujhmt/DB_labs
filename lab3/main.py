from db import Base, session, engine

from models.client import Client
from models.order import Order
from models.category import Category
from models.product import Product

def recreate_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

if __name__ == '__main__':

    product = Product('test',
                      'some',
                      'Windows',
                      '2002-04-05',
                      1, 1)

    session.add(product)
    session.commit()
    session.flush()
    print(product.id)



session.close()