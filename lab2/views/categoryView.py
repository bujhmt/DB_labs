import sys
sys.path.append('../')
import math
from controllers.categoryController import CategoryController
from models.category import Category
from CUI.cui import CUI

class CategoryView:
    def __init__(self):
        self.page = 1
        self.per_page = 10
        self.currentMenu = [None, None]

        self.CUI = CUI("Category model menu")
        self.categoryController = CategoryController()
        self.CUI.addField('Add Category', lambda: self.__addCategory())
        self.CUI.addField('Categorys', lambda: self.__getCategorys())

    def run(self):
        self.CUI.run()

    def __addCategory(self):
        try:
            result = self.categoryController.add()
            if isinstance(result, bool) and not result: raise Exception('Inccorect values')
            else: self.CUI.setError('New Category id: ' + str(result))
        except Exception as err:
            self.CUI.setError(str(err))

    def __changePageParams(self, page: int, per_page: int):
        self.page = page
        self.per_page = per_page
        self.currentMenu[0].stop()
        self.__getCategorys()

    def __getCategorys(self):
        categorysMenu = CUI('Category')
        self.currentMenu[0] = categorysMenu
        try:
            if self.page < math.ceil(self.categoryController.getCount() / self.per_page):
                categorysMenu.addField('NEXT', lambda: self.__changePageParams(self.page + 1, self.per_page))
            if self.page > 1:
                categorysMenu.addField('PREV', lambda: self.__changePageParams(self.page - 1, self.per_page))
            categorys = self.categoryController.getAll(self.page, self.per_page)
            for category in categorys:
                categorysMenu.addField(f"<{category.id}> {category.name}", lambda id=category.id: self.__getCategory(id))

        except Exception as err:
            categorysMenu.setError(str(err))
        categorysMenu.run('Return to main menu')

    def __updateCategory(self, id: int):
        self.categoryController.update(id)
        self.currentMenu[1].stop()
        self.__getCategory(id)

    def __deleteCategory(self, id: int):
        self.categoryController.delete(id)
        self.currentMenu[1].stop()
        self.__supportCUIFunc()

    def __supportCUIFunc(self):
        self.currentMenu[1].stop()
        self.__changePageParams(self.page, self.per_page)

    def __getCategory(self, id: int):
        categoryMenu = CUI('Category menu')
        self.currentMenu[1] = categoryMenu
        try:
            category: Category = self.categoryController.getById(id)
            values = category.getValues().split(',')
            keys = category.getKeys().split(',')
            for i in range(len(keys)):
                categoryMenu.addField(keys[i] + ' : ' + values[i])

            categoryMenu.addField('DELETE', lambda: self.__deleteCategory(category.id))
            categoryMenu.addField('UPDATE', lambda: self.__updateCategory(category.id))
            categoryMenu.addField('Return to prev menu', lambda: self.__supportCUIFunc())
        except Exception as err:
            categoryMenu.setError(str(err))
        categoryMenu.run(False)

