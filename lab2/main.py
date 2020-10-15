import database
import time
from CUI.cui import CUI

if __name__ == '__main__':
    def connectToDB():
        print("Connection to db...")
        time.sleep(2)

    instance = {
        'first': "sfc",
        '2': "skdc"
    }
    test = CUI("Books")
    test.addField("connect to db", lambda: connectToDB())
    test.run()

