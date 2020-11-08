import sys
sys.path.append('../')
import math
from controllers.productController import ProductController
from models.product import Product
from CUI.cui import CUI

class ProductView:
    def __init__(self):
        self.currentMenu = [None, None]
        self.page = 1
        self.per_page = 10

        self.CUI = CUI("Product model menu")
        self.productController = ProductController()
        self.CUI.addField('Add Product', lambda: self.__addProduct())
        self.CUI.addField('Generate rows', lambda: self.__generateRows())
        self.CUI.addField('Products', lambda: self.__getProducts())

    def run(self):
        self.CUI.run()

    def __generateRows(self):
        try:
            rowsNum = int(input('Enter rows num: '))
            if not (isinstance(rowsNum, int) and rowsNum > 0):
                raise Exception('Invalid input')
            self.CUI.setError('   Please wait! Rows are generating...   ')
            time = self.productController.generateRows(rowsNum)
            self.CUI.setError('   Rows generated! Elapsed time: ' + time)
        except Exception as error:
            self.CUI.setError(str(error))

    def __addProduct(self):
        try:
            result = self.productController.add()
            if isinstance(result, bool) and not result: raise Exception('Inccorect values')
            else: self.CUI.setError('New Product id: ' + str(result))
        except Exception as err:
            self.CUI.setError(str(err))

    def __changePageParams(self, page: int, per_page: int):
        self.page = page
        self.per_page = per_page
        self.currentMenu[0].stop()
        self.__getProducts()

    def __getProducts(self):
        productsMenu = CUI('Products')
        self.currentMenu[0] = productsMenu
        try:
            if self.page < math.ceil(self.productController.getCount() / self.per_page):
                productsMenu.addField('NEXT', lambda: self.__changePageParams(self.page + 1, self.per_page))
            if self.page > 1:
                productsMenu.addField('PREV', lambda: self.__changePageParams(self.page - 1, self.per_page))
            products = self.productController.getAll(self.page, self.per_page)
            for product in products:
                productsMenu.addField(f"<{product.id}> {product.name}", lambda id=product.id: self.__getProduct(id))

        except Exception as err:
            productsMenu.setError(str(err))
        productsMenu.run('Return to main menu')

    def __updateProduct(self, id: int):
        if self.productController.update(id):
            self.currentMenu[1].stop()
            self.__getProduct(id)
        else:
            self.currentMenu[1].setError('Incorrect update values')

    def __deleteProduct(self, id: int):
        self.productController.delete(id)
        self.currentMenu[1].stop()
        self.__supportCUIFunc()

    def __supportCUIFunc(self):
        self.currentMenu[1].stop()
        self.__changePageParams(self.page, self.per_page)

    def __getProduct(self, id: int):
        productMenu = CUI('Product menu')
        self.currentMenu[1] = productMenu
        try:
            product: Product = self.productController.getById(id)
            values = product.getValues().split(',')
            keys = product.getKeys().split(',')
            for i in range(len(keys)):
                productMenu.addField(keys[i] + ' : ' + values[i])

            productMenu.addField('DELETE', lambda: self.__deleteProduct(product.id))
            productMenu.addField('UPDATE', lambda: self.__updateProduct(product.id))
            productMenu.addField('Return to prev menu', lambda: self.__supportCUIFunc())
        except Exception as err:
            productMenu.setError(str(err))
        productMenu.run(False)

