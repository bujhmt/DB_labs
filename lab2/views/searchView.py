import sys
import math
import time
sys.path.append('../')

from controllers.searchController import SearchController
from CUI.cui import CUI

class SearchView:
    def __init__(self):
        self.currentMenu = None
        self.page = 1
        self.per_page = 10
        self.min = None
        self.max = None

        self.CUI = CUI("Search menu")
        self.searchController = SearchController()
        self.CUI.addField('Search products cost by cost range', lambda: self.__getProductsByCostRange())
        self.CUI.addField('Search all client orders', lambda: self.__getClientOrders())
        self.CUI.addField('Search all category products', lambda: self.__getCategoryProducts())

    def run(self):
        self.CUI.run()

    def __changePageParams(self, page: int, per_page: int):
        self.page = page
        self.per_page = per_page
        self.currentMenu.stop()
        self.__getProductsByCostRange()

    def __exitMenu(self):
        self.min = None
        self.max = None
        self.page = 1
        self.per_page = 10
        self.currentMenu.stop()

    def __getProductsByCostRange(self):
        searchMenu = CUI('Products')
        self.currentMenu = searchMenu
        try:
            if self.min is None or self.max is None:
                self.min = int(input('Enter min value: '))
                self.max = int(input('Enter max value: '))

                if not (isinstance(self.min, int) and isinstance(self.max, int)
                        and self.max > 0 and self.min > 0  and self.max >= self.min):
                    raise Exception('Invalid input')

            startTime = time.time()
            allRecords = self.searchController.getProductsByCostRange(self.min, self.max)
            endTime = time.time()

            searchMenu.setError('\nElapsed time: ' + str(endTime - startTime)[:9] + 's'
                                '\nRows num: ' + str(len(allRecords)))

            if self.page < math.ceil(len(allRecords) / self.per_page):
                searchMenu.addField('NEXT', lambda: self.__changePageParams(self.page + 1, self.per_page))
            if self.page > 1:
                searchMenu.addField('PREV', lambda: self.__changePageParams(self.page - 1, self.per_page))

            searchMenu.addField('<ID> | Product name | Product cost | Category name')
            for record in self.searchController.getProductsByCostRange(self.min, self.max, self.page, self.per_page):
                searchMenu.addField(f"<{record[0]}> {record[1]} {record[2]} {record[3]}")

        except Exception as err:
            searchMenu.setError(str(err))

        searchMenu.addField('Return to prev menu', lambda: self.__exitMenu())
        searchMenu.run(False)

    def __getClientOrders(self):
        searchMenu = CUI('Client Orders')
        self.currentMenu = searchMenu
        try:
            client_id = int(input('Enter client_id: '))

            if not (isinstance(client_id, int) and client_id > 0):
                raise Exception('Invalid input')

            startTime = time.time()
            allRecords = self.searchController.getAllClientOrders(client_id)
            endTime = time.time()

            searchMenu.setError('\nElapsed time: ' + str(endTime - startTime)[:9] + 's'
                                '\nRows num: ' + str(len(allRecords)))

            searchMenu.addField('<Order id> | transaction date | taxes_sum')
            for record in allRecords:
                searchMenu.addField(f"<{record[0]}> {record[1]} {record[2]}")

        except Exception as err:
            searchMenu.setError(str(err))

        searchMenu.run('Return to prev menu')

    def __getCategoryProducts(self):
        searchMenu = CUI('Cayegory Products')
        self.currentMenu = searchMenu
        try:
            category_id = int(input('Enter category_id: '))

            if not (isinstance(category_id, int) and category_id > 0):
                raise Exception('Invalid input')

            startTime = time.time()
            allRecords = self.searchController.getAllCategoryProducts(category_id)
            endTime = time.time()

            searchMenu.setError('\nElapsed time: ' + str(endTime - startTime)[:9] + 's'
                                '\nRows num: ' + str(len(allRecords)))

            searchMenu.addField('<Product id> | Product name | Product cost | Manufacturer')
            for record in allRecords:
                searchMenu.addField(f"<{record[0]}> {record[1]} {record[2]} {record[3]}")

        except Exception as err:
            searchMenu.setError(str(err))

        searchMenu.run('Return to prev menu')