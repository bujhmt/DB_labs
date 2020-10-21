from models.dbModel import DbModel

class Product(DbModel):
    def __init__(self):
        self.id = {
            'type': 'number',
            'value': "DEFAULT",
            'not null': False
        }
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
            'value': None,
            'not null': False
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
