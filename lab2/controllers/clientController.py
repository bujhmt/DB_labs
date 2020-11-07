import sys
import time
sys.path.append('../')
from models.client import Client
from database import db

class ClientController(object):

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
                f'SELECT {Client().getKeys()} FROM "Client" ORDER BY id LIMIT {per_page} OFFSET {page * per_page}')
            records = self.db.cursor.fetchall()
            for record in records:
                tmpItem = Client()
                tmpItem.parse(record)
                items.append(tmpItem)
        except Exception as err:
            print("Get error! ", err)
            exit(1)
        return items

    def add(self, *args):
        try:
            newEntity: Client = Client()
            if len(args) > 0 and isinstance(args[0], Client):
                newEntity = args[0]
            else:
                newEntity.fill()

            if newEntity.isFull():
                self.db.cursor.execute(f'INSERT INTO db_labs.public."Client" ({newEntity.getKeys()}) '
                                    f'VALUES ({newEntity.getValues()}) RETURNING id')
                self.db.connect.commit()
                return int(self.db.cursor.fetchone()[0])
        except Exception as err:
            print("Add error! ", err)
        return False

    def getById(self, clientId):
        client = Client()
        try:
            if isinstance(clientId, int): clientId = str(clientId)
            if not isinstance(clientId, str): raise Exception('Incorrect arguments')
            self.db.cursor.execute(f'SELECT {client.getKeys()} from "Client" WHERE id = {clientId}')
            record = self.db.cursor.fetchone()
            if record is not None:
                client.parse(record)
            else:
                raise Exception(f'No entry with ID {clientId} found')
        except Exception as err:
            print("Get by id error! ", err)
        return client

    def delete(self, clientId):
        try:
            if isinstance(clientId, int): clientId = str(clientId)
            if not isinstance(clientId, str): raise Exception('Incorrect arguments')
            client = self.getById(clientId)
            self.db.cursor.execute(f'DELETE from "Client" WHERE id = {clientId}')
            self.db.connect.commit()
            return client
        except Exception as err:
            print("Delete error! ", err)
            return False

    def update(self, *args):
        try:
            client: Client = Client()
            if len(args) is 0: raise Exception('Invalid arguments')
            if isinstance(args[0], int) or isinstance(int(args[0]), int):
                client.fill()
                client.id = args[0]
                values = client.getValues().split(',')
                old_values = self.getById(args[0]).getValues().split(',')
                keys = client.getKeys().split(',')
                for i in range(len(keys)):
                    if values[i] == 'null':
                        client.__setattr__(keys[i], old_values[i])

            if isinstance(args[0], Client):
                client = args[0]

            if not client.isFull():
                raise Exception('Invalid input')

            queryStr = ''
            keys = client.getKeys().split(',')
            values = client.getValues().split(',')
            for i in range(len(keys)):
                queryStr += keys[i] + ' = ' + values[i] + ', '
            self.db.cursor.execute(f'Update "Client" Set {queryStr[:-2]} Where id = {client.id}')
            self.db.connect.commit()
            return True
        except Exception as err:
            print("Update error! ", err)
            return False

    def getCount(self):
        try:
            self.db.cursor.execute(f'SELECT count(*)  from "Client"')
            return int(self.db.cursor.fetchone()[0])
        except Exception as err:
            print("Get count error! ", err)

    def generateRows(self, entitiesNum: int):
        startTime = time.time()
        try:
            self.db.cursor.execute(f"INSERT  INTO \"Client\" (name,birthday_date,email)"
                                   f" SELECT generatestring(15),"
                                   f"generatedate()::date,"
                                   f"concat(generatestring(15)::text, '@gmail.com')"
                                   f"FROM generate_series(1, {entitiesNum})")
            self.db.connect.commit()
        except Exception as err:
            print("Generate Rows error! ", err)
        endTime = time.time()
        return str(endTime - startTime)[:9] + 'ms'
