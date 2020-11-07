import sys
import time
sys.path.append('../')
from models.category import Category
from database import db


class CategoryController(object):

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
                f'SELECT {Category().getKeys()} FROM "Category" ORDER BY id LIMIT {per_page} OFFSET {page * per_page}')
            records = self.db.cursor.fetchall()
            for record in records:
                tmpItem = Category()
                tmpItem.parse(record)
                items.append(tmpItem)
        except Exception as err:
            print("Get error! ", err)
            exit(1)
        return items

    def add(self, *args):
        try:
            newEntity: Category = Category()
            if len(args) > 0 and isinstance(args[0], Category):
                newEntity = args[0]
            else:
                newEntity.fill()

            if newEntity.isFull():
                self.db.cursor.execute(f'INSERT INTO db_labs.public."Category" ({newEntity.getKeys()}) '
                                    f'VALUES ({newEntity.getValues()}) RETURNING id')
                self.db.connect.commit()
                return int(self.db.cursor.fetchone()[0])
        except Exception as err:
            print("Add error! ", err)
        return False

    def getById(self, categoryId):
        category = Category()
        try:
            if isinstance(categoryId, int): categoryId = str(categoryId)
            if not isinstance(categoryId, str): raise Exception('Incorrect arguments')
            self.db.cursor.execute(f'SELECT {category.getKeys()} from "Category" WHERE id = {categoryId}')
            record = self.db.cursor.fetchone()
            if record is not None:
                category.parse(record)
            else:
                raise Exception(f'No entry with ID {categoryId} found')
        except Exception as err:
            print("Get by id error! ", err)
        return category

    def delete(self, categoryId):
        try:
            if isinstance(categoryId, int): categoryId = str(categoryId)
            if not isinstance(categoryId, str): raise Exception('Incorrect arguments')
            category = self.getById(categoryId)
            self.db.cursor.execute(f'DELETE from "Category" WHERE id = {categoryId}')
            self.db.connect.commit()
            return category
        except Exception as err:
            print("Delete error! ", err)
            return False

    def update(self, *args):
        try:
            category: Category = Category()
            if len(args) is 0: raise Exception('Invalid arguments')
            if isinstance(args[0], int) or isinstance(int(args[0]), int):
                category.fill()
                category.id = args[0]
                values = category.getValues().split(',')
                old_values = self.getById(args[0]).getValues().split(',')
                keys = category.getKeys().split(',')
                for i in range(len(keys)):
                    if values[i] == 'null':
                        category.__setattr__(keys[i], old_values[i])

            if isinstance(args[0], Category):
                category = args[0]

            if not category.isFull():
                raise Exception('Invalid input')

            queryStr = ''
            keys = category.getKeys().split(',')
            values = category.getValues().split(',')
            for i in range(len(keys)):
                queryStr += keys[i] + ' = ' + values[i] + ', '
            self.db.cursor.execute(f'Update "Category" Set {queryStr[:-2]} Where id = {category.id}')
            self.db.connect.commit()
            return True
        except Exception as err:
            print("Update error! ", err)
            return False

    def getCount(self):
        try:
            self.db.cursor.execute(f'SELECT count(*)  from "Category"')
            return int(self.db.cursor.fetchone()[0])
        except Exception as err:
            print("Get count error! ", err)

    def generateRows(self, entitiesNum: int):
        startTime = time.time()
        try:
            self.db.cursor.execute(f'INSERT  INTO "Category" (name,type)'
                                   f' SELECT generatestring(15),'
                                   f'generatestring(15)'
                                   f'FROM generate_series(1, {entitiesNum})')
            self.db.connect.commit()
        except Exception as err:
            print("Generate Rows error! ", err)
        endTime = time.time()
        return str(endTime - startTime)[:9] + 'ms'
