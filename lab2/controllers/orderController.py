import sys
import time
sys.path.append('../')
from models.order import Order
from database import db


class OrderController(object):

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
                f'SELECT {Order().getKeys()} FROM "Order" ORDER BY id LIMIT {per_page} OFFSET {page * per_page}')
            records = self.db.cursor.fetchall()
            for record in records:
                tmpItem = Order()
                tmpItem.parse(record)
                items.append(tmpItem)
        except Exception as err:
            print("Get error! ", err)
            exit(1)
        return items

    def add(self, *args):
        try:
            newEntity: Order = Order()
            if len(args) > 0 and isinstance(args[0], Order):
                newEntity = args[0]
            else:
                newEntity.fill()

            if newEntity.isFull():
                self.db.cursor.execute(f'INSERT INTO db_labs.public."Order" ({newEntity.getKeys()}) '
                                    f'VALUES ({newEntity.getValues()}) RETURNING id')
                self.db.connect.commit()
                return int(self.db.cursor.fetchone()[0])
        except Exception as err:
            print("Add error! ", err)
        return False

    def getById(self, orderId):
        order = Order()
        try:
            if isinstance(orderId, int): orderId = str(orderId)
            if not isinstance(orderId, str): raise Exception('Incorrect arguments')
            self.db.cursor.execute(f'SELECT {order.getKeys()} from "Order" WHERE id = {orderId}')
            record = self.db.cursor.fetchone()
            if record is not None:
                order.parse(record)
            else:
                raise Exception(f'No entry with ID {orderId} found')
        except Exception as err:
            print("Get by id error! ", err)
        return order

    def delete(self, orderId):
        try:
            if isinstance(orderId, int): orderId = str(orderId)
            if not isinstance(orderId, str): raise Exception('Incorrect arguments')
            order = self.getById(orderId)
            self.db.cursor.execute(f'DELETE from "Order" WHERE id = {orderId}')
            self.db.connect.commit()
            return order
        except Exception as err:
            print("Delete error! ", err)
            return False

    def update(self, *args):
        try:
            order: Order = Order()
            if len(args) is 0: raise Exception('Invalid arguments')
            if isinstance(args[0], int) or isinstance(int(args[0]), int):
                order.fill()
                order.id = args[0]
                values = order.getValues().split(',')
                old_values = self.getById(args[0]).getValues().split(',')
                keys = order.getKeys().split(',')
                for i in range(len(keys)):
                    if values[i] == 'null':
                        order.__setattr__(keys[i], old_values[i])

            if isinstance(args[0], Order):
                order = args[0]

            if not order.isFull():
                raise Exception('Invalid input')

            queryStr = ''
            keys = order.getKeys().split(',')
            values = order.getValues().split(',')
            for i in range(len(keys)):
                queryStr += keys[i] + ' = ' + values[i] + ', '
            self.db.cursor.execute(f'Update "Order" Set {queryStr[:-2]} Where id = {order.id}')
            self.db.connect.commit()
            return True
        except Exception as err:
            print("Update error! ", err)
            return False

    def getCount(self):
        try:
            self.db.cursor.execute(f'SELECT count(*)  from "Order"')
            return int(self.db.cursor.fetchone()[0])
        except Exception as err:
            print("Get count error! ", err)

    def generateRows(self, entitiesNum: int):
        startTime = time.time()
        try:
            self.db.cursor.execute(f"INSERT  INTO \"Order\" (client_id,transaction_date,taxes_sum)"
                                   f"SELECT getrandomrow('Client')::int,"
                                   f"generatedate()::date,"
                                   f"generateint(100)::money "
                                   f"FROM generate_series(1, {entitiesNum})")
            self.db.connect.commit()
        except Exception as err:
            print("Generate Rows error! ", err)
        endTime = time.time()
        return str(endTime - startTime)[:9] + 'ms'

test = OrderController()
print(test.generateRows(3))