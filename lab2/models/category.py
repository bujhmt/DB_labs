from models.dbModel import DbModel

class Category(DbModel):
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

        self.type = {
            'type': 'string',
            'value': None,
        }

