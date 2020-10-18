import psycopg2
import os
import sys
sys.path.append('../')
import utils.jsonReader

def getCursor():
    config = utils.jsonReader.JsonReader(os.getcwd()).getJsonObject('../config.json')
    return psycopg2.connect(dbname=config['dbname'], user=config['user'],
                            password=config['password'], host=config['host'])