import psycopg2
import os
import utils.jsonReader

config = utils.jsonReader.JsonReader(os.getcwd()).getJsonObject('config.json')
conn = psycopg2.connect(dbname = config['dbname'], user = config['user'],
                        password = config['password'], host = config['host'])
cursor = conn.cursor()

def test():
    cursor.execute('SELECT * FROM "Client"')
    for row in cursor:
        print(row)


test()