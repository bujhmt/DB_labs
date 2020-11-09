import sys
sys.path.append('../')
from database import db

class SearchController(object):

    def __init__(self):
        try:
            self.db = db()

            if db is None: raise Exception('No connection. Please, check your config.json or Postgre server')

        except Exception as err:
            print("Connection error! ", err)
            exit(1)

    def getProductsByCostRange(self, min: int, max: int, *args):
        try:
            if len(args) == 0:
                self.db.cursor.execute(
                    f'SELECT p.id, p.name, p.cost, c.name as category  from "Product" as p '
                    f'inner join "Category" C on C.id = p.category_id '
                    f'Where p.cost::numeric::int > {min } and p.cost::numeric::int < {max} '
                    f'ORDER BY p.cost::numeric::int')
                return self.db.cursor.fetchall()
            else:
                self.db.cursor.execute(
                    f'SELECT p.id, p.name, p.cost, c.name as category  from "Product" as p '
                    f'inner join "Category" C on C.id = p.category_id '
                    f'Where p.cost::numeric::int > {min} and p.cost::numeric::int < {max} '
                    f'ORDER BY p.cost::numeric::int LIMIT {args[1]} OFFSET {args[0] * args[1]}')
                return self.db.cursor.fetchall()
        except Exception as err:
            print("Get error! ", err)

    def getAllClientOrders(self, client_id: int):
        try:
            self.db.cursor.execute(
                f'SELECT O.id as OrderId, O.transaction_date, O.taxes_sum from "Order" as O '
                f'INNER JOIN "Client" C on C.id = O.client_id '
                f'WHERE client_id = {client_id}')
            return self.db.cursor.fetchall()
        except Exception as err:
            raise str(err)