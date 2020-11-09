import sys
import time
sys.path.append('../')
from models.product import Product
from database import db

class ProductController(object):

    def __init__(self):
        try:
            self.db = db()

            if db is None: raise Exception('No connection. Please, check your config.json or Postgre server')

        except Exception as err:
            print("Connection error! ", err)
            exit(1)

    def getAll(self, page: int, per_page: int):
        items = []
        try:
            page -= 1
            self.db.cursor.execute(
                f'SELECT {Product().getKeys()} FROM "Product" ORDER BY id LIMIT {per_page} OFFSET {page * per_page}')
            records = self.db.cursor.fetchall()
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
            else:
                newEntity.fill()

            if newEntity.isFull():
                self.db.cursor.execute(f'INSERT INTO db_labs.public."Product" ({newEntity.getKeys()}) '
                                    f'VALUES ({newEntity.getValues()}) RETURNING id')
                self.db.connect.commit()
                return int(self.db.cursor.fetchone()[0])
        except Exception as err:
            print("Add error! ", err)
        return False

    def getById(self, productId):
        product = Product()
        try:
            if isinstance(productId, int): productId = str(productId)
            if not isinstance(productId, str): raise Exception('Incorrect arguments')
            self.db.cursor.execute(f'SELECT {product.getKeys()} from "Product" WHERE id = {productId}')
            record = self.db.cursor.fetchone()
            if record is not None:
                product.parse(record)
            else:
                raise Exception(f'No entry with ID {productId} found')
        except Exception as err:
            print("Get by id error! ", err)
        return product

    def delete(self, productId):
        try:
            if isinstance(productId, int): productId = str(productId)
            if not isinstance(productId, str): raise Exception('Incorrect arguments')
            product = self.getById(productId)
            self.db.cursor.execute(f'DELETE from "Product" WHERE id = {productId}')
            self.db.connect.commit()
            return product
        except Exception as err:
            print("Delete error! ", err)
            return False

    def update(self, *args):
        try:
            product: Product = Product()
            if len(args) is 0: raise Exception('Invalid arguments')
            if isinstance(args[0], int) or isinstance(int(args[0]), int):
                product.fill()
                product.id = args[0]
                values = product.getValues().split(',')
                old_values = self.getById(args[0]).getValues().split(',')
                keys = product.getKeys().split(',')
                for i in range(len(keys)):
                    if values[i] == 'null':
                        product.__setattr__(keys[i], old_values[i])

            if isinstance(args[0], Product):
                product = args[0]

            if not product.isFull():
                raise Exception('Invalid input')

            queryStr = ''
            keys = product.getKeys().split(',')
            values = product.getValues().split(',')
            for i in range(len(keys)):
                queryStr += keys[i] + ' = ' + values[i] + ', '
            self.db.cursor.execute(f'Update "Product" Set {queryStr[:-2]} Where id = {product.id}')
            self.db.connect.commit()
            return True
        except Exception as err:
            print("Update error! ", err)
            return False

    def getCount(self):
        try:
            self.db.cursor.execute(f'SELECT count(*)  from "Product"')
            return int(self.db.cursor.fetchone()[0])
        except Exception as err:
            print("Get count error! ", err)

    def generateRows(self, entitiesNum: int):
        startTime = time.time()
        try:
            self.db.cursor.execute(f"INSERT  INTO \"Product\" (name,cost,brand,manufacture_date,"
                                   f"manufacturer,category_id, order_id) "
                                   f"SELECT generatestring(15),"
                                   f"generateint(2000)::money,"
                                   f"generatestring(15),"
                                   f"generatedate()::date,"
                                   f"generatestring(15),"
                                   f"getrandomrow('Category')::int,"
                                   f"getrandomrow('Order')::int "
                                   f"FROM generate_series(1, {entitiesNum})")
            self.db.connect.commit()
        except Exception as err:
            print("Generate Rows error! ", err)
            exit(1)
        endTime = time.time()
        return str(endTime - startTime)[:9] + 's'
