from models.dbModel import DbModel

class Order(DbModel):
    def __init__(self):
        self.id = {
            'type': 'number',
            'value': "DEFAULT",
            'not null': False
        }

        self.client_id = {
            'type': 'number',
            'value': None
        }

        self.transaction_date = {
            'type': 'date',
            'value': None
        }

        self.taxes_sum = {
            'type': 'money',
            'value': None
        }

