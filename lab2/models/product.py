import sys
sys.path.append('../')
import models.database as database
import CUI.cui as console

class Product:
    def __init__(self):
        self.name = None
        self.cost = None
        self.brand = None
        self.manufacture_date = None
        self.manufacturer = None
        self.category = None

    def __varSetUp(self, key: str, value: str):
        exec("self.%s = \"%s\"" % (key, value))

    def __fillSetUp(self, key: str):
        value = input(f"Enter {key}: ")
        self.__varSetUp(key, value)

    def getSqlString(self):
        if self.name == None:  raise Exception('The entry must have a name')
        if self.cost == None:  raise Exception('The entry must have a cost')
        if self.manufacture_date == None:  raise Exception('The entry must have a manufacture_date')
        if self.manufacturer == None:  raise Exception('The entry must have a manufacturer')
        if self.category == None:  raise Exception('The entry must have a category_id')
        if self.brand == None: self.brand = 'null'

        firstStr = ''
        secondStr = ''
        for key in self.__dict__.keys():
            firstStr += key + ','
        for value in self.__dict__.values():
            secondStr += f"\'{str(value)}\' ,"
        return f"INSERT INTO \"Product\" ({firstStr[:-1]}) VALUES ({secondStr[:-1]})"

    def fill(self):
        for key in self.__dict__.keys():
            self.__fillSetUp(key)

        for value in self.__dict__.values():
            print(value)


class ProductModel:
    def __init__(self):
        self.db = database.getCursor()

    def add(self):
        newP = Product()
        newP.fill()
        self.db.execute(newP.getSqlString())

ProductModel().add()