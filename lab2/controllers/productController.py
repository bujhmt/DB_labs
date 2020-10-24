import sys
sys.path.append('../')
import models.product
import database as db

Product = models.product.Product

class ProductController(object):

    def __init__(self):
        try:
            self.conn = db.getConn()
            self.cursor = self.conn.cursor()
            if self.cursor is None: raise Exception('No connection. Please, check your config.json or Postgre server')
        except Exception as err:
            print("Connection error! ", err)

    def getAll(self, page: int, per_page: int):
        items = []
        try:
            page -= 1
            self.cursor.execute(f'SELECT {Product().getKeys()} FROM "Product" LIMIT {per_page} OFFSET {page * per_page}')
            records = self.cursor.fetchall()
            for record in records:
                tmpItem = Product()
                tmpItem.parse(record)
                items.append(tmpItem)
        except Exception as err:
            print("Get error! ", err)
        return items

    def add(self, *args):
        try:
            newEntity: Product = Product()
            if len(args) > 0 and isinstance(args[0], Product):
                newEntity = args[0]
            else: newEntity.fill()

            if newEntity.isFull():
                print(f'INSERT INTO "Product" ({newEntity.getKeys()}) VALUES ({newEntity.getValues()}) RETURNING id')
                self.cursor.execute(f'INSERT INTO db_labs.public."Product" ({newEntity.getKeys()}) '
                                    f'VALUES ({newEntity.getValues()}) RETURNING id')
                self.conn.commit()
                return int(self.cursor.fetchone()[0])
        except Exception as err:
            print("Add error! ", err)
        return False

    def getById(self, productId):
        product = Product()
        try:
            if isinstance(productId, int): productId = str(productId)
            if not isinstance(productId, str): raise Exception('Incorrect arguments')
            self.cursor.execute(f'SELECT {product.getKeys()} from "Product" WHERE id = {productId}')
            record = self.cursor.fetchone()
            if record is not None: product.parse(record)
            else: raise Exception(f'No entry with ID {productId} found')
        except Exception as err:
            print("Get by id error! ", err)
        return product

    def delete(self, productId):
        try:
            if isinstance(productId, int): productId = str(productId)
            if not isinstance(productId, str): raise Exception('Incorrect arguments')
            product = self.getById(productId)
            self.cursor.execute(f'DELETE from "Product" WHERE id = {productId}')
            self.conn.commit()
            return product
        except Exception as err:
            print("Delete error! ", err)
            return False

    def update(self, product: Product):
        try:
            queryStr = ''
            keys = product.getKeys().split(',')
            values = product.getValues().split(',')
            for i in range(len(keys)):
                queryStr += keys[i] + ' = ' + values[i] + ', '
            self.cursor.execute(f'Update "Product" Set {queryStr[:-2]} Where id = {product.id}')
            self.conn.commit()
            return True
        except Exception as err:
            print("Update error! ", err)
            return False
