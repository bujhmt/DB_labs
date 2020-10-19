import sys
import math
import datetime
sys.path.append('../')
import models.database as database
import CUI.cui as console

class dbModel:

    #private:
    def __varSetUpDate(self, key: str, value: str):
        datetime.datetime.strptime(value, "%Y-%m-%d")
        exec("self.%s = \"\'%s\'\"" % (key, value))

    def __varSetUpNumber(self, key: str, value: str):
        if not isinstance(int(value), int): raise Exception("Invalid input")
        exec("self.%s = %i" % (key, int(value)))

    def __varSetUpMoney(self, key: str, value: str):
        if not isinstance(int(value), int): raise Exception("Invalid input")
        exec("self.%s = %i" % (key, math.fabs(int(value))))

    def __varSetUpString(self, key: str, value: str):
        exec("self.%s = \"\'%s\'\"" % (key, value))

    def __fillValue(self, key: str, type: str):
        value: str = input(f"Enter {key}: ")
        self.__fillMenu.setError('')
        try:
            if (type == 'string'):
                self.__varSetUpString(key, value)

            if (type == 'number'):
                self.__varSetUpNumber(key, value)

            if (type == 'money'):
                self.__varSetUpMoney(key, value)

            if (type == 'date'):
                self.__varSetUpDate(key, value)

            self.__fillMenu.renameField(key, key + f'    ({value})')
        except Exception:
            self.__fillMenu.setError(f"ERROR! Incorrect {key} input")

    #public:
    def getKeys(self):
        outputStr = ''
        for key in self.__dict__.keys():
            outputStr += key + ','
        return  outputStr[:-1]

    def getValues(self):
        outputStr = ''
        for item in self.__dict__.values():
            if isinstance(item, dict): outputStr += str(item['value']) + ','
        return outputStr[:-1]

    def fill(self):
        self.__fillMenu = console.CUI('fill')
        iters = dict((x, y) for x, y in self.__dict__.items() if x[:2] != '__')
        iters.update(self.__dict__)
        for key, value in iters.items():
            if (key != '_dbModel__fillMenu'):
                self.__fillMenu.addField(key, lambda key = key, value = value: self.__fillValue(key, value['type']))
        self.__fillMenu.run("finish")




class Product(dbModel):
    def __init__(self):
        self.name = {
            'type': 'string',
            'value': None
        }

        self.cost = {
            'type': 'money',
            'value': None
        }

        self.brand = {
            'type': 'string',
            'value': None
        }

        self.manufacture_date = {
            'type': 'date',
            'value': None
        }

        self.manufacturer = {
            'type': 'string',
            'value': None
        }

        self.category = {
            'type': 'number',
            'value': None
        }

test = Product()
test.fill()
print(test.getValues())


class ProductModel:
    def __init__(self):
        self.db = database.getCursor()

    def add(self, *args):
        print()


