import sys
sys.path.append('../')
import models.product
import database as db

Product = models.product.Product

class ProductController(object):

    def __init__(self):
        try:
            self.cursor = db.getCursor()
            if self.cursor is None: raise Exception('No connection. Please, check your config.json or Postgre server')
        except Exception as err:
            print("Connection error! ", err)

    def getAll(self, page: int, per_page: int):
        items = [Product]
        page -= 1
        self.cursor.execute(f'SELECT {Product().getKeys()} FROM "Product" LIMIT {per_page} OFFSET {page * per_page}')
        records = self.cursor.fetchall()
        for record in records:
            tmpItem = Product()
            tmpItem.parse(record)
            print(tmpItem.getValues())
            items.append(tmpItem)

        import copy
        return copy.deepcopy(items)

test = ProductController()
products = test.getAll(1, 10)

print( products[0].name)
for product in products:
    print(product.name)