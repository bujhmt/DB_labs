import sys
sys.path.append('../')
import math
from controllers.clientController import ClientController
from models.client import Client
from CUI.cui import CUI

class ClientView:
    def __init__(self):
        self.currentMenu = [None, None]
        self.page = 1
        self.per_page = 10

        self.CUI = CUI("Client model menu")
        self.clientController = ClientController()
        self.CUI.addField('Add Client', lambda: self.__addClient())
        self.CUI.addField('Generate rows', lambda: self.__generateRows())
        self.CUI.addField('Clients', lambda: self.__getClients())

    def run(self):
        self.CUI.run()

    def __generateRows(self):
        try:
            rowsNum = int(input('Enter rows num: '))
            if not (isinstance(rowsNum, int) and rowsNum > 0):
                raise Exception('Invalid input')
            self.CUI.setError('   Please wait! Rows are generating...   ')
            time = self.clientController.generateRows(rowsNum)
            self.CUI.setError('   Rows generated! Elapsed time: ' + time)
        except Exception as error:
            self.CUI.setError(str(error))

    def __addClient(self):
        try:
            result = self.clientController.add()
            if isinstance(result, bool) and not result: raise Exception('Inccorect values')
            else: self.CUI.setError('New Client id: ' + str(result))
        except Exception as err:
            self.CUI.setError(str(err))

    def __changePageParams(self, page: int, per_page: int):
        self.page = page
        self.per_page = per_page
        self.currentMenu[0].stop()
        self.__getClients()

    def __getClients(self):
        clientsMenu = CUI('Clients')
        self.currentMenu[0] = clientsMenu
        try:
            if self.page < math.ceil(self.clientController.getCount() / self.per_page):
                clientsMenu.addField('NEXT', lambda: self.__changePageParams(self.page + 1, self.per_page))
            if self.page > 1:
                clientsMenu.addField('PREV', lambda: self.__changePageParams(self.page - 1, self.per_page))
            clients = self.clientController.getAll(self.page, self.per_page)
            for client in clients:
                clientsMenu.addField(f"<{client.id}> {client.name}", lambda id=client.id: self.__getClient(id))

        except Exception as err:
            clientsMenu.setError(str(err))
        clientsMenu.run('Return to main menu')

    def __updateClient(self, id: int):
        if self.clientController.update(id):
            self.currentMenu[1].stop()
            self.__getClient(id)
        else:
            self.currentMenu[1].setError('Incorrect update values')

    def __deleteClient(self, id: int):
        self.clientController.delete(id)
        self.currentMenu[1].stop()
        self.__supportCUIFunc()

    def __supportCUIFunc(self):
        self.currentMenu[1].stop()
        self.__changePageParams(self.page, self.per_page)

    def __getClient(self, id: int):
        clientMenu = CUI('Client menu')
        self.currentMenu[1] = clientMenu
        try:
            client: Client = self.clientController.getById(id)
            values = client.getValues().split(',')
            keys = client.getKeys().split(',')
            for i in range(len(keys)):
                clientMenu.addField(keys[i] + ' : ' + values[i])

            clientMenu.addField('DELETE', lambda: self.__deleteClient(client.id))
            clientMenu.addField('UPDATE', lambda: self.__updateClient(client.id))
            clientMenu.addField('Return to prev menu', lambda: self.__supportCUIFunc())
        except Exception as err:
            clientMenu.setError(str(err))
        clientMenu.run(False)

