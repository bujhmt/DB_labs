from models.dbModel import DbModel

class Client(DbModel):
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

        self.birthday_date = {
            'type': 'date',
            'value': None,
            'not null': False
        }

        self.email = {
            'type': 'string',
            'value': None,
            'not null': False
        }