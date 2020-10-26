import time
from CUI.cui import CUI

if __name__ == '__main__':

    def connectToDB():
        print("Connection to db...")
        time.sleep(2)


    cui = CUI("HUi Iluxi")
    cui.addField("add film", lambda: connectToDB())
    cui.addField("Avatar")
    cui.addMenu("Oskar")
    cui.addField("Oskar 1")
    cui.addField("delete Oskar")
    cui.deleteField('Oskar')
    cui.run()


