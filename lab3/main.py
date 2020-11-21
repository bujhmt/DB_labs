from db import Base, session, engine
from modelController import EntityController

from models.client import Client
from models.order import Order
from models.category import Category
from models.product import Product

def recreate_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    controller = EntityController(Product)
    product = Product('update_test', 'brand', 'Igor Inc', '2002-04-02', 1, 1)
    product.id = 2
    result = controller.update(product)
    print(result)




session.close()