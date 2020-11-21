from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.client import Client
from models.order import Order

engine = create_engine('postgresql://postgres:bujhm9@localhost:5432/db_labs')
Session = sessionmaker(bind=engine)

session = Session()

if __name__ == '__main__':
    client = Client('Sqlalchemy_test', '2002-04-02', 'wduc@mail.ru')
    #session.add(client)

    order = Order('', 100, 135)
    session.add(order)
    session.commit()



session.close()