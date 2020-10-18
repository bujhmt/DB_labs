import database
import CUI.cui as console

class Product:
    def __init__(self):
        self.name = None
        self.cost = None
        self.brand = None
        self.manufacture_date = None
        self.manufacturer = None
        self.category_id = None

    def getSqlString(self):
        if self.name == None:  raise Exception('The entry must have a name')
        if self.cost == None:  raise Exception('The entry must have a cost')
        if self.manufacture_date == None:  raise Exception('The entry must have a manufacture_date')
        if self.manufacturer == None:  raise Exception('The entry must have a manufacturer')
        if self.category_id == None:  raise Exception('The entry must have a category_id')
        if self.brand == None: self.brand = 'null'

        firstStr = ''
        secondStr = ''
        for key in self.__dict__.keys():
            firstStr += key + ','
        for value in self.__dict__.values():
            secondStr += str(value) + ','
        return f"INSERT INTO Product ({firstStr}) VALUES ({secondStr})"

    def fill(self):
        for value in self.__dict__.values():
            print(value)
        #fillProductCUi = console.CUI("Add Product")
        #fillProductCUi.addMenu("name")

Product().fill()

class ProductModel:
    def __init__(self):
        self.db = database.getCursor()

    def add(self, product: Product):
        print()
