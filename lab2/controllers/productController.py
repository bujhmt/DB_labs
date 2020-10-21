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
        items = []
        page -= 1
        self.cursor.execute(f'SELECT {Product().getKeys()} FROM "Product" LIMIT {per_page} OFFSET {page * per_page}')
        records = self.cursor.fetchall()
        for record in records:
            tmpItem = Product()
            tmpItem.parse(record)
            items.append(tmpItem)

        return items

    def add(self, *args):
        try:
            newEntity: Product = Product()
            if len(args) > 0 and isinstance(args[0], Product):
                newEntity = args[0]
            else:
                newEntity.fill()

            if newEntity.isFull():
                print(f'INSERT INTO "Product" ({newEntity.getKeys()}) VALUES ({newEntity.getValues()}) RETURNING id')
                self.cursor.execute(f'INSERT INTO db_labs.public."Product" ({newEntity.getKeys()}) '
                                    f'VALUES ({newEntity.getValues()}) RETURNING id')
                return int(self.cursor.fetchone()[0])
        except Exception as err:
            print("Add error! ", err)
        return False


test = ProductController()
products = test.getAll(1, 10)

pr = Product()
pr.name = "'igor'"
pr.cost = 200
pr.manufacturer = "'frnl'"
pr.manufacture_date = "'2002-03-04'"
pr.category = 1
print(test.add(pr))