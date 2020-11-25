from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import Config

Base = declarative_base()
engine = create_engine(f'postgresql://{Config.user}:{Config.passwd}@{Config.url}/{Config.db_name}')
session = sessionmaker(bind=engine)()


def recreate_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
