import sys
sys.path.append('../')
from controllers.productController import ProductController
from models.product import Product
from CUI.cui import CUI

class ProductView:
    def __init__(self):
        self.page = 1
        self.per_page = 7

        self.CUI = CUI("Product model menu")
        self.productController = ProductController()
        self.CUI.addField('Add Product', lambda: self.__addProduct())
        self.CUI.addField('Products', lambda: self.__getProducts())
        self.CUI.run()


    def __addProduct(self):
        try:
            result = self.productController.add()
            if not isinstance(result, int): raise Exception('Inccorect values')
            else: self.CUI.setError('New Product id: ' + str(result))
        except Exception as err:
            self.CUI.setError(str(err))

    def __changePageParams(self, page: int, per_page: int):
        self.page = page
        self.per_page = per_page
        self.currentMenu.stop()
        self.__getProducts()

    def __getProducts(self):
        productsMenu = CUI('Products')
        self.currentMenu = productsMenu
        try:
            productsMenu.addField('NEXT', lambda: self.__changePageParams(self.page + 1, self.per_page))
            productsMenu.addField('PREV', lambda: self.__changePageParams(self.page - 1, self.per_page))
            products = self.productController.getAll(self.page, self.per_page)
            for product in products:
                productsMenu.addField(f"<{product.id}> {product.name}", lambda id=product.id: self.__getProduct(id))

        except Exception as err:
            productsMenu.setError(str(err))
        productsMenu.run('Return to main menu')


    def __updateProduct(self, id: int):
        self.productController.update(id)
        self.currentMenu.stop()
        self.__getProduct(id)

    def __deleteProduct(self, id: int):
        self.productController.delete(id)
        self.currentMenu.stop()

    def __getProduct(self, id: int):
        productMenu = CUI('Product menu')
        self.currentMenu = productMenu
        try:
            product: Product = self.productController.getById(id)
            values = product.getValues().split(',')
            keys = product.getKeys().split(',')
            for i in range(len(keys)):
                productMenu.addField(keys[i] + ' : ' + values[i])

            productMenu.addField('DELETE', lambda: self.__deleteProduct(product.id))
            productMenu.addField('UPDATE', lambda: self.__updateProduct(product.id))
        except Exception as err:
            productMenu.setError(str(err))
        productMenu.run('Return to Products menu')

test = ProductView()